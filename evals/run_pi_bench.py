"""Benchmark the simple-english skill through isolated Pi CLI calls.

For each model, condition, and scenario, this script runs a headless `pi -p`
call. It lints each final response with ste_lint.py and writes resumable raw
results, results.json, and RESULTS.md to a separate results directory.

Usage:
  python3 evals/run_pi_bench.py --model PROVIDER/MODEL:THINKING
  python3 evals/run_pi_bench.py --model MODEL --smoke
  python3 evals/run_pi_bench.py --model MODEL --report-only
"""

import argparse
import datetime
import json
import pathlib
import re
import subprocess
import time

import ste_lint

HERE = pathlib.Path(__file__).resolve().parent
SKILL_PATH = HERE.parent / "skills" / "simple-english" / "SKILL.md"
SCENARIOS_PATH = HERE / "scenarios.json"
DEFAULT_RESULTS_DIRECTORY = HERE / "results" / "pi"
CONDITIONS = ("baseline", "skill")
NEUTRAL_SYSTEM_PROMPT = "Return only the final text requested by the user."
CALL_TIMEOUT_SECONDS = 300
CALL_RETRY_LIMIT = 2
INTER_CALL_DELAY_SECONDS = 2


def build_benchmark_prompt(scenario, condition, skill_text):
    """Build the existing baseline or simple-english skill benchmark prompt."""
    if condition == "baseline":
        return scenario["prompt"]
    if condition != "skill":
        raise ValueError(f"Unknown benchmark condition: {condition}")
    return (
        "Follow these writing instructions exactly, including the self-check step:\n\n"
        + skill_text
        + "\n\n---\n\nTask: "
        + scenario["prompt"]
        + "\n\nReturn only the final text, no rule commentary."
    )


def parse_pi_json_events(stdout):
    """Extract final assistant text and usage from Pi newline-delimited JSON events."""
    final_message = None
    for line_number, line in enumerate(stdout.splitlines(), 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                f"Pi returned invalid JSON on output line {line_number}: {error}"
            ) from error
        message = event.get("message", {})
        if event.get("type") == "message_end" and message.get("role") == "assistant":
            final_message = message

    if final_message is None:
        raise RuntimeError("Pi benchmark call returned no final assistant message")

    text = "".join(
        part.get("text", "")
        for part in final_message.get("content", [])
        if part.get("type") == "text"
    )
    if not text.strip():
        raise RuntimeError(
            "Pi benchmark call returned an empty final assistant message"
        )

    usage = final_message.get("usage", {})
    cost = usage.get("cost", {})
    return {
        "text": text,
        "input_tokens": usage.get("input"),
        "output_tokens": usage.get("output"),
        "reasoning_tokens": usage.get("reasoning"),
        "total_tokens": usage.get("totalTokens"),
        "cost_usd": cost.get("total"),
        "provider": final_message.get("provider"),
        "model_id": final_message.get("model"),
        "stop_reason": final_message.get("stopReason"),
    }


def call_pi_model(prompt, model_spec):
    """Generate one response with tools and ambient Pi context disabled."""
    command = [
        "pi",
        "-p",
        "--model",
        model_spec,
        "--mode",
        "json",
        "--no-session",
        "--no-tools",
        "--no-skills",
        "--no-prompt-templates",
        "--no-extensions",
        "--no-context-files",
        "--system-prompt",
        NEUTRAL_SYSTEM_PROMPT,
        prompt,
    ]
    started_at = time.monotonic()
    process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        timeout=CALL_TIMEOUT_SECONDS,
        cwd="/tmp",
    )
    duration_ms = round(1000 * (time.monotonic() - started_at))
    if process.returncode != 0:
        stderr = process.stderr.strip()
        raise RuntimeError(
            f"Pi benchmark call failed for {model_spec} with exit "
            f"{process.returncode}: {stderr[:1000]}"
        )

    result = parse_pi_json_events(process.stdout)
    result["duration_ms"] = duration_ms
    return result


def model_spec_file_slug(model_spec):
    """Convert a provider/model/thinking specification to a flat filename slug."""
    return re.sub(r"[^A-Za-z0-9._-]+", "_", model_spec)


def raw_result_path(raw_directory, model_spec, condition, scenario_id):
    """Return the resumable raw result path for one benchmark matrix cell."""
    return raw_directory / (
        f"{model_spec_file_slug(model_spec)}__{condition}__{scenario_id}.json"
    )


def call_pi_model_with_retries(prompt, model_spec):
    """Retry one Pi generation after timeout or invalid model output."""
    for attempt in range(1, CALL_RETRY_LIMIT + 1):
        try:
            return call_pi_model(prompt, model_spec)
        except (RuntimeError, subprocess.TimeoutExpired) as error:
            print(f"  attempt {attempt} failed: {error}", flush=True)
            if attempt == CALL_RETRY_LIMIT:
                raise RuntimeError(str(error)) from error
            time.sleep(INTER_CALL_DELAY_SECONDS)
    raise AssertionError("Pi retry loop ended without a result or error")


def save_benchmark_cell(model_spec, condition, scenario, skill_text, output_path):
    """Generate, lint, and save one benchmark matrix cell."""
    prompt = build_benchmark_prompt(scenario, condition, skill_text)
    result = call_pi_model_with_retries(prompt, model_spec)
    result.update(
        model=model_spec,
        condition=condition,
        scenario=scenario["id"],
        type=scenario["type"],
        lint=ste_lint.lint(result["text"], scenario["type"]),
    )
    output_path.write_text(json.dumps(result, indent=2) + "\n")
    print(
        f"  OK {result['duration_ms'] / 1000:.1f}s "
        f"{result.get('output_tokens')} output tokens "
        f"{result['lint']['violations_per_100w']} violations/100w",
        flush=True,
    )


def generate_benchmark_matrix(models, scenarios, results_directory):
    """Run missing matrix cells and save each successful response immediately."""
    skill_text = SKILL_PATH.read_text()
    raw_directory = results_directory / "raw"
    failures_path = results_directory / "failures.json"
    raw_directory.mkdir(parents=True, exist_ok=True)
    failures = []
    matrix = [
        (model_spec, condition, scenario)
        for model_spec in models
        for condition in CONDITIONS
        for scenario in scenarios
    ]

    for index, (model_spec, condition, scenario) in enumerate(matrix, 1):
        output_path = raw_result_path(
            raw_directory, model_spec, condition, scenario["id"]
        )
        if output_path.exists():
            print(
                f"[{index}/{len(matrix)}] SKIP {model_spec} "
                f"{condition} {scenario['id']}",
                flush=True,
            )
            continue

        print(
            f"[{index}/{len(matrix)}] RUN  {model_spec} {condition} {scenario['id']}",
            flush=True,
        )
        try:
            save_benchmark_cell(
                model_spec, condition, scenario, skill_text, output_path
            )
        except RuntimeError as error:
            failures.append(
                {
                    "model": model_spec,
                    "condition": condition,
                    "scenario": scenario["id"],
                    "error": str(error),
                }
            )
            failures_path.write_text(json.dumps(failures, indent=2) + "\n")
        time.sleep(INTER_CALL_DELAY_SECONDS)

    if not failures and failures_path.exists():
        failures_path.unlink()
    return failures


def arithmetic_mean(values):
    """Return the arithmetic mean of a non-empty sequence."""
    return sum(values) / len(values)


def aggregate_condition_rows(condition_rows):
    """Aggregate one model and condition without hiding final-text length."""
    violations = sum(row["lint"]["violations_total"] for row in condition_rows)
    words = sum(row["lint"]["words"] for row in condition_rows)
    output_tokens = sum(row.get("output_tokens") or 0 for row in condition_rows)
    reasoning_tokens = sum(row.get("reasoning_tokens") or 0 for row in condition_rows)
    return {
        "violations_per_100w": round(
            arithmetic_mean(
                [row["lint"]["violations_per_100w"] for row in condition_rows]
            ),
            2,
        ),
        "weighted_violations_per_100w": round(100 * violations / words, 2),
        "violations_total": violations,
        "mean_sentence_words": round(
            arithmetic_mean(
                [row["lint"]["mean_sentence_words"] for row in condition_rows]
            ),
            1,
        ),
        "mean_final_words": round(words / len(condition_rows), 1),
        "provider_output_tokens": output_tokens,
        "reasoning_tokens": reasoning_tokens,
        "approximate_final_text_tokens": output_tokens - reasoning_tokens,
        "cost_usd": round(sum(row.get("cost_usd") or 0 for row in condition_rows), 6),
        "duration_seconds": round(
            sum(row["duration_ms"] for row in condition_rows) / 1000, 1
        ),
        "runs": len(condition_rows),
    }


def select_complete_condition_rows(
    model_spec, model_rows, condition, expected_scenario_ids
):
    """Select one condition and reject missing scenario results."""
    condition_rows = [
        row
        for row in model_rows
        if row["condition"] == condition and row["scenario"] in expected_scenario_ids
    ]
    observed_scenario_ids = {row["scenario"] for row in condition_rows}
    if observed_scenario_ids != expected_scenario_ids:
        missing = sorted(expected_scenario_ids - observed_scenario_ids)
        raise RuntimeError(
            f"Incomplete benchmark results for {model_spec} {condition}; "
            f"missing scenarios: {missing}"
        )
    return condition_rows


def calculate_reduction_percentage(baseline_rate, skill_rate):
    """Calculate percentage reduction unless the baseline rate is zero."""
    if not baseline_rate:
        return None
    return round(100 * (baseline_rate - skill_rate) / baseline_rate, 1)


def count_scenario_outcomes(scenario_rates, expected_scenario_ids):
    """Count scenarios whose skill rate improved, tied, or worsened."""
    outcomes = {"improved": 0, "tied": 0, "worsened": 0}
    for scenario_id in expected_scenario_ids:
        baseline = scenario_rates["baseline"][scenario_id]
        skill = scenario_rates["skill"][scenario_id]
        if skill < baseline:
            outcomes["improved"] += 1
        elif skill > baseline:
            outcomes["worsened"] += 1
        else:
            outcomes["tied"] += 1
    return outcomes


def aggregate_model_results(model_spec, rows, expected_scenario_ids):
    """Aggregate baseline and skill conditions for one model."""
    model_rows = [row for row in rows if row["model"] == model_spec]
    rows_by_condition = {
        condition: select_complete_condition_rows(
            model_spec, model_rows, condition, expected_scenario_ids
        )
        for condition in CONDITIONS
    }
    summaries = {
        condition: aggregate_condition_rows(condition_rows)
        for condition, condition_rows in rows_by_condition.items()
    }
    scenario_rates = {
        condition: {
            row["scenario"]: row["lint"]["violations_per_100w"]
            for row in condition_rows
        }
        for condition, condition_rows in rows_by_condition.items()
    }
    baseline = summaries["baseline"]
    skill = summaries["skill"]
    return {
        "model": model_spec,
        "baseline": baseline,
        "skill": skill,
        "reduction_pct": calculate_reduction_percentage(
            baseline["violations_per_100w"], skill["violations_per_100w"]
        ),
        "scenario_outcomes": count_scenario_outcomes(
            scenario_rates, expected_scenario_ids
        ),
        "cost_usd": round(baseline["cost_usd"] + skill["cost_usd"], 6),
        "duration_seconds": round(
            baseline["duration_seconds"] + skill["duration_seconds"], 1
        ),
    }


def aggregate_benchmark_results(models, scenarios, results_directory):
    """Aggregate a complete raw matrix into per-model baseline comparisons."""
    expected_scenario_ids = {scenario["id"] for scenario in scenarios}
    raw_directory = results_directory / "raw"
    rows = [
        json.loads(path.read_text()) for path in sorted(raw_directory.glob("*.json"))
    ]
    selected_rows = [
        row
        for row in rows
        if row["model"] in models and row["scenario"] in expected_scenario_ids
    ]
    return {
        "generated": datetime.datetime.now(datetime.UTC).date().isoformat(),
        "models": [
            aggregate_model_results(model_spec, rows, expected_scenario_ids)
            for model_spec in models
        ],
        "runs": len(selected_rows),
        "scenarios_per_condition": len(scenarios),
        "conditions": list(CONDITIONS),
        "system_prompt": NEUTRAL_SYSTEM_PROMPT,
        "isolation": {
            "tools": "disabled",
            "skills": "disabled",
            "prompt_templates": "disabled",
            "extensions": "disabled",
            "context_files": "disabled",
            "session_persistence": "disabled",
        },
    }


def format_reproduction_command(models, results_directory):
    """Format the exact model portfolio as a copyable benchmark command."""
    lines = [
        "python3 evals/run_pi_bench.py \\",
        f"  --results-dir {results_directory} \\",
    ]
    for index, model_spec in enumerate(models):
        suffix = " \\" if index < len(models) - 1 else ""
        lines.append(f"  --model {model_spec}{suffix}")
    return "\n".join(lines)


def write_benchmark_report(results, models, results_directory):
    """Write machine-readable and human-readable Pi benchmark summaries."""
    results_directory.mkdir(parents=True, exist_ok=True)
    (results_directory / "results.json").write_text(
        json.dumps(results, indent=2) + "\n"
    )

    reductions = [
        row["reduction_pct"]
        for row in results["models"]
        if row["reduction_pct"] is not None
    ]
    if reductions:
        headline = (
            f"**The skill reduced mean linter violations by {min(reductions):.1f}% to "
            f"{max(reductions):.1f}% across {len(results['models'])} models.**"
        )
    else:
        headline = (
            "**Every baseline had zero measured violations, so percentage reduction "
            "is undefined.**"
        )

    model_count = len(results["models"])
    model_label = "model" if model_count == 1 else "models"
    scenario_count = results["scenarios_per_condition"]
    scenario_label = "scenario" if scenario_count == 1 else "scenarios"
    lines = [
        "# Pi benchmark results",
        "",
        headline,
        "",
        (
            f"This run contains {results['runs']} generations: "
            f"{model_count} {model_label} x {scenario_count} {scenario_label} "
            "x 2 conditions."
        ),
        "",
        (
            "| Model | Baseline viol/100w | Skill viol/100w | Reduction | "
            "Final words (base -> skill) | Scenarios (better/tied/worse) | Cost |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in results["models"]:
        baseline = row["baseline"]
        skill = row["skill"]
        outcomes = row["scenario_outcomes"]
        reduction = (
            f"{row['reduction_pct']:.1f}%"
            if row["reduction_pct"] is not None
            else "n/a"
        )
        lines.append(
            f"| `{row['model']}` | {baseline['violations_per_100w']:.2f} | "
            f"{skill['violations_per_100w']:.2f} | {reduction} | "
            f"{baseline['mean_final_words']:.1f} -> {skill['mean_final_words']:.1f} | "
            f"{outcomes['improved']}/{outcomes['tied']}/{outcomes['worsened']} | "
            f"${row['cost_usd']:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Method",
            "",
            "The runner used the same scenarios, skill prompt, linter, and per-scenario averaging as `run_bench.py`.",
            "It sent only the scenario prompt for the baseline condition.",
            "It added the complete `SKILL.md` text for the skill condition.",
            f"Both conditions used this neutral system prompt: `{results['system_prompt']}`",
            "",
            "Pi tools, skills, prompt templates, extensions, context files, and session persistence were disabled.",
            "The runner made one generation for each matrix cell and did not run a judge pass.",
            "",
            "## Reproduce",
            "",
            "```bash",
            format_reproduction_command(models, results_directory),
            "```",
            "",
            "Delete `raw/` first to replace the committed generations. Existing raw files are skipped.",
            "",
            "## Caveats",
            "",
            "- The regex linter undercounts some violations and reports some false positives.",
            "  For example, it treats descriptive sentences with a non-leading `when` clause as trailing conditions.",
            "- One generation per cell does not measure model variance.",
            "- Provider output-token counts can include hidden reasoning tokens.",
            "  The table reports final-text word counts instead.",
            "- Costs are provider-reported estimates, not billing records.",
            "- The run measures the linter score, not ASD-STE100 certification or overall writing quality.",
        ]
    )
    report = "\n".join(lines) + "\n"
    (results_directory / "RESULTS.md").write_text(report)
    print(report)


def parse_command_line_arguments():
    """Parse explicit model portfolio and result-location arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--model",
        dest="models",
        action="append",
        required=True,
        help="Pi model specification; repeat for each model",
    )
    parser.add_argument(
        "--results-dir",
        type=pathlib.Path,
        default=DEFAULT_RESULTS_DIRECTORY,
        help=f"result directory (default: {DEFAULT_RESULTS_DIRECTORY})",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run the first two scenarios only",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="rebuild summaries from existing raw result files",
    )
    return parser.parse_args()


def main():
    args = parse_command_line_arguments()
    scenarios = json.loads(SCENARIOS_PATH.read_text())
    if args.smoke:
        scenarios = scenarios[:2]

    if not args.report_only:
        failures = generate_benchmark_matrix(args.models, scenarios, args.results_dir)
        if failures:
            raise SystemExit(
                f"Benchmark stopped with {len(failures)} failed matrix cells; "
                f"see {args.results_dir / 'failures.json'}"
            )

    results = aggregate_benchmark_results(args.models, scenarios, args.results_dir)
    write_benchmark_report(results, args.models, args.results_dir)


if __name__ == "__main__":
    main()

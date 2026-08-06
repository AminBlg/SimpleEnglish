"""Tests for the Pi benchmark runner's stable input and output boundaries."""

import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import run_pi_bench


class PiJsonEventParsingTests(unittest.TestCase):
    def test_extracts_final_text_and_usage_from_assistant_message(self):
        stdout = "\n".join(
            [
                json.dumps(
                    {
                        "type": "message_end",
                        "message": {
                            "role": "user",
                            "content": [{"type": "text", "text": "prompt"}],
                        },
                    }
                ),
                json.dumps(
                    {
                        "type": "message_end",
                        "message": {
                            "role": "assistant",
                            "provider": "example-provider",
                            "model": "example-model",
                            "content": [
                                {"type": "thinking", "thinking": "hidden"},
                                {"type": "text", "text": "final text"},
                            ],
                            "usage": {
                                "input": 10,
                                "output": 7,
                                "reasoning": 3,
                                "totalTokens": 17,
                                "cost": {"total": 0.25},
                            },
                            "stopReason": "stop",
                        },
                    }
                ),
            ]
        )

        result = run_pi_bench.parse_pi_json_events(stdout)

        self.assertEqual(result["text"], "final text")
        self.assertEqual(result["input_tokens"], 10)
        self.assertEqual(result["output_tokens"], 7)
        self.assertEqual(result["reasoning_tokens"], 3)
        self.assertEqual(result["cost_usd"], 0.25)
        self.assertEqual(result["provider"], "example-provider")
        self.assertEqual(result["model_id"], "example-model")

    def test_rejects_output_without_a_final_assistant_message(self):
        stdout = json.dumps(
            {
                "type": "message_end",
                "message": {
                    "role": "user",
                    "content": [{"type": "text", "text": "prompt"}],
                },
            }
        )

        with self.assertRaisesRegex(RuntimeError, "no final assistant message"):
            run_pi_bench.parse_pi_json_events(stdout)


class BenchmarkPromptTests(unittest.TestCase):
    def test_baseline_prompt_does_not_include_the_skill(self):
        scenario = {"prompt": "Write the document."}

        prompt = run_pi_bench.build_benchmark_prompt(
            scenario, "baseline", "SKILL CONTENT"
        )

        self.assertEqual(prompt, "Write the document.")

    def test_skill_prompt_includes_the_skill_and_original_task(self):
        scenario = {"prompt": "Write the document."}

        prompt = run_pi_bench.build_benchmark_prompt(scenario, "skill", "SKILL CONTENT")

        self.assertIn("SKILL CONTENT", prompt)
        self.assertIn("Task: Write the document.", prompt)
        self.assertTrue(
            prompt.endswith("Return only the final text, no rule commentary.")
        )

    def test_model_spec_file_slug_is_safe_for_provider_and_thinking_suffixes(self):
        slug = run_pi_bench.model_spec_file_slug("openai-codex/gpt-5.6-sol:medium")

        self.assertEqual(slug, "openai-codex_gpt-5.6-sol_medium")


class BenchmarkAggregationTests(unittest.TestCase):
    def test_smoke_aggregation_ignores_other_scenario_rows(self):
        model = "example/model:medium"
        expected_scenario = {"id": "expected"}
        rows = [
            self.make_raw_row(model, condition, scenario_id)
            for condition in run_pi_bench.CONDITIONS
            for scenario_id in ("expected", "extra")
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            results_directory = pathlib.Path(temporary_directory)
            raw_directory = results_directory / "raw"
            raw_directory.mkdir()
            for index, row in enumerate(rows):
                (raw_directory / f"{index}.json").write_text(json.dumps(row))

            results = run_pi_bench.aggregate_benchmark_results(
                [model], [expected_scenario], results_directory
            )

        self.assertEqual(results["runs"], 2)
        self.assertEqual(results["models"][0]["baseline"]["runs"], 1)
        self.assertEqual(results["models"][0]["skill"]["runs"], 1)

    def test_report_handles_zero_violation_baselines(self):
        model = "example/model:medium"
        rows = [
            self.make_raw_row(model, condition, "expected")
            for condition in run_pi_bench.CONDITIONS
        ]

        with tempfile.TemporaryDirectory() as temporary_directory:
            results_directory = pathlib.Path(temporary_directory)
            raw_directory = results_directory / "raw"
            raw_directory.mkdir()
            for index, row in enumerate(rows):
                (raw_directory / f"{index}.json").write_text(json.dumps(row))
            results = run_pi_bench.aggregate_benchmark_results(
                [model], [{"id": "expected"}], results_directory
            )

            with contextlib.redirect_stdout(io.StringIO()):
                run_pi_bench.write_benchmark_report(results, [model], results_directory)

            report = (results_directory / "RESULTS.md").read_text()

        self.assertIn("percentage reduction is undefined", report)

    @staticmethod
    def make_raw_row(model, condition, scenario_id):
        return {
            "model": model,
            "condition": condition,
            "scenario": scenario_id,
            "duration_ms": 100,
            "output_tokens": 10,
            "reasoning_tokens": 2,
            "cost_usd": 0,
            "lint": {
                "violations_per_100w": 0,
                "violations_total": 0,
                "words": 10,
                "mean_sentence_words": 5,
            },
        }


if __name__ == "__main__":
    unittest.main()

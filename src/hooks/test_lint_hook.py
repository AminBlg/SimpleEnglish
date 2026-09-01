import json, pathlib, subprocess, sys, tempfile
HERE = pathlib.Path(__file__).resolve().parent
HOOK = HERE / "lint_hook.py"

def run(event):
    r = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(event), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr

def test_post_tool_use_flags_a_slop_markdown_file():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("You should simply leverage the robust tool, making it seamless.\n"); path = f.name
    code, out, err = run({"hook_event_name": "PostToolUse", "tool_name": "Write", "tool_input": {"file_path": path}})
    assert code == 2 and "STE violations" in err, (code, err)

def test_post_tool_use_ignores_clean_file_and_non_markdown():
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("Run the migration. Then restart the service.\n"); path = f.name
    assert run({"hook_event_name": "PostToolUse", "tool_input": {"file_path": path}})[0] == 0
    assert run({"hook_event_name": "PostToolUse", "tool_input": {"file_path": "/tmp/x.py"}})[0] == 0

def test_stop_flags_long_slop_reply_and_never_blocks():
    long = "Great question! " + "This is a robust sentence. " * 7 + "I hope this helps!"
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": long})
    assert code == 0 and "systemMessage" in out, (code, out)
    msg = json.loads(out)["systemMessage"]
    assert "sentences" in msg and "opener" in msg and "closer" in msg and "slop" in msg, msg

def test_stop_is_silent_on_a_good_reply():
    code, out, err = run({"hook_event_name": "Stop", "last_assistant_message": "The build failed because the disk was full. Free 2 GB and run it again."})
    assert code == 0 and out.strip() == "", (code, out)

def test_garbage_stdin_exits_zero():
    r = subprocess.run([sys.executable, str(HOOK)], input="not json", capture_output=True, text=True)
    assert r.returncode == 0

if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn(); print("ok", name)

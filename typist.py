import subprocess
import shutil
import sys

import state
from code_change_workflow import execute_code_change_workflow


def select_file():
    try:
        selected_item = subprocess.check_output(["fzf"], text=True).strip()
        state.set("selected_file", selected_item)
        # Reset change and test when selecting a new file
        state.set("change", "")
        state.set("test_command", "")
        state.set("custom_instructions", "")
        print(f"Selected file: {selected_item}")
    except subprocess.CalledProcessError:
        print("File selection canceled.")


def apply_change(change):
    if not state.get("selected_file"):
        print("No file selected. Use 'file' to choose a file first.")
        return
    state.set("change", change)
    state.append("change_requests", change)
    print(f"Change applied: {change}")
    perform_code_change()


def set_test_command(test_command):
    state.set("test_command", test_command)
    print(f"Test command set: {test_command}")


def run_test():
    test_command = state.get("test_command")
    if not test_command:
        print("No test command set. Use 'test' to set a test command first.")
        return
    print(f"Running test command: {test_command}")
    result = subprocess.run(test_command, shell=True, capture_output=True, text=True)
    print("\nTest Output (stdout):")
    print(result.stdout)
    print("\nTest Output (stderr):")
    print(result.stderr)


def set_custom_instructions(instructions):
    state.set("custom_instructions", instructions)
    print(f"Custom instructions set: {instructions}")


def retry_last_change():
    last_change = state.get("change_requests").strip().split("\n")[-1]
    if last_change:
        apply_change(last_change)
        print(f"Retrying last change: {last_change}")
    else:
        print("No previous changes to retry.")


def approve_changes():
    selected_file = state.get("selected_file")
    temp_file_path = state.get("temp_file_path")
    if selected_file and temp_file_path:
        shutil.copy(temp_file_path, selected_file)
        print(f"Approved changes copied to: {selected_file}")
    else:
        print("Error: Missing selected file or temporary file path.")


def set_formatter_command(formatter_command):
    state.set("formatter_command", formatter_command)
    print(f"Formatter command set: {formatter_command}")


def perform_code_change():
    selected_file = state.get("selected_file")
    change = state.get("change")
    custom_instructions = state.get("custom_instructions")

    if not selected_file or not change:
        print("No file or change to execute. Aborting.")
        return

    format_cmd = state.get("formatter_command") or None

    change_request = (
        custom_instructions + "\n" + change if custom_instructions else change
    )

    test_cmd = state.get("test_command") or None

    temp_file_path = execute_code_change_workflow(
        target_file=selected_file,
        code_change=change_request,
        test_cmd=test_cmd,
        format_cmd=format_cmd,
    )

    if temp_file_path:
        state.set("temp_file_path", temp_file_path)


def display_status():
    print(f"  File:                {state.get('selected_file') or 'None'}")
    print(f"  Change:              {state.get('change') or 'None'}")
    print(f"  Custom Instructions: {state.get('custom_instructions') or 'None'}")
    print(f"  Test:                {state.get('test_command') or 'None'}")
    print(f"  Format:              {state.get('formatter_command') or 'None'}")


def main():
    state.init()

    if len(sys.argv) < 2:
        print("Usage: python your_script.py [command] [options]")
        return

    command = sys.argv[1]

    if command in ["file", "f"]:
        select_file()
    elif command in ["change", "c"] and len(sys.argv) > 2:
        apply_change(" ".join(sys.argv[2:]))
    elif command in ["set_test_command", "test_cmd", "cmd", "tc"] and len(sys.argv) > 2:
        set_test_command(" ".join(sys.argv[2:]))
    elif command in ["run_test", "run"]:
        run_test()
    elif command in ["instructions", "i"] and len(sys.argv) > 2:
        set_custom_instructions(" ".join(sys.argv[2:]))
    elif command in ["retry", "r"]:
        retry_last_change()
    elif command in ["approve", "a"]:
        approve_changes()
    elif command in ["status", "st"]:
        display_status()
    elif command in ["format", "fmt"] and len(sys.argv) > 2:
        set_formatter_command(" ".join(sys.argv[2:]))
    else:
        print(f"Unknown command: {command}")
        print(
            "Available commands: file (f), change (c), test_cmd (tc), run_test (run), instructions (i), retry (r), approve (a), status (st), format (fmt)"
        )


if __name__ == "__main__":
    main()

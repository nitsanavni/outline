import subprocess
import shutil
import sys

import state
from state import (
    selected_file,
    code_change,
    custom_instructions,
    test_command,
    format_command,
    change_requests,
    temp_file_path,
)
from code_change_workflow import execute_code_change_workflow


def select_file():
    try:
        selected_file.set(subprocess.check_output(["fzf"], text=True).strip())
        code_change.clear()
        test_command.clear()
        format_command.clear()
    except subprocess.CalledProcessError:
        print("File selection canceled.")


def apply_change(change):
    if not selected_file.get():
        print("No file selected. Use 'file' to choose a file first.")
        return
    code_change.set(change)
    change_requests.append(change)
    perform_code_change()


def run_test():
    if not test_command.get():
        print("No test command set. Use 'test' to set a test command first.")
        return
    result = subprocess.run(
        test_command.get(), shell=True, capture_output=True, text=True
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)


def retry_last_change():
    last_change = change_requests.get().strip().split("\n")[-1]
    if last_change:
        print(f"Retrying last change: {last_change}")
        apply_change(last_change)
    else:
        print("No previous changes to retry.")


def approve_changes():
    if selected_file.get() and temp_file_path.get():
        shutil.copy(temp_file_path.get(), selected_file.get())
        print(f"Approved changes copied to: {selected_file.get()}")
    else:
        print("Error: Missing selected file or temporary file path.")


def set_formatter_command(formatter_command):
    format_command.set(formatter_command)


def perform_code_change():
    if not selected_file.get() or not code_change.get():
        print("No file or change to execute. Aborting.")
        return

    change_request = "\n".join(
        [s for s in [custom_instructions.get(), code_change.get()] if s]
    )

    temp_file_path.set(
        execute_code_change_workflow(
            target_file=selected_file.get(),
            code_change=change_request,
            test_cmd=test_command.get(),
            format_cmd=format_command.get(),
        )
    )


def display_status():
    print(f"  File:                {selected_file.get() or 'None'}")
    print(f"  Change:              {code_change.get() or 'None'}")
    print(f"  Custom Instructions: {custom_instructions.get() or 'None'}")
    print(f"  Test:                {test_command.get() or 'None'}")
    print(f"  Format:              {format_command.get() or 'None'}")


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
        test_command.set(" ".join(sys.argv[2:]))
    elif command in ["run_test", "run"]:
        run_test()
    elif command in ["instructions", "i"] and len(sys.argv) > 2:
        custom_instructions.set(" ".join(sys.argv[2:]))
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

import subprocess
import re
import shutil
import os
import sys

# Directory to store state files
STATE_DIR = ".typist"


def ensure_state_dir():
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)


def write_state(filename, content):
    with open(os.path.join(STATE_DIR, filename), "w") as f:
        f.write(content)


def read_state(filename):
    filepath = os.path.join(STATE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read().strip()
    return None


def append_to_state(filename, content):
    with open(os.path.join(STATE_DIR, filename), "a") as f:
        f.write(content + "\n")


def select_file():
    try:
        selected_item = subprocess.check_output(["fzf"], text=True).strip()
        write_state("selected_file", selected_item)
        # Reset change and test when selecting a new file
        write_state("change", "")
        write_state("test_command", "")
        write_state("custom_instructions", "")
        print(f"Selected file: {selected_item}")
    except subprocess.CalledProcessError:
        print("File selection canceled.")


def apply_change(change):
    if not read_state("selected_file"):
        print("No file selected. Use 'file' to choose a file first.")
        return
    write_state("change", change)
    append_to_state("change_requests", change)
    print(f"Change applied: {change}")
    execute_script()


def set_test_command(test_command):
    write_state("test_command", test_command)
    print(f"Test command set: {test_command}")


def run_test():
    test_command = read_state("test_command")
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
    write_state("custom_instructions", instructions)
    print(f"Custom instructions set: {instructions}")


def retry_last_change():
    last_change = read_state("change_requests").strip().split("\n")[-1]
    if last_change:
        apply_change(last_change)
        print(f"Retrying last change: {last_change}")
    else:
        print("No previous changes to retry.")


def approve_changes():
    selected_file = read_state("selected_file")
    temp_file_path = read_state("temp_file_path")
    if selected_file and temp_file_path:
        shutil.copy(temp_file_path, selected_file)
        print(f"Approved changes copied to: {selected_file}")
    else:
        print("Error: Missing selected file or temporary file path.")


def execute_script():
    selected_file = read_state("selected_file")
    change = read_state("change")
    custom_instructions = read_state("custom_instructions")

    if not selected_file or not change:
        print("No file or change to execute. Aborting.")
        return

    change_command = (
        custom_instructions + "\n" + change if custom_instructions else change
    )

    command = [
        "python",
        "type.py",
        "--file",
        selected_file,
        "--change",
        change_command,
    ]

    test_command = read_state("test_command")
    if test_command:
        command.extend(["--test", test_command])

    print("\nExecuting command: " + " ".join(command))

    result = subprocess.run(command, capture_output=True, text=True)

    print("\nOutput (stdout):")
    print(result.stdout)

    print("\nOutput (stderr):")
    print(result.stderr)

    temp_file_path = parse_temp_file_path(result.stdout)
    if temp_file_path:
        write_state("temp_file_path", temp_file_path)
        print(f"Temporary modified file created at: {temp_file_path}")


def parse_temp_file_path(stdout):
    pattern = r"temporary modified file created at: (.+)"
    match = re.search(pattern, stdout, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def display_status():
    selected_file = read_state("selected_file")
    change = read_state("change")
    test_command = read_state("test_command")
    custom_instructions = read_state("custom_instructions")

    print("\nCurrent State:")
    print(f"  File:                {selected_file if selected_file else 'None'}")
    print(f"  Change:              {change if change else 'None'}")
    print(f"  Test Command:        {test_command if test_command else 'None'}")
    print(
        f"  Custom Instructions: {custom_instructions if custom_instructions else 'None'}\n"
    )


def main():
    ensure_state_dir()

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
    else:
        print(f"Unknown command: {command}")
        print(
            "Available commands: file (f), change (c), test_cmd (tc), run_test (run), instructions (i), retry (r), approve (a), status (st)"
        )


if __name__ == "__main__":
    main()

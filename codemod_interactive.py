import subprocess
import re
import shutil
import os

# todos
# - after we change the file, don't exec, back to prompt the user
# - hit 'a' to approve the last change - copy to
# - add 'custom instructions' - additional instructions to add before each change request


def select_file_using_fzf():
    try:
        selected_item = subprocess.check_output(["fzf"], text=True).strip()
        return selected_item
    except subprocess.CalledProcessError:
        return None


def prompt_user(args):
    """
    Prompt the user to modify any of the arguments. The default is modifying the 'change' argument.
    """
    if not args["file"]:
        args["file"] = select_file_using_fzf()
        # Set change and test to None when selecting the file
        args["change"] = None
        args["test"] = None

    print("\nCurrent values:")
    print(f"  File:   {args['file']}")
    print(f"  Change: {args['change']}")
    print(f"  Test:   {args['test'] if args['test'] else 'No test command'}\n")

    choice = input(" > ").strip().lower()  # Changed the prompt to just ' > '

    if choice in ["quit", "q"]:
        print("Exiting the program...")
        exit(0)
    elif choice in ["f", "file"]:
        args["file"] = select_file_using_fzf()
        # Reset change and test after selecting a new file
        args["change"] = None
        args["test"] = None
        return prompt_user(args)
    elif choice == "change":
        args["change"] = input("Enter new change: ").strip()
    elif choice in ["t", "test"]:
        args["test"] = input(
            "Enter new test command (or leave blank to skip testing): "
        ).strip()
    elif choice in ["a", "approve"]:
        args["approved"] = True  # Set a bool to true on approval
        return args
    else:
        # Assume the input is the new value for 'change' if it's anything else
        args["change"] = choice

    return args


def execute_script(current_values):
    """
    Execute the existing script with the current arguments and capture its stdout and stderr.
    """
    command = [
        "python",
        "codemod_diff.py",
        "--file",
        current_values["file"],
        "--change",
        current_values["change"] if current_values["change"] is not None else "",
    ]
    if current_values["test"]:
        command.extend(["--test", current_values["test"]])

    print("\nExecuting command: " + " ".join(command))

    # Execute the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Output the stdout and stderr to the user
    print("\nOutput (stdout):")
    print(result.stdout)

    print("\nOutput (stderr):")
    print(result.stderr)

    # Parse the output to find the path
    temp_file_path = parse_temp_file_path(result.stdout)

    if temp_file_path:
        print(f"Temporary modified file created at: {temp_file_path}")

    return temp_file_path


def parse_temp_file_path(stdout):
    """
    Parse the stdout to find the temporary modified file path.
    """
    pattern = r"temporary modified file created at: (.+)"
    match = re.search(pattern, stdout, re.IGNORECASE)
    if match:
        return match.group(1)
    return None


def main():
    args = {
        "file": None,
        "change": None,
        "test": None,
        "approved": False,  # Initialize the approved state
    }

    while True:
        args = prompt_user(args)

        if args["approved"] and "temp_file_path" in locals() and args["file"]:
            shutil.copy(temp_file_path, args["file"])
            print(f"Approved changes copied to: {args['file']}")
            args["approved"] = False
            continue

        temp_file_path = execute_script(args)


if __name__ == "__main__":
    main()

import subprocess
import re
import shutil


# Initialize a list to keep track of change requests
change_requests = []


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
    print(f"  Test:   {args['test'] if args['test'] else 'No test command'}")
    print(
        f"  Custom Instructions: {args['custom_instructions'] if args['custom_instructions'] else 'None'}\n"
    )

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
        new_change = input("Enter new change: ").strip()
        args["change"] = new_change
        change_requests.append(new_change)  # Keep track of all change requests
    elif choice in ["t", "test"]:
        args["test"] = input(
            "Enter new test command (or leave blank to skip testing): "
        ).strip()
    elif choice in ["a", "approve"]:
        args["approved"] = True  # Set a bool to true on approval
        print("Change approved.")
        return args
    elif choice in ["i", "instructions"]:
        args["custom_instructions"] = input("Enter custom instructions: ").strip()
    elif choice in ["retry", "r"]:
        if change_requests:
            last_change = change_requests[-1]
            print(f"Retrying last change: {last_change}")
            args["change"] = last_change
        else:
            print("No previous changes to retry.")
    else:
        # Assume the input is the new value for 'change' if it's anything else
        args["change"] = choice
        change_requests.append(choice)  # Track the new change request

    return args


def execute_script(current_values):
    """
    Execute the existing script with the current arguments and capture its stdout and stderr.
    If there are no changes, abort and return.
    """
    if current_values["change"] is None:
        print("No changes to execute. Aborting.")
        return None

    i = current_values["custom_instructions"]
    if i:
        change = i + "\n" + current_values["change"]
    else:
        change = current_values["change"]

    command = [
        "python",
        "codemod_diff.py",
        "--file",
        current_values["file"],
        "--change",
        change,
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

    # Clear the "change" argument after executing the script
    current_values["change"] = None

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
        "custom_instructions": None,  # Placeholder for custom instructions
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

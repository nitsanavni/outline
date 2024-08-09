import subprocess


def select_file_using_fzf():
    try:
        selected_item = subprocess.check_output(["fzf"], text=True).strip()
        return selected_item
    except subprocess.CalledProcessError:
        return None


def prompt_user(current_values):
    """
    Prompt the user to modify any of the arguments. The default is modifying the 'change' argument.
    """
    print("\nCurrent values:")
    print(f"  File:   {current_values['file']}")
    print(f"  Change: {current_values['change']}")
    print(
        f"  Test:   {current_values['test'] if current_values['test'] else 'No test command'}\n"
    )

    choice = (
        input(
            "Which argument do you want to change? (file/change/test or type 'quit' to exit, or press Enter to modify 'change'): "
        )
        .strip()
        .lower()
    )

    if choice == "quit":
        print("Exiting the program...")
        exit(0)
    elif choice == "file":
        current_values["file"] = select_file_using_fzf()
    elif choice == "change":
        current_values["change"] = input("Enter new change: ").strip()
    elif choice == "test":
        current_values["test"] = input(
            "Enter new test command (or leave blank to skip testing): "
        ).strip()
    else:
        # Assume the input is the new value for 'change' if it's anything else
        current_values["change"] = choice

    return current_values


def execute_script(current_values):
    """
    Execute the existing script with the current arguments.
    """
    command = [
        "python",
        "codemod_diff.py",
        "--file",
        current_values["file"],
        "--change",
        current_values["change"],
    ]
    if current_values["test"]:
        command.extend(["--test", current_values["test"]])

    print("\nExecuting command: " + " ".join(command))
    subprocess.run(command)


def main():
    # Initial state of the arguments
    current_values = {
        "file": None,
        "change": input("Enter initial change: ").strip(),
        "test": input(
            "Enter initial test command (or leave blank to skip testing): "
        ).strip(),
    }

    current_values["file"] = select_file_using_fzf()

    # Execute the script with initial values right after gathering them
    execute_script(current_values)

    while True:
        # Execute the script with current values
        execute_script(current_values)

        # Prompt the user to modify arguments after executing
        current_values = prompt_user(current_values)


if __name__ == "__main__":
    main()

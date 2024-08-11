import subprocess


# todos
# - hit 't' to run tests
# - hit 'q' to quit
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

    print("\nCurrent values:")
    print(f"  File:   {args['file']}")
    print(f"  Change: {args['change']}")
    print(f"  Test:   {args['test'] if args['test'] else 'No test command'}\n")

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
        args["file"] = select_file_using_fzf()
    elif choice == "change":
        args["change"] = input("Enter new change: ").strip()
    elif choice == "test":
        args["test"] = input(
            "Enter new test command (or leave blank to skip testing): "
        ).strip()
    else:
        # Assume the input is the new value for 'change' if it's anything else
        args["change"] = choice

    return args


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
    args = prompt_user(
        {
            "file": None,
            "change": None,
            "test": None,
        }
    )

    while True:
        execute_script(args)

        args = prompt_user(args)


if __name__ == "__main__":
    main()

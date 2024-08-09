import subprocess


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
            "Which argument do you want to change? (file/change/test or press Enter to modify 'change'): "
        )
        .strip()
        .lower()
    )

    if choice == "file":
        current_values["file"] = input("Enter new file path: ").strip()
    elif choice == "change":
        current_values["change"] = input("Enter new change: ").strip()
    elif choice == "test":
        current_values["test"] = input(
            "Enter new test command (or leave blank to skip testing): "
        ).strip()
    else:
        current_values["change"] = input("Enter new change: ").strip()

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
        "file": input("Enter initial file path: ").strip(),
        "change": input("Enter initial change: ").strip(),
        "test": input(
            "Enter initial test command (or leave blank to skip testing): "
        ).strip(),
    }

    while True:
        # Prompt the user to modify arguments if needed
        current_values = prompt_user(current_values)

        # Execute the wrapped script with the current arguments
        execute_script(current_values)

        # Ask if the user wants to make another change or exit
        cont = input("\nDo you want to make another change? (y/n): ").strip().lower()
        if cont != "y":
            break


if __name__ == "__main__":
    main()

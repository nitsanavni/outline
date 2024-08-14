import sys

from approve_changes import approve_changes
from display_status import display_status
from perform_code_change import perform_code_change
from print_usage import print_usage
from retry_last_change import retry_last_change
from run_test import run_test
from select_file import select_file
from show_diff import show_diff
from show_current_file import show_current_file
from fancy_prompt import fancy_prompt
import state
from state import (
    custom_instructions,
    test_command,
    format_command,
    diff_command,
)


def main():
    state.init()

    if len(sys.argv) < 2:
        print_usage()
        return

    command = sys.argv[1]

    if command in ["file", "f"]:
        select_file()
    elif command in ["change", "c"]:
        if len(sys.argv) > 2:
            perform_code_change(" ".join(sys.argv[2:]))
        else:
            perform_code_change(fancy_prompt("Code change (use '@' for files): "))
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
        run_test()
    elif command in ["status", "st"]:
        display_status()
    elif command in ["format", "fmt"] and len(sys.argv) > 2:
        format_command.set(" ".join(sys.argv[2:]))
    elif command in ["diff_cmd", "diff"] and len(sys.argv) > 2:
        diff_command.set(" ".join(sys.argv[2:]))
    elif command in ["show"]:
        subcommand = sys.argv[2] if len(sys.argv) > 2 else ""
        if subcommand == "diff":
            show_diff()
        if subcommand == "file":
            show_current_file()
    else:
        print(f"Unknown command: {command}")
        print_usage()


if __name__ == "__main__":
    main()

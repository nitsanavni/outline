from code_change_workflow import execute_code_change_workflow
from expand_file_references import expand_file_references
from state import (
    change_requests,
    code_change,
    custom_instructions,
    diff_command,
    format_command,
    selected_file,
    temp_file_path,
    test_command,
)


class FileSelectionError(Exception):
    """Custom exception for file selection errors."""


def update_and_load_state(change):
    target_file = selected_file.get()
    if not target_file:
        raise FileSelectionError("No file selected. Use 'file' to choose a file first.")

    code_change.set(change)
    change_requests.append(change)

    change_request = "\n".join(filter(None, [custom_instructions.get(), change]))

    change_request = expand_file_references(change_request)

    return (
        target_file,
        change_request,
        test_command.get(),
        format_command.get(),
        diff_command.get(),
    )


def perform_code_change(change):
    try:
        target_file, change_request, test_cmd, format_cmd, diff_cmd = (
            update_and_load_state(change)
        )
    except FileSelectionError as e:
        print(e)
        return

    temp_file = execute_code_change_workflow(
        target_file=target_file,
        code_change=change_request,
        test_cmd=test_cmd,
        format_cmd=format_cmd,
        diff_cmd=diff_cmd,
    )

    temp_file_path.set(temp_file)

from code_change_workflow import execute_code_change_workflow
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


def perform_code_change(change):
    if not selected_file.get():
        print("No file selected. Use 'file' to choose a file first.")
        return

    code_change.set(change)
    change_requests.append(change)

    change_request = "\n".join(
        [s for s in [custom_instructions.get(), code_change.get()] if s]
    )

    temp_file_path.set(
        execute_code_change_workflow(
            target_file=selected_file.get(),
            code_change=change_request,
            test_cmd=test_command.get(),
            format_cmd=format_command.get(),
            diff_cmd=diff_command.get(),
        )
    )

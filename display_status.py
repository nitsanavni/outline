from state import (
    code_change,
    custom_instructions,
    diff_command,
    format_command,
    selected_file,
    test_command,
)


def display_status():
    for s in [
        selected_file,
        code_change,
        custom_instructions,
        test_command,
        format_command,
        diff_command,
    ]:
        if s.get():
            print(f"{s.display_name}: {s.get()}")

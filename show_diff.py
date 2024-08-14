import os

import state


def show_diff():
    file = state.selected_file.get()
    if not file:
        return
    temp_file = state.temp_file_path.get()
    if not temp_file:
        return

    os.system(
        (state.diff_command.get() or "diff {file1} {file2}").format(
            file1=temp_file, file2=file
        )
    )

import os

import state


def show_current_file():
    file = state.selected_file.get()
    if not file:
        return

    os.system(f"bat {file}")

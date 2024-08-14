import subprocess

from state import code_change, selected_file


def select_file_with_fzf():
    try:
        return subprocess.check_output(["fzf"], text=True).strip()
    except subprocess.CalledProcessError:
        return None


def select_file():
    file_selected = select_file_with_fzf()
    if file_selected is not None:
        selected_file.set(file_selected)
        code_change.clear()

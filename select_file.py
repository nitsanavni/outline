import subprocess

from state import code_change, selected_file


def select_file_with_fzf():
    try:
        return subprocess.check_output(
            ["fzf", "--preview", "clp {}"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        return None


def select_file(file=None):
    if not file:
        file = select_file_with_fzf()
    if file is not None:
        selected_file.set(file)
        code_change.clear()

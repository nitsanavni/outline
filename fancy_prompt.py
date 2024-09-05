#!/usr/bin/env python
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
import subprocess

from main_decorator import main

bindings = KeyBindings()


def trigger_fzf():
    git_ls_files = subprocess.check_output(["git", "ls-files", "--cached", "--others", "--exclude-standard"], text=True).strip().splitlines()
    fzf_output = subprocess.run(["fzf"], input='\n'.join(git_ls_files), text=True, capture_output=True)
    return fzf_output.stdout.strip()


@bindings.add("@")
def handle_at_key(event):
    file = trigger_fzf()
    if not file:
        return
    buffer = event.app.current_buffer
    buffer.insert_text(f"@{file}")


def shell(command):
    return subprocess.check_output(command, shell=True, text=True).strip()


def fzf_to_select_lines(file):
    start_line = int(shell(f"cat -n {file} | tac | fzf | cut -f1"))
    end_line = int(
        shell(f"cat -n {file} | tail -n +{start_line} | tac | fzf | cut -f1")
    )

    return start_line, end_line


@bindings.add(":")
def handle_colon(event):
    buffer = event.app.current_buffer
    current_text = buffer.text
    is_last_word_a_file = current_text.split()[-1].startswith("@")
    if not is_last_word_a_file:
        buffer.insert_text(":")
        return
    the_file = current_text.split()[-1][1:]
    start_line, end_line = fzf_to_select_lines(the_file)
    buffer.insert_text(f":{start_line}-{end_line}")


def fancy_prompt(prompt_text, history_file=".fancy_prompt_history"):
    return prompt(prompt_text, key_bindings=bindings, multiline=True, history=FileHistory(history_file))


if __name__ == "__main__":
    print(fancy_prompt(""))

from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.keys import Keys
import subprocess

# file exists
import os


# Function to handle @ key press and trigger fzf
def trigger_fzf():
    return subprocess.check_output(["fzf"], text=True).strip()


def shell(command):
    return subprocess.check_output(command, shell=True, text=True).strip()


def fzf_to_select_lines(file):
    start_line = int(shell(f"cat -n {file} | tac | fzf | cut -f1"))
    end_line = int(
        shell(f"cat -n {file} | tail -n +{start_line} | tac |  fzf | cut -f1")
    )

    return start_line, end_line


# Key bindings
bindings = KeyBindings()


# Define what happens when '@' is pressed
@bindings.add("@")
def handle_at_key(event):
    fzf_result = trigger_fzf()
    if fzf_result:
        buffer = event.app.current_buffer
        buffer.insert_text(f"file:///{fzf_result}")


@bindings.add("#", "L")
def handle_hashtag_l_key(event):
    buffer = event.app.current_buffer

    text = buffer.text
    last_file = text.split("file:///")[-1]

    exists = os.path.exists(last_file)
    if exists:
        start_line, end_line = fzf_to_select_lines(last_file)
        buffer.insert_text(f"#L{start_line}:{end_line}")


# Define what happens when 'Enter' is pressed
@bindings.add("enter")
def handle_enter(event):
    buffer = event.app.current_buffer
    event.app.exit(result=buffer.text)


@bindings.add(Keys.Down)
def _(event):
    event.current_buffer.insert_text("\n")


# Create a prompt session with multiline support
session = PromptSession(multiline=True, key_bindings=bindings)


def main():
    try:
        text = session.prompt("> ")
        print(f"You entered: {text}")
    except KeyboardInterrupt:
        return
    except EOFError:
        return


if __name__ == "__main__":
    main()

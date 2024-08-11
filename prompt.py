from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.keys import Keys
from subprocess import Popen, PIPE
import subprocess


# Function to handle @ key press and trigger fzf
def trigger_fzf():
    return subprocess.check_output(["fzf"], text=True).strip()


# Key bindings
bindings = KeyBindings()


# Define what happens when '@' is pressed
@bindings.add("@")
def handle_at_key(event):
    fzf_result = trigger_fzf()
    if fzf_result:
        buffer = event.app.current_buffer
        buffer.insert_text(f"file:///{fzf_result}")


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

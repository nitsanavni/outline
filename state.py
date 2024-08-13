import os


STATE_DIR = ".typist"


def init():
    ensure_state_dir()


def ensure_state_dir():
    if not os.path.exists(STATE_DIR):
        os.makedirs(STATE_DIR)


def set(filename, content):
    with open(os.path.join(STATE_DIR, filename), "w") as f:
        f.write(content)


def get(filename):
    filepath = os.path.join(STATE_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read().strip() or None
    return None


def append(filename, content):
    with open(os.path.join(STATE_DIR, filename), "a") as f:
        f.write(content + "\n")


class Thing:
    def __init__(self, name):
        self.name = name

    def get(self):
        return get(self.name)

    def set(self, content):
        set(self.name, content)

    def clear(self):
        set(self.name, "")

    def append(self, content):
        append(self.name, content)


selected_file = Thing("selected_file")
code_change = Thing("change")
custom_instructions = Thing("custom_instructions")
test_command = Thing("test_command")
format_command = Thing("formatter_command")
change_requests = Thing("change_requests")
temp_file_path = Thing("temp_file_path")
diff_command = Thing("diff_command")
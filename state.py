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
    def __init__(self, name, display_name=None):
        self.name = name
        self.display_name = display_name or name

    def get(self):
        return get(self.name)

    def set(self, content):
        set(self.name, content)

    def clear(self):
        set(self.name, "")

    def append(self, content):
        append(self.name, content)


selected_file = Thing("selected_file", "File")
code_change = Thing("change", "Last Change")
custom_instructions = Thing("custom_instructions", "Custom Instructions")
test_command = Thing("test_command", "Test")
format_command = Thing("formatter_command", "Format")
diff_command = Thing("diff_command", "Diff")
change_requests = Thing("change_requests")
temp_file_path = Thing("temp_file_path")

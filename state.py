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
            return f.read().strip()
    return None


def append(filename, content):
    with open(os.path.join(STATE_DIR, filename), "a") as f:
        f.write(content + "\n")

import os


def debug(msg):
    if not os.environ.get("DEBUG"):
        return
    print(msg, file=sys.stderr)
    return msg

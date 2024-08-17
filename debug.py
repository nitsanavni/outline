import os
import sys


def debug(msg):
    if not os.environ.get("DEBUG"):
        return msg
    print(msg, file=sys.stderr)
    return msg

import sys
import os
import inspect


def main(func):
    if not inspect.getmodule(func).__name__ == "__main__":
        return func

    num_of_params = len(inspect.signature(func).parameters)

    if num_of_params == 0:
        print(func())
    else:
        if os.isatty(sys.stdin.fileno()):
            return func

        print(func(sys.stdin.read()))

    return func

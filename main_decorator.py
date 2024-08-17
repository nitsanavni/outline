import sys
import inspect


def main(func):
    if inspect.getmodule(func).__name__ == "__main__":
        print(func(sys.stdin.read()))
    return func

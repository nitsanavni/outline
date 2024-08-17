import sys
import inspect


def main(func):
    if inspect.getmodule(func).__name__ == "__main__":
        num_of_params = len(inspect.signature(func).parameters)
        if num_of_params == 0:
            print(func())
        else:
            print(func(sys.stdin.read()))
    return func

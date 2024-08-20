import inspect
import os
import sys
from typing import Optional
from approvaltests import verify
from approvaltests.core.options import Options


class Name:
    def __init__(self, base) -> None:
        self.base = base

    def get_received_filename(self, base: Optional[str] = None) -> str:
        base = base or self.base
        return base + ".received"

    def get_approved_filename(self, base: Optional[str] = None) -> str:
        base = base or self.base
        return base + ".approved"


def verify_with(input):
    def decorator(func):
        cli_args = sys.argv[1:]
        is_verify = "--verify" in cli_args or os.environ.get("VERIFY")

        if not is_verify:
            return func

        # this extra wrapper is working around an err from stack_frame_namer
        def test_func():
            func_filename = inspect.getsourcefile(func)
            func_name = func.__name__
            verify(
                func(input),
                options=Options().with_namer(Name(f"{func_filename}.{func_name}")),
            )

        func_module_name = inspect.getmodule(func).__name__
        # if func_module_name == "__main__":
        test_func()

        return func

    return decorator


if __name__ == "__main__":
    # find all files using the verify_with decorator
    # and import them
    files = [
        f for f in os.listdir(".") if f.endswith(".py") and f != "verify_decorator.py"
    ]
    files_with_verify = [f for f in files if "@verify_with(" in open(f).read()]

    os.environ["VERIFY"] = "true"

    for f in files_with_verify:
        print(f"importing {f}")
        # import the file
        __import__(f[:-3])

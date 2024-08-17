import sys
import subprocess

from main_decorator import main
from state import test_command


@main
def run_test():
    if not test_command.get():
        return
    result = subprocess.run(
        test_command.get(), shell=True, capture_output=True, text=True
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)

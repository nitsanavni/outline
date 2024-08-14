from state import test_command


import subprocess


def run_test():
    if not test_command.get():
        return
    result = subprocess.run(
        test_command.get(), shell=True, capture_output=True, text=True
    )
    print(result.stdout)
    print(result.stderr, file=sys.stderr)

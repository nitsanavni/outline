import sys
import tempfile
import subprocess
import shutil
import os
from pathlib import Path


def apply_change(original_file, change):
    # Assuming codemod.py is in the same directory and takes care of applying the change
    new_code = subprocess.check_output(["python", "codemod.py", original_file, change])
    return new_code.decode("utf-8")


def show_diff(file1, file2):
    subprocess.run(["code", "--diff", file1, file2])


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply code change with a diff and optional test"
    )
    parser.add_argument("--file", required=True, help="File to modify")
    parser.add_argument("--change", required=True, help="Change to apply")
    parser.add_argument("--test", help="Test command to run after applying the change")

    args = parser.parse_args()

    original_file = args.file
    change = args.change
    test_cmd = args.test

    # Create temporary files for the original and modified code
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as tmp_original, tempfile.NamedTemporaryFile(delete=False) as tmp_modified:
        # Copy the original file to the temp original file
        shutil.copyfile(original_file, tmp_original.name)

        # Apply the change and write the new code to the temp modified file
        new_code = apply_change(original_file, change)
        with open(tmp_modified.name, "w") as f:
            f.write(new_code)

        if test_cmd:
            # Save a copy of the original file
            backup_file = tempfile.NamedTemporaryFile(delete=False)
            shutil.copyfile(original_file, backup_file.name)

            try:
                # Replace the original file with the modified version
                shutil.copyfile(tmp_modified.name, original_file)

                # Run the test command
                subprocess.run(test_cmd, shell=True, check=True)
            finally:
                # Restore the original file
                shutil.copyfile(backup_file.name, original_file)
                backup_file.close()

        show_diff(tmp_modified.name, original_file)

        os.remove(tmp_original.name)


if __name__ == "__main__":
    main()

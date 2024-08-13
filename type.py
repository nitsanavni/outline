import os
import shutil
import subprocess
import tempfile


def apply_change(original_file, change):
    new_code = subprocess.check_output(["python", "codemod.py", original_file, change])
    return new_code.decode("utf-8")


def format_code(file, formatter):
    subprocess.run(formatter.split() + [file], check=True)


def show_diff(file1, file2, diff_cmd=None):
    if diff_cmd:
        # Replace placeholders in the diff command with the file paths
        diff_cmd = diff_cmd.replace("{file1}", file1).replace("{file2}", file2)
        subprocess.run(diff_cmd, shell=True)
    else:
        subprocess.run(["code", "--diff", file1, file2])


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Apply code change with a diff and optional test"
    )
    parser.add_argument("--file", required=True, help="File to modify")
    parser.add_argument("--change", required=True, help="Change to apply")
    parser.add_argument("--test", help="Test command to run after applying the change")
    parser.add_argument(
        "--format", help="Code formatter command to run on the modified file"
    )
    parser.add_argument(
        "--diff", help="Custom diff command to compare the original and modified files"
    )

    args = parser.parse_args()

    original_file = args.file
    change = args.change
    test_cmd = args.test
    formatter = args.format
    diff_cmd = args.diff

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as tmp_original, tempfile.NamedTemporaryFile(delete=False) as tmp_modified:
        shutil.copyfile(original_file, tmp_original.name)

        new_code = apply_change(original_file, change)
        with open(tmp_modified.name, "w") as f:
            f.write(new_code)

        if formatter:
            format_code(tmp_modified.name, formatter)

        # Print the path to the temporary modified file for approval
        print(f"Temporary modified file created at: {tmp_modified.name}")

        if test_cmd:
            backup_file = tempfile.NamedTemporaryFile(delete=False)
            shutil.copyfile(original_file, backup_file.name)

            try:
                shutil.copyfile(tmp_modified.name, original_file)

                subprocess.run(test_cmd, shell=True, check=False)
            finally:
                shutil.copyfile(backup_file.name, original_file)
                backup_file.close()

        show_diff(tmp_modified.name, original_file, diff_cmd)

        os.remove(tmp_original.name)


if __name__ == "__main__":
    main()

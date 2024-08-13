import os
import shutil
import subprocess
import tempfile

from prompt_llm_for_code_change import prompt_for_change_and_extract_code


def format_code(file, formatter):
    subprocess.run(formatter.split() + [file], check=True)


def show_diff(file1, file2, diff_cmd=None):
    if diff_cmd:
        # Replace placeholders in the diff command with the file paths
        diff_cmd = diff_cmd.replace("{file1}", file1).replace("{file2}", file2)
        subprocess.run(diff_cmd, shell=True)
    else:
        subprocess.run(["code", "--diff", file1, file2])


def save(to_file, content):
    with open(to_file, "w") as f:
        f.write(content)


def create_backup(file):
    backup_file = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfile(src=file, dst=backup_file.name)
    return backup_file


def execute_test(test_cmd):
    subprocess.run(test_cmd, shell=True, check=False)


def restore_from_backup(backup_file, original_file):
    shutil.copyfile(backup_file.name, original_file)
    backup_file.close()


def execute_code_change_workflow(
    target_file, code_change, test_cmd=None, format_cmd=None, diff_cmd=None
):
    """
    the workflow:
    1. get new code by prompting llm -> save to a temp file
    2. optional: format the new code using provided cmd
    3. optional: run test cmd
    3.1. backup the original file
    3.2. modify the original file with the new code
    3.3. run the test command
    3.4. restore the original file
    4. show the diff between the original and modified file
    5. clean up temp files
    """
    with tempfile.NamedTemporaryFile(
        delete=False
    ) as tmp_original, tempfile.NamedTemporaryFile(delete=False) as tmp_modified:
        shutil.copyfile(target_file, tmp_original.name)

        new_code = prompt_for_change_and_extract_code(
            file_to_change=tmp_original.name, change_to_make=code_change
        )

        save(tmp_modified.name, new_code)

        if format_cmd:
            format_code(tmp_modified.name, format_cmd)

        if test_cmd:
            backup_file = create_backup(target_file)

            try:
                # Modify the original file with the new code
                shutil.copyfile(tmp_modified.name, target_file)

                execute_test(test_cmd)
            finally:
                restore_from_backup(backup_file, target_file)

        show_diff(tmp_modified.name, target_file, diff_cmd)

        os.remove(tmp_original.name)

        return tmp_modified.name


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

    tmp_modified = execute_code_change_workflow(
        target_file=args.file,
        code_change=args.change,
        test_cmd=args.test,
        format_cmd=args.format,
        diff_cmd=args.diff,
    )

    print(f"Modified code saved to: {tmp_modified}")


if __name__ == "__main__":
    main()

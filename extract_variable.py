import argparse
import rope.base.project
import rope.base.libutils
import rope.refactor.extract
import rope.base.change
import shutil


def extract_variable(file_path: str, char_range_start: int, end: int, new_name: str):
    # Initialize the project
    project = rope.base.project.Project(".")

    # Read the content of the file
    with open(file_path, "r") as file:
        source_code = file.read()

    # Get the resource for the file
    resource = rope.base.libutils.path_to_resource(project, file_path)

    # Perform the extraction
    extractor = rope.refactor.extract.ExtractVariable(
        project, resource, char_range_start, end, variable=True
    )
    changes = extractor.get_changes(new_name)

    # do the changes
    project.do(changes)

    refactored_file_path = f"{file_path}.refactored"

    # copy to a new file
    shutil.copy(file_path, refactored_file_path)

    # rewrite the original file
    with open(file_path, "w") as file:
        file.write(source_code)

    project.close()
    print(f"Refactored code written to {refactored_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Extract a variable from a Python file."
    )
    parser.add_argument("-f", "--file", required=True, help="Path to the Python file")
    parser.add_argument(
        "-s",
        "--start",
        required=True,
        type=int,
        help="Start position of the character range",
    )
    parser.add_argument(
        "-e",
        "--end",
        required=True,
        type=int,
        help="End position of the character range",
    )
    parser.add_argument("-n", "--name", required=True, help="New variable name")

    args = parser.parse_args()

    extract_variable(args.file, args.start, args.end, args.name)


if __name__ == "__main__":
    main()

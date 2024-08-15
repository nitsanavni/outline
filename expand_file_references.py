import re
import sys
from pathlib import Path

from outline import Outline


def expand_file_references(change_request):
    # Improved regex pattern
    file_and_line_range_pattern = re.compile(
        r"@(\S+?)(?::(\d+)(?:-(\d+))?)?(?=\s|$)|(\S+#O)"
    )

    def file_and_line_range_replace_match(match):
        file_name = match.group(1)
        start_line = match.group(2)
        end_line = match.group(3)

        if "#O" in file_name:  # Check for outline references
            outline_filename = file_name[:-2]  # remove #O
            outline = Outline(root_nodes=[outline_filename])
            return outline.summary()

        # Check if the file exists
        file_path = Path(file_name)
        if not file_path.is_file():
            return match.group(0)  # If file doesn't exist, return the original pattern

        # Read the file content
        with file_path.open() as file:
            lines = file.readlines()

        # Handle line numbers
        if start_line:
            start_line = int(start_line) - 1  # Convert to 0-based index
            end_line = (int(end_line) - 1) if end_line else start_line
            file_content = lines[start_line : end_line + 1]  # Include end_line
        else:
            file_content = lines

        # Prepare the replacement text
        lines_header = f"(lines {start_line+1}-{end_line+1}) " if start_line else ""
        header = f"\n### File: `{file_name}` {lines_header}\n"
        content = "".join(
            f"{i+1}: {line}"
            for i, line in enumerate(file_content, start=start_line or 0)
        )

        return header + "```\n" + content + "```\n"

    # Replace all occurrences of the pattern
    expanded_change_request = file_and_line_range_pattern.sub(
        file_and_line_range_replace_match, change_request
    )

    return expanded_change_request


if __name__ == "__main__":
    # Read from standard input
    change_request = sys.stdin.read()
    # Expand file references in the change request
    expanded_request = expand_file_references(change_request)
    # Print the expanded change request
    print(expanded_request)

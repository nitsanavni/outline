import re

from main_decorator import main


def parse_markdown(md):
    file_header_pattern = re.compile(r"^### File: `(.+?)`")
    inside_code_block = False
    current_file_name = None
    current_code = []
    result = []

    for line in md.splitlines():
        header_match = file_header_pattern.match(line)

        if header_match:
            if inside_code_block and current_file_name:
                result.append((current_file_name, "\n".join(current_code)))
            current_file_name = header_match.group(1)
            current_code = []
            inside_code_block = False
            continue

        if "```" in line:
            if inside_code_block:
                result.append((current_file_name, "\n".join(current_code)))
                inside_code_block = False
            else:
                inside_code_block = True
            continue

        if inside_code_block:
            current_code.append(line)

    # If a code block ends the file without closing it properly
    if inside_code_block and current_file_name:
        result.append((current_file_name, "\n".join(current_code)))

    return result


@main
def printer(md):
    parsed_files = parse_markdown(md)

    return "\n".join(
        [
            f"### File: `{file_name}`\n```{source}\n```"
            for file_name, source in parsed_files
        ]
    )

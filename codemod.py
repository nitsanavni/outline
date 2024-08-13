import sys

from prompt_llm import prompt_llm


def extract_code_block(text):
    lines = text.splitlines()
    in_code_block = False
    code_lines = []

    for line in lines:
        if "```" in line:
            if in_code_block:
                break
            in_code_block = True
        elif in_code_block:
            code_lines.append(line)

    return "\n".join(code_lines)


def read_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def make_prompt(file_to_change, change_to_make):
    code = read_file(file_to_change)

    prompt = f"""
    I need you to modify the following code according to the instructions below. 
    Write the whole code again with the modifications.
    Instructions: {change_to_make}

    Code:
    ```
    {code}
    ```
    """

    return prompt


def prompt_for_change_and_extract_code(file_to_change, change_to_make):
    modified_code = extract_code_block(
        text=prompt_llm(prompt=make_prompt(file_to_change, change_to_make))
    )

    return modified_code


def main():
    if len(sys.argv) != 3:
        print("Usage: python codemod.py <file_to_change> <change_to_make>")
        sys.exit(1)

    file_to_change = sys.argv[1]
    change_to_make = sys.argv[2]

    modified_code = prompt_for_change_and_extract_code(file_to_change, change_to_make)

    print(modified_code)


if __name__ == "__main__":
    main()

from openai import OpenAI
import sys


def call_openai_api(prompt):
    client = OpenAI()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-4o-mini",
    )

    return chat_completion.choices[0].message.content


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


def main():
    if len(sys.argv) != 3:
        print("Usage: python codemod.py <file_to_change> <change_to_make>")
        sys.exit(1)

    file_to_change = sys.argv[1]
    change_to_make = sys.argv[2]

    with open(file_to_change, "r") as file:
        code = file.read()

    prompt = f"""
    I need you to modify the following code according to the instructions below. 
    Write the whole code again with the modifications.
    Instructions: {change_to_make}

    Code:
    ```
    {code}
    ```
    """

    response = call_openai_api(prompt)
    modified_code = extract_code_block(response)

    if modified_code:
        print(modified_code)
    else:
        print("Failed to extract modified code.")


if __name__ == "__main__":
    main()

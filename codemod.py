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
    code_block_start = text.find("```")
    code_block_end = text.rfind("```")

    if code_block_start != -1 and code_block_end != -1:
        return text[code_block_start + 3 : code_block_end].strip()
    else:
        return None


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

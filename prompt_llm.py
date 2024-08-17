from openai import OpenAI
from debug import debug
import sys


def prompt_llm(prompt):
    debug(f"Prompting LLM with:\n{prompt}")

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

    return debug(chat_completion.choices[0].message.content)


if __name__ == "__main__":
    print(prompt_llm(sys.stdin.read()))

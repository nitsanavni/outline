from openai import OpenAI
from debug import debug

from main_decorator import main


@main
def prompt_llm(prompt):
    debug(f"Prompting LLM with:\n{prompt}")

    return debug(
        OpenAI()
        .chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="gpt-4o-mini",
        )
        .choices[0]
        .message.content
    )

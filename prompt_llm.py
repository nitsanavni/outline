from openai import OpenAI
from debug import debug

from verify_decorator import verify_with
from main_decorator import main


@verify_with("Hello! whats the day?")
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

from openai import OpenAI


def prompt_llm(prompt):
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

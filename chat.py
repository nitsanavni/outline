import argparse
import requests
import json
import os


def chat_with_gpt4(api_key, text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception(
            "Couldn't find the 'OPENAI_API_KEY' environment variable!")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}',
    }
    data = {
        "model": "gpt-4",
        "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": text}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        raise Exception(
            f'Request to GPT-4 API failed with status {response.status_code}. The response is: {response.text}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "text", help="The text to be used as prompt for GPT-4.")
    args = parser.parse_args()

    # Please replace 'your-api-key' with your actual OpenAI GPT-4 API Key
    api_key = 'your-api-key'
    print(chat_with_gpt4(api_key, args.text))


if __name__ == "__main__":
    main()

#!/usr/bin/env python
import argparse
import requests
import os
import json

CACHE_FILE = "chat_cache.json"


def read_cache():
    try:
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def write_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def chat_with_gpt4(text, use_cache=True):
    if use_cache:
        cache = read_cache()
        if text in cache:
            return cache[text]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("Couldn't find the 'OPENAI_API_KEY' environment variable!")
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Short answers.",
            },
            {"role": "user", "content": text},
        ],
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()["choices"][0]["message"]["content"].strip()
        if use_cache:
            cache[text] = result
            write_cache(cache)
        return result
    else:
        raise Exception(
            f"Request to GPT-4 API failed with status {response.status_code}. The response is: {response.text}"
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="The text to be used as prompt for GPT-4.")
    parser.add_argument(
        "--cache",
        dest="use_cache",
        action="store_true",
        help="Enable caching (default).",
    )
    parser.add_argument(
        "--no-cache", dest="use_cache", action="store_false", help="Disable caching."
    )
    parser.set_defaults(use_cache=True)
    args = parser.parse_args()

    print(chat_with_gpt4(args.text, use_cache=args.use_cache))


if __name__ == "__main__":
    main()

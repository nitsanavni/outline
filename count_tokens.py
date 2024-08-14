#!/usr/bin/env python3

import sys
import tiktoken


def main():
    # Read text from stdin
    input_text = sys.stdin.read().strip()

    # Select the tokenizer for the model you're using
    encoding = tiktoken.get_encoding(
        "cl100k_base"
    )  # cl100k_base is used for GPT-4 and GPT-3.5-turbo models

    # Encode the text to get the token count
    tokens = encoding.encode(input_text)

    # Print the number of tokens
    print(f"Number of tokens: {len(tokens)}")


if __name__ == "__main__":
    main()

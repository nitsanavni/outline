import sys
import os
import argparse

from fancy_prompt import fancy_prompt
from expand_file_references import expand_file_references
from multi_file_diffs import multi_file_diffs
from parse_multiple_files_in_markdown import parse_markdown
from prompt_llm_multi_file_response import prompt_llm_multi_file_response
from vimdiff import vimdiff

def main():
    parser = argparse.ArgumentParser(description="Change in files utility", add_help=False)
    # Set the default history file to be in the same directory as this script
    default_history_file = os.path.join(os.path.dirname(__file__), ".change_in_files_history")
    parser.add_argument('-h', '--history', type=str, default=default_history_file
                        )

    args = parser.parse_args()

    change_request = fancy_prompt("", history_file=args.history)
    print("on it...")
    expanded = expand_file_references(change_request)
    response = prompt_llm_multi_file_response(request=expanded)
    files = parse_markdown(response)
    multi_file_diffs(files, diff=vimdiff)

if __name__ == "__main__":
    main()

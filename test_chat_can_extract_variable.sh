#!/bin/bash

function test {
    ./verify.sh -t "chat_extract_variable.$1" || true
}

cat -n example.py | test cat_with_line_numbers

prompt="locate the char range of the hello world string in full, including the surrounding quotes

format:
starts_on_line:
ends_on_line:
starts_with_str:
ends_with_str:

note:
- start and end lines are inclusive, and could be the same
- strs should full words if possible, at least 4 chars long
- don't quote the strings
- no trailing spaces

$(cat -n example.py)"

./chat.py "$prompt" | test hello_world_range

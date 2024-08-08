#!/bin/bash

function test {
    ./verify.sh -t "chat_extract_variable.$1" || true
}

cat -n example.py | test cat_with_line_numbers

export thing_to_locate="the hello world string"
export code=$(cat -n example.py)

prompt=$(envsubst <locate_range_prompt_template)

./chat.py "$prompt" | test hello_world_range

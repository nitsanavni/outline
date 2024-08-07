#!/bin/bash

default_diff_tool="code --diff"
diff_tool=$default_diff_tool

while getopts ":r:t:d:" opt; do
    case $opt in
    d) diff_tool=$OPTARG ;;
    r) received_text=$OPTARG ;;
    t) test_name=$OPTARG ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
    esac
done

received="${test_name}.received"
approved="${test_name}.approved"

if [ -z "$received_text" ]; then
    cat - >"$received"
else
    echo "$received_text" >"$received"
fi

touch "$approved"

if diff -q "$received" "$approved" >/dev/null; then
    echo "✅ test passed" >&2
    rm "$received"
else
    echo "❌ test failed" >&2
    $diff_tool "$received" "$approved" </dev/tty
    false
fi

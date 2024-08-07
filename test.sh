#!/bin/bash

function outline {
    python outline.py "$@"
}

function test {
    ./verify.sh -t "$1" || true
}

function scrub {
    local patterns=("$@")
    local cmd="cat"
    for pattern in "${patterns[@]}"; do
        cmd="$cmd | grep -v '$pattern'"
    done
    eval "$cmd"
}

outline | scrub no_args regex_scores cache | test no_args
outline -r outline.py -l 19 | test self
outline -r *.py -l 14 | test py

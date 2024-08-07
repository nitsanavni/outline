#!/bin/bash

function outline {
    python outline.py "$@"
}

function test {
    ./verify.sh -t "$1" || true
}

function scrub {
    grep -v "$1"
}

outline | scrub no_args | scrub regex_scores | test no_args
# TODO: support multiple scrubbed patterns: outline | scrub no_args regex_scores | test no_args
outline -r outline.py -l 19 | test self
outline -r *.py -l 14 | test py

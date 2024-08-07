#!/bin/bash

function scrub {
    grep -v "$1"
}

function test {
    ./verify.sh -t "$1" || true
}

function outline {
    python outline.py "$@"
}

outline | scrub no_args | scrub regex_scores | test no_args
outline -r outline.py -l 19 | test self
outline -r *.py -l 14 | test py

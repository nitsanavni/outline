#!/bin/bash

function scrub {
    grep -v "$1"
}

function test {
    ./verify.sh -d ./idiff.sh -t "$1"
}

function outline {
    python outline.py "$@"
}

outline | scrub no_args | scrub regex_scores | test no_args

#!/bin/bash

function test {
    ./verify.sh -t "chat.$1" || true
}

./chat.py hello | test hello
./chat.py "three musical instruments

one of them yellow" | test musical_instruments

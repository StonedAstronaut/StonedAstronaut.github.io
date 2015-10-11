#!/bin/bash

CONTENT="content"
OUTPUT="output"

pelican "${CONTENT}" -o "${OUTPUT}" -s publishconf.py

sleep 1

ghp-import -p -b master -r origin "${OUTPUT}"

sleep 1

git add ./ && git commit -m "init" && git push origin markup

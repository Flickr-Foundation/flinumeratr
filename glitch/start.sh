#!/usr/bin/env bash
# This is the script that runs when the app starts in Glitch, which
# installs basic dependencies and then runs the app with gunicorn.

set -o errexit
set -o nounset

pip3 install --upgrade pip
pip3 install -r requirements.txt

gunicorn redirectr:app -w 4 --log-file -

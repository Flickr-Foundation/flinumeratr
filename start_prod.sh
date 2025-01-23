#!/usr/bin/env bash

set -o errexit
set -o nounset

source .venv/bin/activate

# Get secrets from the keychain.
#
# If this fails and you're logging in to the web server over SSH,
# you may need to unlock the keychain first:
#
#     $ security unlock-keychain ~/Library/Keychains/login.keychain
#
export FLICKR_API_KEY=$(keyring get flickr_api key)

# This config setting tells the Flask app to serve all of
# its routes with this prefix.
export SCRIPT_NAME=/tools/flinumeratr

# Actually start the web app.
gunicorn flinumeratr.app:app \
  --workers 4 \
  --bind 127.0.0.1:8001 \
  --access-logfile access.log \
  --log-file app.log \
  --pid flinumeratr.pid \
  --daemon

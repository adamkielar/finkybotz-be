#!/usr/bin/env bash
set -e

# This script loads environment variables from a file.
# Example: $ . load_env.sh .env

test -f "$1" || { echo "No file: $1"; return; }
echo "Loading... $1"

# remove comments, remove empty lines, add quotes, add export
eval "$(sed -e 's/\([^#]*\)#.*/\1/' -e '/^[[:space:]]*$/d' -e "s/\([^=]*\)=\(.*\)/\1=\"\2\"/" -e 's/\(.*\)/export \1/' $1)"

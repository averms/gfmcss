#!/bin/sh
# Preview github-flavored markdown
set -e

if [ $# -eq 0 ]; then
    echo >&2 "No file name given."
    exit 1
fi
if [ ! -f "$1" ]; then
    echo >&2 "Not a file."
    exit 1
fi

html_file="$(mktemp -u).html"

markdown="$1"

body="$(curl -s https://api.github.com/markdown/raw -X "POST" \
    -H "Content-Type: text/plain" -H "Accept: application/vnd.github.v3+json" \
    --data-binary @"$markdown")"

printf '<!DOCTYPE html>
<html><head><title>Markdown Preview</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet"
href="https://cdn.jsdelivr.net/gh/a-vrma/gfmcss@0.1.1/gfm.min.css">
</head><body><article class="markdown-body">
  %s
</article></body></html>
' "$body" >"$html_file"

echo "$html_file"
if command -v open; then
    open "$html_file"
else
    xdg-open "$html_file"
fi

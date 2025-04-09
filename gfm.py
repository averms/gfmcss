#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx",
# ]
# ///

import sys
import webbrowser
from pathlib import Path
from tempfile import NamedTemporaryFile

import httpx

TEMPL = """
<!doctype html>
<html>
<head>
<title>GitHub Markdown Preview</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/averms/gfmcss@0.1.1/gfm.min.css">
</head>
<article class="markdown-body">
{}
</article>
</body>
</html>
"""

markdown = Path(sys.argv[1]).read_text()

r = httpx.post(
    "https://api.github.com/markdown",
    headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    },
    json={"text": markdown, "mode": "gfm"},
    follow_redirects=True,
)

with NamedTemporaryFile("w", suffix=".html", delete=False) as f:
    f.write(TEMPL.format(r.text))
    print(f.name)
    webbrowser.open("file://" + f.name)

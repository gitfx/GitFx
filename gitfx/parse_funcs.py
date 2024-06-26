#!/usr/bin/env python3
# coding=utf-8
# https://github.com/gifx/GitFx

"""Parse function code to get function info."""

import os
import sys
import re
import json
from glob import glob


EXT_LANG = {'.py': 'python',
            '.rb': 'ruby',
            '.pl': 'perl',
            '.go': 'golang',
            '.js': 'node',
            '.hs': 'haskell',
            '.exs': 'elixir',
            '.php': 'php',
            '.sh': 'bash',
            '.ts': 'deno',
            '.rs': 'rust'}

COMMENT_PREFIX = {'python': '#',
                  'ruby': '#',
                  'perl': '#',
                  'golang': '//',
                  'node': '//',
                  'haskell': '--',
                  'elixir': '#',
                  'php': '//',
                  'bash': '#',
                  'deno': '//',
                  'rust': '//'}


def get_language(extension):
    return EXT_LANG[extension]


def get_routes(lines, lang):
    routes = []
    prefix = COMMENT_PREFIX[lang]

    if not prefix:
        return routes

    for l in lines:
        pattern = rf'^\s*{re.escape(prefix)}\s*(GET|POST|PUT|DELETE)\s+?(\S+?)\s*?$'
        matched = re.search(pattern, l)
        if matched and matched.lastindex >= 2:
            routes.append({'action': matched.group(1), 'route': matched.group(2).lstrip('/')})
    return routes


def parse(path):
    if not path:
        print("no path provided")
        return

    result = []
    types = ('*.rb',    # Ruby
             '*.py',    # Python
             '*.go',    # Golang
             '*.js',    # Node.js
             '*.pl',    # Perl
             '*.hs',    # Haskell
             '*.exs',   # Elixir
             '*.php',   # PHP
             '*sh',     # Bash
             '*.ts',    # Deno
             '*.rs')    # Rust

    files = [f for fs in [glob(os.path.join(path, t)) for t in types] for f in fs]

    for f in files:
        file_name = os.path.basename(f)
        ext_name = os.path.splitext(file_name)[1]
        lang = get_language(ext_name)

        with open(f, 'r') as _f:
            lines = _f.read().splitlines()
            routes = get_routes(lines, lang)
            if not routes:
                continue
            result.append({'routes': routes, 'file_name': file_name, 'language': lang})

    return result


if __name__ == "__main__":
    funcs = parse(sys.argv[1])
    print(json.dumps(funcs))

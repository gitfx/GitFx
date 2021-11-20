#!/usr/bin/env python3
# coding=utf-8
# https://github.com/gitx-io/GitFx

"""Detect and get language version if exists."""

import os
import sys


LANG_VERSION_FILES = {'python': '.python-version',   # pyenv
                      'ruby': '.ruby-version',       # rvm/rbenv
                      'perl': '.perl-version',       # plenv
                      'node': '.nvmrc',              # nvm
                      'php': '.phpenv-version'}      # phpenv


def read_first_line(ver_file):
    if not os.path.exists(ver_file):
        return ''

    with open(ver_file, 'r') as fh:
        line = fh.read().splitlines()[0]
        if line:
            line = line.strip()
        return line


def get_version(func_path, lang):
    if lang not in LANG_VERSION_FILES:
        return ''
    ver_file = os.path.join(func_path, LANG_VERSION_FILES[lang])
    version = read_first_line(ver_file)
    return version


if __name__ == "__main__":
    version = get_version(sys.argv[1], sys.argv[2])
    print(version)

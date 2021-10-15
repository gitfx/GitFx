#!/usr/bin/env python3
# coding=utf-8
# https://github.com/gitx-io/GitFx

"""The main program to run functions."""

import os
import subprocess

from gitfx import parse_funcs
from gitfx import lang_version


ROOT_DIR = os.getenv('GITHUB_WORKSPACE', os.getcwd())

SUPPORTED_LANGS = ['ruby',
                   'python',
                   'perl',
                   'node',
                   'golang',
                   'elixir',
                   'haskell',
                   'php',
                   'bash',
                   'rust']

RUN_CMDS = {'ruby': 'ruby',
            'python': 'python',
            'node': 'node',
            'perl': 'perl',
            'golang': 'go run',
            'elixir': 'elixir',
            'haskell': 'runhaskell',
            'rust': 'perl -e \'($n = $ARGV[0]) =~ s/\.rs$//; system "rustc $ARGV[0] && ./$n && rm $n"\'', # noqa
            'php': 'php'}

LANG_DEP_FILE = {'ruby': 'Gemfile',
                 'python': 'requirements.txt',
                 'node': 'package.json',
                 'perl': 'cpanfile',
                 'php': 'composer.json'}

LANG_DEP_CMD = {'ruby': 'bundle install >/dev/null 2>&1',
                'python': 'pip install -r requirements.txt >/dev/null 2>&1',
                'node': 'npm install --only=prod >/dev/null 2>&1',
                'perl': 'cpanm --installdeps . >/dev/null 2>&1',
                'php': 'curl -sS https://getcomposer.org/installer -o composer-setup.php && \
                        php composer-setup.php --install-dir=/usr/local/bin --filename=composer >/dev/null 2>&1 && \
                        php composer.phar install >/dev/null 2>&1'}

DOCKER_IMAGES = {}


def docker_image(lang):
    """you can specify a docker image name for a language,
    otherwise the language name will be returned as the image name"""
    return DOCKER_IMAGES.get(lang, lang)


def deps_install_cmd(lang, func_path):
    if lang not in LANG_DEP_FILE.keys():
        return ':'

    if os.path.isfile(os.path.join(func_path, LANG_DEP_FILE[lang])):
        return LANG_DEP_CMD[lang]
    else:
        return ':'


def run_fun(func_path, func):
    func_lang = func['language']
    if func_lang not in SUPPORTED_LANGS:
        return ""
    func_file_name = func['file_name']
    if func_file_name.strip() == '':
        return ""

    # before_script is a shell script that start with a same name of
    # the function file but ends with '.sh',
    # will be run before the function running
    before_script_file = func_file_name + '.sh'
    if os.path.isfile(os.path.join(func_path, before_script_file)):
        run_before_script = './{} >/dev/null 2>&1'.format(before_script_file)
    else:
        run_before_script = ':'

    # decide language version
    version = lang_version.get_version(func_lang) or 'latest'

    if func_lang == 'bash':
        cmd = ["bash", os.path.join(func_path, func_file_name)]
    else:
        cmd = ['docker', 'run', '--rm', '--workdir', '/github/workspace',
               '-v', ROOT_DIR + ':/github/workspace',
               docker_image(func_lang) + ':' + version, 'sh', '-c',
               "cd " + os.path.relpath(func_path, ROOT_DIR) + " && " +        # noqa
               deps_install_cmd(func_lang, func_path) + " && " +                    # noqa
               run_before_script + " && " +                                   # noqa
               RUN_CMDS[func_lang] + " " + func_file_name]

    output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
    return output.decode("utf8")


def write_to_route(result, func_route):
    if func_route.strip() == '':
        return

    dst_dir = os.path.join(ROOT_DIR, os.path.dirname(func_route))
    if dst_dir and not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    file_path = os.path.join(ROOT_DIR, func_route)
    f = open(file_path, 'w')
    f.write(result)
    f.close()

    print_github_raw_url(func_route)


def print_github_raw_url(file_path):
    repo_name = os.getenv('GITHUB_REPOSITORY')
    branch = os.getenv('GITHUB_REF')
    if not repo_name or not branch:
        return
    branch = branch.split('/')[-1]
    base_url = 'https://raw.githubusercontent.com/{}/{}'.format(repo_name, branch)
    raw_url = os.path.join(base_url, file_path)
    if raw_url:
        print(raw_url)


def run(*func_paths):
    if not func_paths:
        func_path = ROOT_DIR
        do_run(func_path)
    else:
        for func_path in func_paths:
            do_run(func_path)


def do_run(func_path):
    func_path = os.path.abspath(func_path)
    if not os.path.isdir(func_path):
        return

    funcs = parse_funcs.parse(func_path)

    for func in funcs:
        routes = func['routes']
        if not routes:
            continue
        if len(routes) == 1:
            if routes[0]['action'] != 'GET':
                continue
            result = run_fun(func_path, func)
            if result.strip() == '':
                continue
            print(result)
            write_to_route(result, routes[0]['route'])
        else:
            results = run_fun(func_path, func)
            if results.strip() == '':
                continue
            print(results)
            output_list = str.splitlines(results)
            for i in range(len(routes)):
                if 'route' in routes[i] and routes[i]['action'] == 'GET':
                    write_to_route(output_list[i], routes[i]['route'])

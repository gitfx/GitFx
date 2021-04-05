import os
import subprocess

from gitfx import parse_funcs
from gitfx import lang_version


ROOT_DIR = os.getenv('GITHUB_WORKSPACE', os.getcwd())

SUPPORTED_LANGS = [
        'ruby',
        'python',
        'perl',
        'node',
        'golang',
        'elixir',
        'haskell',
        'php',
        'bash',
        'rust',
        ]

RUN_CMDS = {
        'ruby': 'ruby',
        'python': 'python',
        'node': 'node',
        'perl': 'perl',
        'golang': 'go run',
        'elixir': 'elixir',
        'haskell': 'runhaskell',
        'php': 'php',
        'rust': 'perl -e \'($n = $ARGV[0]) =~ s/\.rs$//; system "rustc $ARGV[0] && ./$n && rm $n"\'',
        }

DOCKER_IMAGES = {
        'php': 'composer',
        }


def docker_image(lang):
    """you can specify a docker image name for a language,
    otherwise the language name will be returned as the image name"""
    return DOCKER_IMAGES.get(lang, lang)

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
    run_before_script = '[ -f {0} ] && sh {0} >/dev/null 2>&1'.format(before_script_file)

    deps_install = {
        'ruby': '[ -f Gemfile ] && bundle install >/dev/null 2>&1',
        'python': '[ -f requirements.txt ] && pip install -r requirements.txt >/dev/null 2>&1',
        'node': '[ -f package.json ] && npm install --only=prod >/dev/null 2>&1',
        'perl': '[ -f cpanfile ] && cpanm --installdeps . >/dev/null 2>&1'}

    # decide language version
    version = lang_version.get_version(func_lang) or 'latest'

    if func_lang == 'bash':
        cmd = ["bash", os.path.join(func_path, func_file_name)]
    else:
        cmd = ['docker', 'run', '--rm', '--workdir', '/github/workspace',
               '-v', ROOT_DIR + ':/github/workspace',
               docker_image(func_lang) + ':' + version, 'sh', '-c',
               "cd " + os.path.relpath(func_path, ROOT_DIR) + ";" +
               deps_install.get(func_lang, ':') + ";" +
               run_before_script + ";" +
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


def run(func_path):
    if not func_path:
        func_path = ROOT_DIR
    func_path = os.path.abspath(func_path)

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

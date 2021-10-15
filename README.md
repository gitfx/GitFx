# GitFx - Create a Serverless service in Git hosting

[![GitFx Testing](https://github.com/gitx-io/GitFx/workflows/Test%20run%20funcs/badge.svg)](https://github.com/gitx-io/GitFx/blob/master/.github/workflows/test_run_funcs.yml)
[![GitFx Lint](https://github.com/gitx-io/GitFx/workflows/Lint/badge.svg)](https://github.com/gitx-io/GitFx/blob/master/.github/workflows/linter.yml)

GitFx can be used to run some functions and serve the output as a service in a Git hosting.

GitFx is a Python lib extracted from an action [ActionServerless](https://github.com/gitx-io/ActionServerless). And now the action uses this lib as a dependency to do the real job, you can run the lib locally in a same way as in the action.

## Prerequisites

* Python 3.5+
* Docker

## Install

```shell
pip3 install gitfx

# or
python3 -m pip install gitfx
```

Note: Python 2 is not supported

## Usage

Let's start with a Python code that'll be used to create a Serverless service:

```python
# function.py
import json

# GET /api/py_hello.json

print(json.dumps({"hello": "world"}))
```

put the program to a path under current directory, for example, `test` folder and run:

```shell
python3 -m gitfx test/
# you can pass more folders if you have
```

then the program's output is written to a file located in `api/py_hello.json` that you defined as a route in the comment.

You can use the [ActionServerless](https://github.com/gitx-io/ActionServerless) to run functions in GitHub, and also you can run locally as above example then push the generated files to the remote.

more languages' examples you can find [here](https://github.com/gitx-io/GitFx/tree/master/test/func_examples).


## Languages supported

| Language      | Dependency Installation | Version Management    | Example code                                                                        |
| ------------- | -------------           | --------------------  | :------------:                                                                      |
| Python        | ✅ `requirements.txt`   | ✅ `.python-version` [pyenv](https://github.com/pyenv/pyenv) | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.py)  |
| Ruby          | ✅ `Gemfile`            | ✅ `.ruby-version` [rvm](https://rvm.io/)/[rbenv](https://github.com/rbenv/rbenv) | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.rb)  |
| Node.js       | ✅ `package.json`       | ✅ `.nvmrc` [nvm](https://github.com/nvm-sh/nvm) | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.js)  |
| Perl          | ✅ `cpanfile`           | ✅ `.perl-version` [plenv](https://github.com/tokuhirom/plenv) | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.pl)  |
| PHP           | ✅ `composer.json`      | ✅ `.phpenv-version` [phpenv](https://github.com/phpenv/phpenv) | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.php) |
| Golang        | ⬜️                      | ⬜️                   | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.go)  |
| Haskell       | ⬜️                      | ⬜️                   | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.hs)  |
| Elixir        | ⬜️                      | ⬜️                   | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.exs) |
| Bash          | --                      | --                   | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.sh)  |
| Rust          | ⬜️                      | ⬜️                   | [See](https://github.com/gitx-io/GitFx/blob/master/test/func_examples/function.rs)  |

* ✅  Feature supported
* ⬜  Feature not supported yet
* --  N/A

## Documents

* [before_script](https://github.com/gitx-io/GitFx/wiki/before_script)
* [HTTP Headers](https://github.com/gitx-io/GitFx/wiki/HTTP-Headers)

## Real world examples

* [Shell functions to get Docker image versions](https://github.com/gitx-io?q=docker-major-versions&type=public&language=shell&sort=name)
* [Run examples for 30-Days-Of-Python tutorial](https://github.com/gitx-io/30-Days-Of-Python)

## Contributions

Contributions are welcome! You may check the following features in case you'd like to contribute but no idea what to do:

* Support to add your favorite languages
* Support dependency installation to the existing languages
* Use this action to create an application and share it


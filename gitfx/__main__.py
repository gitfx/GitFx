import os
import sys
from gitfx import run_funcs


if __name__ == "__main__":
    # func_path is a path where the functions locate
    if len(sys.argv) > 1:
        run_funcs.run(*sys.argv[1:], './.gitfx')
    else:
        func_path = os.getcwd()
        run_funcs.run(func_path, './.gitfx')

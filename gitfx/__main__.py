import os
import sys
from gitfx import run_funcs


if __name__ == "__main__":
    # func_path is a path where the functions locate
    func_path = os.getcwd()
    if len(sys.argv) > 1:
        func_path = sys.argv[1]

    run_funcs.run(func_path)

#!/usr/bin/env python3

import os

def get_venv():
    venv_path = os.environ.get('VIRTUAL_ENV')
    if venv_path:
        return venv_path
    else:
        return "No virtual environment"

if __name__ == '__main__':
    print(f"Your current virtual environment is {get_venv()}")
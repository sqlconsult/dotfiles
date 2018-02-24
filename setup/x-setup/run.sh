#!/usr/bin/env bash

# use python3 to run shell.py
python3 shell.py

# clean up after running by removing bytecode that was
# created by the python interpreter
rm -rf wrappers/__pycache__
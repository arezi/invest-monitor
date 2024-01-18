#!/usr/bin/env sh

. .venv/bin/activate 

cd tests

export PYTHONPATH=../

python3 -m unittest


#!/usr/bin/env bash
pip install -r requirements-dev.txt
export PYTHONPATH=$(pwd)/ouroboros
$(which python3) -m pytest -v
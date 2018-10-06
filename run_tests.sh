#!/usr/bin/env bash
pip install -r requirements-dev.txt
$(which python3) -m pytest -v
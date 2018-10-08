#!/usr/bin/env bash
module_list=$(pip list | awk '{print $1'})
export PIP_FORMAT=columns

# Install modules that arent present, save time instead of reinstalling everytime
for i in $(cat requirements-dev.txt);
  do
    if ! grep -x $i <<< "$module_list" 1>/dev/null; then
        pip install $i
    fi
  done

export PYTHONPATH=$(pwd)/ouroboros
$(which python3) -m pytest -v --cov-report term-missing --cov=$PYTHONPATH
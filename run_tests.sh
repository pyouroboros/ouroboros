#!/usr/bin/env bash
# Usage:
# ./run_tests.sh # Runs all
# ./run_tests.sh unit # Runs unit tests
# ./run_test.sh integration # Runs integration tests

module_list=$(pip list --format=columns | awk '{print $1'})

# Install modules that arent present, save time instead of reinstalling everytime
for i in $(cat requirements-dev.txt);
  do
    if ! grep -x $i <<< "$module_list" 1>/dev/null; then
        pip install $i
    fi
  done

export PYTHONPATH=$(pwd)/ouroboros

$(which python3) -m pytest tests/$1 -v --cov-report term-missing --cov=$PYTHONPATH -s
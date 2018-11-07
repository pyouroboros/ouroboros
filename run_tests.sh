#!/usr/bin/env bash
# Usage:
# ./run_tests.sh # Runs all
# ./run_tests.sh unit # Runs unit tests
# ./run_test.sh integration # Runs integration tests

cd "$( dirname "$0" )"

# output only lines unique to "file" 1 - the requirements file
function list_missing_modules {
  comm -2 -3 \
  <( sort ./requirements-dev.txt ) \
  <( pip list --format=columns | awk '$0=$1' | sort )
}

# create associative array of missing modules
declare -A missing_modules
while read module
do
  missing_modules[$module]=1
done < <( list_missing_modules )

vendor=""
which lsb_release >/dev/null 2>&1 && vendor=$( lsb_release -is )
sudo=""
[[ "$( id -u )" != 0 ]] && sudo="sudo"

# try to install packages using vendor package manager
shopt -qs nocasematch extglob
case "$vendor" in
  @(?(open)suse) )
    for m in "${!missing_modules[@]}"
    do
      $sudo zypper install -y "python3-$m" && unset missing_modules["$m"]
    done
    ;;
  ubuntu )
    for m in "${!missing_modules[@]}"
    do
      $sudo apt install -y "python3-$m" && unset missing_modules["$m"]
    done
    ;;
esac
shopt -qu nocasematch extglob

# Generate a requirement "file" containing only remaining missing modules
# If everything is installed, file will be empty and pip exits quietly
pip install --requirement <( for m in  "${!missing_modules[@]}"; do echo "$m"; done )

export PYTHONPATH="$(pwd)/ouroboros"

python3 -m pytest "tests/$1" -v --cov-report term-missing --cov="$PYTHONPATH"

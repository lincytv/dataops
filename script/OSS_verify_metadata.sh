#!/bin/bash

# __     __                _    __             __  __          _                 _           _
# \ \   / /   ___   _ __  (_)  / _|  _   _    |  \/  |   ___  | |_    __ _    __| |   __ _  | |_    __ _
#  \ \ / /   / _ \ | '__| | | | |_  | | | |   | |\/| |  / _ \ | __|  / _` |  / _` |  / _` | | __|  / _` |
#   \ V /   |  __/ | |    | | |  _| | |_| |   | |  | | |  __/ | |_  | (_| | | (_| | | (_| | | |_  | (_| |
#    \_/     \___| |_|    |_| |_|    \__, |   |_|  |_|  \___|  \__|  \__,_|  \__,_|  \__,_|  \__|  \__,_|
#                                    |___/

# ---------------------------------------------------------------------------
# Usecase
# -------
# Verify runbooks that are changed have valid metadata

# Usage
# -----
# bash script/OSS_verify_metadata.sh

# ---------------------------------------------------------------------------

function echo_green() {
    echo -e "\e[32m$1\e[0m"
}

function echo_red() {
    echo -e "\e[91m$1\e[0m"
}

function print_array() {
    echo "New or Modified Runbooks:"
    for filename in $@; do
        echo -e "\t$filename"
    done
}

# Allow for this script to be called from anywhere
FULL_PATH=$(readlink -f $0)
PARENT_DIR=$(dirname $FULL_PATH)

# array to keep track of changed runbooks
runbooks=()

# Directory all runbook links contain
RB_DIR="docs/runbooks"

CHANGED_FILES="$(git diff --name-only --diff-filter=ACMR $TRAVIS_COMMIT_RANGE)"

# Strip all changed runbooks out of changed files
for filename in ${CHANGED_FILES}; do
    if [[ $filename == *"${RB_DIR}"* ]]; then
      temp_file="${filename/$RB_DIR/}"
      # Append to runbooks array
      runbooks+=("\""$temp_file"\" ")
    fi
done

runbook_str=$(IFS= ; echo "${runbooks[*]}")

# If there are changed runbooks in this PR check if they have missing metadata
if [[ -n "$runbooks" ]]; then
    # Print changed runbooks
    print_array ${runbooks[*]}
    # Check if the runbooks that are changed have missing metadata git
    python $PARENT_DIR/OSScheckkeys.py -l $runbook_str
    # If previous command has an error
    if [[ $? -ne 0 ]]; then
        echo_red "There are errors in the runbooks metadata :("
        exit 1
    else
        echo_green "Runbooks have valid metadata :)"
    fi

# If there are no runbooks in this pull request
else
    echo_green "No runbooks have changed"
fi

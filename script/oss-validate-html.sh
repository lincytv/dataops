#!/bin/bash

# ---------------------------------------------------------------------------
# Usecase
# -------
# Verify runbooks that are changed in the pull request have valid generated html

# Usage
# -----
# bash script/oss-validate-html.sh

# ---------------------------------------------------------------------------
#set -xe  'remove the #, to activate debugging capabilities
function echo_green() {
    echo -e "\e[32m$1\e[0m"
}

function echo_red() {
    echo -e "\e[91m$1\e[0m"
}

function print_array() {
    echo "Changed Runbooks:"
    for filename in $@; do
        echo -e "\t$filename"
    done
}

FILE=$(readlink -f "$0")
CWD=$(dirname $FILE)
PARENT_DIR=$(dirname $CWD)
SITE_DIR="$PARENT_DIR/_site"

# First check all the site json files are valid
echo "Validating JSON files"
JSON_FILES=($(find $SITE_DIR/assets/json -iname '*.json'))
for file in ${JSON_FILES[@]}; do
  echo "Running jsonlint on file: $file";
  jsonlint $file;
  if [ $? -eq 1 ]; then
    echo "Invalid JSON on file: $file"
    exit 1
  fi
done
echo "JSON is valid"

# array to keep track of changed runbooks
runbooks=()

# Directory containing the runbooks to validate
RB_DIR="docs/runbooks"

echo "TRAVIS_BRANCH="${TRAVIS_BRANCH}
echo "TRAVIS_COMMIT="${TRAVIS_COMMIT}

CHANGED_FILES="$(git diff --name-only --diff-filter=ACMR $TRAVIS_COMMIT_RANGE)"
echo "${CHANGED_FILES}"

repo_slug=$(echo "$TRAVIS_REPO_SLUG" | sed 's/\//\\\//g')

# Strip all changed runbooks out of changed files
for filename in ${CHANGED_FILES}; do
    if [[ $filename == *"${RB_DIR}"* ]]; then
        # Replace `.md` with `.html` since runbook links are converted to hyperlinks
        html_file="${filename/.md/.html}"
        temp_file="${html_file/$RB_DIR/}"
        # Append to runbooks array
        runbooks+=("$temp_file")
    fi
done

# If there are changed runbooks in this PR check if they have valid html using html-proofer
if [[ -n "$runbooks" ]]; then
    # Print changed runbooks
    print_array ${runbooks[*]}
    echo "Validating HTML"
    errors=0
    for html in ${runbooks[*]}; do

        #escape the forward slashes in runbook path for use in regex
        runbook_html=$(echo "$html" | sed 's/\//\\\//g')

        #ignore all files except the runbook currently being validated
        ignore_str="/.+\/test.+/,/.+\/dashboard.+/,/.+\/assets.+/,/\/docs(?!.*"${runbook_html}")(.*)/"

        #validate
        htmlproofer --disable-external --empty-alt-ignore --allow-hash-href --file-ignore $ignore_str --url-swap \/${repo_slug}: $SITE_DIR

        # If previous command has an error
        if [[ $? -ne 0 ]]; then
            errors=1
        fi
    done

    # If any runbooks have failed validation
    if [[ errors -ne 0 ]]; then
        echo_red "There are errors in the runbooks generated HTML :("
        exit $errors
    else
        echo_green "Runbooks generate valid HTML :)"
    fi

# If there are no runbooks in this pull request
else
    echo_green "No runbooks have changed"
fi
#set +x 'remove the #, to activate debugging capabilities

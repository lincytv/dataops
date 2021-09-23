#!/bin/bash -e

# based on:
# https://github.com/cdown/travis-automerge/blob/master/travis-automerge
# https://github.com/brollb/automerge-ci
# https://github.ibm.com/bluemix-mobile-services/bmd-devops-pipeline/blob/v1/scripts/register-starter.sh


# Merge push from pull request branch to master branch
if [ ! -n $1 ] ; then
    echo "Usage: automerge.sh <token>"
    exit 1;
fi

export GIT_TOKEN="$1"

if  [[ "${TRAVIS_EVENT_TYPE}" == "pull_request" ]] && [[ "${TRAVIS_BRANCH}" == "master" ]]; then
    # We have to do some workarounds to figure out what the source branch is for this pull request.
    # Travis is not setting env vars when it's a PR.
    # See:  https://github.ibm.com/Whitewater/TravisCI/issues/413
    echo "Running pull request build on Travis"
    echo "TRAVIS_COMMIT_RANGE=${TRAVIS_COMMIT_RANGE}"
    echo "TRAVIS_COMMIT=${TRAVIS_COMMIT}"
    COMMIT=(${TRAVIS_COMMIT_RANGE//\.\.\./ })
    COMMIT=${COMMIT[1]}
    SOURCE_BRANCH=$(git ls-remote | grep ${COMMIT} | grep "refs/heads" | cut -f 2)
    export SOURCE_BRANCH=(${SOURCE_BRANCH/refs\/heads\//})
    echo "SOURCE_BRANCH=${SOURCE_BRANCH}"
    if [[ -z ${SOURCE_BRANCH} ]]; then
        echo ""
        echo "ERROR: Could not determine the branch of the pull request. TRAVIS_COMMIT_RANGE was ${TRAVIS_COMMIT_RANGE}"
        exit 1
    fi
    export COMMITTER_EMAIL="$(git log -1 ${COMMIT} --pretty="%cE")"
    echo "COMMITTER_EMAIL=${COMMITTER_EMAIL}"

    # Define the following variables in the Travis environment
    export BRANCH_TO_MERGE_INTO="master"

    #use next line when https://github.ibm.com/Whitewater/TravisCI/issues/413 is fixed
    #PR should come from same remote, ie. $TRAVIS_PULL_REQUEST_SLUG == $TRAVIS_REPO_SLUG.  We can verify this when env is available.

    #GITHUB_REPO=${TRAVIS_PULL_REQUEST_SLUG}

    export GITHUB_REPO=${TRAVIS_REPO_SLUG}
    echo "GITHUB_REPO=${GITHUB_REPO}"

    printf 'Checking out %s\n' "${SOURCE_BRANCH}" >&2
    git branch "${SOURCE_BRANCH}" "${TRAVIS_COMMIT}"
    git checkout "${SOURCE_BRANCH}"

    git remote set-branches --add origin "${BRANCH_TO_MERGE_INTO}"
    git fetch origin "${BRANCH_TO_MERGE_INTO}"

    printf 'Checking out %s\n' "${BRANCH_TO_MERGE_INTO}" >&2
    git checkout "${BRANCH_TO_MERGE_INTO}"


    printf 'Merging %s\n' "${SOURCE_BRANCH}" >&2
    printf 'Commit Message: %s\n' "${TRAVIS_COMMIT_MESSAGE}" >&2
    git merge --no-edit "${SOURCE_BRANCH}"

    printf 'Pushing to %s\n' "${GITHUB_REPO}" >&2
    push_uri="https://${GIT_TOKEN}@github.ibm.com/${GITHUB_REPO}"

    # Redirect to /dev/null to avoid secret leakage
    git push "$push_uri" "${BRANCH_TO_MERGE_INTO}" >/dev/null 2>&1

else
    echo "Not a Pull Request to master branch, auto merge not completed."
fi

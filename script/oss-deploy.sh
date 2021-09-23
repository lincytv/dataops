#!/bin/bash
#set -xe # remove the #, to activate debugging capabilities

# Push updates from master branch to gh-pages branch
if [ ! -n $1 ] ; then
    echo "Usage: oss-deploy.sh <token>"
    exit 1;
fi

export GIT_TOKEN="$1"
PUSH_REPO="https://${GIT_TOKEN}@github.ibm.com/${TRAVIS_REPO_SLUG}"

SOURCE_BRANCH="master"
TARGET_BRANCH="gh-pages"
DEPLOY_DEST="_site"

function doValidate {
  # Validate runbook metadata
  ./script/OSS_verify_metadata.sh

  # Generate the html site ready for validation
  jekyll build --verbose --baseurl /${TRAVIS_REPO_SLUG} --destination ./${DEPLOY_DEST} >/dev/null 2>&1

  # Validate generated html and json
  ./script/oss-validate-html.sh
}

function doDeploy {
  # from https://github.com/X1011/git-directory-deploy
  ./script/deploy.sh
}

# Testing of travis env variables
# Travis is not setting env vars when it's a PR.
# See:  https://github.ibm.com/Whitewater/TravisCI/issues/413
if [  "${TRAVIS_EVENT_TYPE}" == "pull_request" ]; then
    echo "Eventy type is PULL REQUEST:"
    echo "TRAVIS_PULL_REQUEST_SLUG=${TRAVIS_PULL_REQUEST_SLUG}"
    echo "TRAVIS_PULL_REQUEST_SHA=${TRAVIS_PULL_REQUEST_SHA}"
    echo "TRAVIS_PULL_REQUEST_BRANCH=${TRAVIS_PULL_REQUEST_BRANCH}"
fi

# Pull requests and commits to other branches shouldn't try to deploy, just build to verify
if [  "${TRAVIS_EVENT_TYPE}" == "pull_request" -o "$TRAVIS_BRANCH" != "$SOURCE_BRANCH" ]; then
    echo "Skipping deploy; just doing validation."
    doValidate
    exit 0
fi

# Run validation scripts
doValidate

# Define required variables for deploy
export GIT_DEPLOY_DIR=${DEPLOY_DEST}
export GIT_DEPLOY_BRANCH=${TARGET_BRANCH}
export GIT_DEPLOY_REPO=${PUSH_REPO}
export GIT_DEPLOY_EMAIL="$(git log -1 ${TRAVIS_COMMIT} --pretty="%cE")"

git config user.name "Travis CI deploy"
git config user.email "$GIT_DEPLOY_EMAIL"

# Deploy _site to gh-pages branch
doDeploy
#set +x	remove the #, to activate debugging capabilities

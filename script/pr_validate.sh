#!/bin/bash
# Generate the html site ready for validation

# Validate The YAML format of the Front Matter.

# For each file in the docs/runbooks folder

FILE=$(readlink -f "$0")
CWD=$(dirname $FILE)
PARENT_DIR=$(dirname $CWD)
RB_DIR="$PARENT_DIR/docs/runbooks"

cd $RB_DIR || exit 1
echo "Validating YAML headers"
for file in */*.md *.md; do
  echo "Validating YAML in file: $file"
  echo "---" > tmp.yml 2>&1
  counter=0
  while read line; do
    echo $line | grep -qE "\-{3}"
    if [ $? == 0 ]; then
      let "counter += 1"
    fi
    if [[ $counter -lt 2 ]]; then
      echo $line >> tmp.yml
    else
      break
    fi
  done < $file

  yamllint tmp.yml > /dev/null &2>1
  YAML_EXIT_CODE=$?
  if [ $YAML_EXIT_CODE != 0 ]; then
    echo "ERROR Linting File: $file, Exiting with Code: $YAML_EXIT_CODE"
    exit $YAML_EXIT_CODE
  fi
done
echo "YAML OK"

SITE_DIR="$PARENT_DIR/_site"
mkdir $SITE_DIR; chown -R jekyll:jekyll $SITE_DIR
echo "Building the site with Jekyll"
jekyll build --source $PARENT_DIR --destination $SITE_DIR

# Check all the json files are valid
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

# Validate the generated html
echo "Validating HTML"
htmlproofer --disable-external --empty-alt-ignore --allow-hash-href --file-ignore "/.+\/docs\/process.+/,/.+\/docs\/runbooks\/general_documentation.+/,/.+\/docs\/runbooks\/images.+/,/.+\/docs\/runbooks\/armada.+/,/view.html$/" $SITE_DIR
if [ $? -eq 1 ]; then
  echo "Invalid HTML. Please check logs"
  exit 1
else
  echo "HTML Valid - OK"
fi

# Check for existence of mark down files
echo "Checking for existence of mark down files"
for i in $SITE_DIR/docs/runbooks/*md;
do
	test -f "$i"
	if [ $? -eq 0 ]
	then
		echo "One or more md files exist"
		exit 1;
	fi
done

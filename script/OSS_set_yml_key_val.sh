#!/bin/sh
# Program: OSS_set_yml_key_val.sh
# Rev: 1.0.0
# Created by: Alejandro Torres Rojas
# Date: 06-Dec-2017
# Developed on bash
# Tested on bash macOS Sierra
#
# Sample program call:
# sh OSS_set_yml_key_val.sh  key val file.yml
# sh OSS_set_yml_key_val target wanda _config.yml
#
# Arguments used:
#     key          = A key inside the yml file
#     val          = A new value to be set for the key passed
#     file.yml     = A yml file
#
# # OSS_set_yml_key_val recieves a Key to search and Value to replace for the
# Key in the YAML input file.
#  First checks the number of parameters is equal 3 KEY, Value and File.yml.
#  Checks that the passed file is a valid yaml file otherwise stops there.
#  If a valid yml file, then uses AWK to scan every line,vvalidates if the a Key
#  is in the line, if exist then replaces a line wiht the new Key and Value
#  Creates a temporary file to store the new file then removes the passed file
#  and copies the temporary into the passing file, and finally removes the tmp file

if [ $# -ne 3 ]; then
    echo "usage: $0 key value file.yml" >&2
    exit 1
fi

yamllint $3 >1


if [ $? -eq 0 ]
then
    awk -F : -v key="$1" -v val=" $2" '
        function ltrim(s) { sub(/^[ \t\r\n]+/, "", s); return s }
        function rtrim(s) { sub(/[ \t\r\n]+$/, "", s); return s }
        function trim(s) { return rtrim(ltrim(s)); }
        BEGIN {OFS = FS}
        $1 == key {in_key = 1}
        NF == 0   {in_key = 0}
        in_key && trim($1) == key {$2 = val}
        {print}
    ' "$3" > tmp.yml
    rm $3 && cp tmp.yml $3 && rm tmp.yml
    echo "The script ran ok"
    exit 0
else
  echo "The script failed $3 is not a valid ymal file" >&2
  exit 1
fi

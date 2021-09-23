#!/usr/bin/python
#
# author: John Murphy
#
# Modules:
#    requests (to install: "pip install requests" or "easy_install requests")
#
# This program queries for the last successful Jenkins build. The query returns
# info in json format.  Search the json for key "timestamp" which is in epoch
# format in ms.  Print to console a human readable format date

import json
import sys
import requests
import time


def main():
    if len(sys.argv) > 1:
        jenkinsUrl = sys.argv[1]
        username = sys.argv[2]
        token = sys.argv[3]
    else:
        sys.exit(1)

    try:
        r = requests.get(
            jenkinsUrl +
            "lastSuccessfulBuild/api/json",
            auth=(
                username,
                token))
        buildjson = r.json()  # capture json data
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    if "timestamp" in buildjson:
        # timestamp = epoch time in milliseconds.
        epochtime = (buildjson["timestamp"] + 2000) / 1000
        # Adding 2 seconds to epoch time. Doing this to avoid overlap between
        # Jenkins Jobs which checking for differences in files in their builds.
        print time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(epochtime))
        sys.exit(0)

if __name__ == '__main__':
    main()

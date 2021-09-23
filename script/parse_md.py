#!/usr/bin/python
"""
Program: parse_md000.py

Sample program call:
python parse_md.py docs/runbooks/service_discovery_troubleshooting.md M
output.json runbooks_template_keys.json

Arguments used:
    runbook_name = sys.argv[1]
    modify_type = sys.argv[2]
    runbook_json = sys.argv[3]
    template_keys = sys.argv[4]

Explanation of program:
This program is executed as part of a Jenkins job that is triggered by a
webhook when git is updated.  The modify_type argument to this script (argv[2])
is a value that is derived from the Git push. The valid options for modify_type
are: M = Modified file, A = Added file, D = Deleted file.

This script tries to read the embedded metadata in the Runbook (if this
exists). If the metadata exists, it verifies that the metadata keys are
correct for the type of Runbook it is (using argv[4] as source).  The script
exits if the keys are not correct.  The metadata in the Runbook is used to
update the metadata in the 'runbooks.json' file (argv[3]). 'runbooks.json' is
used by Doctor to display runbooks. It does not modify the metadata in the
Runbook if metadata is in the Runbook.
"""
import os
import sys
import re
import json
from pprint import pprint
import yaml  # PyYaml

'''
Following methods are general purpose:
    getkeys() = get keys for a given Runbook Type from template file
    checkkeys() = checks if the keys in the Runbook match the Runbook type.
    stripToRunbookName() = Extracts Runbook name.
    parseLink() = Strips URL of content after '#'
    updateJson() = Finds and replaces the metadata for a Runbook based on
        the modified ('M' = Modified, 'A' = Add or 'D' = Delete)
    updateJsonNEW() = writes Runbooks metadata to file.
 '''


def getkeys(type_of_runbook):
    # This method gets the relevant metadata 'keys' for runbook type
    template_keys = sys.argv[4]

    with open(template_keys, 'r') as json_types:
        jsontypes = json.load(json_types)
    json_types.close()

    # For each item in jsontypes, find a match for the 'type' and return keys
    for t in jsontypes:
        if re.match(type_of_runbook, t['type'], re.I):
            return t.keys()
    keys = []
    return keys


def checkkeys(keys_to_check):
    # This method checks if the metadata headings in the Runbook are valid.
    # This method is only run on Runbooks that have metadata incorporated in
    # the runbook. Method gets the correct metadata for a given 'type' of
    # Runbook (the default is type 'Informational'). Checks for the existence
    # of each key in the metadata headings in the Runbook.
    template_keys = sys.argv[4]
    comparekeys = []

    with open(template_keys, 'r') as json_types:
        jsontypes = json.load(json_types)
    json_types.close()

    # For each item in jsontypes, find a match for the 'type' and return keys
    for t in jsontypes:
        if re.search(t['type'], keys_to_check['type'], re.I):
            comparekeys = t.keys()

    if not comparekeys:
        comparekeys = getkeys('Informational')

    for k in comparekeys:
        if k not in keys_to_check.keys():
            return False
    return True


def stripToRunbookName(runbookname):
    # This method will strip, for example:
    # (./../runbooks/registry_healthcheck.html)
    # and return /runbooks/registry_healthcheck.html
    runbook = ''
    runbookname_split = runbookname.split('/')
    if runbookname_split:
        runbook = runbookname_split[len(runbookname_split)-1]
        if runbook.find('.html'):
            endindex = runbook.find('.html') + 5  # Add back in the .html!
            runbook = runbook[: endindex]
            runbook = '/' + runbook  # Important so that Runbook name is not
            # matched against partial name.
    return runbook.strip()


def getRunbookLink(runbookname):
    # This method will strip, for example:
    # (./../runbooks/registry_healthcheck.html)
    # and return /runbooks/registry_healthcheck.html
    prepended = "docs/runbooks"
    length = len(prepended)

    if runbookname.find('.md'):
        index = runbookname.find('.md')
        runbookname_html = runbookname[: index] + ".html"

        # Remove pre-pended info:
        if re.search(prepended, runbookname_html, re.I):
            runbookname_html = runbookname_html[length:]
        runbookname_html.strip()
        return runbookname_html
    return runbookname


def parseLink(item):
    # This method will strip # from a URL
    item_hash_split = item.split('#')
    link = item_hash_split[0]
    return link.strip()


def updateJson(json_item, modified):
    # This method will update the metadata elements in the runbooks json file
    output_json_file = sys.argv[3]
    runbookname = sys.argv[1]

    with open(output_json_file, mode='r') as out:
        input_json = json.load(out)
    out.close()

    if modified == 'D':
        for item in input_json:
            if getRunbookLink(runbookname) == parseLink(
                    stripToRunbookName(item['link'])):
                input_json.remove(item)
                updateJsonNEW(input_json)
                return
    else:
        for item in input_json:
            if getRunbookLink(runbookname) == parseLink(
                    stripToRunbookName(item['link'])):
                input_json.remove(item)
                json_item['link'] = getRunbookLink(runbookname)
                json_item['type'] = json_item['type'].upper()
                print json_item
                input_json.append(json_item)
                updateJsonNEW(input_json)
                return

    if modified == 'A' or modified == 'M':
        json_item['link'] = getRunbookLink(runbookname)
        json_item['type'] = json_item['type'].upper()
        input_json.append(json_item)
        updateJsonNEW(input_json)

    return


def updateJsonNEW(runbook):
    # This method will print al the metadata results to the runbooks json file
    output_json_file = sys.argv[3]
    with open(output_json_file, mode='w') as out:
        res = json.dump(
            runbook,
            out,
            sort_keys=True,
            indent=4,
            separators=(
                ',',
                ': '))
    out.close()
    return


'''
    read_yaml() = This method checks if there are multiple colons in a line
    and quotes the line if there are.
    read_runbook_metadata() = read metadata from Runbook with inbuilt metadata
'''


def read_yaml(line):
    # This method checks if there are multiple colons in a line and quotes
    # the line if there are.
    line_colon = line.split(':')
    # if >= 2 colons, then quote the 'value' part of key-value pair:
    if len(line_colon) <= 2:
        return line
    else:
        # check if value is already quoted:
        line_value = line[len(line_colon[0]) + 1:].strip()
        if line_value[0] == '[' and line_value[len(line_value) - 1] == ']':
            return line
        elif line_value[0] == '"' and line_value[len(line_value) - 1] == '"':
            return line_colon[0] + ': ' + line[len(
                line_colon[0]) + 1:].strip() + '\n'
        else:
            return line_colon[0] + ': "' + line[len(
                line_colon[0]) + 1:].strip() + '"\n'


def read_runbook_metadata(name_md_file):
    with open(name_md_file, 'r') as infile:
        reader = infile.readlines()
    infile.close()

    metadata = ''
    count_dashes = 0
    start_dash = 0
    end_dash = 0
    line_number = 0
    record = False

    for line in reader:
        # Search for "---" - denotes start/end of yaml metadata section
        if re.search('---', line):
            count_dashes = count_dashes + 1
            if count_dashes == 1:
                start_dash = line_number
            if count_dashes == 2:
                end_dash = line_number
        if count_dashes == 1:
            metadata = metadata + read_yaml(line)
        if count_dashes > 2:
            break
        line_number += 1

    try:
        thisdict = yaml.load(metadata)  # load meta string into dict format
        thisdict['startline'] = start_dash
        thisdict['endline'] = end_dash
    except:
        print "************************************************************"
        print "**** Error parsing yaml info from Runbook " + str(
            name_md_file) + " ****"
        print "************************************************************"
        sys.exit(1)
    return thisdict


'''
The following methods control the flow of work to be done:
    process() = Calls above methods as needed.
        Calls the following method based Runbook containing metadata or not:
    process_metadata() = Process Runbooks with Metadata in them
    main() = starts the program/script
'''


def process_metadata(modified, thisyaml):
    try:
        del thisyaml['startline']
    except KeyError:
        pass
    try:
        del thisyaml['endline']
    except KeyError:
        pass

    updateJson(thisyaml, modified)
    return


def process(runbook_name, runbook_json, modified):
    # Read in Runbook into 'reader'

    with open(runbook_name, 'r') as infile:
        reader = infile.readlines()
    infile.close()

    # Open, e.g. 'doctor.json' file.
    with open(runbook_json, 'r') as json_data:
        runbook = json.load(json_data)
    json_data.close()

    oldyamldata = {}
    found = False

    # Get metadata of current Runbook
    oldyamldata = read_runbook_metadata(runbook_name)
    print "Metadata read from Runbook " + str(oldyamldata)

    if 'type' not in oldyamldata:
        print "Old style metadata in this Runbook"
        print "Metadata needs to be added to Runbook"
        print "Exiting script"
        sys.exit(1)
    else:
        # Dealing with Runbook with METADATA in it.
        # check metadata in Runbook is valid:
        if not checkkeys(oldyamldata):
            print 'Error in Keys in this Runbook'
            sys.exit(1)
        # If keys are not correct
    process_metadata(modified, oldyamldata)
    return


def main():
    program = sys.argv[0]
    if len(sys.argv) != 5:
        sys.stderr.write("Check arguments. Usage: %s runbook-filename modify-type runbook-json type-template-file\n" % program)
        sys.exit(1)

    runbook_name = sys.argv[1]
    modify_type = sys.argv[2]
    runbook_json = sys.argv[3]
    template_keys = sys.argv[4]

    try:
        process(runbook_name, runbook_json, modify_type)

    except EnvironmentError:
        print("def main().Error accessing file passed as argument to program")
    return

if __name__ == '__main__':
    main()

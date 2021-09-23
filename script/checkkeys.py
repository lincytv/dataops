#!/usr/bin/python
"""
Program: parse_md.py
Rev: 1.0.0
Author: John Murphy
Date: 22-Mar-2016
Developed on Python 2.7.10
Tested on Python 2.7.6 ?

Sample program call:
python checkkeys.py runbook_name runbooks_template_keys.json

Arguments used:
    runbookname = sys.argv[1]
    template_keys = sys.argv[2]

Explanation of program:
This script reads the embedded metadata in the Runbook (if this
exists) and compares it to the metadata of the file that passed as an
argument to this script
"""
import os
import sys
import re
import json
from pprint import pprint


def getkeys(type_of_runbook):
    # This method gets the relevant metadata 'keys' for runbook type
    template_keys = sys.argv[2]

    with open(template_keys, 'r') as json_types:
        jsontypes = json.load(json_types)
    json_types.close()

    # For each item in jsontypes, find a match for the 'type' and return keys
    for t in jsontypes:
        if re.match(type_of_runbook, t['type']):
            return t.keys()

    keys = []
    return keys


def read_runbook_metadata(reader):
    # If metadata is in Runbook, it is in a  key:value format section.
    line = 0
    thisdict = {}
    record = False
    count = 0
    for element in reader:
        if record:  # Now read the key:value pairs
            keyvalue = element.split(':')  # Split key: value items
            if len(keyvalue) > 1:
                index = element.find(':')
                key1 = element[:index]
                key1 = key1.strip()
                if key1[0] == '-':  # Remove leading '-'
                    key1 = key1.lstrip('- ')
                value = element[index + 1:]
                value = value.strip()
                if len(value) > 0:
                    if key1 in ['failure', 'playbooks']:
                        if value[0] == '[' and value[len(value) - 1] == ']':
                            value = value[1: len(value)-1]  # eliminate []
                            value = value.strip()
                        newvaluelist = []
                        csv = value.split(',')
                        for c in csv:
                            c = c.strip()
                            newvaluelist.append(c)
                        value = ','.join(newvaluelist)
                thisdict[key1] = value

        # Search for "---" - denotes start/end of yaml metadata section
        if re.match('---', element):
            count = count + 1
            if count == 1:
                thisdict = {}
                thisdict['startline'] = line
                record = True
            if count == 2:
                thisdict['endline'] = line
                record = False
        line += 1
    return thisdict


def checkkeys(keys_to_check):
    # This method checks if the metadata headings in the Runbook are valid.
    # This method is only run on Runbooks that have metadata incorporated in
    # the runbook. Method gets the correct metadata for a given 'type' of
    # Runbook (the default is type 'Informational'). Checks for the existence
    # of each key in the metadata headings in the Runbook.
    template_keys = sys.argv[2]
    comparekeys = []


    if not 'type' in keys_to_check:
        print 'ERROR: No type specified'
        return False


    with open(template_keys, 'r') as json_types:
        jsontypes = json.load(json_types)
    json_types.close()

    # For each item in jsontypes, find a match for the 'type' and return keys
    # 26-May-2016: Comment out the following 3 lines & add following 8 lines.
    for t in jsontypes:
        if t['type']:
            if re.search(t['type'], keys_to_check['type']):
                comparekeys = t.keys()

    if not comparekeys:
        comparekeys = getkeys('Informational')

    for k in comparekeys:
        if k not in keys_to_check.keys():
            return False
    print '   Keys are good'

    return True


def process(runbook_name):
    # Read in Runbook into 'reader'

    with open(runbook_name, 'r') as infile:
        reader = infile.readlines()
    infile.close()

    new_json_data = {}
    y = {}
    found = False
    yamllist = []

    # Get metadata of current Runbook
    yamllist = read_runbook_metadata(reader)
    if not yamllist:
        print "Dealing with Runbook with NO metadata in it."
        printerrormessage()
        sys.exit(1)
        return

    if yamllist:
        # check metadata in Runbook is valid:
        if not checkkeys(yamllist):
            print 'ERROR: Error in Metadata Keys in this Runbook'
            printerrormessage()
            sys.exit(1)
    return


def printerrormessage():
    print "   Please add/correct metadata in this Runbook."
    print "   Metadata templates available at:"
    print "   git: alchemy-conductors/documentation-pages/docs/doc_updates/"
    return


def main():
    program = sys.argv[0]
    if len(sys.argv) != 3:
        sys.stderr.write("Check arguments. Usage: %s runbook-filename type-template-file\n" % program)
        print "runbookname = " + sys.argv[1]
        print "template_keys = " + sys.argv[2]
        sys.exit(1)
    runbookname = sys.argv[1]
    template_keys = sys.argv[2]

    try:
        process(runbookname)

    except EnvironmentError:
        print("def main().Error accessing file passed as argument to program")
    return


if __name__ == '__main__':
    main()

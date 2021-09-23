#!/usr/bin/python
'''
================================================================================
Program: UpdSearchJSON.py
Rev: 1.0.0
Created by: Alejandro Torres Rojas
Date: 13-Feb-2018
Developed on Python 3.6.2
Tested on Python 3.6.2 within BASH 3.2.57(1)-release MacOS HD Sierra

Use to update the components listed by target under the -_includes/docs-toc.html file. The docs-tocs looks like the
follow for the drop down menu section:

    <ul id="runbooklist" class="dropdown-menu">
        <!--<li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#armada" data-proofer-ignore>armada</a></li>-->
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#doctor" data-proofer-ignore>doctor</a></li>
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#gre" data-proofer-ignore>GRE</a></li>
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#marmot" data-proofer-ignore>marmot</a></li>
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#netcool" data-proofer-ignore>Netcool</a></li>
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#ossplatform" data-proofer-ignore>OSS Platform</a></li>
        <!--<li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#general_documentation" data-proofer-ignore>general_documentation</a></li>-->
        <!--<li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#netint" data-proofer-ignore>netint</a></li>-->
        <!--<li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#schematics" data-proofer-ignore>schematics</a></li>-->
        <li><a href="{{ site.baseurl }}/docs/runbooks/runbooks.html#sosat" data-proofer-ignore>sosat</a></li>
    </ul>

The get_components parser will return a string with the list of the active components, using as example the <ul> above
the string returned will be "doctor gre marmot netcool ossplatform sosat" armada and general_documentation are not
included because they are commented out.

Once completed the generate_search_json call will open the search.json file use for the jekyll search and will update
the value of line '{% assign valid_components = "doctor gre" | split: " " %}'  with the follow
{% assign valid_components = "doctor gre marmot netcool ossplatform sosat" | split: " "  %} in this example.
This idea of using only valid components was originated by Irma Sherif and this script just enhanced her idea by adding
automation to this process.

Will default the .html file at ../_includes/docs-tocs.html, unless a basename passed by --in <file>.
Will default the .json file at ../assets/simple-jekyll-search/search.json, unless a basename passed by --out <file>.
The search string to match in the JSON file  by default is "assign valid_components =", unless a vales passed by --s <str>.
The replace string for the matching above by default is 'assign valid_components = "%s" | split: " " ' where %s will be
replaced by the components list use --r <str> to pass a different string, %s must be included {% will be added.


Sample program call:
python3 UpdSearchJSON.py

Using python3 UpdSearchJSON.py --help will get the command line help

usage: UpdSearchJSON.py --in </path/filename> --out </path/filename> --s <str> --r <str>

'''

from html.parser import HTMLParser
from html.entities import name2codepoint
import io
import time
import os
import argparse
import sys
import json



class OOSHTMLParser(HTMLParser):
    '''
    :param HTMLParser python class

    '''
    # Initializing lists
    lsStartTags = list()
    lstAttr = list()
    lsEndTags = list()
    lstData   = list()
    lsComments = list()
    lsStartEndTags = list()
    lstEntityRef = list()
    lstCharRef =list()
    lstDecl =list()



    def handle_starttag(self, tag, attrs):
        self.lsStartTags.append(tag)
        for attr in attrs:
            self.lstAttr.append(attr)

    def handle_endtag(self, tag):
        self.lsEndTags.append(tag)

    def handle_data(self, data):
        self.lstData.append(data)

    def handle_comment(self, data):
        self.lsComments.append(data)

    def handle_entityref(self, name):
        c = chr(name2codepoint[name])
        self.lstEntityRef.append(c)

    def handle_charref(self, name):
        if name.startswith('x'):
            c = chr(int(name[1:], 16))
        else:
            c = chr(int(name))
        self.lstCharRef.append(c)

    def handle_decl(self, data):
        self.lstDecl.append(data)


def get_components(fName):
    '''
    Will return a string with the list of the active components, using the attributes that contain '#ref' value.
    A returned will be like  "doctor gre marmot netcool ossplatform sosat"

    :param:fName An html file with the menu values for the runbook portal
    :return components a string value with the active components
    '''

    parser = OOSHTMLParser()
    components=''
    try:
        with io.open(fName, 'r', encoding="utf-8") as infile:
            data = infile.readlines()
        infile.close()
        parser.feed(''.join(data)) #data is a tuple the join is use to covert it into string use by the HTMLParser

        lstAttr = parser.lstAttr # Get all attributes
        lstData = []
        for attr in lstAttr:
            if 'href' in attr[0].lower() and '#' in attr[1] and len(attr[1]) > 2:
                # Only get lines with metadata
                lstData.append(''.join(attr))
        for component in lstData:
            # Attributes will return a line like href="{{ site.baseurl }}/docs/runbooks/runbooks.html#doctor
            # look for the '#' amd return the component to add to the components variable
            components += component[component.find('#') + 1:] + ' '
    except IOError as e:
        print("I/O error({0}): {1} {2}".format(e.errno, e.strerror,fName))
    return components[:len(components)-1] #removes the extra space at the end


def generate_search_json(components,fSearchJS,strMatch,strLine):
    '''

    :param components: A string with the list of components to be added
    :param fSearchJS: search.json file use by Jekyll
    :param strMatch: A string to match on the search.json file
    :param strLine: A string to replace in the json file if strMatch found
    :return: a new search.json file
    '''

    fPath = os.path.dirname(os.path.realpath(fSearchJS))
    tmpFile = fPath + '/tmp_file_' + time.strftime("%Y%m%d-%H%M%S") + '.json'
    cpJson  = fPath +'/search_' + time.strftime("%Y%m%d-%H%M%S") +'.json'
    newFile = fPath + '/search.json'
    try:
        with io.open(fSearchJS, 'r', encoding="utf-8") as inFile:
            dataOut = inFile.readlines()
        st_cmd = os.system('mv ' + fSearchJS + ' ' + cpJson)
        if st_cmd ==0:
            outFile=io.open(tmpFile,'w')
            for line in dataOut:
                if strMatch in line:
                    updLine= '\t{% '+ strLine % (components) + ' %}\n'
                    outFile.write(updLine)
                else:
                    outFile.write(line)
            outFile.close()
            st_cmd=os.system('mv ' + tmpFile + ' ' + newFile)
            if st_cmd ==0:
                os.chmod(newFile, 0o644)
                os.remove(cpJson)
            else:
                os.system('mv ' + cpJson + ' ' + fSearchJS)
    except IOError as e:
        print("I/O error({0}): {1} {2}".format(e.errno, e.strerror,fSearchJS))
        os.system('mv ' + cpJson + ' ' + fSearchJS)

def is_valid_json_file(f_name):
    '''
    Checks if the passed file exist and also it is in a valid JSON format
    :param f_name:  A file name.

    :return:        A dictionary object created from a JSON files passed
    '''

    try:
        with io.open(f_name, 'r', encoding="utf-8") as f_json:
            try:
                is_json = json.load(f_json)
                f_json.close()
                return is_json
            except  ValueError as e:
                print(
                "!Fatal Error!: " + f_name + " is not a valid JSON file, expecting a JSON file, system error: %s" % e)
                sys.exit(1)
    except EnvironmentError:
        print(
            "!Fatal Error!: " + f_name + " does not exist, make sure the json file is located in the same directory of this script %s" % __file__)
        sys.exit(1)

def get_system_values(script_path):
    '''
    Gets the metadata use to run this script from a JSON format file defined the a user.

    :param    script_path:   A location of this script.

    :return:  _sys_values:   All metadata info defined by a user loaded into a global dictionary object.
    '''

    global _sys_values
    f_name = os.path.basename( __file__).replace('.py', '.json')
    f_name = script_path+'/data/'+f_name
    _sys_values = is_valid_json_file(f_name)
    return _sys_values


def main():

    program = os.path.basename(sys.argv[0])
    script_path = os.path.dirname(os.path.realpath(__file__))
    _sys_values = get_system_values(script_path)  # Loads the system variable into a global dictionary object

    # Sets the argparse object with the parameter the script will accept as valid parameters
    strPrgUse = program + " --in <filename> --out <filename> --s <str> --r <str>"


    iArgv = argparse.ArgumentParser(prog=program, usage=strPrgUse,
                                    description=_sys_values['description'])
    iArgv.add_argument('-version', '--version', '-Version', '--Version', action='version',
                       version='%(prog)s ' + _sys_values['version'])
    iArgv.add_argument('-in', '--in', '-IN', '--IN', action='store', dest='html_file', default=_sys_values['html_file'],
                       help=_sys_values['hlp_in'])
    iArgv.add_argument('-out', '--out', '-OUT', '--OUT', action='store', dest='json_file', default=_sys_values['json_file'],
                       help=_sys_values['hlp_out'])
    iArgv.add_argument('-s', '--s', '-S', '--S', action='store', dest='str_2_match', default=_sys_values['str_2_match'],
                       help=_sys_values['hlp_str_2_match'])


    iArgv.add_argument('-r', '--r', '-R', '--R', action='store', dest='ln_2_upd', default=_sys_values['ln_2_add_cmpnnts'],
                        help=_sys_values['hlp_ln_2_add_cmpnnts'])

    argv_passed = iArgv.parse_args()

    # ln_2_add_cmpnnts = 'assign valid_components = "%s" | split: " " '
    # str_2_match = 'assign valid_components ='
    generate_search_json(get_components(argv_passed.html_file), argv_passed.json_file,argv_passed.str_2_match,
                         argv_passed.ln_2_add_cmpnnts)





if __name__ == '__main__':
    main()

#!/usr/bin/python

'''
Program: parse_md.py
Rev: 1.0.0
Author: John Murphy
Date: 22-Mar-2016
Developed on Python 2.7.10
Tested on Python 2.7.6 ?

Sample program call:
python checkkeys.py runbook_name runbooks_template_keys.json

Arguments used:
    runbookname   = sys.argv[1]
    template_keys = sys.argv[2]

Explanation of program:
This script reads the embedded metadata in the Runbook (if this
exists) and compares it to the metadata of the file that passed as an
argument to this script

========================================================================
Program: OSScheckkeys.py
Rev: 2.0.0
Updated by: Alejandro Torres Rojas
Date: 15-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Sample program call:
python OSScheckkeys.py  runbooks_template_keys.json default_replacement.json _example_metadata.json

Arguments used:
    template_keys               = sys.argv[1] <script/runbooks_template_keys.json>
    default_replacements        = sys.argv[2] <script/_defaults_replacement.json>
    _example_metadata           = sys.argv[3] <script/_example_metadata.json>
    template_keys:              Contains the metadata to look for a specific runbook in order to check a new type it
                                needs to be added to this file.
    default_replacements:       Contains the default values for a metadata.
    _example_metadata:          Contains example of valid values for a metadata.
    script/OSScheckkeys.json:   Contains all custom messages displayed, REQUIRED. this file name must be the same as
                                the python one.

If bad metadata is verified in a runbook it will reported on the screen as well as on an output file called
runbook_errors_YYYYMMDD_HHMMSS.json the name can be changed updated the key:value [ouput_file_name] inside
OSScheckkeys.json file

================================================================================
Program: OSScheckkeys.py
Rev: 2.1.0
Updated by: Alejandro Torres Rojas
Date: 16-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Added get_component(lst_all_components,component_name,runbook_full_path):

Checks if the component_name passed is root component, if it is, it should be listed in lst_all_components
otherwise it is a child component, if it is a child component, returns their parent.


        :param lst_all_components:  Contains all the parent components form the docs/runbooks directory
        :param component_name:      The component name of a runbook it could be a parent or a child
        :param runbook_full_path:   runbook's full path to detect the parent of a child component
        :return:                    parent component name

This enhancement will allow to report errors under a  parent component for a file structure like the follow:

--docs
-----runbooks
--------armada
----------api
----------cluster
------------etcd

all the above runbook with errors will reported under armanda component
================================================================================
Program: OSScheckkeys.py
Rev: 2.1.1
Updated by: Alejandro Torres Rojas
Date: 21-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Added   def yes_no(answer):
Added   def is_valid_json_file(f_name):
Updated def main():
Updated def check_file_loc(script_path,file_name):
Updated def get_runbooks(runbook_directory,list_of_files=None)
Updated def get_system_values()
Renamed from:   def printerrormessage(runbook_with_errors, runbook_types_cnt)
        to:     def show_results(runbook_with_errors, runbook_types_cnt)
Renamed from:   def loadJSONDatadflts_rplcmnt,xmpl_mtdt,template_keys)
        to:     def load_json_data(dflts_rplcmnt,xmpl_mtdt,template_keys):
================================================================================
Program: OSScheckkeys.py
Rev: 2.2.2
Updated by: Alejandro Torres Rojas
Date: 27-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Added the verification point of the YML metadata using yamllint instead YAML python library.
the YAML python library does not detect if ___ is not added at the end and it is required by Jekyll
also does not detect if a key values is like this key:value or like this key: value. Jekyll does
required an space otherwise it will fail a build

Added   def log_error(keys_to_check,runbook_type,component_name,runbook_with_errors,runbooks_type_cnt,msg=None):
Added   def is_valid_yml(runbook_name,str_metadata):
Updated def read_runbook_metadata(reader,thisdict):
Updated def checkkeys(keys_to_check,runbook_with_errors,runbook_name,component_name,runbook_types_cnt):
Updated def process(lst_runbook_name,runbook_with_errors,runbook_types_cnt):
Updated def verify_link(key,keys_to_check,runbook_name,err_flag):
========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.2
Updated by: Alejandro Torres Rojas
Date: 28-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Moved all JSON files to a data directory for better administration of the script folder
Formatted to follow PEP 8 -- Style Guide for Python Code https://www.python.org/dev/peps/pep-0008/

./script/data/_defaults_replacement.json
./script/data/_example_metadata.json
./script/data/OSScheckkeys.json
./script/data/OSScheckkeys.readme
./script/data/runbooks_template_keys.json

Updated def get_system_values():

========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.3
Updated by: Alejandro Torres Rojas
Date: 29-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Added two more validations after some testing:

    1) If a value is passed on the layout key ot the YML metadata, the value must be a valid file name under /_layouts
    directory.
    2) If a value is passed on the link key of the YML metadata, the value must not have http or https on it

Added   def get_layouts():
Updated def verify_layout(key, keys_to_check, err_flag):
Updated def verify_link(key, keys_to_check, runbook_name, err_flag):
========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.3
Updated by: Alejandro Torres Rojas
Date: 30-Nov-2017
Developed on Python 2.7
Tested on Python 2.7

Fixed a bug when checking service and related-service key:value pairs

Updated def verify_service(key, keys_to_check, err_flag):
Updated def run_verify(key, keys_to_check, err_flag, type, runbook_name):

========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.3
Updated by: Alejandro Torres Rojas
Date: 1-Dec-2017
Developed on Python 2.7
Tested on Python 2.7

Fixed the following bugs:

    * When YML metadata contained unicode characters creating a temportary file for the yamllint yet failed
    added codecs to when creating the temporary file using uft-8 encoding.
    * When a runbook did not have a type only the first one of was logged to the output JSON file, the counter
    was OK. The code was corrected to use the log_error function instead
    * Updated the error message  when the link for a runbook does not contain the runbook name
    * verify_name had a typo error, ['missing'] instead of _sys_values['missing']

Additionally,  OSScheckeys JSON file was updated with a new entry 'file_2_exclude' to exclude for now all files under
readme.md file name. dir_2_exclde is now dir_2_exclude in the same JSON file.
Finally, all JSON files under data were adjusted to documention repo.


Updated def check_keys(keys_to_check, runbook_with_errors, runbook_name, component_name, runbook_types_cnt):
Updated def is_valid_yml(runbook_name, str_metadata):
def verify_name(key, keys_to_check, err_flag):
========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.4

Updated by: Alejandro Torres Rojas
Date: 08-Mar-2018
Developed on Python 3.6.2
Tested on Python 2.7.10 and Python 3.6.2
OS MacOS High Sierra 10.13.3
Bash version: 3.2.57(1)-release

Fixes:

    * Adapted the code to run in both versions 2.7 and 3.6 instead to maintain two separated versions.
    * Updated verify_link version to check the URL starting with http instead of containing http
    * Added the relaxed.yml file at ./script/data to use it the yamllint check
    * Updated is_valid_yml to use the relaxed.yml file on the yamllint verification
========================================================================================================================
Program: OSScheckkeys.py
Rev: 2.2.4

Updated by: Alejandro Torres Rojas
Date: 14-Mar-2018
Developed on Python 3.6.2
Tested on Python 2.7.10 and Python 3.6.2
OS MacOS High Sierra 10.13.3
Bash version: 3.2.57(1)-release

Fixes:

    * check_keys called the error_log function using the wrong sequence of parameters
      Fixed bug opened at issues #4026 by JONASTEI
'''

import argparse
import io
import json
import os
import re
import sys
import time
import codecs
import logging
import random


def exist_folder(subdir_path):
    '''
    Check if the directory exist, if does not then creates it
    :param subdir_path: subdirectory to save data
    :return: None
    '''

    if not (os.path.exists(subdir_path)):
        try:
            os.makedirs(subdir_path)
        except IOError as e:
            print("I/O error({0}): {1} {2} at {3}".format(e.errno, e.strerror, subdir_path, 'exist_folder'))
            sys.exit(1)


def clean_logs(prog_name,script_path):
    '''
    Clean the log and tmp files only keeps the last run logs

    :return: None
    '''

    for path, subdirs, files in os.walk(script_path + '/logs'):
        for name in files:
            if (prog_name in name) or (_sys_values['ouput_file_name'] in name):
                os.remove(os.path.join(path, name))




def set_logging(prog_name,script_path,arg_log_level):
    '''

    :param prog_name:   This script name
    :param script_path: This script path

    :return:            logger object
    :return             log files path
    '''


    log_path = script_path + '/logs/'
    exist_folder(log_path)
    file_name = log_path + prog_name + time.strftime("%Y%m%d-%H%M%S") + '.log'
    logger = logging.getLogger(prog_name)
    hdlr = logging.FileHandler(file_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    if arg_log_level in ['DEBUG','INFO','WARNING','ERROR']:
        log_level = arg_log_level
    else:
        log_level=_sys_values['log_level']

    if log_level == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    elif log_level == 'INFO':
        logger.setLevel(logging.INFO)
    elif  log_level == 'WARNING':
        logger.setLevel(logging.WARNING)
    else:
        logger.setLevel(logging.ERROR)
    return logger,log_path


def get_keys(type_of_runbook,logger):
    '''
     This method gets the relevant metadata 'keys' for runbook type
     For each item in _jsontypes, find a match for the 'type' and return keys
     _jsontypes is global variable loaded when load_json_data is called

    :param type_of_runbook: Runbook type (Alert/Informational/PagerDuty...)

    :return: keys to be checked if found then in the runbooks_template_keys.json file
             otherwise returns an empty list
    '''
    logger.debug('def get_keys starting\n runbook type:{0}',type_of_runbook)

    for _type in _jsontypes:
        if re.match(type_of_runbook, _type['type']):
            logger.debug('returning keys:{0}'.format(_type.keys()))
            return _type.keys()

    keys = []
    logger.debug('did not find a runbook type:{0}'.format(type_of_runbook))
    return keys


def read_runbook_metadata(reader, thisdict,logger):
    '''
    If metadata is in Runbook, it is in a  key:value format section.

    :param reader:      Runbook file to extract metadata
    :param thisdict:    a dictionary type variable when metadata (key:value) will be stored

    :return:            thisdict a dictionary with the metadata detected in the passing file,
                        also the same metadata in a string format. if not metadata found returns empty objects
    '''
    logger.debug('def read_runbook_medatada starting \n runbook:{0}'.format(reader))
    line = 0
    record = False
    count = 0
    str_metadata = ''
    for element in reader:
        logger.debug("for element in reader: element:%s"%(element))
        if record:  # Now read the key:value pairs
            logger.debug('if {0} :'.format(record))
            keyvalue = element.split(':')  # Split key: value items
            logger.debug('set keyvalue:{0}'.format(keyvalue))
            str_metadata += element # store the complete line of value pairs in this variable
            if len(keyvalue) > 1:
                logger.debug('getting key values...')
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
                            value = value[1: len(value) - 1]  # eliminate []
                            value = value.strip()
                        newvaluelist = []
                        csv = value.split(',')
                        for c in csv:
                            c = c.strip()
                            newvaluelist.append(c)
                        value = ','.join(newvaluelist)
                logger.debug('Adding key/value pair to thisdict')
                thisdict[key1] = value

        # Search for "---" - denotes start/end of yaml metadata section
        if re.match('---', element):
            logger.debug("matched element with '----'")
            count = count + 1
            if count == 1:
                thisdict['startline'] = line
                str_metadata += element
                record = True
                logger.debug('found start line at {0} set record = True'.format(line))
            if count == 2:
                thisdict['endline'] = line
                record = False
                logger.debug('found end line at {0} set record = False'.format(line))
        elif count < 2 and line > 20: # This option won't work for pager duty runbooks when they have all elements
            break
        line += 1
    logger.debug('returning metadata')
    return str_metadata[:str_metadata.rfind('---')] # removed the last --- to check only one ymal set



def log_error(keys_to_check, runbook_type, component_name, runbook_with_errors, runbooks_type_cnt, logger, msg=None):
    '''
    If an error is detected yml or value:pair this function will log the runbooks in the dictionary object
    runbook_with_errors.

    :param keys_to_check:        A value:pair defined in the runbooks_template_keys.json file to be checked
                                 with the metadata obtained from the yml runbook section.
    :param runbook_type:         Runbook type detected from the runbook metadata.
    :param component_name:       A component_name (doctor/armada/marmot/oss...) detected base on the runbook path.
    :param runbook_with_errors:  A dictionary object that contains all detected runbooks with yml or value:pair errors.
    :param runbooks_type_cnt:    A list of counters by runbook type to display total of runbook with errors by runbook type.
    :param msg:                  Optional, if a message passed it will use as error message otherwise will use the default.
                                 one from the system values object
    :return:
    '''
    logger.debug('def log_error starting \n keys_to_check[{0}]\n runbook type:{1}'.format(keys_to_check,runbook_type))
    logger.debug('component name:{0} '.format(component_name))
    keys_to_check['msg'] = (msg if msg else _sys_values['yml_failed'])
    # Removed startline and endline from the dictionary, no need to display on the output file
    keys_to_check.pop('endline')
    keys_to_check.pop('startline')
    logger.debug('revomed start and end lines from keys')
    set_counter(runbooks_type_cnt, runbook_type,logger) # increase the counter of the runbooks type to be reported as error
    if component_name not in runbook_with_errors:
        runbook_with_errors[component_name] = []
        logger.debug('Adding a new component name:component_name to runbook_with_errors'.format(component_name))
    # add the metadata with error(s) to the output object
    logger.debug('Appeding keys for component name:{0} into runbook_with_errors dictionary'.format(component_name))
    runbook_with_errors[component_name].append(keys_to_check)



def check_keys(keys_to_check, runbook_with_errors, runbook_name, component_name, runbook_types_cnt,logger):
    # This method checks if the metadata headings in the Runbook are valid.
    # This method is only run on Runbooks that have metadata incorporated in
    # the runbook. Method gets the correct metadata for a given 'type' of
    # Runbook (the default is type 'Informational'). Checks for the existence
    # of each key in the metadata headings in the Runbook.

    '''

    Updated by:     Alejandro Torres Rojas
    Date:           01-Dec-2017
    Notes:          When a runbook does not have a type: the runbook was not recorded, to be
                    displayed on the output JSON file. only the counter was added but not data
                    bug fixed.


    :param keys_to_check:         A value:pair defined in the runbooks_template_keys.json file to be checked
                                  with the metadata obtained from the yml runbook section.
    :param runbook_with_errors:   A dictionary object that contains all detected runbooks with yml or value:pair errors.
    :param runbook_name:          A runbook file name.
    :param component_name:        A component_name (doctor/armada/marmot/oss...) detected base on the runbook path.
    :param runbook_types_cnt:     A list of counters by runbook type to display total of runbook with errors by runbook type.

    :return: runbook_with_errors: A dictionary object that contains all detected runbooks with yml or value:pair errors.
             runbook_types_cnt:   A list of counters by runbook type to display total of runbook with errors by runbook type.

    '''

    logger.debug('def check_keys starting')
    compare_keys = []
    err_flag = False

    if not 'type' in keys_to_check:
        logger.debug('keys_to_check metadata does not contains a type key')
        log_error(keys_to_check, _sys_values['unknown'], component_name,runbook_with_errors, runbook_types_cnt,logger,_sys_values['no_type'])
    else:
        for _type in _jsontypes:
            if _type['type']:
                if re.search(_type['type'], keys_to_check['type']):
                    compare_keys = _type.keys()
                    logger.debug('found the template type:{0} exiting the for loop'.format(_type['type']))
                    break  # found the template 'type' exit the for

        # if the runbook type is not defined in runbooks_templete_keys.json file,
        # 'Information' runbook type will be use to compare
        if not compare_keys:
            # gets the default runbook type when type is not present in the template
            logger.debug('Using default type:{0}'.format(_sys_values['def_type']))
            compare_keys = get_keys(_sys_values['def_type'],logger)

        for k in compare_keys:
            err_flag = run_verify(k, keys_to_check, err_flag, _type['type'], runbook_name,logger)

        if err_flag:
            logger.debug('An error found after run_verify sending error to the log error file')
            log_error(keys_to_check, _type['type'], component_name, runbook_with_errors, runbook_types_cnt,logger)


def is_valid_yml(runbook_name, str_metadata,script_path,logger):
    '''
    Will extract the YML metadata section from the md file and using yamllint and two temporary files
    tmp.yml and yml_val_log will report if the metadata is in valid YML format

    Pre-requirements: yamllint must be installed in the hosting system https://yamllint.readthedocs.io/en/latest/
    if yml_os_system is set to True in the  OSScheckeys.json file will use the OS command line version otherwise
    will use the the ymal python library

    Updated by:     Alejandro Torres Rojas
    Date:           01-Dec-2017
    Date:           01-Dec-2017
    Notes:          Added the import codecs library to be able to save string using utf-8 encoding

    Updated by:     Alejandro Torres Rojas
    Date:           08-Mar-2018
    Notes:          Added a call to the yamllint if a configuration files is passed.


    :param runbook_name:    A runbook file name.
    :param str_metadata:    A string variable containing the runbook yml metadata detected in read_runbook_metadata()
    :param script_path      This script path.
    :return:                A triplet:
                                is_valid: Boolean True if YML is valid otherwise False.
                                str_err:  A string with YML error capture from yamllint log, None if mot errors.
                                str_type: A runbook type, if it exist in the metadata passed in the str_matadata,
                                          None if mot errors.
    '''

    logger.debug('def is_valid_yml starting')
    tmp_file = _sys_values['yml_tmp_file'] + time.strftime("%Y%m%d-%H%M%S") + '.yml'
    log_file = _sys_values['yml_log_file'] + time.strftime("%Y%m%d-%H%M%S") + '.log'
    cnf_yaml_file= script_path+'/data/'+_sys_values['cnf_yaml_file']
    str_err = _sys_values['yml_err']
    if os.path.exists(tmp_file): os.remove(tmp_file)
    if os.path.exists(log_file): os.remove(log_file)
    str_type = ''
    is_valid = True
    # grep -B50 "\-\-\-" $(file) | grep -vE "\b\-\-\b" > tmp.yml;
    # Nov-27-2017 this option does not work when a file name has spaces on it
    # str_cmd = 'grep -B50 "\-\-\-" %s | grep -vE "\\b\-\-\\b" > \'%s\';' % (runbook_name,tmp_file)
    # st_cmd = os.system(str_cmd)
    try:
        logger.debug('Saving metadata into a temporary file')
        with codecs.open(tmp_file, 'w',"utf-8") as f:
            f.write(str_metadata) #save the yml metadata in a temporary file to be use with yamllint
            f.close()
    except IOError as e:
        str_err="I/O error({0}): {1}".format(e.errno, e.strerror)
        print(str_err)
        logger.error(str_err)
        sys.exit(1)
    # if st_cmd == 0:
    # passed the yml using a temporary file and store the output in a the log file defined above
    if os.path.exists(cnf_yaml_file):
        logger.debug('Found {0} configuration yamllint file that will use to check YMAL metadata'.format(cnf_yaml_file))
        # Checks if a config file to be use exist, if does will be used it
        #str_cmd = 'yamllint -d %s %s>%s' % (cnf_yaml_file, tmp_file, log_file)
        #using yamllint from ubuntu 16.04 using the relaxed flag instead the relaxed.yml file 
        str_cmd = 'yamllint -d relaxed %s>%s' % (tmp_file, log_file)
    else:
        logger.debug('Checking YMAL metadata without configuration file')
        str_cmd = 'yamllint %s>%s' % (tmp_file, log_file)
    st_cmd = os.system(str_cmd) # excute the command line and captures the execution results
    if st_cmd != 0: # if the status of the command was not zero then an error occurred on the YML validation
        logger.debug('Invalid YAML metadata check the log error')
        is_valid = False
        lines = open(log_file).readlines() # gets the error information form the log file
        for line in lines:
            # replaces the temporary file name with the runbook name to report an error with the correct file name
            # and captures the complete log error to be added at the error log JSON file
            str_err += line.replace(tmp_file, runbook_name)
        lines = open(tmp_file).readlines() # get the yml metadata from the file
        for line in lines:
            # if the metadata has a runbook type it will use it to report the error otherwise will use unknown key value
            if 'type' in line.lower():
                str_type = line[line.find(':') + 1:].replace(' ', '').replace('\n', '')
                break

    # remove the temporary files
    if os.path.exists(tmp_file): os.remove(tmp_file)
    if os.path.exists(log_file): os.remove(log_file)
    logger.debug('returning is_valid[{0}] \n str_err[{1}] \n str_type[{2}]'.format(is_valid,str_err,str_type))
    return (is_valid,str_err, str_type)
    # else:
    #     print(_sys_values['grep_err'] %str_cmd)
    #     sys.exit(1)



def process(lst_runbook_name, runbook_directory,runbook_with_errors, runbook_types_cnt,not_yml_check,only_yml,script_path,logger):
    '''
    This function will read all the runbook from the /docs/runbooks directory or will use a list of runbooks passed
    using the -l parameter. If -ny or -oy is passed. -ny will not check YML and -oy will only check YML. if neither
    one passed will check both YML and value:pairs



    :param lst_runbook_name:       A List of runbooks found in the docs/runbooks directory or passed by the -l parameter.
    :parameter runbook_directory:  A current location of the runbooks, the location is defined on the JSON system file.
    :param runbook_with_errors:    A dictionary object that contains all detected runbooks with yml or value:pair errors.
    :param runbook_types_cnt:      A list of counters by runbook type to display total of runbook with errors by runbook type.
    :param not_yml_check:          If -ny option passed it will not check YML structure validation.
    :param only_yml                If -oy option passed will only check YML valid structure metadata,
                                   but not value:pair validation
    :param script_path             This script path.

    :return: runbook_with_errors:  A dictionary object that contains all detected runbooks with yml or value:pair errors.
             runbook_types_cnt:    A list of counters by runbook type to display total of runbook with errors by runbook type.

    '''
    logger.debug('def process starting')
    valid_yaml = True
    yaml_err =''
    str_type=''
    lst_all_components = next(os.walk(runbook_directory))[1]  # Get all parent component names
    print ("Analyzing runbooks metadata, please wait ...")
    for runbook_name in lst_runbook_name:
        logger.debug('Processing runbook[{0}]'.format(runbook_name))

        runbook_dir = os.path.dirname(runbook_name)

        component_name = os.path.split(runbook_dir)[1]

        if all([xclude_dir not in component_name for xclude_dir in _sys_values['dir_2_exclude']]):
            with io.open(runbook_name, 'r', encoding="utf-8") as infile:
                reader = infile.readlines()
            infile.close()

            # Get always the parent component name of a runbook
            component_name = get_component(lst_all_components, component_name, runbook_name)
            logger.debug('runbook component_name[{0}]'.format(component_name))

            yamllist = {}

            str_metadata = read_runbook_metadata(reader, yamllist,logger)  # Get metadata of current Runbook
            if not not_yml_check:
                (valid_yaml, yaml_err, str_type) = is_valid_yml(runbook_name, str_metadata,script_path,logger)
            if valid_yaml:
                if not only_yml: #check the flag set from the command line
                    if not yamllist:
                        yamllist['file_name'] = runbook_name
                        yamllist['msg'] = _sys_values['no_yml']
                        if component_name not in runbook_with_errors: runbook_with_errors[component_name] = []
                        runbook_with_errors[component_name].append(yamllist)
                        set_counter(runbook_types_cnt, _sys_values['unknown'])
                    elif yamllist:
                        yamllist['file_name'] = runbook_name
                        # hecks if the metadata in the runbook is valid:
                        check_keys(yamllist, runbook_with_errors, runbook_name, component_name, runbook_types_cnt,logger)
            else:  # Did not pass the yml verification
                yamllist = {}
                yamllist['file_name'] = runbook_name
                yamllist['msg'] = yaml_err
                if component_name not in runbook_with_errors: runbook_with_errors[component_name] = []
                runbook_with_errors[component_name].append(yamllist)
                set_counter(runbook_types_cnt, (str_type if str_type else _sys_values['unknown']),logger)


def set_counter(runbook_types_cnt, _type,logger):
    '''
    Update the counter of runbooks with bad metadata by type to report at the end of the validation checking.

    :param runbook_types_cnt:  A list of counters by runbook type to display total of runbook with errors by runbook type.
    :param type:               A runbook type with error if the metadata has a runbook type it will use it to report
                               the the runbook type, otherwise will use unknown key value
    :return:
           runbook_types_cnt:  A slist of counters by runbook type to display total of runbook with errors by runbook type.
    '''
    logger.debug('def set_counter :params runbook_types_cnt[{0}] _type[{1}]'.format(runbook_types_cnt,_type))
    if _type in runbook_types_cnt:
        logger.debug('def set_counter type is in runbook_types_cnt ')
        counter_val = runbook_types_cnt[_type]
        runbook_types_cnt[_type] = counter_val + 1
    else:
        logger.debug('adding new a new type[{0}]'.format(_type))
        runbook_types_cnt[_type] = 1


def show_results(runbook_with_errors, runbook_types_cnt,log_path,logger):
    '''
    Report the runbooks that did not meet the YML and value:pair validations.

    Updated by:     Alejandro Torres Rojas
    Date:           21-Nov-2017
    Notes:          Name changed from printerrormessage to show_results.

    :param runbook_with_errors  A list of runbooks to be reviewed
    :param runbook_types_cnt    A list a runbooks to be review by type
    :param log_path             Logger path folder
    :return: None
    '''
    logger.debug('def show_results :params runbook_with_errors[dict] runbook_types_cnt[{1}]',runbook_types_cnt)
    str_msg = ''
    file_name = log_path+'/'+_sys_values['ouput_file_name'] + time.strftime("%Y%m%d-%H%M%S") + '.json'
    print(_sys_values['results_msg'])
    print(json.dumps(runbook_with_errors, indent=3))
    # Create am output file in a JSON  format to report errors
    try:
        with open(file_name, 'w') as f:
            f.write(json.dumps(runbook_with_errors, indent=3))
            f.close()
    except IOError as e:
        str_err="I/O error({0}): {1}".format(e.errno, e.strerror)
        logger.error(str_err)
        print (str_err)
        sys.exit(1)
    # Print out the total number of runbooks with error(s) by runbook type
    logger.info('Print out the total number of runbooks with error(s) by runbook type')
    for key in runbook_types_cnt:
        str_msg += _sys_values['counter_msg'] % (key, runbook_types_cnt[key])
    logger.info(str_msg)
    print(str_msg)


def yes_no(answer):
    '''
    Verify a user enter a valid (Y)es/(N)o response.

    :param answer:    A custom message to be prompted.

    :return:          A Boolean True, If a correct answer is selected, otherwise False.
    '''
    yes = set(['yes', 'y', 'ye', ''])
    no = set(['no', 'n'])

    while True:
        choice = raw_input(answer).lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print(_sys_vales['yes_no_msg'])


def check_file_loc(script_path, file_name,logger):
    '''
    If the file name only contains the name, the full path will be added to it.

    :param script_path:     A full path for the runbook location.
    :param file_name:       A runbook name.

    :return:    file name with a full path.
    '''
    logger.debug('def check_file_loc params: script_path[{0}] file_name[{1}'.format(script_path,file_name))
    f_name = os.path.basename(file_name)
    if script_path not in file_name:
        file_name = script_path + '/data/' + f_name
        logger.debug('Sets file_name to: {0}'.format(file_name) )

    return file_name


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
                err_msg='!Fatal Error!: {0} is not a valid JSON file, expecting a JSON file, system error: {1}'.format(f_name,e)
                print(err_msg)
                sys.exit(1)
    except EnvironmentError:
        err_msg="!Fatal Error!: {0} does not exist, make sure the json file is located in the same directory of this script {1}".format(f_name,__file__)
        print(err_msg)
        sys.exit(1)


def get_system_values(script_path):
    '''
    Gets the metadata use to run this script from a JSON format file defined the a user.

    Updated by:     Alejandro Torres Rojas
    Date:           21-Nov-2017
    Notes:          Replaced the open file sentence by is_valid_json_file to add more validations

    :parameter script_path      A location of this script.

    :return:    _sys_values     All metadata info defined by a user loaded into a global dictionary object.
    '''

    global _sys_values
    f_name = os.path.basename( __file__).replace('.py', '.json')
    f_name = script_path+'/data/'+f_name
    _sys_values = is_valid_json_file(f_name)
    return _sys_values


def load_json_data(dflts_rplcmnt, xmpl_mtdt, template_keys,logger):
    '''
    Load the JSON templates passed on the command line, they are use to review runbooks key:value pairs and custom messages
    upload the JSON files into global variable to be accessible for all methods

    Updated by:     Alejandro Torres Rojas
    Date:           21-Nov-2017
    Notes:          Name changed from loadJSONData to load_json_data.
                    Replaced the open file sentence by is_valid_json_file to add more validations

    Parameters
    ----------
    dflts_rplcmnt:       defaults_replacement.json.
    xmpl_mtdt:           example_metadata.json.
    template_keys:       runbooks_template_keys.json.


    Returns
    -------
    All metadata loaded into a global dictionary objects to be accessible for all methods.

    '''
    logger.debug('def load_json_dat params dflts_rplcmnt[{0}] xmpl_mtdt[{1}] template_keys{2}'.format(dflts_rplcmnt,xmpl_mtdt,template_keys))
    global _example_metadata
    global _defaults_replacement
    global _jsontypes

    logger.info('Loadding JSON runbooks template keys file into memory')
    _jsontypes = is_valid_json_file(template_keys)
    logger.info('Loadding JSON example metadata template file into memory')
    _example_metadata = is_valid_json_file(xmpl_mtdt)
    logger.info('Loadding JSON default metadata template file into memory')
    _defaults_replacement = is_valid_json_file(dflts_rplcmnt)



def verify_link(key, keys_to_check, runbook_name, err_flag,logger):
    '''
    Check Line contains the runbook link.

    Updated by:     Alejandro Torres Rojas
    Date:           29-Nov-2017
    Notes:          If a link contains http in it, it will flag a runbook with error.

    Updated by:     Alejandro Torres Rojas
    Date:           30-Nov-2017
    Notes:          When looking for runbook name be part of the link, both are converted to lower case to match them

    Updated by:     Alejandro Torres Rojas
    Date:           1-Dec-2017
    Notes:          Changed the message when a runbook name is not part of the link, to be more specific to users.

    Updated by:     Alejandro Torres Rojas
    Date:           6-Mar-2018
    Notes:          Changed elif 'http' in value.lower(): by  elif value.lower().startswith('http') only checks if
                    the URL starts with http instead of contains. Bug reported by Irma Sheriff.

    Parameters
    ----------
    key:            The key value from rumbooks template. (link)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.
    runbook_name:   Runbook name passed to the verify_link only.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''



    logger.debug('def verify_link starting')
    value = keys_to_check[key].replace('"', '')
    filename = os.path.basename(runbook_name).replace(".md", ".html")

    if not value:
        logger.debug('Value is null')
        keys_to_check[key] = _sys_values['missing'] + _defaults_replacement[key]
        err_flag = (err_flag or True)
    elif filename.lower() not in value.lower():
        str_err=_defaults_replacement[key] % 'expecting '+ filename + ' instead of ' + value
        keys_to_check[key] = str_err
        logger.info(str_err)
        err_flag = (err_flag or True)
    # elif 'http' in value.lower():
    elif value.lower().startswith('http'):
        str_err=_sys_values['http_in_link'] % value
        keys_to_check[key] = str_err
        logger.info(str_err)
        err_flag = (err_flag or True)
    else:
        logger.debug('Setting key:{0} with {1}'.format(key,value))
        keys_to_check[key] = value

    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_title(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook title.

    Parameters
    ----------
    key:            The key value from rumbooks template. (title)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    logger.debug('def verify_title stating')
    value = keys_to_check[key].replace('"', '')
    if not value:
        str_msg=_sys_values['missing'] + _defaults_replacement[key]
        logger.info(str_msg)
        keys_to_check[key] = str_msg
        err_flag = (err_flag or True)
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_service(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook related services.

    Updated by:     Alejandro Torres Rojas
    Date:           30-Nov-2017
    Notes:          Added a new entry to the default_replacement,json file for service-related key.
                    Use the first entry for the list of values set.


    Parameters
    ----------
    key:            The key value from rumbooks template. (service)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    logger.debug('def verify_service starting')
    value = keys_to_check[key].replace('"', '')

    if not value:
        str_msg=_sys_values['missing'] +_defaults_replacement[key][0] # Will return only the first element of the list
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif all([default_service in value for default_service
              in _defaults_replacement[key]] or not value):
        keys_to_check[key] = _defaults_replacement[key]
        err_flag = (err_flag or False)
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_description(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook description.

    Parameters
    ----------
    key:            The key value from rumbooks template. (description)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    logger.debug('def verify_description stating')
    value = keys_to_check[key].replace('"', '')
    if not value:
        str_msg= _sys_values['missing'] + _example_metadata[key]
        keys_to_check[key] =str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif all([default_description in value for default_description
              in _defaults_replacement[key]]):
        keys_to_check[key] = _example_metadata[key]
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_name(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook name.

    Parameters
    ----------
    key:            The key value from rumbooks template. (name)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Updated by:     Alejandro Torres Rojas
    Date:           01-Dec-2017
    Notes:          Corrected a type error form ['missing'] to  _sys_values['missing']



    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    logger.debug('def verify_name starting')
    value = keys_to_check[key].replace('"', '')
    if not value:
        str_msg=_sys_values['missing'] + _defaults_replacement[key]
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif _defaults_replacement[key] in value:
        keys_to_check[key] = _example_metadata[key]
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_layout(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook layout.

    Updated by:     Alejandro Torres Rojas
    Date:           29-Nov-2017
    Notes:          Added additional verification. Will check that the layout passed is one of the files listed
                    under the _layout directory, if not will flag the runbook with an error.

    Parameters
    ----------
    key:            The key value from rumbooks template. (layout)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    logger.debug('def verify_layout starting')
    value = keys_to_check[key].replace('"', '')
    lst_layouts= get_layouts() # Get a list of the valid layouts use to build the html files using Jekyll
    if not value:
        keys_to_check[key] = _sys_values['missing']
        logger.info(_sys_values['missing'])
        err_flag = (err_flag or True)
    elif _defaults_replacement[key] in value or not value:
        keys_to_check[key] = _example_metadata[key]
        err_flag = (err_flag or True)
    # Compares the layput passed,line,  with the existing ones
    elif next((layout_item for layout_item in lst_layouts if value+'.html' in layout_item), None):
        keys_to_check[key] = value
    else:
        keys_to_check[key] = _sys_values['invalid_layout']%value
        err_flag = (err_flag or True)
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_playbooks(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook playbooks.

    Parameters
    ----------
    key:            The key value from rumbooks template. (pklaybooks)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''
    logger.debug('def verify_playbooks starting')
    value = keys_to_check[key].replace('"', '')

    if not value:
        str_msg=_sys_values['missing'] + _defaults_replacement[key][0]
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif all([default_service in value for default_service
              in _defaults_replacement[key]]):
        # Verify playbooks is a list
        keys_to_check[key] = _example_metadata[key]
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_tags(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook tags.

    Parameters
    ----------
    key:            The key value from rumbooks template. (tags)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''
    logger.debug('def verify_tags starting')
    value = keys_to_check[key].replace('"', '')

    if not value:
        str_msg=_sys_values['missing'] + _defaults_replacement[key]
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif _defaults_replacement[key] in value:
        keys_to_check[key] = "REPLACE " + _defaults_replacement[key] + " WITH VALID VALUES"
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_type(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook type

    Parameters
    ----------
    key:            The key value from rumbooks template. (type)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''
    logger.debug('def verify_type starting')
    value = keys_to_check[key].replace('"', '')

    if not value:
        str_msg=_sys_values['missing'] + _defaults_replacement[key]
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif _defaults_replacement['type'] in value:
        keys_to_check[key] = _defaults_replacement[key]
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def verify_failure(key, keys_to_check, err_flag,logger):
    '''Check Line contains the runbook failures

    Parameters
    ----------
    key:            The key value from rumbooks template. (failure)
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       Flag carrying is a missing data is found in runbook.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.
    '''

    # Verfiy there are no default values in file

    logger.debug('def verify_failure starting')
    value = keys_to_check[key].replace('"', '')

    if not value:
        str_msg=_sys_values['missing'] + _example_metadata[key]
        keys_to_check[key] = str_msg
        logger.info(str_msg)
        err_flag = (err_flag or True)
    elif all([default_failure in value for default_failure
              in _defaults_replacement[key]]):
        keys_to_check[key] = _example_metadata[key]
        err_flag = (err_flag or True)
    else:
        keys_to_check[key] = value
    logger.debug('returning:{0}'.format(err_flag))
    return err_flag


def run_verify(key, keys_to_check, err_flag, type, runbook_name,logger):
    '''Map the metadata key words to the verify functions

    Updated by:     Alejandro Torres Rojas
    Date:           30-Nov-2017
    Notes:          Added service and service-related to be checked using verify_service function


    Parameters
    ----------
    key:            The key value from rumbooks template such as link,type, description ...
    keys_to_check:  Metadata extracted from the runbook to be checked.
    err_flag:       True if at least one error was detected otherwise stays False.
    type:           Runbook type detected Informational,Troubleshooting, PagerDuty ...
    runbook_name:   Runbook name use only in verify_link function.

    Returns
    -------
    err_flag:       True if at least one error was detected otherwise stays False.

    '''
    logger.debug('def run_verify stating')
    if key not in keys_to_check.keys():
        str_err= "MISSING <key:value> PAIR: <{0}> IS MANDATORY FOR '{1}' RUNBOOKS".format(key,type)
        keys_to_check[key] = str_err
        logger.debug("returning {0}".format(str_err))
        return (err_flag or True)
    else:
        if key == 'link':
            return verify_link(key, keys_to_check, runbook_name, err_flag,logger)
        elif key == 'failure':
            return verify_failure(key, keys_to_check, err_flag,logger)
        elif key in ['related-service','service']:
            return verify_service(key, keys_to_check, err_flag,logger)
        elif key == 'type':
            return verify_type(key, keys_to_check, err_flag,logger)
        elif key == 'description':
            return verify_description(key, keys_to_check, err_flag,logger)
        elif key == 'runbook-name':
            return verify_name(key, keys_to_check, err_flag,logger)
        elif key == 'layout':
            return verify_layout(key, keys_to_check, err_flag,logger)
        elif key == 'playbooks':
            return verify_playbooks(key, keys_to_check, err_flag,logger)
        elif key == 'tags':
            return verify_tags(key, keys_to_check, err_flag,logger)
        elif key == 'title':
            return verify_title(key, keys_to_check, err_flag,logger)
    return err_flag


def get_runbooks(runbook_directory, list_of_files=None):
    '''get_runbooks

    Scrap the runbook directory and return all files with the .md extension.
    Updated by:     Alejandro Torres Rojas
    Date:           21-Nov-2017
    Notes:          Modified logic and code to be able to habdle a list of runbooks paased by the command line.

    Parameters
    ----------
    runbook_directory:      The location of the runbooks, the main location is set at the system values JSON file.
    list_of_files:          Optional, a list of files to test if empty will scan the whole runbooks directory.

    Returns
    -------
    List:                   A list of runbook file names.
    '''

    temp_runbooks = []
    for path, subdirs, files in os.walk(runbook_directory):
        for name in files:
            if name.endswith(".md") and (name.lower() not in _sys_values['file_2_exclude']):
                if not list_of_files:
                    temp_runbooks.append(os.path.join(path, name))
                else:
                    if next((s for s in list_of_files if name in s), None):
                        temp_runbooks.append(os.path.join(path, name))
    return temp_runbooks


def get_component(lst_all_components, component_name, runbook_full_path):
    '''
    Checks if the component_name passed is a root component, if it is, it should be listed in lst_all_components
    otherwise it is a child component, if it is a child component, returns their parent.


    :param lst_all_components:  Contains all the parent components form the docs/runbooks directory.
    :param component_name:      The component name of a runbook it could be a parent or a child.
    :param crunbook_full_path:  Runbook's full path to detect a parent of a child component.
    :return:                    A parent component name
    '''

    if component_name not in lst_all_components:
        for component in lst_all_components:
            if component in runbook_full_path:
                component_name = component
                break
    return component_name

def get_layouts():
    '''
    Get the list of the current layout under /_layouts directory.

    :return: A list of valid file name of layouts
    '''

    lst_layouts=[]
    script_path =  os.path.dirname(os.path.realpath(__file__))

    if os.path.exists(script_path+'/../_layouts'):
        lst_layouts =next(os.walk(script_path+'/../_layouts'))[2] # get the file names form the _layouts directory
    else:
        print(_sys_values['no_layout_dir'])
        sys.exit(1)
    return lst_layouts



def main():
    '''
    Added argparse class parser to create the input data more generic and provide more help to the end user
    also take advantage of the parser to read a list of vales
    Updated by: Alejandro Torres Rojas
    Date:       21-Nov-2107
    '''
    program = os.path.basename(sys.argv[0])
    script_path = os.path.dirname(os.path.realpath(__file__))
    _sys_values = get_system_values(script_path) #Loads the system variable into a global dictionary object

    #This script can use with or without user interaction. If no_argv_check is set to True means no user interaction
    if _sys_values['no_argv_check'] == 'False':
        resp = ''
        if len(sys.argv) == 1:
            print(_sys_values['no_argv'] % (_sys_values['runbook_loc'], program))
            if not yes_no(resp): sys.exit(0)

    #Sets the argparse object with the parameter the script will accept as valid parameters
    strPrgUse = program + " -t runbooks_template_keys.json -d default_replacement.json -e example_metadata.json -l [runbook1,runbook2..] <options>"

    if str(sys.version_info[0]) == '3':  # when using Pyhton 3
        iArgv = argparse.ArgumentParser(prog=program, usage=strPrgUse,
                                         description=_sys_values['description'])
        iArgv.add_argument('-v','--version', action='version', version='%(prog)s ' + _sys_values['version'])
    else:
        iArgv = argparse.ArgumentParser(prog=program, usage=strPrgUse,
                                        description=_sys_values['description'], version='%(prog)s ' + _sys_values['version'])
    iArgv.add_argument('-d', '--default_replacement', '--D', action='store', dest='default',
                       default=_sys_values['default'],help=_sys_values['hlp_default'])
    iArgv.add_argument('-t', '--template_keys', '--T', action='store', dest='template', default=_sys_values['template'],
                       help=_sys_values['hlp_template'])
    iArgv.add_argument('-e', '--example_metadata', '--E', action='store', dest='example',
                       default=_sys_values['example'],help=_sys_values['hlp_example'])
    iArgv.add_argument('-l', '--list_runbooks', '--L', nargs='+', dest='runbooks_lst', default=[],
                       help=_sys_values['hlp_lst'])
    iArgv.add_argument('-ny', '--no_YML_validation', '-NY', action="store_true", default=False, dest='not_yml',
                       help=_sys_values['hlp_not_yml_check'])
    iArgv.add_argument('-oy', '--only_YML_on_metadata', '--OY', action="store_true", default=False, dest='only_yml',
                       help=_sys_values['hlp_only_yml_check'])
    iArgv.add_argument('-ll', '--log_level', '--LL', action='store', default=_sys_values['log_level'], dest='log_level',
                       help=_sys_values['hlp_verbose'])


    argv_passed = iArgv.parse_args()
    clean_logs(program.replace('.py','_'), script_path,)
    logger,log_path=set_logging(program.replace('.py','_'),script_path,argv_passed.log_level)
    template_keys = check_file_loc(script_path, argv_passed.template,logger)
    dflts_rplcmnt = check_file_loc(script_path, argv_passed.default,logger)
    xmpl_mtdt = check_file_loc(script_path, argv_passed.example,logger)
    lst_runbooks = argv_passed.runbooks_lst


    # If only_yml and not_yml options are passed then both will be excluded, they are mutually exclusives
    if argv_passed.only_yml and argv_passed.not_yml:
        argv_passed.only_yml = False
        argv_passed.not_yml = False


    try:
        runbook_with_errors = {}
        runbook_types_cnt = {}
        load_json_data(dflts_rplcmnt, xmpl_mtdt, template_keys,logger)
        runbook_directory = script_path + _sys_values['runbook_loc']
        process(get_runbooks(runbook_directory, lst_runbooks), runbook_directory,runbook_with_errors,
                runbook_types_cnt,argv_passed.not_yml,argv_passed.only_yml,script_path,logger)
        if runbook_with_errors:
            logger.info('Found an error in one or more runbooks')
            show_results(runbook_with_errors, runbook_types_cnt,log_path,logger)
            sys.exit(1)
        else:
            logger.info(_sys_values['completed_wo_errors'])
            print(_sys_values['completed_wo_errors'])
            sys.exit(0)
    except EnvironmentError:
        print("def main().Error accessing file passed as an argument")
        logger.error('def main(). Error accessing file passed as an argument')
        sys.exit(1)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
import argparse
import ast
import copy
import json
import os
import sys
import os.path
import yaml
import time
import io
import re
'''
      _                            ____                                        _
     | |  ___    ___    _ __      / ___|   ___   _ __     ___   _ __    __ _  | |_    ___    _ __
  _  | | / __|  / _ \  | '_ \    | |  _   / _ \ | '_ \   / _ \ | '__|  / _` | | __|  / _ \  | '__|
 | |_| | \__ \ | (_) | | | | |   | |_| | |  __/ | | | | |  __/ | |    | (_| | | |_  | (_) | | |
  \___/  |___/  \___/  |_| |_|    \____|  \___| |_| |_|  \___| |_|     \__,_|  \__|  \___/  |_|


Use Case:
---------
There are a few files for the runbooks that need to be udated as part of a submission or a change of a runbook.
They are:
    - assets/json/runbook-list.json
    - assets/json/troubleshooting.json
New users adding to runbooks don't understand why they need to add to these files and when they do
many people run into merge conflicts with them.

This tool will generate these files for the metadata specified at the top of the runbooks.

It also creates the doctor file that keeps track of what files have default values in the metadata
or are missing values. The file is located here:
    - assets/json/doctor.json

Example Uses:
-------------

# Generate assets/json/runbook-list.json file from the runbooks metadata
python script/RunbookJsonGenerator.py --runbooks

# Generate assets/json/troubleshooting.json file from the runbooks metadata
python script/RunbookJsonGenerator.py --troubleshoot

# Generate all possible files from the runbooks metadata
python script/RunbookJsonGenerator.py --all

# Return all runbooks that are missing metadata or using default values
python script/RunbookJsonGenerator.py --missing

# Return all metadata for specific runbooks that are missing metadata
# or using default values
python script/RunbookJsonGenerator.py --verify_missing "/container_groups_502.html,/ELK_logstash_forwarder.html"

# Show the help text for this script
python script/RunbookJsonGenerator.py --help

================================================================================================================
Program: OSSRunbookJsonGenerator.py
Rev: 1.0.0
Updated by: Alejandro Torres Rojas
Date: 16-Nov-2017
Developed on Python 2.7
Tested on Python 2.7



Sample program call:
# Generate assets/json/runbook-list.json file from the runbooks metadata
python script/OSSRunbookJsonGenerator.py --runbooks

Added _get_component(self,lst_all_components,component_name,runbook_full_path):

Checks if the component_name passed is root component, if it is, it should be listed in lst_all_components
otherwise it is a child component, if it is a child component, returns their parent.


        :param lst_all_components:  Contains all the parent components form the docs/runbooks directory
        :param component_name:      The component name of a runbook it could be a parent or a child
        :param runbook_full_path:  runbook's full path to detect the parent of a child component
        :return:                    parent component name

This enhancement will allow to generate one JSON file like assets/json/armada-runbook-list.json for an aramadad file
structure like the follow:

--docs
-----runbooks
--------armada
----------api
----------cluster
------------etcd

================================================================================================================
Program: OSSRunbookJsonGenerator.py
Rev: 2.0.3
Updated by: Alejandro Torres Rojas
Date: 19-Feb-2018
Developed on Python 3.6.2
Tested on Python 2.7.10 and Python 3.6.2
OS MacOS High Sierra 10.13.3
Bash version: 3.2.57(1)-release

Fixes:

OSSRunbookJsonGenerator.py is not displaying the full description https://github.ibm.com/cloud-sre/ToolsPlatform/issues/3670
Originally the program was considering only one line by tag when a tag had multi-lines only the first line was use to be
displayed on the JSON file.

Using a YAML parser all metadata is capture and analyzed, instead of only one line.

Additionally, listed the fixes and enhancementes added:

*   The program was scanning all files including the ones excluded by the OSScheckkeys.py.
    Added the same exclusion used on OSSCheckkeys.py.  The new logic excludes subdirectories listed at 'dir_2_exclude' under the script/data/OSSRunbookJsonGenerator.json file.
*   Detects if a runbook contains a YML metadata, if does not, then, it is reported in an error file created at
    the new logs folder.
*   All readme.md files were exclude using the same logic as OSScheckkeys.py does.
*   Validate the YML medatada before to process it.
*   Validates the JSON file use for the configuration data
*   Use the runbook_template metadata to validate keys by runbook type instead to have them hard code
*   A new logs directory was created, and a log file will be created in case of warning and/or errors found in the runbooks. The log file will provide
    the runbooks name and extra information for the users review.
*   Remove as much as possible hard code values.
*   Cleanup code and removing redundancy.
*   Change 'service' by 'related-service' for runbook that use 'service' instead 'related-service', such as armada. The OSS portal expects
    'related-service' for the runbooks list.


'''
class RunbookJsonGenerator(object):

    def __init__(self):
        # Path of this script
       # self.script_path = os.path.dirname(os.path.realpath(__file__))

        # Make all paths relative to the location of this script so it can be called from anywhere

        self._script_path = os.path.dirname(os.path.realpath(__file__))
        self._sys_values = self._get_system_values(self._script_path)  # Loads the system variable into a global dictionary object

        self._prg_version = _sys_values['version']
        self.runbook_directory      = self._script_path + self._sys_values['runbook_path']
        self.runbook_list_path      = self._script_path + self._sys_values['runbook_list_path']
        self.troubleshoot_file_path = self._script_path + self._sys_values['troubleshoot_file_path']
        self._runbook_madatory_values = self._sys_values['runbook_mandatory_values']

        self.template_keys = self._check_file_loc(self._sys_values['runbook_template'])
        self.runbook_template_keys = self._is_valid_json_file(self.template_keys)
        self.finished_with_errors = self._sys_values['completed_with_errors']
        self.finished_success= self._sys_values['completed_wo_errors']
        self.files_to_exlude= self._sys_values['file_2_exclude']
        self.dirs_to_exclude= self._sys_values['dir_2_exclude']
        self.metadata_error_flag = self._sys_values['metadata_error_flag']
        self.metadata_warning_flag=self._sys_values['metadata_warning_flag']
        self.missing_data_flag=self._sys_values['missing_data_flag']
        self.set_default_value=self._sys_values['set_default_value']

        # Base link for all runbook references in the below files:
        #    - assets/json/runbook-list.json
        #    - assets/json/troubleshooting.json
        self.runbook_sub_link  = self._sys_values['runbook_sub_link']

        # The default replacement text for 'failure' is not a valid list so se need to replace it
        # with a valid list before its loaded in
        self.invalid_failure_string = self._sys_values['invalid_failure_string']
        self.failure_replacement    = self._sys_values['failure_replacement']

        self.defaults_replacement = {
            'description': ['<replace with description>', 'Need to update Description',
                            'Runbook needs to be updated with description'],
            'runbook-name': '<replace with runbook-name. Surround with inverted commas>',
            'link': '<link to Runbook - replace .md with .html>',
            'type': 'Unknown',
            'related-service': ['<replace with service, e.g. Containers>',
                                'Runbook needs to be updated with service'],
            'failure': [self.invalid_failure_string,
                        'Runbook needs to be Updated with failure info (if applicable)'],
            'playbooks': ['[Runbook needs to be Updated with playbooks info (if applicable)]',
                          '[Runbook needs to be updated with playbooks]',
                          ('[<add Ansible-playbook command to automate Runbook. Separate each Playbook '
                           'with a comma and surround with inverted commas>]'),
                          '<NoPlayBooksSpecified>'],
            'tags': 'None',
            'title': 'Unknown',
            'layout': 'Unknown',
            'ownership-details': ['[<NoOwnershipSpecified>]']
        }


        self.example_metadata = self._sys_values['example_metadata']

    def main(self):
        '''main

        Tool to generate runbook and troubleshooting json files.

        Currently every runbook added or changed needs to edit 2 json files:
          - assets/json/runbook-list.json
          - assets/json/troubleshooting.json

        These files are continually out of date. With this tool it will strip out all the
        metadata information out of the runbooks and generate the 2 files on the fly.

        NOTE: This tool is meant to run from the base directory of the documentation-pages
        project

        Parameters
        ----------
        runbooks: (optional) Flag to generate runbook-list.json file
        troubleshoot: (optional) Flag to generate troubleshooting.json file

        Returns
        -------
        None: writes the 2 files specified above in assets/json
        '''
        # program = os.path.basename(sys.argv[0])
        # script_path = os.path.dirname(os.path.realpath(__file__))
        # _sys_values = self._get_system_values(script_path)  # Loads the system variable into a global dictionary object
        # _sys_values['script_path']=script_path


        # Sets the argparse object with the parameter the script will accept as valid parameters
        program_name = os.path.basename(sys.argv[0])
        strPrgUse = "You must call {0} with one of the specified options.\n Use --help for usage.".format(program_name)



        if str(sys.version_info[0]) =='3': # when using Pyhton 3
            parser = argparse.ArgumentParser(prog=program_name, usage=strPrgUse,
                                             description=' '.join(self._sys_values['program_description']))
            parser.add_argument('--version', action='version',version='%(prog)s ' + self._prg_version)
        else:
            parser = argparse.ArgumentParser(prog=program_name, usage=strPrgUse,
                                            description=' '.join(self._sys_values['description']), version=self._prg_version)


        parser.add_argument('--runbooks',  action='store_true',help=self._sys_values['hlp_runbooks'])
        parser.add_argument('--troubleshoot',  action='store_true',help=self._sys_values['hlp_troubleshoot'])
        parser.add_argument('--all',  action='store_true',help=self._sys_values['hlp_all'])
        parser.add_argument('--missing',  action='store_true',help= self._sys_values['hlp_missing'] % (', '.join(self.defaults_replacement.keys())))
        parser.add_argument('--verify_missing', type=str,help=self._sys_values['hlp_verify_missing'])

        # Verify all arguments are valid
        args = parser.parse_args()


        if (len(sys.argv) > 1):

            if args.all:
                self.generate_runnbook()
                self.generate_troubleshooting()
                return
            elif args.runbooks:
                self.generate_runnbook()
                return
            elif args.troubleshoot:
                self.generate_troubleshooting()
                return
            elif args.missing:
                self.generate_missing()
                return
            elif args.verify_missing:
                self.generate_missing(specific_missing_runbooks=args.verify_missing)
                return
        else:
            parser.print_help()




    def _check_file_loc(self,file_name):
        '''
        If the file name only contains the name, the full path will be added to it.

        :param script_path:     A full path for the runbook location.
        :param file_name:       A runbook name.

        :return:    file name with a full path.

        '''

        script_path = os.path.dirname(os.path.realpath(__file__))
        f_name = os.path.basename(file_name)
        if script_path not in file_name:
            file_name = script_path + '/data/' + f_name

        return file_name

    def _is_valid_json_file(self,f_name):
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
                        "!Fatal Error!: {0} is not a valid JSON file, expecting a JSON file, system error: {1} at {2}".format(f_name,e,'_is_valid_json_file'))
                    sys.exit(1)
        except EnvironmentError:
            print(
                "!Fatal Error!: {0} does not exist, make sure the json file is located in the same directory of this script {1} at {2}".format(f_name, __file__,'_is_valid_json_file'))
            sys.exit(1)


    def _get_system_values(self,script_path):
        '''
        Gets the metadata use to run this script from a JSON format file defined the a user.

        Updated by:     Alejandro Torres Rojas
        Date:           19-Feb-2018
        Notes:          Replaced the open file sentence by is_valid_json_file to add more validations

        :parameter script_path      A location of this script.

        :return:    _sys_values     All metadata info defined by a user loaded into a global dictionary object.
        '''

        global _sys_values
        f_name = os.path.basename(__file__).replace('.py', '.json')
        f_name = script_path + '/data/' + f_name
        _sys_values = self._is_valid_json_file(f_name)
        return _sys_values

    def generate_runnbook(self):
        '''generate_runnbook

        Generate runbook file and replace the existing one

        Parameters
        ----------
        None

        Returns
        -------
        None: writes the file
        '''


        metadata,err_log = self.get_metadata(self.get_runbooks(), self._runbook_madatory_values
                                             ,self.runbook_template_keys)
        self.replace_file_contents(self.runbook_list_path, metadata,err_log)

    def generate_missing(self, specific_missing_runbooks=None):
        '''generate_missing

        Prints list of runbooks that are missing attributes

        Parameters
        ----------
        specific_missing_runbooks: comma seperated list of runbooks to return
        the missing values for

        Returns
        -------
        Prints list of dictionaries container runbook metadata
        '''

        def _filter_runbook_type(temp_metadata, sort_type, missing_types=False):
            '''Sort a certain 'type' out of metadata'''

            temp_meta = []
            for runbook_meta in temp_metadata:
                if 'type' in runbook_meta:
                    for temp_type in sort_type:
                        if not missing_types and runbook_meta['type'] in temp_type:
                            temp_meta.append(copy.deepcopy(runbook_meta))
                            break
                        elif missing_types and runbook_meta['type'] not in sort_type:
                            temp_meta.append(copy.deepcopy(runbook_meta))
                            break

            return temp_meta

        # Runbooks we are showing missing data for

        # runbook_types = ['Informational', 'PagerDuty', 'Troubleshooting', 'Operations', 'Configuration',
        #                  'Deployment', 'API', 'Recovery', 'Test']
        # Using the types defined om the runbooks_template_keys.json
        runbook_types = sorted([metadata['type'] for metadata in self.runbook_template_keys])

        # Find values that are missing in informational runbooks
        if 'Informational' in self.runbook_template_keys:
            informational_values = [m.keys() for m in self.runbook_template_keys if m['type'] == 'Informational']
        else:
            informational_values = self._sys_values['default_informational_values']

        if 'PagerDuty' in self.runbook_template_keys:
            pd_and_troubleshoot_recovery_values = [m.keys() for m in self.runbook_template_keys if m['type'] == 'PagerDuty']
        else:
            pd_and_troubleshoot_recovery_values = self._sys_values['default_pd_and_troubleshoot_recovery_values']

        if 'Troubleshooting' in self.runbook_template_keys:
            troubleshooting = [m.keys() for m in self.runbook_template_keys if m['type'] == 'Troubleshooting']
        else:
            troubleshooting = self._sys_values['default_troubleshooting']

        if 'API' in self.runbook_template_keys:
            ops_api_test_deploy_conf_values = [m.keys() for m in self.runbook_template_keys if m['type'] == 'API']
        else:
            ops_api_test_deploy_conf_values = self._sys_values['default_ops_api_test_deploy_conf_values']

        if 'Alert' in self.runbook_template_keys:
            alert_values = [m.keys() for m in self.runbook_template_keys if m['type'] == 'Alert']
        else:
            alert_values = self._sys_values['default_alert_values']

        self.overview_string  = ''
        missing_runbook_info  = []
        self.runbook_criteria = self._sys_values['runbook_criteria_msg']

        def get_missing_runbook_info(local_type, values):

            metadata_dict = self.get_metadata(self.get_runbooks(specific_missing_runbooks), values,
                                              self.runbook_template_keys, show_missing=True)
            metadata = []
            for item in metadata_dict.values():
                metadata += item
            self.runbook_criteria += '\n\n %s\n\t->%s' % (
                ', '.join(local_type),
                '\n\t->'.join(values))

            self.overview_string += self._sys_values['counter_msg'] % (', '.join(local_type),
                len(_filter_runbook_type(metadata, local_type)))

            # If looking for specific runbooks filter these out
            temp_json = _filter_runbook_type(metadata, local_type)

            return temp_json

        temp_type = ['Informational']
        missing_runbook_info.extend(get_missing_runbook_info(temp_type, informational_values))

        temp_type = ['PagerDuty', 'Recovery']
        missing_runbook_info.extend(get_missing_runbook_info(temp_type, pd_and_troubleshoot_recovery_values))

        temp_type = ['Troubleshooting']
        missing_runbook_info.extend(get_missing_runbook_info(temp_type, troubleshooting))

        temp_type = ['Operations', 'Deployment', 'Configuration', 'API', 'Test']
        missing_runbook_info.extend(get_missing_runbook_info(temp_type, ops_api_test_deploy_conf_values))



        metadata_dict = self.get_metadata(self.get_runbooks(specific_missing_runbooks),
                                     pd_and_troubleshoot_recovery_values,self.runbook_template_keys,show_missing=True)
        metadata = []
        for item in metadata_dict.values():
            metadata += item
        if specific_missing_runbooks and missing_runbook_info:
            print (self.runbook_criteria)
            sys.exit(self._sys_values['missing_runbook_info_msg'] % json.dumps(missing_runbook_info, indent=2))

        if missing_runbook_info:
            print(json.dumps(missing_runbook_info, indent=3))

        self.overview_string += self._sys_values['runbook_missing_counter_msg'] % (
            len(_filter_runbook_type(metadata, runbook_types, missing_types=True)))

        if missing_runbook_info:
            print(self.overview_string)

    def generate_troubleshooting(self):
        '''generate_troubleshooting

        Generate troubleshooting file and replace the existing one

        Parameters
        ----------
        None

        Returns
        -------
        None: writes the file
        '''

        troubleshooting_values = self._sys_values['default_troubleshooting_values']

        metadata = self.get_metadata(self.get_runbooks(), troubleshooting_values,self.runbook_template_keys)
        for component_name,  runbook_meta_list in metadata.items():
            for runbook_meta in runbook_meta_list:
                if 'Troubleshooting' == runbook_meta['type']:
                    runbook_meta.pop('type')

        self.replace_file_contents(self.troubleshoot_file_path, metadata)


    def _get_component(self,lst_all_components,component_name,runbook_full_path):
        '''
        Checks if the component_name passed is root component, if it is, it should be listed in lst_all_components
        otherwise it is a child component, if it is a child component, returns their parent.


        :param lst_all_components:  Contains all the parent components form the docs/runbooks directory
        :param component_name:      The component name of a runbook it could be a parent or a child
        :param crunbook_full_path:  runbook's full path to detect the parent of a child component
        :return:                    parent component name
        '''

        if component_name not in lst_all_components:
            for component in lst_all_components:
                if component in runbook_full_path:
                    component_name = component
                    break
        return component_name

    def _exist_folder(self,subdir_path):
        '''
        Check if the directory exist, if does not then creates it
        :param subdir_path: subdirectory to save data
        :return: None
        '''

        if not (os.path.exists(subdir_path)):
            try:
                os.makedirs(subdir_path)
            except IOError as e:
                print("I/O error({0}): {1} {2} at {3}".format(e.errno, e.strerror,subdir_path,'_exist_folder'))
                sys.exit(1)


    def _get_yml_metadata(self,runbook):
        '''
        Capture the YML metadata for a runbook if, exist

        :param runbook: A runbook to extract YML data
        :return:        YML metadata if exists
        '''
        data={}
        l_count =0
        header_block_counter=0
        f_path=self._script_path+"/tmp/"
        tmp_file = f_path+"yml_tmp_json_gen_" + time.strftime("%Y%m%d-%H%M%S") + '.yml'
        # Get the yml metadata and save it in a temporary file to parse it using PyYMAL
        try:
            self._exist_folder(f_path)
            with io.open(tmp_file,'w',encoding="utf-8") as out_file:
                try:
                    with io.open(runbook, 'r', encoding="utf-8") as runbook_file:
                        for line in runbook_file:
                            if not (line.startswith('#') or line.startswith('`')):
                                l_count +=1
                            else:
                                continue
                            # Only look at the table at the top of the file
                            if line.startswith('---'):
                                header_block_counter += 1
                            # Exit file when we reach the end of the markdown table
                            if header_block_counter == 2:
                                break
                            if l_count == 1 and header_block_counter == 0:
                                # The runbook does not start with YML metadata
                                return (data)
                            out_file.write(line)
                except IOError as e:
                    print("I/O error({0}): {1} {2} at {3} ".format(e.errno, e.strerror, runbook,'_get_yml_metadata'))
                    sys.exit(1)
            out_file.close()
        except IOError as e:
            print("I/O error({0}): {1} {2} at {3}".format(e.errno, e.strerror,tmp_file,'_get_yml_metadata'))
            sys.exit(1)

        data=yaml.load(open(tmp_file,'r'))
        os.remove(tmp_file)
        return (data)


    def _get_keys_to_track(self,template_keys,runbook_type,meta_values_to_track):
        '''

        If the runbook type is present on the runbook_templaes use the keys from the template otherwise use the default
        runbook type keys.

        :param template_keys:           Keys from the JSON template runbools file
        :param runbook_type:            The type of the runbook detected
        :param meta_values_to_track:    Default runbook keys to parse
        :return:
        '''
        compare_keys=meta_values_to_track
        for _type in template_keys:
            if _type['type']:
                if re.search(_type['type'], runbook_type):
                    compare_keys = _type.keys()
                    break  # found
        return (compare_keys)

    def _has_min_tags(self,runbook_tags,yml_keys):
        r = [k for k in yml_keys if k in runbook_tags]
        if not 'related-service' in r and 'service' in yml_keys:
            r.append('related-service')
        return (len(r)==len(runbook_tags))

    def _clean_logs(self):
        '''
        Clean the log and tmp files only keeps the last run logs

        :return: None
        '''


        for path, subdirs, files in os.walk(self._script_path+'/tmp'):
            for name in files:
                if 'yml_tmp_json_gen' in name:
                    os.remove(os.path.join(path, name))

        for path, subdirs, files in os.walk(self._script_path + '/logs'):
            for name in files:
                if 'error_log_json_gen' in name:
                    os.remove(os.path.join(path, name))


    def get_metadata(self, runbooks, meta_values_to_track, template_keys,show_missing=False):
        '''get_metadata

        Scrap the metadata from the runbooks


        Updated by: Alejandro Torres Rojas
        Date:       19-Feb-2018
        Notes:      This function experience the major updates of all the follow updates were made:
                        * Capture the yml metadata into a list of dictionaries to be able to analyze multiple lines
                        * Review if a runbook contains metadata otherwise skip and report it.
                        * Exclude runbooks that are in the exclude components list.
                        * If a runbook does not contain the minimum tags listed at 'runbook_mandatory_values' under
                          script/data/OSSRunbookJsonGenerator.json it is skipped and reported or the error_log.
                        * Change 'service' by 'related-service' for runbook that use 'service' instead 'related-service',
                          such as armada. The OSS portal expects 'related-service' for the runbooks list.
                        * Reports if a tag was a missing value.
                        * Reports if a tag listed on the runbook templtes is not present in a runbook.
                        * If the runbbok link value contains https or http looks if the link has runbook also, and
                          corrects the link and also reports it for user review.

        Updated by:     Alejandro Torres Rojas
        Date:           6-Mar-2018
        Notes:          Changed elif 'http' in value.lower(): by  elif value.lower().startswith('http') only checks if
                        the URL strats with http instead of contains. Bug reported by Irma Sheriff.


        Parameters
        ----------
        runbooks: list of runbooks file names
        meta_values_to_track: List of metadata keys you are expecting to find
        show_missing: (optional) Just return the the metadata of files that are
        missing attributes

        Returns
        -------
        List: list of dictionaries containing the metadata
        List: error_log if any
        '''

        lst_all_components = next(os.walk(self.runbook_directory))[1] # Get all parent component names
        temp_metadata = {}
        error_log={}
        basic_meta_values_to_track=meta_values_to_track

        for runbook in runbooks:
            runbook_meta = {}
            runbook_dir = os.path.dirname(runbook)
            component_name= os.path.split(runbook_dir)[1]


            # Get always the parent component name of a runbook
            component_name= self._get_component(lst_all_components, component_name, runbook)

            if component_name in self.dirs_to_exclude: continue


            if component_name not in temp_metadata:
                temp_metadata[component_name] = []
            # If we don't cache the metadata when use the 'missing' it won't show
            # all the missing attributes if the last one is the one that is missing.
            # For example if the metadata looks as expected we won't add it to runbook_meta
            # if we are just looking for missing attributes. Then we get to the last attribute
            # and its missing we need to append all the other attributes to keep track of all
            # the metadata for a runbook
            cache_all_metadata = {}
            missing_metadata = False

            yml_metadata=self._get_yml_metadata(runbook)
            if not yml_metadata:
                error_log.update({runbook:{self.metadata_error_flag:self._sys_values['yml_missed']}})
                continue #If file does not contain YML data it is skipped
            if not self._has_min_tags(basic_meta_values_to_track,yml_metadata.keys()):
                error_log.update({runbook: {self.metadata_error_flag: self._sys_values['metadata_missed_min_tags'] %
                                                     ', '.join(meta_values_to_track)}})
                continue  # Runbook does not have minimum tags to be displayed on the Portal
            if 'type' in yml_metadata.keys():
                if not yml_metadata['type']:
                    yml_metadata['type'] =self._sys_values['default_runbook_type'] # runbook type value is null set type to  default type
                    error_log.update({runbook: {self.metadata_error_flag: self._sys_values['metadata_type_tag_empty']}})
                meta_values_to_track = self._get_keys_to_track(template_keys,yml_metadata['type'],meta_values_to_track)
            else:
                error_log.update({runbook: {self.metadata_error_flag: self._sys_values['metadata_type_tag_missed']}})
                continue  # If file does not contain YML data it is skipped

            for key in meta_values_to_track:

                if key in yml_metadata:
                    metadata_value = yml_metadata[key]
                    key = ('related-service' if 'service' in key else key)
                    if metadata_value:
                        _metadata, valid_value = self.run_verify(key, metadata_value, show_missing)
                        # If has a valid metadata and not trying to show the missing attributes

                        if valid_value and key not in runbook_meta and not show_missing:
                            runbook_meta[key] = _metadata
                        if show_missing:
                            if not valid_value and _metadata:
                                missing_metadata = True
                            if _metadata and missing_metadata:
                                runbook_meta[key] = _metadata
                            elif _metadata:
                                cache_all_metadata[key] = _metadata

                        # If 'show_missing' and there is missing metadata in the runbook empty cached
                        # metadata into 'runbook_meta', since 'runbook_meta' only consists of the missing
                        # attributes
                        if show_missing and missing_metadata and cache_all_metadata:
                            for key, value in cache_all_metadata.items():
                                runbook_meta[key] = value
                        # if key =='link' and 'http' in _metadata:
                        if key == 'link' and _metadata.lower().startswith('http'):
                            error_log.update(
                                {runbook: {self.metadata_warning_flag: self._sys_values['http_in_link']%_metadata}})

                    else:
                        runbook_meta[key]=self.missing_data_flag
                        error_log.update({runbook: {self.metadata_warning_flag:
                                                        self._sys_values['metadata_value_for_key_is_empty'].format(key)}})
                else:
                    runbook_meta[key] = self.missing_data_flag
                    msg=self._sys_values['missing_runbook_key_msg'].format(key,yml_metadata['type'])
                    error_log.update({runbook: {self.metadata_warning_flag:msg}})
            # Add missing keys to dict
            if show_missing and missing_metadata:
                for item in meta_values_to_track:
                    if item not in runbook_meta.keys():
                        runbook_meta[item] = self.missing_data_flag

            # Only append the runbooks that have valid info or your trying to show missing
            if (len(meta_values_to_track) == len(runbook_meta.keys()) or
                    show_missing and missing_metadata):
                temp_metadata[component_name].append(runbook_meta)

        return temp_metadata, error_log

    def run_verify(self, key, metadata_value, show_missing):
        '''Map the metadata key words to the verify functions'''
        if key == 'link':
            return self._verify_link(metadata_value, show_missing)
        elif key == 'failure':
            return self._verify_failure(metadata_value, show_missing)
        elif "service" in key:
            return self._verify_service(metadata_value, show_missing)
        elif key in ['type','runbook-name','layout','tags','title']:
            return self._verify_key(metadata_value, show_missing,key)
        elif key == 'description':
            return self._verify_description(metadata_value, show_missing)
        elif key in ['playbooks','ownership-details']:
            return self._verify_playbooks(metadata_value, show_missing)


    def _verify_link(self, metadata_value, show_missing):
        '''Check Line contains the runbook link

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'link' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Updated by:     Alejandro Torres Rojas
        Date:           6-Mar-2018
        Notes:          Changed elif 'http' in value.lower(): by  elif value.lower().startswith('http') only checks if
                        the URL strats with http instead of contains. Bug reported by Irma Sheriff.

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        verified = False
        if metadata_value:
            metadata_value = metadata_value.replace('"', '')
            # if "http" in metadata_value:
            if metadata_value.lower().startswith('http'):
                i=metadata_value.find("runbooks/")
                metadata_value= metadata_value[i+len("runbooks/"):]
            if self.defaults_replacement['link'] not in metadata_value:
                verified = True
            else:
                if show_missing:
                    return (self.set_default_value, False)
            return ('%s%s' % (self.runbook_sub_link, metadata_value),verified)
        return (None, verified)


    def _verify_failure(self, metadata_value, show_missing):
        '''Check Line contains the runbook failures

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'failure' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''

        verified = False
        if metadata_value:
            temp_failure = metadata_value
            # Verfiy there are no default values in file
            if all([default_failure not in temp_failure for default_failure in self.defaults_replacement['failure']]):
                verified=True
            else:
                if show_missing:
                    return (self.set_default_value, verified)
                else:
                    if self.invalid_failure_string in metadata_value:
                        return (self.failure_replacement, verified)
            return (metadata_value,verified)
        return (None,verified)


    def _verify_service(self, metadata_value, show_missing):
        '''Check Line contains the runbook related services

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'service' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        verified = False
        if metadata_value:
            if all([default_service not in metadata_value for default_service in self.defaults_replacement['related-service']]):
                verified=True
            else:
                if show_missing:
                    return (self.set_default_value, verified)
            return (metadata_value, verified)

        return (None,verified)


    def _verify_description(self, metadata_value, show_missing):
        '''Check Line contains the runbook description

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'description' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        verified = False
        if metadata_value:
            if all([default_description not in metadata_value for default_description
                    in self.defaults_replacement['description']]):
                verified = True
            else:
                if show_missing:
                    return (self.set_default_value, verified)
            return (metadata_value, verified)

        return (None,verified)



    def _verify_playbooks(self, metadata_value, show_missing):
        '''Check Line contains the runbook playbooks

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'playbooks' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Updated by: Alejandro Torres Rojas
        Date:       19-Feb-2018
        Notes:      Instead to have a different calls for the same logic this function will be used for the follow keys:
                    ['playbooks','ownership-details']

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''

        verified = False
        if metadata_value:
            if all([default_service not in metadata_value for default_service in self.defaults_replacement['playbooks']]):
                # Verify playbooks is a list
                verified = True
            else:
                if show_missing:
                    return (self.set_default_value, verified)
            return (metadata_value, verified)

        return (None,verified)


    def _verify_key(self, metadata_value, show_missing,key):
        '''Check Line contains the runbook title

        Parameters
        ----------
        metadata_value: value obtained from the yml metadata for the 'tags' key

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        key: could be title, tags, layout

        Updated by: Alejandro Torres Rojas
        Date:       19-Feb-2018
        Notes:      Instead to have a different calls for the same logic this function will be used for the follow keys:
                    ['type','runbook-name','layout','tags','title']

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        verified=False
        if metadata_value:
            if self.defaults_replacement[key]  not in metadata_value:
                verified = True
            else:
                if show_missing:
                    return (self.set_default_value, verified)
            return (metadata_value, verified)

        return (None,verified)


    def replace_file_contents(self, path, content,err_log=None):
        '''Replace contents of the specified file

        Make sure we are not writing no content to file, then
        Replace the content


        Updated by: Alejandro Torres Rojas
        Date:       19-Feb-2018
        Notes:      If a waring or error found in a runbook, the runbook name and extra information is added to the
                    error_log dictionary. If at least an errors/warning will be displayed in a JSON format
        Parameters
        ----------
        path        Script path
        content     Runbook metadata verified
        err_log     error_log metadata
        '''
        try:
            self._clean_logs()
            if len(content) > 0:
                for component_name, runbook_meta_list in content.items():
                    if component_name == "runbooks":
                        continue

                    file_name = os.path.join(os.path.dirname(path), component_name + "-" +os.path.basename(path))
                    with open(file_name, 'w+') as file:
                        file.write(json.dumps(runbook_meta_list, indent=2, separators=(',', ': ')))
            #this serction added to report warnigg/errors
            if err_log:
                f_path=self._script_path+'/logs/'
                file_name = f_path +self._sys_values['output_file_name']+time.strftime("%Y%m%d-%H%M%S")+'.json'
                self._exist_folder(f_path)
                with open(file_name, 'w+') as file:
                    file.write(json.dumps(err_log, indent=2, separators=(',', ': ')))
                print(self.finished_with_errors % file_name)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

        print(self.finished_success)


    def get_runbooks(self, list_of_files=None):
        '''get_runbooks

        Scrap the runbook directory and return all files with the .md extension
        Updated by: Alejandro Torres Rojas
        Date:       19-Feb-2018
        Notes:      Exclude any files listed on the file_2_exclude metadata from the script/data/OSSRunbookJsonGenerator.json

        Parameters
        ----------
        list_of_files a list of runbooks passed by user to be analyzed and added to the JSON file

        Returns
        -------
        List: list of runbook file names
        '''
        temp_runbooks = []
        #for file in os.listdir(self.runbook_directory):
        for path, subdirs, files in os.walk(self.runbook_directory):
            for name in files :
                f_name=os.path.join(path, name)
                if name.endswith(".md") and (name.lower() not in self.files_to_exlude):
                    if not list_of_files:
                        temp_runbooks.append(f_name)
                    elif os.path.join(path, name) in list_of_files:
                      temp_runbooks.append(f_name)
        return temp_runbooks


if __name__ == '__main__':
    RunbookJsonGenerator().main()

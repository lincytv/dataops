#!/usr/bin/env python



import argparse
import ast
import copy
import json
import os
import sys

'''
      _                            ____                                        _
     | |  ___    ___    _ __      / ___|   ___   _ __     ___   _ __    __ _  | |_    ___    _ __
  _  | | / __|  / _ \  | '_ \    | |  _   / _ \ | '_ \   / _ \ | '__|  / _` | | __|  / _ \  | '__|
 | |_| | \__ \ | (_) | | | | |   | |_| | |  __/ | | | | |  __/ | |    | (_| | | |_  | (_) | | |
  \___/  |___/  \___/  |_| |_|    \____|  \___| |_| |_|  \___| |_|     \__,_|  \__|  \___/  |_|


Use Case:
---------
There are a few files for the runbooks that need to be udated as part of a submission or a change
of a runbook. They are:
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

'''
class RunbookJsonGenerator(object):

    def __init__(self):
        # Path of this script
        self.script_path = os.path.dirname(os.path.realpath(__file__))

        # Make all paths relative to the location of this script so it can be called from anywhere
        self.runbook_directory      = self.script_path + '/../docs/runbooks/'
        self.runbook_list_path      = self.script_path + '/../assets/json/runbook-list.json'
        self.troubleshoot_file_path = self.script_path + '/../assets/json/troubleshooting.json'

        # Base link for all runbook references in the below files:
        #    - assets/json/runbook-list.json
        #    - assets/json/troubleshooting.json
        self.runbook_sub_link  = '/docs/runbooks'

        # The default replacement text for 'failure' is not a valid list so se need to replace it
        # with a valid list before its loaded in
        self.invalid_failure_string = ('<add failures that this Runbook addresses. Separate each '
                                       'failure with a comma and surround with inverted commas>')
        self.failure_replacement    = ['<add failures that this Runbook addresses. Separate each '
                                       'failure with a comma and surround with inverted commas>']

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
            'layout': 'Unknown'
        }

        self.example_metadata = {
            'description': 'description: Covers everything you need to know about the Alchemy Reference Application.',
            'runbook-name': 'runbook-name: Troubleshooting Sensu Check Disk - statvfs() function failed',
            'link': 'link: /debugging_sensu_statvfs.html',
            'type': 'type: Troubleshooting',
            'related-service': 'Sensu',
            'failure': ('failure: ["PagerDuty Check Disk: Check failed to run: statvfs() function failed: '
                        'Stale file handle..."]'),
            'playbooks': ('playbooks: ["Update Runbook with Ansible Playbook for PagerDuty Check Disk: Check '
                          'failed to run: statvfs() function failed: Stale file handle..."]'),
            'title': 'title: Troubleshooting Sensu Check Disk - statvfs() function failed',
            'layout': 'layout: Unknown'
        }

        self.description_str   = 'description: '
        self.name_str          = 'runbook-name: '
        self.link_str          = 'link: '
        self.type_str          = 'type: '
        self.service_str       = 'service: '
        self.failure_str       = 'failure: '
        self.playbooks_str     = 'playbooks: '
        self.tags_str          = 'tags: '
        self.title_str         = 'title: '
        self.layout_str        = 'layout: '

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

        parser = argparse.ArgumentParser()

        parser.add_argument(
            '--runbooks',  action='store_true',
            help='Generate runbook-list.json file')

        parser.add_argument(
            '--troubleshoot',  action='store_true',
            help='Generate troubleshooting.json file')

        parser.add_argument(
            '--all',  action='store_true',
            help='Generate runbook-list.json and troubleshooting.json files')

        parser.add_argument(
            '--missing',  action='store_true',
            help=('Return all the runbooks metadata that are missing any of these key '
                  'values: ' + ', '.join(self.defaults_replacement.keys())))

        parser.add_argument(
            '--verify_missing', type=str,
            help=('Return all missing metadata for specific runbooks passed in the command line.'
                  ' Runbooks must be comma sperated'))

        # Verify all arguments are valid
        args = parser.parse_args()
        if args.all:
            self.generate_runnbook()
            self.generate_troubleshooting()
            return
        else:
            if args.runbooks:
                self.generate_runnbook()
                return
            if args.troubleshoot:
                self.generate_troubleshooting()
                return
        if args.missing:
            self.generate_missing()
            return

        if args.verify_missing:
            self.generate_missing(specific_missing_runbooks=args.verify_missing)
            return

        print('UsageError: You must call this tool with one of the specified options. '
              'Use --help for usage.')

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

        runbook_values = [
            'description',
            'related-service',
            'runbook-name',
            'link',
            'type'
        ]

        metadata = self.get_metadata(self.get_runbooks(), runbook_values)
        self.replace_file_contents(self.runbook_list_path, metadata)

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
        runbook_types = ['Informational', 'PagerDuty', 'Troubleshooting', 'Operations', 'Configuration',
                         'Deployment', 'API', 'Recovery', 'Test']

        # Find values that are missing in informational runbooks
        informational_values = [
            'title',
            'runbook-name',
            'type',
            'description',
            'related-service',
            'link'
        ]
        # Find values that are missing in PagerDuty and Troubleshooting runbooks
        # NOTE(tjcocozz): PagerDuty runbooks include 'ownership-details' metadata but there will
        # need to be some re-design here to check for it, since it's spread across multiple lines
        pd_and_troubleshoot_recovery_values = [
            'title',
            'runbook-name',
            'type',
            'description',
            'related-service',
            'failure',
            'playbooks',
            'link'
        ]
        troubleshooting = [
            'title',
            'runbook-name',
            'type',
            'description',
            'related-service',
            'link'
        ]
        ops_api_test_deploy_conf_values = [
            'title',
            'runbook-name',
            'related-service',
            'description',
            'type',
            'link'
        ]
        deploy_values = [
            'title',
            'runbook-name',
            'related-service',
            'description',
            'type',
            'link',
            'playbooks'
        ]

        self.overview_string  = ''
        missing_runbook_info  = []
        self.runbook_criteria = '\nRunbook Types and their corresponding MANDATORY VALUES:'

        def get_missing_runbook_info(local_type, values):
            metadata_dict = self.get_metadata(self.get_runbooks(specific_missing_runbooks), values, show_missing=True)
            metadata = []
            for item in metadata_dict.values():
                metadata += item
            self.runbook_criteria += '\n\n %s\n\t->%s' % (
                ', '.join(local_type),
                '\n\t->'.join(values))

            self.overview_string += 'Number of %s Runbooks Missing Info: %d\n' % (
                ', '.join(local_type),
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
                                     pd_and_troubleshoot_recovery_values,
                                     show_missing=True)
        metadata = []
        for item in metadata_dict.values():
            metadata += item
        if specific_missing_runbooks and missing_runbook_info:
            print self.runbook_criteria
            sys.exit('\nFIX YOUR RUNBOOKS METADATA!!\n\n%s' % json.dumps(missing_runbook_info, indent=2))

        if missing_runbook_info:
            print(json.dumps(missing_runbook_info, indent=3))

        self.overview_string += 'Number of Runbooks Missing "Type": %d\n' % (
            len(_filter_runbook_type(metadata, runbook_types, missing_types=True)))

        if missing_runbook_info:
            print self.overview_string

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

        troubleshoot_values = [
            'link',
            'type',
            'related-service',
            'failure'
        ]

        metadata = self.get_metadata(self.get_runbooks(), troubleshoot_values)
        for component_name,  runbook_meta_list in metadata.items():
            for runbook_meta in runbook_meta_list:
                if 'Troubleshooting' == runbook_meta['type']:
                    runbook_meta.pop('type')

        self.replace_file_contents(self.troubleshoot_file_path, metadata)

    def get_metadata(self, runbooks, meta_values_to_track, show_missing=False):
        '''get_metadata

        Scrap the metadata from the runbooks

        Parameters
        ----------
        runbooks: list of runbooks file names
        meta_values_to_track: List of metadata keys you are expecting to find
        show_missing: (optional) Just return the the metadata of files that are
        missing attributes

        Returns
        -------
        List: list of dictionaries containing the metadata
        '''
        temp_metadata = {}
        for runbook in runbooks:
            runbook_meta = {}

            runbook_dir = os.path.dirname(runbook)

            component_name = os.path.split(runbook_dir)[1]

            if component_name.startswith('_'):
                continue

            # include runbooks under ibm nested folder one level up
            # we need to be able to exclude the runbooks under ibm easily when sending to Wanda
            if component_name == 'ibm':
                component_name = os.path.split(os.path.split(runbook_dir)[0])[1]


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

            header_block_counter = 0

            #CULLEPL: changed and removed runbook_directory reference as this is now in the list we build up
            with open(runbook) as runbook_file:
                # Loop through every line in the file
                for line in runbook_file:
                    line = line.strip()

                    # Only look at the table at the top of the file
                    if line.startswith('---'):
                        header_block_counter += 1
                        continue

                    # Exit file when we reach the end of the markdown table
                    if header_block_counter == 2:
                        break

                    for key in meta_values_to_track:
                        _meatdata, valid_value = self.run_verify(key, line, show_missing)
                        # If has a valid metadata and not trying to show the missing attributes
                        if valid_value and key not in runbook_meta and not show_missing:
                            runbook_meta[key] = _meatdata
                            break
                        if show_missing:
                            if not valid_value and _meatdata:
                                missing_metadata = True
                            if _meatdata and missing_metadata:
                                runbook_meta[key] = _meatdata
                                break
                            elif _meatdata:
                                cache_all_metadata[key] = _meatdata

                # If 'show_missing' and there is missing metadata in the runbook empty cached
                # metadata into 'runbook_meta', since 'runbook_meta' only consists of the missing
                # attributes
                if show_missing and missing_metadata and cache_all_metadata:
                    for key, value in cache_all_metadata.items():
                        runbook_meta[key] = value

            # Add missing keys to dict
            if show_missing and missing_metadata:
                for item in meta_values_to_track:
                    if item not in runbook_meta.keys():
                        runbook_meta[item] = 'MISSING'

            # Only append the runbooks that have valid info or your trying to show missing
            if (len(meta_values_to_track) == len(runbook_meta.keys()) or
                    show_missing and missing_metadata):
                temp_metadata[component_name].append(runbook_meta)


        return temp_metadata

    def run_verify(self, key, line, show_missing):
        '''Map the metadata key words to the verify functions'''
        if key == 'link':
            return self._verify_link(line, show_missing)
        elif key == 'failure':
            return self._verify_failure(line, show_missing)
        elif key == 'related-service':
            return self._verify_service(line, show_missing)
        elif key == 'type':
            return self._verify_type(line, show_missing)
        elif key == 'description':
            return self._verify_description(line, show_missing)
        elif key == 'runbook-name':
            return self._verify_name(line, show_missing)
        elif key == 'layout':
            return self._verify_layout(line, show_missing)
        elif key == 'playbooks':
            return self._verify_playbooks(line, show_missing)
        elif key == 'tags':
            return self._verify_tags(line, show_missing)
        elif key == 'title':
            return self._verify_title(line, show_missing)
        print 'INVALID KEY: %s' % key

    def _verify_link(self, line, show_missing):
        '''Check Line contains the runbook link

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.link_str):
            line = line.replace('"', '')
            if self.defaults_replacement['link'] not in line:
                return ('%s%s' % (self.runbook_sub_link, line.replace(self.link_str, '')), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return ('%s%s' % (self.runbook_sub_link, line.replace(self.link_str, '')),
                            False)
        return (None, False)

    def _verify_failure(self, line, show_missing):
        '''Check Line contains the runbook failures

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.failure_str):
            temp_failure = line.replace(self.failure_str, '')
            # Verfiy there are no default values in file
            if all([default_failure not in temp_failure for default_failure
                    in self.defaults_replacement['failure']]):

                return (self.convert_to_json(
                    temp_failure,
                    self.example_metadata['failure']), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    if self.invalid_failure_string in line:
                        return (self.failure_replacement, False)
                    return (self.convert_to_json(
                        temp_failure,
                        self.example_metadata['failure']), False)
        return (None, False)

    def _verify_type(self, line, show_missing):
        '''Check Line contains the runbook type

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.type_str):
            line = line.replace('"', '')
            if self.defaults_replacement['type'] not in line:
                return (line.replace(self.type_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.type_str, ''), False)
        return (None, False)

    def _verify_service(self, line, show_missing):
        '''Check Line contains the runbook related services

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.service_str):
            line = line.replace('"', '')
            if all([default_service not in line for default_service
                    in self.defaults_replacement['related-service']]):
                return (line.replace(self.service_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.service_str, ''), False)
        return (None, False)

    def _verify_description(self, line, show_missing):
        '''Check Line contains the runbook description

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.description_str):
            line = line.replace('"', '')
            if all([default_description not in line for default_description
                    in self.defaults_replacement['description']]):
                return (line.replace(self.description_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.description_str, ''), False)
        return (None, False)

    def _verify_name(self, line, show_missing):
        '''Check Line contains the runbook name

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.name_str):
            line = line.replace('"', '')
            if self.defaults_replacement['runbook-name'] not in line:
                return (line.replace(self.name_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.name_str, ''), False)
        return (None, False)
    def _verify_layout(self, line, show_missing):
        '''Check Line contains the runbook layout

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.layout_str):
            line = line.replace('"', '')
            if self.defaults_replacement['layout'] not in line:
                return (line.replace(self.layout_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.layout_str, ''), False)
        return (None, False)

    def _verify_playbooks(self, line, show_missing):
        '''Check Line contains the runbook playbooks

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.playbooks_str):
            # Remove key from string
            temp_playbook = line.replace(self.playbooks_str, '')

            if all([default_service not in temp_playbook for default_service
                    in self.defaults_replacement['playbooks']]):


                # Verify playbooks is a list
                return (self.convert_to_json(
                    temp_playbook,
                    self.example_metadata['playbooks']), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (self.convert_to_json(
                        temp_playbook,
                        self.example_metadata['playbooks']), False)
        return (None, False)

    def _verify_tags(self, line, show_omissing):
        '''Check Line contains the runbook tags

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.tags_str):
            line = line.replace('"', '')
            if self.defaults_replacement['tags'] not in line:
                return (line.replace(self.tags_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.tags_str, ''), False)
        return (None, False)

    def _verify_title(self, line, show_missing):
        '''Check Line contains the runbook title

        Parameters
        ----------
        line: line of the file

        show_missing: (Bool) If True we replace the metadata with a keyword to help
        show where missing values are

        Returns
        -------
        Tuple: (<metadata>, <True if we have valid metadata>)
        '''
        if line.startswith(self.title_str):
            line = line.replace('"', '')
            if self.defaults_replacement['title'] not in line:
                return (line.replace(self.title_str, ''), True)
            else:
                if show_missing:
                    return ('DEFAULT VALUE', False)
                else:
                    return (line.replace(self.title_str, ''), False)
        return (None, False)

    def convert_to_json(self, item_str, failure_example):
        try:
            return ast.literal_eval(item_str)
        except SyntaxError:
            print '\n\nMETADATA USING THE WRONG FORMAT!! \n\nEXAMPLE FORMAT:\n%s\n\n' % failure_example
            raise

    def replace_file_contents(self, path, content):
        '''Replace contents of the specified file

        Make sure we are not writing no content to file, then
        Replace the content
        '''
        if len(content) > 0:
            for component_name, runbook_meta_list in content.items():
                if component_name == "runbooks":
                    continue
                file_name = os.path.join(os.path.dirname(path), component_name + "-" +os.path.basename(path))
                with open(file_name, 'w+') as file:
                    file.write(json.dumps(runbook_meta_list, indent=2, separators=(',', ': ')))

    def get_runbooks(self, list_of_files=None):
        '''get_runbooks

        Scrap the runbook directory and return all files with the .md extension

        Parameters
        ----------
        None

        Returns
        -------
        List: list of runbook file names
        '''
        temp_runbooks = []
        #for file in os.listdir(self.runbook_directory):
        for path, subdirs, files in os.walk(self.runbook_directory):
            for name in files:
              if name.endswith(".md"):
                if not list_of_files:
                    temp_runbooks.append(os.path.join(path, name))
                elif os.path.join(path, name) in list_of_files:
                    temp_runbooks.append(os.path.join(path, name))
        return temp_runbooks

if __name__ == '__main__':
    RunbookJsonGenerator().main()

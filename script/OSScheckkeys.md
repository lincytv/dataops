## OSScheckkeys.py


Validates the YML structure using yamllint.
Validates the YML metadata and structure in a md file.
Returns a JSON file with the runbooks that did not meet the YAML structure or metadata validation.


### Pre-requirements:

*	Python 2.7
*	YAML lint  
*	Bash kernel


All runbook must contain a valid YML metadata for Jekyll to be able to build a static web portal. The portal uses a table build using a JSON generate file and to build the table, a runbook must have a type key value pair, also, Jekyll needs to have a layout to use to display data in the correct format, additionally if a runbook does not have YML header then Jekyll won’t convert it into html format.

Base on the previous statement the follow is mandatory for a runbook:

*	Must have a YML header in the format required by Jekyll https://jekyllrb.com/docs/frontmatter/
*	The metadata must include a layout value:pair , the default layout is default, but marmot documents use default_marmot layout
*	The metadata must include a type value:pair the type is use to generate the JSON file
*	The matadata must contain a service, it is use to display a value on table catalog

Additional validations to flag a run runbook to be reviewed are:

* A key must have a value passed.
* The link key must contain the runbook name with html extension.
* The link key cannot contain http or https on it.


Returns:

* Completion code of **1** and a list of runbooks with metadata to be reviewed in a JSON format, if at least one pair value fails.
* Completion code of **0** if all runbooks to be reviewed have a valid metadata.

OSScheckkeys.py uses four JSON files under the `scripts/data` directory:

| Name    | Description    |
| :------------- | :------------- |
| runbooks_template_keys| Originally from checkkeys.py, contains the metadata to look for a specific                      		runbook to check a new type it needs to be added to this one   |
|default_replacements|From RunbookJsonGenerator.py, contains the default values for a metadata|
|example_metadata|       	From RunbookJsonGenerator.py, contains example of valid values for a metadata
|OSScheckkeys.json| New, contains all custom messages displayed and other system data to customize this program, REQUIRED.


### Sample program call:

``python OOScheckkeys.py  -t runbooks_template_keys.json -d default_replacement.json -e example_metadata.json -l "runbook1.md" "runbook2.md" ... "runbookn.md" [-ny/-oy]``

All parameters are optional use python `OOScheckkeys.py --help` for more information


Use the runbooks_template_keys.josn filesystem to add/remove/update any runbook templates types.

A example of template keys:
```{
      "runbook-name": "",
      "type": "Informational",
      "description": "",
      "service": "",
      "link": "",
      "title": "",
      "layout": ""
   },
 ```

The above is the metadata expected for runbooks of type **Informational**.

Use this entry in the template_keys.json file to add/delete/update metadata for **Informational** runbooks.

e.g.:

```{
      "runbook-name": "",
      "type": "Informational",
      "description": "",
      "service": "",
      "link": "",
      "title": "",
      "tags:"
      "layout": ""
   },
 ```

A new key **tags** got added from the previous version of the **Informational** template, now the **tags** key will be a new key:value pair to be checked when the OSScheckkeys script runs. Likewise you can remove keys that are not in use anymore.

## OSScheckkeys.json key:value information:

| Key name     | Description    |
| :------------- | :------------- |
| counter_msg| Message displayed to report totals by runbook type.|
|completed_wo_errors|Message displayed when this script completes without errors.|
|def_layout|Specify the default layout under _layouts.|
|def_type|If a runbook has a type but the type does not exist under template_keys.json will use the type defined here.|
|default|Name of the defaults_replacement.json file, set a valid name here.|
|description|Script description use in the argparse.ArgumentParser description argument.|
|dir_2_exclude|List of locations to be excluded form the review.|
|example|Name of the example_metadata.json file, set a valid name here.|
|file_2_exclude|List of files to be excluded form the review.|
|grep_err|Error message displayed when the bash grep cannot be executed, _currently not in use_|
|hlp_default|Help message for the defaults_replacement.json file use in the argparse.ArgumentParser.|
|hlp_example|Help message for the example_metadata.json file use in the argparse.ArgumentParser.|
|hlp_lst|Help message for the optional list runbooks parameter use in the argparse.ArgumentParser.|
|hlp_not_yml_check|Help message for -ny option, use in the argparse.ArgumentParser.|
|hlp_only_yml_check|Help message for -oy option, use in the argparse.ArgumentParser.|
|hlp_template|Help message for the runbooks_template_keys.json file use in the argparse.ArgumentParser.|
|http_in_link|Message displayed when the value for the link key contains http or https on it.|
|invalid_layout|Message displayed when the layout name for the layout key does not exist under _layouts directory.|
|missing|If a value for a key is empty on the YML metadata, the missing word will be added to the value key.|
|no_argv_check|If set to True it will allow to run the script without parameters, otherwise will spect input parameters. It is set to True by default.|
|no_argv|Message displayed when no arguments are passed, it works in conjunction with no_argv_check.|
|no_layout_dir|Message displayed when the _layouts directory does not exist in the current project.|
|no_type|Message displayed when a runbook does not have type pair value.|
|no_yml|Message to be displayed when a md file does not contain a yml header.|
|ouput_file_name|Name of the output JSON file to report errors, if any.|
|results_msg|Message displayed when reporting errors.|
|runbook_loc|Default location of the runbooks. Set a different location here|
|template|Name of the runbooks_template_keys.json file, set a valid name here.|
|unknown|If a runbook does not have a type it will add it to the output file as Unknown type.|
|version|Current version of the OSScheckkeys.py script.
|yml_failed|Message displayed when at least one validation check failed.|
|yes_no_msg|Message displayed in the yes_no function.|
|yml_err|Message send the yamllint verification failed.|
|yml_failed|Message added to the metadata when at least one of the key:value pair failed to be verified|
|yml_log_file|Temporary file name use for the yamllint verification log. It gets deleted after the verification is completed.|
|yml_tmp_file|Temporary file name use for the yamllint verification. It gets deleted after the verification is completed.|
|yml_os_system|Use to select the yamllint by os commands or Python libraries, _currently not in use_|

---
layout: default
title: Troubleshooting Runbook Template
type: Informational
runbook-name: "Info on Runbook template for Runbook of Type 'Troubleshooting'. Surround with inverted commas. Escape internal inverted commas."
description: "Info on Runbook template for Runbook of Type 'Troubleshooting'"
service: Conductors
link: /troubleshooting_runbook_template.html
---
---
#### Required Metadata
```yaml
---
layout: default
title: <replace with a title to be displayed on the runbook page>
type: Troubleshooting
runbook-name: <replace with runbook-name. Surround with inverted commas>
description: <replace with description>
service: <replace with service, e.g. Containers>
failure: [<add failures that this Runbook addresses. Separate each failure with a comma and surround with inverted commas>]
playbooks:  [<add Ansible-playbook command to automate Runbook. Separate each Playbook with a comma and surround with inverted commas>]
link: <link to Runbook - replace .md with .html>
```
_**Explanation Section:**  Completing the metadata section above will eliminate the need to update the
'runbook-list.json' file. Please complete this, and then delete the text in this 'explanation' section._


## Issue

  * How can the issue be verified?
  * What PD incidents might occur?

## Actions to take

  * What steps should be taken to fix the problem?
  * If more information must be gathered (e.g. by looking at logs) make sure to specify what
  to look for, where to find it, and how the gathered information is used to decide what actions to take
  * What might go wrong in attempting the fix?
  * Are there cases where we can't reach a resolution but also don't need to page out your team?

## Escalation

  * Escalation policy and slack channel.

## Further reading

  * Link to informational documentation here
  * Such documentation could be useful for Conductors attempting more extensive debugging
  during business hours.  

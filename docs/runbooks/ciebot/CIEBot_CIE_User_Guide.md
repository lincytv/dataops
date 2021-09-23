---
layout: default
description: CIEBOT CIE  Guide
title: CIEBOT CIE User Guide
service: ciebot
runbook-name: CIEBOT CIE User Guide
tags: oss, ciebot,
link: /ciebot/CIEBot_CIE_User_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Overview

This document is intended to be used in conjunction with [CIEBOT General Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html).

Before start running *cie* command for the first time, make sure you have permission to TIP Platform APIs. Details can be found in [Authentication Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html) and [CIEBOT General Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html).

The majority of users use command **[bot name] cie** to start a Slack interactive menu. The initial menu displays a drop down list with available actions related to CIEs. Some of the actions will display a dialog requesting information, others will ask you to pick an incident from the list. If the incident you are intersted in is not in the list, you can use the menu action to add one to the list. Once an incident is selected, just follow the instruction.

**[bot name]** is **ciebot**, **cietest**, etc.

## Frequently Asked Questions

**Q: Where can I get info on the commands available in [bot name]?**

A: More details about the commands can be found in this document and by running **[bot name] help** in Slack.

## CIE Commands

**Creating a CIE**

Creates a new Incident in ServiceNow.

- Use command **[bot name] cie**
- Select **Create a New Incident** from the list of actions.
- Complete the fields on the form and click submit.

----------------------

**Confirming a CIE**

Set the state of the Incident in ServiceNow to Potential CIE or Confirmed CIE.

- Use command **[bot name] cie**
- Select **Change Incident State** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------
**Change severity of a CIE**

Switch between severity 1 and 2.

- Use command **[bot name] cie**
- Select **Change Incident Severity** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Select the severity and click submit.

----------------------

**Add a Comment to a CIE**

Add a comment to the work notes field of an Incident in ServiceNow.

- Use command **[bot name] cie**
- Select **Add a Comment** to an Incident from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------

**Resolve a CIE**

Resolve a CIE and set its close state.

- Use command **[bot name] cie**
- Select **Resolve an Incident** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------

**Add a CRN Service Name**

The following will be deprecated. Use **[bot name] crnservice add [service name]** instead. See 
[CIEBOT General Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html)

Add a CRN Service Name to the drop down list of available choices when creating a new ServiceNow Incident.

- Use command **[bot name] cie**
- Select **Add a CRN Service Name** from the list of actions.
- Complete the fields on the form and click submit.

----------------------

**Remove a CRN Service Name**

The following will be deprecated. Use **[bot name] crnservice add [service name]** instead. See 
[CIEBOT General Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html)

Remove a CRN Service Name from the drop down list of available choices when creating a new ServiceNow Incident.

- Use command **[bot name] cie**
- Select **Remove a CRN Service Name** from the list of actions.
- Complete the fields on the form and click submit.

----------------------

**Add an Incident to the Channel**

Add a ServiceNow Incident to the drop down list of known Incidents for the channel when selecting an action for an Incident.

- Use command **[bot name] cie**
- Select **Add an Incident** to the List from the list of actions.
- Complete the fields on the form and click submit.

----------------------

**Remove an Incident from the Channel**

Remove a ServiceNow Incident from the drop down list of known Incidents for the channel.

- Use command **[bot name] cie**
- Select **Remove an Incident** from the List from the list of actions.
- Complete the fields on the form and click submit.

----------------------

**Set Affected Activity Field for an Incident**

Update the Affected Activity Field for a ServiceNow Incident.

- Use command **[bot name] cie**
- Select **Update Affected Activity** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------
**Set Audience for an Incident**

A value of PRIVATE will invoke auto-targeting of notifications to customers, and a value of NONE will notify no customers.

- Use command **[bot name] cie**
- Select **Update Audience** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Make the selection and click submit.

----------------------

**Set Customer Impact Description Field for an Incident**

Update the Customer Impact Description Field for a ServiceNow Incident.

- Use command **[bot name] cie**
- Select **Update Customer Impact Description** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------

**Set Customers Impacted Field for an Incident**

Update the Customers Impacted Field for a ServiceNow Incident.

- Use command **[bot name] cie**
- Select **Update Customers Impacted** from the list of actions.
- Select an incident from the list. NOTE: Incidents are stored on a per Slack channel basis.
- Complete the fields on the form and click submit.

----------------------

**Show Incident Details**

Show details about the Incident by display the fields in Slack.

Command Format:

```
[bot name] cie [incident_id]
```
Examples:

```
[bot name] cie 24891
[bot name] cie INC0024891
```

----------------------

**Check Authorization**

The command `[bot name] cie auth [user email]` is deprecated. Use `[bot name] chkauth [user email]` instead.

See [CIEBOT General User Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#list-crn-sesrvice-name)


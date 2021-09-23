---
layout: default
description: Gobot User Guide
title: Gobot User Guide
service: ciebot
runbook-name: Gobot User Guide
tags: oss, ciebot
link: /ciebot/Gobot_User_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Gobot Overview

The intention of this bot is to improve operational efficiency by automating various processes by exposing various commands.

## Frequently Asked Questions

**Q: Where can I get info on the commands available in gobot?**

A: More details about the commands can be found in this document and by running **gobot help** in Slack.


### Help Command Processor Overview

Lists the Help command for each supported service.

Command Format:

```
gobot help
```

The following groups of commands are available on gobot and supported by bot team

- alias
- dutymgr
- iae
- link
- pd (pagerduty)
- ticket
- bot user commands: 
  - feedback
- bot administrator's commands: 
  - audit
  - notification

To get the Help for each group of commands, do
```
gobot alias help
gobot dutymgr help
...
```

### Alias Command Processor Overview
The alias command makes it possible to launch another bot command (inclusive of any arguments) by entering a string to represent your new command.

That is, it allows a user to create simple names or abbreviations (even consisting of just a single character) for bot commands regardless of how complex the original commands are and then use them in the same way that ordinary bot commands are used.

**Create an Alias**

New aliases are created on a per Slack channel basis. (ProTip: Direct message gobot to create your own personal command aliases.)

Command Format:

```
gobot alias [alias_name]=[bot_command]
```
Example (no arguments):

```
gobot alias p=ping
gobot p
```

Example (with arguments):
```
gobot alias create_issue=github issue create wdp-infra/tracker-test $1
gobot create_issue This is the title of my new github issue
```

**List Aliases**

List all aliases for the current Slack channel, and delete selected alias by press the Delete button.

Command Format:

```
gobot alias list
```


### Duty Manager Command Processor Overview

The dutymgr command provides a way to contact a duty manager

**Contact a duty manager**

Use an interactive form to contact a duty manger

Command Format:

```
gobot dutymgr
```
Select the action from the pulldown and fill in details.



### IAE Command Processor Overview

**Lookup**

Look up machines from iae production database.

Command Format:

```
gobot iae lookup [yp|lyp|lys1] [cluster url]
```

**clustercheck**

Check Ambari status for the cluster when provided with the id number

Command Format:

```
gobot iae clustercheck [yp|lyp|lys1] [cluster url]
```


### Link Command Processor Overview

The Link command links URLs to the channel

**Linking URL to channel**

Add a new URL with a description to the channel

Command Format:

```
gobot link [ url ] as [ description ]
```

**Show links**

Returns a list of all URL's saved in the channel.

Command Format:

```
gobot links
```

**Find a link**

Returns all URL's saved in the channel that match the keyword search.

Command Format:

```
gobot link find [regex|keyword]
```

Example:

```
gobot link find abc
```


### Pager Duty Command Processor Overview

The pagerduty command, `pd` for short, is for interacting with pagerduty incidents.

**Subscribe Pager Duty alerts**

Create a new pagerduty alert subscription for the channel

Command Format:

```
gobot [pd|pagerduty] subscribe [pagerduty_service_id]
```

**List Pager Duty subscriptions**

List all pagerduty alert subscriptions for the channel.

Command Format:

```
gobot [pd|pagerduty] subscriptions
```

**Snooze Pager Duty alerts**

Snooze one or more incidents for X minutes.

Command Format:

```
pd|pagerduty snooze <incident_number1, incident_number2, ... incident_numberN> <minutes>
```

Example:

```
gobot pd snooze 293844, 293845 30
```
 
**Acknowledge and snooze Pager Duty alerts**

Acknowledge and snooze one or more incidents for X minutes.

```
pd|pagerduty ignore <incident_number1, incident_number2, ... incident_numberN> <minutes>
```

Example:

```
gobot pd ignore 293844, 293845 30
```
 
**Reassign Pager Duty alerts**

Assign one or more incidents to a user.

```
pd|pagerduty assign <incident_number1, incident_number2, ... incident_numberN> @user
```

Example:

```
gobot pd assign 293844, 293845 @slackuser
```
 
**Add note to Pager Duty alerts**

Add a note to one or more pagerduty incidents.

```
pd|pagerduty note <incident_number1, incident_number2, ... incident_numberN> <text>
```

Example:

```
gobot pd note 293844 my comment text here
gobot pd note 293844, 293845 my single note added to multiple incidents
```

**Get notes for Pager Duty alerts**

Get all pagerduty notes for an incident.

```
pd|pagerduty notes <incident_number>
```

Example:

```
gobot pd notes 293844
```

**Get details for Pager Duty alerts**

Get details about a pagerduty incident.

```
pd|pagerduty incident <incident_number>
```

Example:

```
gobot pd incident 293844
```

**Acknowledge Pager Duty alerts**

Acknowledge one or more pagerduty incidents.

```
pd|pagerduty ack <incident_number1 incident_number2 ... incident_number3>
```

Example:

```
gobot pd ack 293844 293845
```

**Resolve Pager Duty alerts**

Resolve one or more pagerduty incidents.

```
pd|pagerduty res <incident_number1 incident_number2 ... incident_number3>
```

Example:

```
gobot pd res 293844 293845
```

**Acknowledge my Pager Duty alerts**

Acknowledge one or more pagerduty incidents owned by me.  NOTE: If the user has an alter ego set for pagerduty it will use that instead of their email defined in slack.

```
pd|pagerduty me ack!
```

Example:

```
gobot pd me ack!
```

**Resolve my Pager Duty alerts**

Resolve one or more pagerduty incidents owned by me.  NOTE: If the user has an alter ego set for pagerduty it will use that instead of their email defined in slack.

```
pd|pagerduty me res!
```

Example:

```
gobot pd me res!
```

**List my Pager Duty alerts**

Display all pagerduty incidents owned by me.  NOTE: If the user has an alter ego set for pagerduty it will use that instead of their email defined in slack.

```
pd|pagerduty me
```

Example:

```
gobot pd me
```

**List Pager Duty alerts by email**

Display all pagerduty incidents owned by the specified email.

```
pd|pagerduty user [email]
```

Example:

```
gobot pd user gobot@us.ibm.com
```

**List Pager Duty alerts by email**

Display all pagerduty incidents for my team.  NOTE: all incidents will be displayed, you have to provide a list of pagerduty services to mike@us.ibm.com to limit the results returned.

```
pd|pagerduty incidents
```

Example:

```
gobot pd incidents
```

**Ask who is on calll**

Returns a list of all WDP pagerduty schedules by service.

```
whos on call
```

Example:

```
gobot whos on call
```

**Ask who is on calll with filter**

Returns a list of WDP pagerduty schedules that match the regex.

```
whos on call <regex filter>
```

Example:

```
gobot whos on call dashdb
```


### Ticket Command Processor Overview

The ticket command creates, lists, and modifies tickets in a repository, such as issiues in github repo.

**Ticket configuration**

Open the ticket config interactive menu in Slack to list or create ticket definitions.

Command Format:

```
gobot ticket config
```

**Create a ticket**

Use interactive dialogs to create a github issue.

Command Format:

```
gobot ticket
```


###  Feedback Command Processor Overview

This command allows you to open a ticket for feature requests and to report issues directly to the dev team.

**Submit a Feedback**

Creates a new Github issue for the specified application in the drop down list.

Command Format:

```
gobot feedback
```

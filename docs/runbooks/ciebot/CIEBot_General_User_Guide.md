---
layout: default
description: CIEBOT General User Guide
title: CIEBOT General User Guide
service: ciebot
runbook-name: CIEBOT General User Guide
tags: oss, ciebot
link: /ciebot/CIEBot_General_User_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

# Overview

The **ciebot** has been installed in *IBM Cloud Platform*, *IBM Watson Data Platform*, *Cloud Incident Management*, and *IBM Data & AI* slack workspaces.

The **ciebot** supports Incident Management activities for CIEs and Bastion Connections using Slack.
Specific user guides are available for [CIE](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html) and [Bastion Connection](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_INCB_User_Guide.html).

Most of the CIE and Bastion Connection related activities require the user to be authenticated by Platform API User Group. 
For getting access, see [Authentication Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html). 

Platform API authentication is done every time a TIP API is being called. Each validation is effective for one hour. 

The **ciebot** bot supports commands starting with **cie**, and **incb**, and other commands shared by all bot users. See [**CIE guide**](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html) and [**INCB guide**](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_INCB_User_Guide.html), All shared commonds are described below.

Two bots are supported. 
**ciebot** is for production, and is connected to production Service Now. 
**cietest** runs in a staging cluster, connected to test Service Now, and is there for practicing. Use slack channel [ciebot-practice](https://ibm-cloudplatform.slack.com/archives/C9WA5T2PJ) in *IBM Cloud Platform* or *IBM Watson Data Platform* to learn how to use the production bot by issuing commands starting with **cietest** instead of **ciebot**.

# ciebot-level Commands

In the following, **[@bot name]** is the name of the slack bot/app you are using, such as **ciebot**, **cietest**, etc.


## Supported commands:

----------------------

### Help

Get a short message for bot-level commands (describe in this document)
```
[@bot name] help
```

Get a short message for [cie commands](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_CIE_User_Guide.html)
```
[@bot name] help cie
```

Get a short message for [incb commands](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_INCB_User_Guide.html)
```
[@bot name] help incb
```

----------------------

### Feedback

If you find a defect, have a requirement or suggestion, submit a github ticket to ciebot developers.

```
[@bot name] feedback
```

Set a title and fill in the details. Once summitted, the development team will be notified. 

----------------------

### Who is on Call

Find who is on call to support this bot.

```
[@bot name] whos oncall
```

----------------------

## Authentication

New users of ciebot must make a request to become a Platform API User in order to run the commands. The following command is used to check if the user have all the required permission.

For more information related to authentication, see [Authentication Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html)

----------------------

### Check Authorization

Check if the current slack user or another user is authorized to use the bot for incident management actions.

Command Format, specify a user email to check for that user; otherwise check for the current user: 

```
[@bot name] chkauth [user email]
```
Examples:

```
[@bot name] chkauth
[@bot name] chkauth user.name@country.ibm.com
```

These commands used to be called *cie auth*

----------------------

## CRN Service Name

All *cie* and *incb* incidents belong to a known *CRN Service*. When creating an incident, a valid CRN Service Name must be provided. 
There is a large number of CRN service names, and the list may change from time to time, although not constantly.
However, a single user should only need a few service names. 

For this reason, each Slack channel keeps its own short list of service names. 
For the sake of efficiency, when a slack command is run, there is no validation of the input service name.
If the service name turns out to be invalid, the command returns an error.

The following commands can be used to list, add, and remove CRN Service Names in the channel from which the command is issued. 
When starting a new channel, or anticipating a new CRN Service, it is recommended to add the CRN Service Name using the *add* action.

Under *cie* command, there used to be a way to add or remove a Service Name to/from the channel-specific list. The old action has been removed from the _cie_ menu.

----------------------

### List CRN Service Name

Get the list of CRN Service Names kept for the current channel, as well as examples of many other CRN Service Names in case you may need to add one.

```
[@bot name] crnservice list
```

----------------------

### Add a CRN Service Name

Add a CRN Service Name to the channel specific list, which will be used for the drop-down when creating a new Service Now incident (*CIE* or *Bastion Connection*)

```
[@bot name] crnservice add [name]
```

----------------------
### Remove a CRN Service Name

Remove a CRN Service Name from the list kept for the channel. Do this if a previously added service name is no longer valid or needed.

```
[@bot name] crnservice remove [name]
```

----------------------

## Administrator commands

Only available to bot developers.


----------------------

**Audit**

Used by bot admins to get a summary of bot commands executed by a bot.

For more details, see [Audit guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Dev_Manual.html#audit)

```
[bot name] audit command [bot name]
```
----------------------

**Notification**

Used by bot admins to send messages to some or all channels of all Slack workspaces in which a bot is a member of. Refer to https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Bot_Notification.html

For more details, see [Notification guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Dev_Manual.html#notification)

```
[bot name] notification
```
----------------------

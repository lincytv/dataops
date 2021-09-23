---
layout: default
description: CIEBOT INC User Guide
title: CIEBOT INCB User Guide
service: ciebot
runbook-name: CIEBOT INCB User Guide
tags: oss, ciebot
link: /ciebot/CIEBot_INCB_User_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Overview

This document is intended to be used in conjunction with [CIEBOT General Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html).

The **incb** commands used on *ciebot* allow users to quickly open a Bastion connection.
To get started, each team would need to do:

- Have every user of *incb* to request TIP Platform API Usage. Refer to [steps to request](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html) and [use chkauth to verify](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#check-authorization).
- Create a channel in one the Slack workspaces in which *ciebot* is installed. Invite *ciebot* to the channel.
- Add the name of CRN services you will work on to the channel. See the [crnservice commands](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#list-crn-service-name). This list can be populated later.

Then the routine steps: Create a Bastion connection using a dialog, or command line; close a connection using command line.


![]({{site.baseurl}}/docs/runbooks/ciebot/images/incb.png){:width="700px" height="400px"}


## INCB Commands

**Ceate a Bastion Connection**

Start with command

```
[@bot name] incb
```

If you have not logged into *ciebot* during the past hour, you will be prompted. See [Login Before Working with Incidents](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html). If you have aleady logged in, then you get to *click a button to create incident in dialog* or type *incb create -s [service-name] -e [environment] -j [justification] (-a [assignment-group])* to run the command line.

If you use the dialog, there are three mandatory fields: CRN service name (choose from a list), Environment (chose from a list), and Justification (free form text).

- The CRN service name must be a valid Configeration Item. If the drop down list does not include your Configuration Item, Get out of the dialog. Add your service name to the list for the channel by one using the [**crnservice add**](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#add-a-crn-service-name) command. Then run **incb** again.
- Choose an environment for the connection you want to create. If your exact environment is not in the list, pick the closest one, and clarify in the justification field. Optionally, you may open a [**feedback**](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#feedback) for development to update the list.
- The justification field is for your reason for the Bastion Connection.

The last text entry for **Assignment group** is *optional*. When creating a Service Now incident, the assignment group is automatically set based on the *Configuration Item*, aka *CRN Service Name*. You need to enter a valid *Assignment Group* name *only if* you know the default *Assignment Group* for your *Service* is not what you need for the Bastion connection.
The *Assignment Group* must be entered exactly the same as defined in Service Now.

----------------------

The command line could be faster for creating a Bastion Connection.

```
[@bot name] incb create -s [service-name] -e [environment] -j [justification] (-a [assignment group])
```
Examples
```
@ciebot incb create -s your-service-name -e toronto -j Here is my justification
@cietest incb create  -e toronoto 02 -j here is a justification -s valid-name -a my team
@ciebot incb create -j here is my reason for the incident -s my-service -e TORONTO01 
@ciebot incb create -s service-123 -e XYZ data center 01 -a ABC Support Team -j a good reason
```

where
- The *service-name* must be a valid CRN Service Name. The *ciebot* does not validate the input name. If the name is invalid, Service Now will give an exception.
- The *environment* must be a valid location. The *ciebot* keeps a static list of known environment locations, however the list may not be up to date or complete. If your exact environment is not in the list, input a close one, and clarify in the justification field. Optionally, you may open a [**feedback**](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html#feedback) for development to update the list.
- The *justification* field is for your reason for the Bastion Connection. The justification text can be anything except "-s", "-e", "-j", "-a" and newline. No quotes needed.
- The *Assignment group* is optional, and must be a valid pre-defined group name, enter exactly the same spelling as in Service Now.
- The parameters can come in any order.

----------------------

**Get info of a Bastion Connection**

Get more information about a Bastion Connection with the given incident number:

```
[@bot name] incb (INC)nnnnnnn
```

The following details will be shown: 
- Short description which contains the environment name
- Service name
- Creation time
- Current state
- Justification

Note: due to API limitation, Assignment Group name is not shown. It can be seen in Service Now.

If the connection is still active (incident is not in _resolved_ state), there will be a button to `Close connection`.

----------------------

**List active Bastion Connections**

List all _active_ Bastion Connections for a given CRN service name:

```
[@bot name] incb list [service-name]
```
Example
```
@ciebot incb list pnp-api-oss
```

If the given service name is unknown, return an empty list.
Otherwise, a list of incident information will be shown in a thread, each incident with a button to `Close connection`.

----------------------

**Close a Bastion Connection**

Close a Bastion Connection with incident number:

```
[@bot name] incb close (INC)nnnnnnn
```

The user must provide an incident number representing a Bastion Connection. 
The Service Now incident will be resolved.
**Caution:** The action will resolve the given Service Now incident, even if it is not a Bastion connection. If you are not sure about the incident ID, run **incb (INC)nnnnnnn** which will show more info about the ID, and will provide a button to close the connection if it is an active Bastion Connection.

----------------------

**List environment locations**

The environment names are there to help command line users when creating a Bastion Connection.

```
[@bot name] incb env list
```

---
layout: default
description: EU Emergency Process Revoke User Privilege Failure.
title: "EU Emergency Process Revoke User Privilege Failure"
service: doctor
runbook-name: EU Emergency Process Revoke User Privilege Failure
tags: oss, bluemix, doctor, AccessHub
link: /doctor/Runbook_EU_Emergency_Process_Revoke_User_Privilege_Failure_AH.html
type: Alert
---


{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert happens when AccessHub execute revoke task failed, it will not be resolved automatically, **if the problem is fixed please resolve it manually**. 

## Instructions to Fix

 - Find the task id from the detail of the PagerDuty alert. e.g. 

```
Some error happened when execute Accesshub revoke <TASK_ID>
```

 - Go to slack channel #accesshub_ask .
 - Post a message in this channel about this issue. e.g.

```
Hi, we have a revoke task failed on production environment of AccessHub, the task id is <TASK_ID>, please help to take a look.
```

  Replace TASK_ID with the real one got from the first step.

 - If no one help to take a look this issue from slack channel, please open a ticket [here](https://w3.ibm.com/help/#/article/accesshub).
 - Find `contact support` link on this page, click on it.
 - Click `Create Ticket` button.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/create-ticket-AH.png){:width="640px"}

 - Input the issue with task id in `Description` part, then click `Submit` button. e.g. 

```
We have a revoke task failed on production environment of AccessHub, the task id is <TASK_ID>, please help to take a look.
``` 

  Replace TASK_ID with the real one got from the first step.

 - You can find the ticket ID on the pop-up window, please copy this ID and post a message to #accesshub_ask channel. e.g. 

```Hi, can anyone help to look into this ticket <TICKET_ID>```

 - Once the problem is fixed, please resolve it manually.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

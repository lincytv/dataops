---
layout: default
description: EU Emergency Process Refresh AccessHub Token Failure.
title: "EU Emergency Process Refresh AccessHub Token Failure"
service: doctor
runbook-name: EU Emergency Process Refresh AccessHub Token Failure
tags: oss, bluemix, doctor, AccessHub
link: /doctor/Runbook_EU_Emergency_Process_Refresh_AccessHub_Token_Failure.html
type: Alert
---


{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert happens when refresh AccessHub token failed. 

## Instructions to Fix

Please open a ticket to Accesshub team.

 - Open a ticket [here](https://w3.ibm.com/help/#/article/accesshub).
 - Find `contact support` link on this page, click on it.
 - Click `Create Ticket` button.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/create-ticket-AH.png){:width="640px"}

 - Input following content in `Description` part, then click `Submit` button. 

```
Using Doctor functional ID (eudoctor.eudoctor@it.ibm.com/Y9D47S758) request AH production token failed, when make API call on "/ECM/api/login". 
The API call to AH production needs a token for authentication. It failed when requesting the token for Doctor EU functional ID.This failure directly impacts IBM's ability to support IBM Cloud EU customers. This failure directly impacts IBM's ability to support IBM Cloud EU customers. Until this is resolved, the ability to grant IBM Cloud personnel not located within the EU, emergency access to resolve issues in customer environments is broken.This  have direct NPS impacts.This is urgent issue,please resovle ASAP.
``` 

 - You can find the ticket ID on the pop-up window, please copy this ID and post a message to #accesshub_ask channel. e.g. 

```Hi, can anyone help to look into this ticket <TICKET_ID>```

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

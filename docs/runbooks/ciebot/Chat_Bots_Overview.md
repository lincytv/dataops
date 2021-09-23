---
layout: default
description: Chat Bots Overview
title: Chat Bots Overview
service: ciebot
runbook-name: Chat Bots Overview
tags: oss, ciebot
link: /ciebot/Chat_Bots_Overview.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

# Bots
The OSS bot development team inherited two bots, **ciebot** and **gobot** and made them officially supported apps for IBM community. They are compliant with Service Framework and security requirement.
The **ciebot** is a handy tool to quickly manage CIEs, replacing Service Now for some common quick actions; The **gobot** provides a set of tools related to Pager Duty, and tools like links and aliases. The slack-consumer and webhook of *gobot* allow other services to plug in their microservices. 
A few other bots serve as staging or development for the two production bots.

| Bot Name | Environment | Regions               | HA & LB   | Function                                               |
|----------|-------------|-----------------------|-----------|--------------------------------------------------------|
| ciebot   | production  | useast, ussouth, eude | automated | Service Now actions related to (1) CIE/incident management (2) Bastion Connection actions|
| gobot    | production  | useast, ussouth, eude | manual    | Various tools related to PagerDuty, alias, links, duty manager, tickets etc.      |
| ciebotwdp| production  | useast                | no        | Sandbox & backup for ciebot and gobot during emergency |
| cietest  | staging     | useast                | no        | Let users practice for ciebot actions                  |
| cietest1 | staging     | useast, ussouth, eude | manual    | Sandbox for ciebot and gobot developers                |
| ciedev1  | develoment  | useast                | no.       | Sandbox for ciebot and gobot developers                |


## Bot and Slack Workspaces 
| Bot Name | Slack Workspace                                                             |
|----------|-----------------------------------------------------------------------------|
| ciebot   | [Watson Data Platform](watsondataplatform.slack.com) , [IBM Cloud Platform](ibm-cloudplatform.slack.com) , [Cloud Incident Manager](ibm-cim.slack.com) , [IBM Data & AI](ibm-analytics.slack.com) |
| gobot    | [Watson Data Platform](watsondataplatform.slack.com) , [IBM Cloud Platform](ibm-cloudplatform.slack.com) |
| ciebotwdp| [IBM Cloud Platform](ibm-cloudplatform.slack.com) |
| cietest  | [IBM Cloud Platform](ibm-cloudplatform.slack.com) |
| cietest1 | [Cloud OSS Platform](cloud-oss-platform.slack.com) |
| ciedev1  | [Cloud OSS Platform](cloud-oss-platform.slack.com) |

## Bot Workflow and Overview

A bot needs at least three micro-services, running in the `ciebot` namespace and in the various Kubernetes clusters.
- slack-consumer to receive slask commands and put into a message queue;
- incoming-webhook to interact with user through dialogs, and put responses into the message queue;
- handler or processor to take messges from the queue, process the message, and respond in slack
To provide more services, more handlers or processors can be added, all share the same slack-consumer and incoming-webhook.
The handler may need a database to store data; and may interact with other external application.
CIEBbot commands will be executed after the user is authenticated through IAM services.

Workflow of a single handler:
![]({{site.baseurl}}/docs/runbooks/ciebot/images/bots_workflow.png){:width="700px" height="400px"}

All supported production bots and services (the image below was made on January 19, 2021. New services may be added afterwards):
![]({{site.baseurl}}/docs/runbooks/ciebot/images/bots_overview.png){:width="700px" height="400px"}


## Utilities

In addition to CIE/incident management, and various functions provided by Gobot, a few tools and utilities are provided.

- Chkauth: check access right to bot function for self or for another user.
- Feedback: for users to conveniently raise concerns or ask questions about the bot using the bot.
- Audit: keep track of usage of commands, helping management to prioritize.
- Notification: send message to multiple channels a bot is a member of.
- List channels: list all channels a bot is a member of in all slack workspaces.
- Slack app installer: install a slack app already in Slack workspace A into workspace B. Details at [Slack App Installer](https://github.ibm.com/aria/slack-app-installer/blob/master/README.md)


## Development

The code base for the bots is Node JS, stored in https://github.ibm.com/aria, and built and deployed by the OSS CICD process.

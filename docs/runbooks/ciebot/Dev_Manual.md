---
layout: default
description: Internal design and utilities for bot admins and developers
title: Bot Developer Manual
service: ciebot
runbook-name: Bot Developer's Manual
tags: oss, ciebot, gobot
link: /ciebot/Dev_Manual.html
type: Informational
---


## Table of Content

- [Notification](#notification): List channels, send messages, and notification history
- [Audit Command](#audit-command)
- [Modify CRN Service Name List](#modify-crn-service-name-list)
- [Slack App Installer](#slack-app-installer)
- [CICD](#cicd)
- [Bot Configuration](#bot-configuration)
- [Rabbit MQ Credential and Debugging](#rabbit-mq-credential-and-debugging) 
- [Mongo DB](#mongo-db)
- [Authentication](#authentication)

## Notification

Use the command to send messages to some or all channels in each Slack workspace in which a bot is a member of.

This command is available only to bot admins, and the admin list is stored Cloudant.

### Notification actions

The following actions are supported:

- **Create template**: Start a new draft message to be used for future notifications.
- **Delete template**: Delete a previously created template by selecting a template name.
- **List channels**: List all channels the selected bot is a member of.
- **List notification history**: List all notifications sent for all bots. (Currently there is no filter.) 
- **Modify template**: Edit an existing template by selecting a template name.
- **Send notification**: Send a notification; a dialog will be opened for selecting options.

### Notification template

This is a _sample_ template for the *notification* command.

A notification template contains the text of the notification.
To format the text, refer to <https://api.slack.com/reference/surfaces/formatting|Slack API: Formatting text>. For example:

- `_italic_` produces _italicized_ text
- `*bold*` produces **bold** text
- `~strike~` produces ~strikethrough~ text
- `<http://www.foo.com|text for link>` gives a [hyperlink](http://www.foo.com)

Refer to slack channels and users by their IDs, this way will result in a clickable link:

- `<#C9WA5T2PJ>` refers to the <#C9WA5T2PJ> (Slack channel #ciebot-practice)
- `<#C8GS7RAER>` refers to the <#C8GS7RAER> (Slack channel #cie-bot-dev)
- `<@WLFV2QLHJ>` refers to <@WLFV2QLHJ> (Slack user Crystal)
- `<@W4DL6RQLR>` refers to <@W4DL6RQLR> (Slack user Hui)

Refer to Slack channels and users the usaul way will not result in a clickable link

- `#cie-bot-dev` for the #cie-bot-dev channel, will not get <#C8GS7RAER>
- `@crystals` for the user @crystals, will not get <@WLFV2QLHJ>

Last but not least, *never* do `@here`, or `!here` surrounded by angle brackets. It will drive Slack users crazy!

Notification templates are stored in Cloudant DBs. All production bots share the same set of production templates; Similarly for staging and dev.

### List channels

Before sending a notification, a user might want to get a complete list of channels a bot is a member of.

### Send a notification

To make a notification, ssue `@[botname] notification`, then

- select action `Send notification`
- select a bot (default to the bot running the notification command), notification will be sent to channels in which the bot is a member 
- select a template by name, modify content if necessary (you have to have created a template earlier)
- specify when the notification is to be sent. The time zone is the user's local time zone
- specify channels the notification will be sent to (use channels names or channel slack IDs)

### Select a bot

In the **List channels** action and the **Send notification** dialog, there are the select bot dropdown.
Normally, if you need to send notification for bot-x, run the notification commands on bot-x, and the bot selection dropdown  only contains bot-x.
If bot-x is down, you may use bot-y to send notification or list channel regarding bot-x, after doing the following

- add the Slack tokens of bot-x into the SLACK-TOKENS environment variable of bot-y
- restart the service _miscellaneous-commands-processor_ of bot-y. 

### Notification history

Run the command to see notifications sent before.

## Audit

The following commands are supported:

- `ciebot audit command [bot-name] ([subCommand]) (since [YYYY-MM-DD] (until [YYYY-MM-DD]|now))` To list within the slack conversation a summary of usage frequency of commands on a specified bot.
- `ciebot audit export [bot-name] ([subCommand]) (since [YYYY-MM-DD] (until [YYYY-MM-DD]|now)) ` To export to a CSV file the invacation history of commands on a specified bot.

Specify the following if desired:

- a specific command
- starting date
- ending date

Example: 
```
@ciebot audit command ciebot incb since 2021-08-11 until 2021-08-12
``` 

If the *bot-name* is not the bot you are running the command from, you may need to add the slack tokens. See [Select a bot](#select-a-bot) above for more info.

## Modify CRN Service Name List

To add or remove a CRN service name to/from the sample CRN service name list for all channels, e.g. the list obtained by "crnservice list", run `crnservice [add | remove] global [service-name]`.


## Slack App Installer

This is a [service](https://github.ibm.com/aria/slack-app-installer) to install a slack app already in slack workspace A into slack workspace B.

This service makes use of the Cloudant DB to store slack tokens.

## CICD

Due to the number of services being supported, and tripling for HA, a large number of [helm charts](https://github.ibm.com/cloud-sre/oss-charts) are needed.

- Charts for all bot which does not support HA *ciedev1*, *cietest*, and *ciebotwdp* are in https://github.ibm.com/cloud-sre/oss-charts/ciebot-bots-*
- Charts for *cietest1* are in https://github.ibm.com/cloud-sre/oss-charts/ciebot-cietest1-*
- Charts for *cietbot* are in https://github.ibm.com/cloud-sre/oss-charts/ciebot-ciebot-*
- Charts for *gobot* are in https://github.ibm.com/cloud-sre/oss-charts/ciebot-gobot-*

## Bot Configuration

Configure bots at https://api.slack.com/apps/. 
For bots supporting HA, adjust `Interactivity & Shortcuts --> Request URL` and `Event Subscription --> Request URL` to use a global URL (enable HA) or a regional URL (disable HA).


## Rabbit MQ Credential and Debugging

Each bot running in each region and environment uses its own RabbitMQ instance.
The RMQ instances can be found from [cloud portal](https://cloud.ibm.com/services), look for 
- dev-eude-rabbitmq-shared
- dev-useast-rabbitmq-shared
- dev-ussouth-rabbitmq-shared
- prod-eude-rabbitmq-shared
- prod-useast-rabbitmq-shared
- prod-ussouth-rabbitmq-shared
- test-eude-rabbitmq-shared
- test-useast-rabbitmq-canopus
- test-useast-rabbitmq-shared

Under **service credentials**, 
- service-credential-xxx-**interactive**-rabbitmq-xxx is for managing the RMQ instance interactively
- service-credential-xxx-**shared**-rabbitmq-xxx is credentials used by the bot code
- service-credential-xxx-**XXX**-rabbitmq-xxx	is credentials created for microservices owned by team XXX working with our bot infrastructure

Use the interactive portal to investigate queue issues:

Check message queue size and if there is any activity in "Message rates" when interacting with the bot in a Slack channel.
The queue exchange names are `aria.[botname].event_hub` and quene names are `aria.[name of the microservice]`

Also check the exchange named `aria.dead_letters` and dead letters there. If there is a big number of messages in a dead letter queue, manually purge the queue, then check if the deadletter consumer for the queue is working.

If the kubernetes pod log shows any problem related to a RMQ queue, try purging the queue, deleting the queue, and as the last resort, deleting the exchange. After the rmq clean up, restart the pod.


## Cloudant DB

All bots running in the same environment share the same Cloudant DB instance.
The Cloudant instances can be found from [cloud portal](https://cloud.ibm.com/services), look for 
- dev-ussouth-cloudant-shared-public
- test-ussouth-cloudant-shared-public
- prod-ussouth-cloudant-shared-public

## Authentication

Regarding authentication and request for access, see [CIEBot Authorizaton Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html).





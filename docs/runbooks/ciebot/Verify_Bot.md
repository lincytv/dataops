---
layout: default
description: How to verify if a bot is working
title: How to verify bot is working
service: gobot
runbook-name: Verify bot
tags: oss,gobot
link: /ciebot/Verify_Bot.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}


## Purpose
When a bot stops responding, this guide provides instructio on identifying the possible cause. 

## Components
- Slack consumer: communicate with slack and RMQ , supported by OSS development team
- Service handlers: handle business logic for slack command, supported by service team 
- Rabbit MQ: message bus provided by OSS development team
- @aria/microservice-lib: library working with RMQ, supported by OSS development team

## Description
* Slack consumer is a core service for a bot, it's the first and the only component that receives message from Slack, then passes the message to service handlers. So if a slack consumer works well, then we can say the error comes from service handler. 
* One slack consumer deployment can only work with one slack workspace, so we have several slack consumer instances deployed, one for each workspace 
* Another core resource in bot is Rabbit MQ, all communication between bot components work through RMQ, they must listen on the same channel (bound to the same exchange)


## Verify Slack Consumer
#### Option 1： 
1. The quickest and most straitforward method is to check another service running on the same bot
  > note: please verify the command in same work space or channel.
 - There are simple commands like `help`, `links`, `feedback`.... which don't require any additional parameter. If any command works, then we can say slack consumer is working correctly. 
 - All bot commands can be found at [CIEBot CIE user guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_CIE_User_Guide.html), [CIEBot INCB user guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_INCB_User_Guide.html and [Gobot user guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Gobot_User_Guide.html).
 

#### Option 2:
##### Check slack consumer log
1. If you are an OSS developer, go to the cluster, check the log of the corresponding slack consumer pod. If there is an error about RMQ connection, delete the pod and check the log again to make sure slack-consumer is restarted successfully.
2. If there is no error in slack consumer, send a message in slack to the bot, there should have an output in slack consumer pod's log. If there is no log, contact bot developer to fix it
##### Check Rabbit MQ for Slack consumer
3. If you cannot access slack-consumer pod or no issue found after checking pod's log, go to RabbitMQ admin portal to check if the message was consumed by slack-consumer. 
    1. Open below link according the bot you are working on 
     * gobot:
       https://98b11776-9b5d-4ad6-82a7-536ece8d063a.66c11f9786bc40cfa3a0086f6582f2e7.databases.appdomain.cloud:30138/
     * ciedev1: https://2904572b-72ae-48ab-8a1c-f3940521b33e.brjdfmfw09op3teml03g.databases.appdomain.cloud:32689/
     * cietest1: https://37a23ec5-63c5-4c3e-9c5f-511dff24d742.bn2a0fgd0tu045vmv2i0.databases.appdomain.cloud:30206/
    2. In the RMQ admin page, click on Queue, find the queue with name like "slack-consumer", check if the messages total is "0" . If not, then slack-consumer must have an issue， contact gobot developer to fix it. 
    
## Check service handler
If the slack consumer is working well, you need to check the queue and code for your handler service.
1. First check if the queue exists. It should have been created when the service was starting. You can delete it using RMQ admin portal, then restart your service handler to recreate it
2. Then check if the queue is bound to the correct exchange; the exchange name should be `aria.[botName].event-hub`. If it's not correct, check your env file, there should be a BOT_NAME defined with current bot name as value. 
3. Also, please make sure your dependency @aria/microservice-lib is at version 0.3.3 or above. If not, please update packages.json and remove the old code in node_modules, then re-install it by running command `npm install`
4. When issue a command to bot in slack, if there are messages left in the queue, it means that your service handler is not picking up the messages. Please check for any error when your service starts or check the connectivity with RMQ.
5. If there is no message left in the queue, there should be some output in your service handler when issue command to bot, check the detail in log.

## Reference
[Various user guides](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/runbooks.html#ciebot)

## Contact
 * Hui WH Wang/China/IBM
 * Crystal Su/Toronto/IBM
 * Ali Hussain/Toronto/IBM
 * Management: Jing You/China/IBM
 * Slack channel [#cie-bot-dev](https://ibm-cloudplatform.slack.com/archives/C8GS7RAER)
 

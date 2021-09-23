---
layout: default
description: CIEBot Gobot Alerts
title: CIEBot Gobot Incidents
service: ciebot
runbook-name: Runbook CIEBot Gobot Incidents
tags: oss, edb, ciebot, gobot
link: /ciebot/Runbook_CIEBot.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}


## Purpose
Use this runbook to confirm and resolve the issue.
Contact a developer ( {% include contact.html slack=oss-ciebot-slack name=oss-ciebot-name userid=oss-ciebot-userid notesid=oss-ciebot-notesid%} or {% include contact.html slack=oss-ciebot-2-slack name=oss-ciebot-2-name userid=oss-ciebot-2-userid notesid=oss-ciebot-2-notesid%} ) if the steps here isn't sufficient to resolve the problem, or if the instruction says to contact a developer.

## User Impact
The impact depends on the nature of the problem.
The alert indicates one of the following issues:
* The bot is not running
* The bot doesn't respond to slack commands
* The bot responds incorrectly
* The bot responds with an access failure

## Incidents covered by this runbook
Bot monitors are documented [here](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Bots_Auto_Tests.html). There are the following categories:
* Bot end-to-end test failure from EDB `Alert generated via EDB on Bot health test failure`
* The slack-consumer external URL not responding `[bot]-[region]-[env]-consumer`
* The incoming-webhook external URL not responding  `[bot]-[region]-[env]-webhooks`
* A bot handler heartbeat is absent `[Env]-[region]-[bot]-[handler]`
* Rabbit MQ URL check failure `[Env]-[region]-rabbitmq-queue-check-failed`
* Deadletter-consumer not in Running state `k8s:[cluster]:ciebot:pod:[bot]-[service]-deadletter-consumer-*`


## Frequent Asked Questions in Slack

### Q1: Bots actions very slow, dialog doesn't come up
A1: It is most likely a RMQ or MongoDB problem. Look at the the log for clue. Anyway, it doesn't hurt to delete the affected pods so that the new pods will try to reconnect.

If deleting the pod does not fix the problem related to RMQ or Mongo, contact the oss team; you can start from ( {% include contact.html slack=oss-ciebot-slack name=oss-ciebot-name userid=oss-ciebot-userid notesid=oss-ciebot-notesid%} or {% include contact.html slack=oss-ciebot-2-slack name=oss-ciebot-2-name userid=oss-ciebot-2-userid notesid=oss-ciebot-2-notesid%} )

### Q2: Authentication and access related questions
A2: Refer to [User Authenticate Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Runbook_CIEBot_User_Authentication.html). If an access request is delayed, ask the user to followup with the next approver in the request. 

## Problem description and confirmation

#### Incident related to production bots

Both **gobot** and **ciebot** are running in production environment. During alert investigation and verification, please avoid actions resulting in modifying the state of the back end.

**Special note about incident related to the production ciebot**

```diff
- Try the scenario using @cietest first if possible
- If you don't have to, don't run @ciebot commands.
- If you have to use @ciebot, stick to actions not altering the incident (create, resolve, change severity, ...), such as `@ciebot cie INCnnnnnnn` or `@ciebot crnservice` etc.
```

#### Kubernetes

The following instruction for fixing the problems involve the `kubectl` command. If you are new to Kubernetes, refer to [Configure kubectl to connect to specific regions](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/ibm/Configuring_kubectl_all_regions.html)

Usually what an on-call person needs to do is to delete the problematic pod and wait for Kubernetes to recreate the pod.
If you do not have right to delete the pod, contact developers.

#### Slack

Use the _IBM Cloud Platform_ Slack workspace to verify Slack bot behavior, since all supported bots are installed in this workspace, and can be invited to any channel.

To confirm a reported problem in Slack, you can Direct Message with a bot to avoid disurbing a public channel, or use the designated channel [#ciebot-practice](https://ibm-cloudplatform.slack.com/archives/C9WA5T2PJ).

#### Commands to fix the peoblem
Get the bot name from the alert title or description. It should be one of `ciebot`, `gobot`, `cietest`, `ciebotwdp`, `cietest1`, `ciedev1`.

In the following instructions, replace `[bot]` in command examples with the action bot name found form the alert. So for `@[bot] help`, the command is `@ciebot help` or `@gobot help` etc.

Run the commands as described as needed. If you do not have authority to execute the commands, contact a bot developer.

### 1. Bot end-to-end test failure from EDB `Alert generated via EDB on Bot health test failure`

#### Problem description:
When using an independent tester to send a slack command to the slack channel [#bot-liveliness](https://ibm-cloudplatform.slack.com/archives/C01QPPBBQG2), one of the follow happened:
- there was no response in the Slack channel
- the response took longer than expected time to arrive
- the response did not contain the expected content. 
An error message was sent to EDB, and triggered TIP to raise the alert.

Which bot is having the problem? What was the command sent to slack?
Look for the _ServiceInput: [bot_name] [help|whos oncall oss platform]_ in the _Description_ of the Pager Duty alert, that tells the bot name, as well as the command.

#### Confirmation
Go to slack channel [#bot-liveliness](https://ibm-cloudplatform.slack.com/archives/C01QPPBBQG2) and do `@[bot_name] help` or `@[bot_name] whos oncall oss platform`.
If the response comes in quickly (currently set within 3 seconds for help and 8 seconds for whos-oncall), then there is no issue any more. The alert should resolve on its own.
If there is no response or the response comes noticablly slow, proceed to fix.

#### Fix
In each cluster, there are three pods being tested during the end to end test. 
The ciebot has HA and LB enabled therefore may be running in any of the three production regions, the problem could be from any region.
The gobot usually runs in us-south, but when there is a problem in us-south, gobot would run from either us-east or eu-de. So try to fix us-south first.

Here are the pods to be deleted

| Command | Bot      | Cluster    | Pod 1 to delete              | Pod 2 to delete              | Pod 3 to delete |
|------|----------|------------|------------------------------|------------------------------|------------------------------|
| help | ciebot | us-south-prod, us-east-prod, eu-de-prod | ciebot-handler-* | ciebot-slack-consumer-* | ciebot-incoming-webhooks-app-* |
| help | cietest | us-east-stage | cietest-handler-* | cietest-slack-consumer-* | cietest-incoming-webhooks-app-* |
| help | gobot | us-south-prod (and may be others) | gobot-commands-processor-*  or gobot-help-command-registry-*| gobot-slack-consumer-* | gobot-incoming-webhooks-app-* |
| whos oncall ... | gobot | us-south-prod (and may be others) | pagerduty-handler-* | gobot-slack-consumer-* | gobot-incoming-webhooks-app-* |

After configuring `kubectl oss`to the proper cluster, use the following one-liners and replace the `[bot]` to the actual bot name
```
kubectl oss pod get -nciebot | awk '/[bot]-handler/{print $1}' | xargs kubectl oss pod delete -nciebot
kubectl oss pod get -nciebot | awk '/[bot]-slack-consumer/{print $1}' | xargs kubectl oss pod delete -nciebot
kubectl oss pod get -nciebot | awk '/[bot]-incoming-webhooks-app/{print $1}' | xargs kubectl oss pod delete -nciebot
kubectl oss pod get -nciebot | awk '/gobot-commands-processor/{print $1}' | xargs kubectl oss pod delete -nciebot
kubectl oss pod get -nciebot | awk '/gobot-pagerduty-handler/{print $1}' | xargs kubectl oss pod delete -nciebot
kubectl oss pod get -nciebot | awk '/gobot-help-command-registry/{print $1}' | xargs kubectl oss pod delete -nciebot
```

OR, After configuring `kubectl`to the proper cluster, use the following one-liners and replace the `[bot]` to the actual bot name
```
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-handler/{print $1}' | xargs kubectl delete -nciebot pod
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-slack-consumer/{print $1}' | xargs kubectl delete -nciebot pod
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-incoming-webhooks-app/{print $1}' | xargs kubectl delete -nciebot pod
kubectl get pods -nciebot --no-headers=true | awk '/gobot-commands-processor/{print $1}' | xargs kubectl delete -nciebot pod
kubectl get pods -nciebot --no-headers=true | awk '/gobot-pagerduty-handler/{print $1}' | xargs kubectl delete -nciebot pod
kubectl get pods -nciebot --no-headers=true | awk '/gobot-help-command-registry/{print $1}' | xargs kubectl delete -nciebot pod
```

### 2. The slack-consumer external URL not responding `[bot]-[region]-[env]-consumer`

#### Problem description:

The slack-consumer is responsible all user interaction with the slack UI. So when this alert is open, the slack does not respond to user issued slack commands.

For `[env]= prd(prod)`, this is the URL failed: 
```
https://[region].pnp-api-oss.cloud.ibm.com/[bot]-consumer/events
```
For `[env]= stg(stage) and dev`, this is the URL failed: 
```
https://[region].pnp-api-oss.test.cloud.ibm.com/[bot]-consumer/events
```

#### Confirmation

Try any supported command on the bot. For example `@[bot] help`.

#### Fix

After configuring `kubectl oss` to the proper cluster, replace the `[bot]` with the actual bot name in the following, and run
```
kubectl oss pod get -nciebot | awk '/[bot]-slack-consumer/{print $1}' | xargs kubectl oss pod delete -nciebot

```

OR, After configuring `kubectl` to the proper cluster, replace the `[bot]` with the actual bot name in the following, and run
```
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-slack-consumer/{print $1}' | xargs kubectl delete -nciebot pod

```

### 3. The incoming-webhook external URL not responding  `[bot]-[region]-[env]-webhooks`

#### Problem description:

The incoming-webhook is responsible for generating dialogs and popups from Slack UI. When the alert opens, slack does not open dialog or popup when it supposed to. 

For `[env]= prd(prod)`, this is the URL failed: 
```
https://[region].pnp-api-oss.cloud.ibm.com/[bot]/slack/action
```
For `[env]= stg(stage) and dev`, this is the URL failed: 
```
https://[region].pnp-api-oss.test.cloud.ibm.com/[bot]/slack/action
```

#### Confirmation

If you happen to know a sequence of bot commands that will lead to a dialog, you can try. Otherwise, just wait to see if the alert resolves in about 20 minutes.

#### Fix

After configuring `kubectl oss` to the proper cluster, replace the `[bot]` with the actual bot name in the following, and run
```
kubectl oss pod get -nciebot | awk '/[bot]-incoming-webhooks-app/{print $1}' | xargs kubectl oss pod delete -nciebot

```

OR, After configuring `kubectl` to the proper cluster, replace the `[bot]` with the actual bot name in the following, and run
```
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-incoming-webhooks-app/{print $1}' | xargs kubectl delete -nciebot pod

```

### 4. A bot handler heartbeat is absent `[Env]-[region]-([bot]-)[handle]-not-responding` or `[Env]-[region]-[handler]-not-responding`

If the alert name does not have `[bot]` portion, it should be for `gobot`.

#### Problem description:

The micro service handling a certain bot feature is not running. Some Slack function is broken.

#### Confirmation and fix

From the alert, figure out the cluster you need to `kubectl`. The table below tells you the corresponing help command for confirmation and pod to delete.

| Handler in alert          | Command to test     | Pod to delete                    | Bot possible       |
|---------------------------|---------------------|----------------------------------|--------------------|
| handler                   | @[bot] cie help     | [bot]-handler                    | all cie* bots      |
| misc-commands-processor   | @[bot] feedback     | miscellaneous-commands-processor | all cie* and gobot |
| alias-command-processor   | @[bot] alias help   | alias-command-processor          | gobot or cietest1  |
| dutymgr-command-processor | @[bot] dutymgr help | dutymgr-command-processor        | gobot or cietest1  |
| help-command-registry     | @gobot help         | gobot-help-command-registry      | gobot or cietest1  |
| iae-handler               | @[bot] iae help     | iae-handler                      | gobot or cietest1  |
| link-command-processor    | @[bot] link help    | link-command-processor           | gobot or cietest1  |
| pagerduty-handler         | @[bot] pd help      | pagerduty-handler                | gobot or cietest1  |
| ticket-command-processor  | @[bot] ticket help  | ticket-command-processor         | gobot or cietest1  |

After configuring `kubectl oss` to the proper cluster, replace the `[bot]` with the actual bot name, and `[pod]` with `[pod to delete]`  in the table, and run
```
kubectl oss pod get -nciebot | awk '/[bot]-[pod]/{print $1}' | xargs kubectl oss pod delete -nciebot

```

OR, After configuring `kubectl` to the proper cluster, replace the `[bot]` with the actual bot name, and `[pod]` with `[pod to delete]`  in the table, and run
```
kubectl get pods -nciebot --no-headers=true | awk '/[bot]-[pod]/{print $1}' | xargs kubectl delete -nciebot pod

```

### 5. Rabbit MQ URL check failure `[Env]-[region]-rabbitmq-queue-check-failed`

#### Problem description:

There might be an on-going problem with RabbitMQ, in which case there should be another team investigating. There is a [rmq runbook](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html). The owner of the bot alert just needs to make sure the RMQ problem is being looked after.

There might have been a RMQ problem recently resolved, in which case the owner if the bot alert should restart all rlated pods.

#### Confirmation

Run the `@[bot] help` to check if the bot in the affected cluster is working.

| Env | Region   | Bot                       |
|-----|----------|---------------------------|
| prd | us-south | ciebot, gobot             |
| prd | us-east  | ciebot, gobot , ciebotwdp |
| prd | eu-de    | ciebot, gobot             |
| stg | us-south | cietest1                  |
| stg | us-east  | cietest, cietest1         |
| stg | eu-de    | cietest1                  |
| dev | us-east  | ciedev1                   |

#### Fix

After configuring `kubectl oss` to the proper cluster, run the following to delete all pods
```
kubectl oss pod get -nciebot | awk '/./{print $1}' | xargs kubectl oss pod delete -nciebot

```

OR, After configuring `kubectl` to the proper cluster, run the following to delete all pods
```
kubectl get pods -nciebot --no-headers=true | awk '/./{print $1}' | xargs kubectl delete -nciebot pod

```

### 6. Deadletter consumer pod not in Running state `k8s:[cluster]:ciebot:pod:[bot]-[service]-deadletter-consumer-*`

#### Problem description:

The alert reports that a pod for deadletter consumer failed to start or hung.
Usually when this happens, all deadletter consumer pods in that cluster for bots are in the same failure state.

#### Fix

After configuring `kubectl oss` to the proper cluster, just run the following command to delete all deadletter consumer pods, and let them restart. 
```
kubectl oss pod get -nciebot | awk '/-deadletter-consumer-/{print $1}' | xargs kubectl oss pod delete -nciebot

```

OR, After configuring `kubectl` to the proper cluster, just run the following command to delete all deadletter consumer pods, and let them restart. 
```
kubectl get pods -nciebot --no-headers=true | awk '/-deadletter-consumer-/{print $1}' | xargs kubectl delete -nciebot pod

```

#### Confirmation

All the pods should be restarted and get into Running state.
If any one does not go to Running state, check the log and follow up. For example, if there is RMQ problem, contact RMQ team.


## Helpful info

Find information in [Bots Overview](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Chat_Bots_Overview.html), [CIEBot User Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_General_User_Guide.html), [CIEBot CIE User Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_CIE_User_Guide.html), [CIEBot INCB User Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/CIEBot_INCB_User_Guide.html), and [Gobot User Guide](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/ciebot/Gobot_User_Guide.html) if you need to.

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

### Do not mark {{doctor-alert-system-name}} incident _resolved_
Once the underline issue is fixed, {{new-relic-porta-name}} will recognize the violation no longer exists, and send a _resolved_ signal to TIP, and the ServiceNow and {{doctor-alert-system-name}} incidents will become resolved on their own.

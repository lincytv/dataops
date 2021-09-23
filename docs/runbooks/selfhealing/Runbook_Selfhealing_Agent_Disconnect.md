---
layout: default
description: Runbook Selfhealing Agent Disconnect
title: Runbook Selfhealing Agent Disconnect
service: pte-selfhealing
runbook-name: Runbook Selfhealing Agent Disconnect
tags: oss, selfhealing, agent, disconnect
link: /selfhealing/Runbook_Selfhealing_Agent_Disconnect.html
type: Alert
---

## Purpose

This alert is triggered when selfhealing agent in one CF env can not be connected.

## Technical Details
Selfhealing shared services are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are instances running including
+ pte-selfhealing-action
+ pte-selfhealing-common
+ pte-selfhealing-consumer
+ pte-selfhealing-engine
+ pte-selfhealing-iam
+ pte-selfhealing-scheduler
+ pte-selfhealing-scheduler-logs
+ pte-selfhealing-webhook

In every CF env, there is a docker container **selfhealing_scriptengine** as agent on boshcli vm.


## User Impact

If the agent can not be connected, then the selfhealing action and flow can not be triggered. Alert in the specific env can not self-healing.

## Instructions to Fix

1. Check which env that the agent can not be connected, click here to [Check Agents](https://pnp-api-oss.cloud.ibm.com/selfhealing/api/v1/healthz).

  Get result like `... "lost_agents":[{"env":"d_dys1","ip":"10.144.11.107","service":"scriptengine","last_heartbeat":"2020-06-19 08:29:00"}]`, env field means D_DYS1 agent can not be connected.


2. Login boshcli vm in specific CF env, restart the service **selfhealing_scriptengine**.
`sudo docker restart selfhealing_scriptengine`.
After 5 minutes, retry step 1 to check connectivity, if the result like `... "lost_agents":[]...`, you can resolve the alert. If it can not connect to agent, goto next step.

3. In container **selfhealing_scriptengine**, `sudo docker exec -it selfhealing_scriptengine bash`
-  Find the redis server in configuration, `vim /usr/local/etc/stunnel/stunnel.conf`, pay attention to **connect**
```
[redis-cli]
client=yes
accept=127.0.0.1:6830
connect=89a9842a-008f-48da-b8a8-212770ace60a.d7deeff0d58745aba57fa5c84685d5b4.databases.appdomain.cloud:30331
```
- Check the connectivity to redis server, if the result shows **open**, means redis can be connected.
Then in China timezone, reassign pd alert to `bjyanzh@cn.ibm.com` in CDL daytime, or in NA timezone, snooze the pd alert to China daytime.
```
root@43915de3c72e:/# nc -vzw 3 89a9842a-008f-48da-b8a8-212770ace60a.d7deeff0d58745aba57fa5c84685d5b4.databases.appdomain.cloud  30331
icd-prod-us-south-db-kn2ep.us-south.containers.appdomain.cloud [169.46.17.86] 30331 (?) open
```

- If the result shows **Connection timed out**, it means there is network issue, you need to ask helps from CF SRE and CF Network team to fix the network issue.
```
root@43915de3c72e:/# nc -vzw 3 89a9842a-008f-48da-b8a8-212770ace60a.d7deeff0d58745aba57fa5c84685d5b4.databases.appdomain.cloud  30331
icd-prod-us-south-db-kn2ep.us-south.containers.appdomain.cloud [169.46.17.86] 30331 (?) Connection timed out
```
You could give info below to the network team to help fix this issue, host and port are in `/usr/local/etc/stunnel/stunnel.conf`, such as
```
Environment:
  D_DYS1
Source:
  Bochcli vm ip: 10.164.0.43
Destination:
  IBM cloud ICD redis:
  host: 89a9842a-008f-48da-b8a8-212770ace60a.d7deeff0d58745aba57fa5c84685d5b4.databases.appdomain.cloud
  port: 30331
```
- After the network issue fixed, please retry from step 1.

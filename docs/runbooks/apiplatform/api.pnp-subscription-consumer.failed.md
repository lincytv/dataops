---
layout: default
title: "API Platform - PnP Subscription Consumer failed"
type: Alert
runbook-name: "api.pnp-subscription-consumer.failed"
description: "This alert will be triggered when there is a failure in the PnP Status Consumer"
service: tip-api-platform
tags: api-pnp-subscription-consumer, subscription
link: /apiplatform/api.pnp-subscription-consumer.failed.html
---

## Purpose
This document covers the various cases where the subscription consumer may indicate a failure:
 - Failures during add or delete to the watchmap
 - Failed while checking a message for a valid watch
 - Failed while trying to post a message to a configured hook
 - The PnP Subscription Consumer(PSC) is down



## Technical Details
The PnP Subscription Consumer(PSC) is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.

The PSC consumes messages generated from various sources.   It watches for changes to incidents, cases, notificatons and maintenances(change records).   Internally it maintains as structure called a watchMap.  This is used to determine if the message generated from the sources has a subscription that it needs to process.


## User Impact
Potentially unavailable, invalid or corrupt data.  It's possible that the subscriptions will generate a delayed alert if the consumer is down.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

- Before proceeding, [check Slack - {{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there is a reason for this issue
- In each case, review the logs of the affected pod.  Copy the relevant log data to a file and to a ServiceNow incident assigned to the tip-api-platform configuration item
    - [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
        - The logs should give some indication on what the problem is.
        - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
        - In the relavent region, in a cluster, execute  
        `kubectl logs -napi -lapp=api-pnp-subscription-consumer -c api-pnp-subscription-consumer --tail=200`  
        If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  

 | Incident Title | Runbook Link | NR Link |
   | -------------- | ------------ | ---------- |
   | api-pnp-subscription-consumer watchmap failed during Check Message | [Check Message]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#check-message) | [New Relic]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/759503?filters=%255B%257B%2522key%2522%253A%2522monitorName%2522%252C%2522value%2522%253A%2522api-pnp-sub-consumer_watchmapCheckFailed_prd%2522%257D%255D) |
   | api-pnp-subscription-consumer watchmap failed during Add or Delete  | [Add or Delete]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#add-or-delete) | [New Relic]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/759503?filters=%255B%257B%2522key%2522%253A%2522monitorName%2522%252C%2522value%2522%253A%2522api-pnp-sub-consumer_watchmapCrudFailed_prd%2522%257D%255D) |
   | api-pnp-subscription-consumer watchmap failed during Post Message | [Posting]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#post-failures) | [New Relic]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/759503?filters=%255B%257B%2522key%2522%253A%2522monitorName%2522%252C%2522value%2522%253A%2522api-pnp-sub-consumer_watchmapPostFailed_prd%2522%257D%255D) |
   | api-pnp-subscription-consumer down | [Down]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#subscription-consumer-down) | [New Relic]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/546408?filters=%255B%257B%2522key%2522%253A%2522label%252eapp%2522%252C%2522value%2522%253A%2522tip-subscription-consumer%2522%257D%255D) |


### Check Message
 This is indicative of message that is improperly formatted.  If this problem continues to occur, use the command below to restart the subscription consumer by killing the pods in all the production environments.   

        `kubectl oss pod delete  -l app=api-pnp-subscription-consumer -n api`

 If the problem continues, proceed to [After Remediation Steps]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#after-remediation-steps) section.

### Add or Delete
  This may be indicative of a problem with the watchmaps structure.   The first step would be to log into the subscription pod and run a curl command to reinitialize the watchmap

        kubectl oss pod get -napi|grep subscription
        kubectl exec -it api-pnp-subscription-<pod id> -- sh
        curl api-pnp-subscription-consumer:8000/wminit       


### Post Failures
  This may only be a single bad configuration or potentially a larger problem of connectivity.   You can identify the problem message in the logs by looking for the following pattern

         failed to post - >  <message>

  In this case there should be an error message as well that may give more clear information on the nature of the failure.  To continue with identifying the problem, there should be a "targetAddress" field.    See if you can connect to the field via a rest client like Postman or curl on your local client.   Compare that to running curl from the subscription pod:

        kubectl oss pod get|grep subscription
        kubectl exec -it api-pnp-subscription-<pod id> -- sh
        curl <targetAddress>

  Valid response is not required, only that connectivity is possible.  If your local client is able to connect but the pod is not, we will need to proceed to escalate.   See the [After Remediation Steps]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#after-remediation-steps) section.

### Subscription Consumer Down
  1. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-subscription-consumer%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl oss pod get  -l app=api-pnp-subscription-consumer -napi`
        - You should see at least 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if there are similar issues for other PnP components in that region]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html). Need to contact Technical Foundation squad if you believe there is problem with Kubernetes, Postgresql database or the underlying infrastructure [contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).

  2. Check logs in logDNA or Kubernetes
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-subscription-consumer -c api-pnp-subscription-consumer --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

  If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -napi <pod_name>`.  
  You can attempt `kubectl oss pod delete <pod_name> -napi `, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod(which can be found out using the kubectl describe command).

  If there are panic errors or any other coding specific issue in the logs which are preventing the container to be in a Running state, proceed to [After Remediation Steps]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-subscription-consumer.failed.html#after-remediation-steps) section.


## After remediation steps

  If the problem continues then reassign the PagerDuty incident to **tip-api-platform level 2.**



## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

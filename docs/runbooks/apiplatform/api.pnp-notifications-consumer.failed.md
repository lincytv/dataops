---
layout: default
title: "API Platform - PnP Notification Consumer failed"
type: Alert
runbook-name: "api.pnp-notifications-consumer.failed"
description: "This alert will be triggered when there is a failure or all instances of the PnP Notification Consumer is unavailable"
service: tip-api-platform
tags: api-pnp-notifications-consumer, notification
link: /apiplatform/api.pnp-notifications-consumer.failed.html
---

## Purpose
This alert is triggered when there is a detected failure.  This could be:
    - PnP Notification Consumer is not responding and/or NewRelic is not receiving metrics.
    - A failure to post to RabbitMQ

## Technical Details
PnP Notification Consumer is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. The PnP Notification Consumer listens for messages on the queue coming from nq2ds which involve Maintenance records. For each record it processes, it creates a notification message which will be consumed by the Subscription Consumer and nq2ds.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-notifications-consumer%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
PnP Notifications will not be created or processed from RTC Change records.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

 | Incident Title | Runbook Link |
   | -------------- | ------------ |
   | api-pnp-notification-consumer is down | [api-pnp-notification-consumer down]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-notifications-consumer.failed.html#api-pnp-notification-consumer-down) |
   | api-pnp-notification-consumer failed in posting to MQ  | [MQ issues]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-notifications-consumer.failed.html#encryption-or-mq-posting-errors) |

### `api-pnp-notification-consumer down`  

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Verify if PnP Notification Consumer has been running regularly. [Access New Relic MQ and DB failures for the Notification Consumer]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/query?hello=overview&query=SELECT%20%60pnp-db-failed%60,%20%60pnp-mq-failed%60%20from%20Transaction%20WHERE%20appName%20like%20%27api-pnp-notification%25%27%20%20and%20appName%20NOT%20LIKE%20%27%25adapter%27%20and%20apiKubeAppDeployedEnv%3D%27prod%27%20and%20apiKubeClusterRegion%3D%27us-east%27%20since%201%20day%20ago)
    - Verify that `pnp-db-failed` value is not true. If it is, check if there is an alert for PnP database. Otherwise move onto step
    - Verify that `pnp-mq-failed` value is not true. If it is, check if there is an alert for PnP RabbitMQ. Otherwise move onto step

3. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-notifications-consumer%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.  
        - Execute `kubectl get po -n api -l app=api-pnp-notification-consumer`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can check if other PnP components in that region are having problems.
        - [US-East]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522clusterName%2522%252C%2522value%2522%253A%2522OSSDev-US-East%2522%257D%255D)
        - [US-South]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522clusterName%2522%252C%2522value%2522%253A%2522OSSDev-US-South%2522%257D%255D)
        - [EU-DE]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522clusterName%2522%252C%2522value%2522%253A%2522OSSProd-EU-DE%2522%257D%255D)

    You will need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

4. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oos pod delete <pod_name> -n api `, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

5. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.  
    - In each region, in a cluster, execute  
    `kubectl logs -n api -l app=api-pnp-notification-consumer -c api-pnp-notification-consumer --tail 50`
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

### Encryption or MQ Posting errors
For failures in encryption or posting to MQ, check logs in logDNA
- See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
- The logs should give some indication on what the problem is.
- If you are unable to see logs in logDNA, you can see it using `kubectl` command.
- In each region, in a cluster, execute
    `kubectl logs -napi -lapp=api-pnp-notification-consumer -c api-pnp-notification-consumer --tail=50`  
    If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  

Resolution is likely a failure in other components (for example the rabbit MQ or the vault).   Identify the problem component and take necessary actions to fix the issue there.  

For example if the MQ server is not responding, can you determine the cause (i.e. bad network resolution, the service is actually not available, bad connection or use [the MQ runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html)).  If it is not obvious what the problem or resolution is then [follow the "After remediation steps" section]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-notifications-consumer.failed.html#after-remediation-steps) if that doesn't resolve it.


## After remediation steps

   Once all the issues have been resolved, use the command below torestart the PRA by killing the pod.   It will automatically restart and run an import.   It should be able to complete the process in less than 5 minutes without errors.

    - `kubectl oos pod delete api-pnp-notification-consumer -n api`

   If the steps above did not resolve the problem then reassign the PagerDuty incident to **tip-api-platform level 2.**


## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

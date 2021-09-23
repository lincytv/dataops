---
layout: default
title: "EDB Processing Status API down and other issues"
type: Alert
runbook-name: "api.edb-processing-status.error"
description: "This alert will be triggered when the EDB Processing Status API did not work properly"
service: tip-api-platform
tags: api-edb-processing-status
link: /apiplatform/api.edb-processing-status.error.html
---

## Purpose
Alerts will be triggered when EDB processing status API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
Processing status data is short lived and scrubbed after 12 hours.
The processing status service provides information on the processing of posted event data to backend data stores including any errors that may have occurred.

## User Impact
If the processing status API is not functioning we will be unable to check on the status of ingested event data.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### `api-edb-processing-status down`


1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-status%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.   
        - Execute `kubectl oss pod get -n api -l app=api-edb-processing-status`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

3. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-edb-processing-status -c api-edb-processing-status --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

---
layout: default
title: "EDB Audit down and other issues"
type: Alert
runbook-name: "api.edb-audit.error"
description: "This alert will be triggered when EDB Audit did not work properly"
service: tip-api-platform
tags: api-edb-audit
link: /apiplatform/api.edb-audit.error.html
---

## Purpose
Alerts will be triggered when EDB Audit is not responding and/or NewRelic is not receiving metrics.

## Technical Details
EDB Audit is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances running.

## User Impact
Users of the EDB Audit API will be unable to reach the service if none of the regions is healthy. Scorecard is not able to get the service names that are using the TIP adapter.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

This runbook is for many incidents that triggered by edb-audit . Please look for the title of the incident below, and follow the instructions.



### EDB Audit is down

   `api-edb-audit_down`

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions.
    - Manually check if pods are running is the affected regions with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.
        - Execute `kubectl oss pod get -n api | grep audit`
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_EDB_Healthz_Paths.html) have similar issue. Also, you can check if other EDB components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).

3. If the pod is in a non-Running state you can first see the logs from the pods in bad state (see **Check logs** section below) and also see error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.  


### EDB Audit failed to write to MongoDB

   `api-edb-audit has Mongo error`

1. Check the log (see **Check logs** section below) to see if there is any error when sending data to Mongo database.

2. See [EDB MongoDB has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-mongodb.down.html) on how to test connection to MongoDB.

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-edb-audit -c api-edb-audit --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)

If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

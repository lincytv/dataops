---
layout: default
title: "EDB Sysdig Adapter down and other issues"
type: Alert
runbook-name: "api.edb-adapter-sysdig.error"
description: "This alert will be triggered when the EDB Sysdig Adapter did not work properly"
service: tip-api-platform
tags: api-edb-adapter-sysdig
link: /apiplatform/api.edb-adapter-sysdig.error.html
---

## Purpose
Alerts will be triggered when EDB Sysdig adapter is not responding and/or NewRelic is not receiving metrics.

## Technical Details
The Sysdig adapter is used to send availability metrics.
EDB Sysdig Adapter is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`.

In each region the Sysdig Adapter is deployed as 6 different instances with 1 replica for each.  There is an umbrella chart which has [6 charts as
dependencies](https://github.ibm.com/cloud-sre/oss-charts/tree/staging/api-edb-adapter-sysdig/charts).  Each of these are deployed onto
a different node.  

## User Impact
Availability platform metrics will not be sent to Sysdig.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

This runbook is for many incidents that are triggered by edb-adapter-sysdig. Please look for the title of the incident below, and follow the instructions.


### EDB Sysdig adapter down

   - `api-edb-adapter-sysdig_down`

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions.
    - Manually check if pods are running is the affected regions with the `kubectl` command as follows
        - Execute `kubectl oss pod get  -n api | grep adapter-sysdig `
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_EDB_Healthz_Paths.html) have similar issue. Also, you can check if other EDB components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).

3. If the pod is in a non-Running state you can first see the logs from the pods in bad state (see **Check logs** section below) and also see error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.  


### EDB Sysdig Adapter get OSS Catalog failed

   - `api-edb-adapter-sysdig initialize has get OSS Catalog error`
   - `api-edb-adapter-sysdig has fetch OSS Catalog error`

1. Check the log (see **Check logs** section below) to see if there is any error when calling gcor OSS Catalog API.

2. Run this command, if you got 200 status code, then that means gcor api is healthy, New Relic should resolve the incident soon; otherwise go to next step.
   ```
   curl -v https://pnp-api-oss.cloud.ibm.com/gcorapi/api/v1/gcor/healthz -H "Authorization: <API Platform ApiKey>"
   ```

3. Execute `kubectl oss pod get -n api | grep gcor`, you should see pod(s) with the status `Running`, if status is different continue to the next step

4. If the gcor pod is in a non-Running state you can first see the logs from the pods in bad state, and also see error messages shown by running `kubectl describe pod -n api <pod_name>`.  
    - Try to restart the `api-gcor-api` service. `kubectl oss pod delete -l app=api-gcor-api -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.

5. If the issue in `api-gcor-api` service is resolved, `api-edb-adapter-sysdig` service should be able to get OSS Catalog, and New Relic should auto resolve the incident. If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.


### EDB Sysdig Adapter Unmarshal error

   - `api-edb-adapter-sysdig has unmarshal error`

   - This means that the transformed message received from the RabbitMQ cannot be unmarshalled. Check the logs (see **Check logs** section below) and reassign the PagerDuty incident to tip-api-platform level 2.

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### EDB Sysdig Adapter get initialize Redis database client failed

1. Check the log (see Check logs section below) to see if there is any error when initialize Redis database
2. To resolve, follow [Redis Down]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-redis.down.html)

### EDB Sysdig Adapter get Redis all keys failed
1. Check the log (see Check logs section below) to see if there is any error when initialize Redis database
2. To resolve, follow [Redis Down]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-redis.down.html)

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-adapter-sysdig-useast -c api-adapter-sysdig-useast --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)
	`kubectl logs  -n api -l app=api-adapter-sysdig-ussouth -c api-adapter-sysdig-ussouth --tail=50`
	`kubectl logs  -n api -l app=api-adapter-sysdig-ausyd -c api-adapter-sysdig-ausyd --tail=50`
	`kubectl logs  -n api -l app=api-adapter-sysdig-eugb -c api-adapter-sysdig-eugb--tail=50`
	`kubectl logs  -n api -l app=api-adapter-sysdig-eude -c api-adapter-sysdig-eude --tail=50`
	`kubectl logs  -n api -l app=api-adapter-sysdig-default  -c api-adapter-sysdig-default --tail=50`


## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

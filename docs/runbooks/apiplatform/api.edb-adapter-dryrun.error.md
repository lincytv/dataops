---
layout: default
title: "EDB Dry Run Adapter down and other issues"
type: Alert
runbook-name: "api.edb-adapter-dryrun.error"
description: "This alert will be triggered when the EDB Dry Run Adapter did not work properly"
service: tip-api-platform
tags: api-edb-adapter-dryrun
link: /apiplatform/api.edb-adapter-dryrun.error.html
---

## Purpose
Alerts will be triggered when EDB dry run adapter is not responding and/or NewRelic is not receiving metrics.

## Technical Details
The dry run adapter is used to validate that a defined map properly transforms event data to the standardized format.

When posting event data that targets the dry run adapter, the processing status service will place the transformed data in the result message field which you may visually inspect for correctness.

EDB dry run adapter is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances running.

## User Impact
Users will be unable to view and validate transformed data in the result message field.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

This runbook is for many incidents that triggered by `edb-adapter-dry-run` . Please look for the title of the incident below, and follow the instructions.

### EDB dry run adapter down

   - `api-edb-adapter-dry-run_down`

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions.
    - Manually check if pods are running is the affected regions with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.
        - Execute `kubectl oss pod get -n api|grep dry-run `
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_EDB_Healthz_Paths.html) have similar issue. Also, you can check if other EDB components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).

3. If the pod is in a non-Running state you can first see the logs from the pods in bad state (see **Check logs** section below) and also see error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss edb delete api-edb-adapter-dry-run`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.  


### EDB dry run adapter get OSS Catalog failed

   - `api-edb-adapter-dry-run initialize has get OSS Catalog error`
   - `api-edb-adapter-dry-run has fetch OSS Catalog error`

1. Check the log (see **Check logs** section below) to see if there is any error when calling `gcor` OSS Catalog API.

2. Run this command, if you got 200 status code, then that means gcor api is healthy, New Relic should resolve the incident soon; otherwise go to next step.
   ```
   curl -v https://pnp-api-oss.cloud.ibm.com/gcorapi/api/v1/gcor/healthz -H "Authorization: <API Platform ApiKey>"
   ```

3. Execute `kubectl oss pod get -l app=api-gcor-api -napi`, you should see pod(s) with the status `Running`, if status is different continue to the next step

4. If the gcor pod is in a non-Running state you can first see the logs from the pods in bad state, and also see error messages shown by running `kubectl describe pod -n api <pod_name>`.  
    - Try to restart the api-gcor-api service. `kubectl oss pod delete -l app=api-gcor-api -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.

5. If the issue in `api-gcor-api` service is resolved, `api-edb-adapter-dry-run` service should be able to get OSS Catalog, and New Relic should auto resolve the incident. If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

{% include_relative _{{site.target}}-includes/edb-logdna.md %}


### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-adapter-dry-run -c api-adapter-dry-run --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

---
layout: default
title: "EDB API Healthz Failures"
type: Alert
runbook-name: "api.edb-api-healthz.failed"
description: "This alert will be triggered when pinging or calling EDB APIs' healthz failed"
service: tip-api-platform
tags: api-edb-ingestor, api-edb-mapping-api, api-edb-processing-status, api-edb-audit
link: /apiplatform/api.edb-api-healthz.failed.html
---

## Purpose
Alerts will be triggered when NewRelic PING or API synthetic monitors for an EDB API component have failed.


## Technical Details
EDB API components are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 pod instances running.

PING and API synthetic monitors have been set up in New Relic to monitor the healthz url of API Platform components in each region (i.e. the URL tested is the regional URL for the API component so we know the test is calling the correct region).

## User Impact
The API component may not be reachable or functioning correctly so this alert is critical to resolve.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### EDB API Healthz Failed

1. Verify if API component is responding

    - Find out from the PagerDuty incident, which API component is failing, and production or staging environment, and whether it is failed globally or in a particular region.
    - Find for the proper URL based on the component and region from [EDB API Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_EDB_Healthz_Paths.html), and click on the link or do **curl** command on it.
    - The response should be something like  
      ```
      {"href":"{{site.data[site.target].oss-apiplatform.links.edb-ingestor-api-prod.link}}","code":0,"description":"The API is available and operational."}
      ```
    - If the reply was as above with `code:0`, then we know that we have at least 1 region is up.
    - If the reply has `code:1`, and the description indicates a failure in MongoDB, then follow the [MongoDB Down]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-mongodb.down.html) runbook.
    - If the reply has `code:1`, and the description indicates a failure in Redis, then follow the [Redis Down]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-redis.down.html) runbook.
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.


2. Check pods are running in all 3 regions

    - Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  
    - Manually check if pods are running is the affected regions with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.
        - Execute `kubectl oss pod get -n api | grep audit`
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_EDB_Healthz_Paths.html) have similar issue. Also, you can check if other EDB components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).
    - If there are pods in non-Running state, you can first see the logs from the pods in bad state (see **Check logs** section below) and also see error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api `, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.  


3. Check logs in Kubernetes

      - In each region, in a cluster, execute
    `kubectl logs -n api -l app=api-edb-audit -c api-edb-audit --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)
    - If the pod is in a non-Running state you can first check logs from the pods in bad state and also see error messages shown by running `kubectl describe po -napi <pod_name>`. Then you can attempt `kubectl oss pod delete <pod_name>`, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod(which can be found out using the kubectl describe command).
    - If there are panic errors or any other coding specific issue in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.

{% include_relative _{{site.target}}-includes/edb-logdna.md %}


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

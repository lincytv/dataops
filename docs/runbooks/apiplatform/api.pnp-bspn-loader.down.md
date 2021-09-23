---
layout: default
title: "API Platform - BSPN Loader is down"
type: Alert
runbook-name: "api.pnp-bspn-loader.down"
description: "This alert will be triggered when all instances of the PnP BSPN Loader went down"
service: tip-api-platform
tags: api-pnp-bspn-loader, bspn
link: /apiplatform/api.pnp-bspn-loader.down.html
---

## Purpose

This alert is triggered when PnP BSPN Loader is not responding and/or NewRelic is not receiving metrics.

## Technical Details
PnP BSPN Loader is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. The PnP BSPN Loader **bulk loads** BSPN records into the PnP database. It first calls ServiceNow to obtain a list of qualifying incidents and then checks each incident to see if it has a BSPN record associated with it. If it does, it will make another call to ServiceNow to get the BSPN record(s) and then transform the record into a format that nq2ds can process. At the end of the process, it will insert properly formatted BSPN records into the RabbitMQ queue for nq2ds to process. **This should be a service that only runs when bulk loading is needed.**

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-bspn-loader%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

## User Impact

There could be missing records in the PnP database if BSPN Loader has not been run.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### PnP BSPN Loader unmarshal failed
- `api-pnp-bspn-loader unmarshal failed during getRecordsFromSN`
- `api-pnp-bspn-loader unmarshal failed during getBSPNRecordsFromSN`
- `api-pnp-bspn-loader unmarshal failed during getCmdbCisFromSN`
- `api-pnp-bspn-loader unmarshal failed during getEnvsFromSN`


- If there are more than one active related alert, this can mean that data received from ServiceNow is not as expected. Follow the [ServiceNow down runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-servicenow.down.html) to check if ServiceNow is down. If not, gather the logs for the request and response data to ServiceNow and escalate to 'tip-api-platform' Level 2 support team.

### PnP BSPN Loader ServiceNow failed
- `api-pnp-bspn-loader ServiceNow failed during getRecordsFromSN`
- `api-pnp-bspn-loader ServiceNow failed during getBSPNRecordsFromSN`
- `api-pnp-bspn-loader ServiceNow failed during getCmdbCisFromSN`
- `api-pnp-bspn-loader ServiceNow failed during getEnvsFromSN`  


- If there are more than one active related alert, this can mean that there was an error in attempting to make a request to ServiceNow. Follow the [ServiceNow down runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-servicenow.down.html) to check if ServiceNow is down. If not, gather the logs for the request (and response if any) to ServiceNow and escalate to 'tip-api-platform' Level 2 support team.

### api-pnp-bspn-loader down  


1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions.
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-bspn-loader%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.
        - Execute `kubectl oss pod get -n api -l app=api-pnp-bspn-loader`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Also, you can check if other PnP components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).
    - Verify that `pnp-unmarshal-failed` value is not true. `pnp-unmarshal-failed` is TRUE when there is an error in reading/unmarshalling the data response received from ServiceNow. Check the log for the specific request and payload. You can search for messages in logDNA which contain text `ReadAll: ` or `Error unmarshal: ` that occurred around the time of the alert.  
    - Verify that `pnp-SN-failed` value is not true. `pnp-SN-failed` is TRUE when there has been an error in the HTTP GET request to ServiceNow. Check if there are any other current open ServiceNow alerts and/or the log for the specific request details. You can search for messages in logDNA which contain text `Do: ` or `NewRequest: ` that occurred around the time of the alert.

3. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api `, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

4. Check logs in logDNA. Make sure that it has been running at least once in the past 24 hours.
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -n api -l app=api-pnp-bspn-loader -c api-pnp-bspn-loader --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

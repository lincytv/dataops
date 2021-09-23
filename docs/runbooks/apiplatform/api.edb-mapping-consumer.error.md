---
layout: default
title: "EDB Mapping Consumer down and other issues"
type: Alert
runbook-name: "api.edb-mapping-consumer.error"
description: "This alert will be triggered when the EDB Mapping Consumer did not work properly"
service: tip-api-platform
tags: api-edb-mapping-consumer
link: /apiplatform/api.edb-mapping-consumer.error.html
---

## Purpose
Alerts will be triggered when EDB mapping consumer is not responding and/or NewRelic is not receiving metrics.

## Technical Details
The mapping consumer consumes posted event data messages and transforms the raw JSON object to the standardized format using the user provided map.

## User Impact
If the mapping consumer is not functioning ingested data will not get consumed for processing.
The processing status may be checked for any possible errors.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### `edb-mapping-consumer-unmarshalErr`  
- Check the log for the specific message that it was trying to unmarshal into data struct.  
- If there are multiple occurences of this error in a very short time period, there is something wrong with the JSON unmarshalling. Try to restart the api-edb-mapping-consumer service   

### `edb-mapping-consumer-marshalErr`  
- Check the log for the specific message that it was trying to marshal into bytes.  
- If there are multiple occurences of this error in a very short time period, there is something wrong with the JSON marshalling. Try to restart the api-edb-mapping-consumer service  

### `edb-mapping-consumer-rabbitmqErr`  
- Verify that RabbitMQ is up and running [{{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html)  
- Check that the configuration for RabbitMQ is correct. Check the beginning of the log to see if there were any startup errors in connection.  

### `api-edb-mapping-consumer has GetMap error`
- Check the logs (LogDNA) to see if there are many errors.
- If the error is `401 Unauthorized`, perform a curl request to check edb-mapping-api
`curl -i 'https://pnp-api-oss.cloud.ibm.com/edbmapmgmt/api/v1/edb/maps/5cc75fbb20bbe53d0ea5d25a' --header 'Authorization: <YOUR_IAM_API_KEY_UNDER_PNPSERVE_IBM_CLOUD_ACCOUNT>'`
If you still get a 401 Unauthorized error, continue to next step. If you get success (200 OK), this could mean that the EDB Service API Key could be bad. Ask Irma to regenerate the API key.
- Check that the [PNPServeAccount value](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/api-edb-mapping-api/production-values.yaml#L18) is set to `16629eea1f9b4c74bbf5e6b3e6f4fee8` for production. Redeploy edb-mapping-api if necessary.

### `api-edb-mapping-consumer down`  

These instructions mention `kubectl`, if you don't know how to configure it for each region, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)


1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-status%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.  
        - Execute `kubectl oss pod get -n api -l app=api-edb-mapping-consumer`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

3. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-edb-mapping-consumer -c api-edb-mapping-consumer --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

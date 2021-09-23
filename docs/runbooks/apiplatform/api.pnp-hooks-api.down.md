---
layout: default
title: "API Platform - PnP Hooks API is down"
type: Alert
runbook-name: "api.pnp-hooks-api.down"
description: "This alert will be triggered when all instances of the PnP Hooks API service went down"
service: tip-api-platform
tags: api-pnp-hooks, apis
link: /apiplatform/api.pnp-hooks-api.down.html
---

## Purpose
This alert is triggered when PnP Hooks API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
PnP Hooks API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-hooks%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
If PnP Hooks API is not reachable, then ServiceNow will not be able send incident, case, BSPN and change information to PnP, as well as Doctor changes.  
PnP Hooks API must be running at all times, at least in one region.  


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Verify if PnP Hooks API is responding
    - If the alert is for production, click on the link or do curl command on
    [{{site.data[site.target].oss-apiplatform.links.pnp-hooks-api-prod.link}}]({{site.data[site.target].oss-apiplatform.links.pnp-hooks-api-prod.link}})  
    - If the alert is for staging, click on the link or do curl command on
     [{{site.data[site.target].oss-apiplatform.links.pnp-hooks-api-stage.link}}]({{site.data[site.target].oss-apiplatform.links.pnp-hooks-api-stage.link}})
    - If the alert is for a particular region, refer to [PnP API Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) for the proper URL, and click on the link or do curl command on it.
    - The reply should be  
    ```
    {"href":"{{site.data[site.target].oss-apiplatform.links.pnp-hooks-api-prod.link}}","code":0,"description":"The API is available and operational."}
    ```
    - If the reply was as above with code:0, then we know that we have at least 1 region up.
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need to check.
    - It's worth checking [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) slack channel for any changes or issues going on with Kubernetes.

2. Check RabbitMQ and Catalog API healthz

    - Open [APIs Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html#pnp-hooks).
    - Under `PnP Hooks`, test all the region-specific URLs for the specific environment for this alert (prod or stage).  
    When PnP Hooks is called, it tests connectivity to RabbitMQ and Catalog API, whereas all the other PnP APIs do not test them.  
    - If any of the regionals URLs return a code different than zero, then it will say what is the component with problems ([RabbitMQ]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html) or [API Catalog]({{site.baseurl}}/docs/runbooks/apiplatform/api.catalog-api.down.html)). Follow the links to work on each issue if needed.  

3. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-hooks%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl oss pod get -napi -l app=api-pnp-hooks`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

4. Check logs in logDNA or Kubernetes  
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-hooks -c api-pnp-hooks --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.  

If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -napi <pod_name>`.  
You can attempt `kubectl oss pod delete  <pod_name> -napi`, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod(which can be found out using the kubectl describe command).

If there are panic errors in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

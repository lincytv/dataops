---
layout: default
title: "API Platform - PnP Resource Adapter is down"
type: Alert
runbook-name: "api.pnp-resourceadapter.down"
description: This alert will be triggered when all instances of the PnP Resource Adapter are down
service: tip-api-platform
tags: api-pnp-resourceadapter, apis
link: /apiplatform/api.pnp-resourceadapter.down.html
---

## Purpose
This alert is triggered when PnP Resource Adapter is not responding and/or NewRelic is not receiving metrics.


## Technical Details
The PnP Resource Adapter(PRA) is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-hooks%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Resource or ServiceNow data could be out of date or not populated


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-subscription-consumer%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl get po -napi -lapp=api-pnp-resource-adapter`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)

2. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-resource-adapter -c api-pnp-resource-adapter --since=5m`  
    


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})
---
layout: default
title: "API Platform - Catalog service instance is down"
type: Alert
runbook-name: "api.catalog-api.down"
description: "This alert will be triggered API Catalog is not responding and/or NewRelic is not receiving metrics"
service: tip-api-platform
tags: catalog, apis
link: /apiplatform/api.catalog-api.down.html
---

## Purpose
This alert is triggered when Catalog API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
Catalog API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-api-catalog%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Many users and applications rely on this service to access the rest of our APIs. These services and users may be unable to get to another API if Catalog is not working.
It is very important for this service to be up and running at all times.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Verify if Catalog API is indeed down
    - Depends on which environment is failing, refer to [API Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) for the proper URL, and do curl command on it, e.g.
      `curl {{site.data[site.target].oss-apiplatform.links.catalog-api-prod.link}}`
    - The reply should be  
      ```
      {"href":"{{site.data[site.target].oss-apiplatform.links.catalog-api-prod.link}}","code":0,"description":"The API is available and operational."}
      ```
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.

2. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-api-catalog%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl get po -napi -lapp=api-api-catalog`
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can
        - [Ask the network team for assistance](https://ibm-cloudplatform.slack.com/messages/G0D908KMH), or do @cybot who is on call network and contact the on-call person from network team.
        - [Check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) have similar issue. You will need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure
            - [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)

3. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-api-catalog -c api-api-catalog --since=5m`  
    

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

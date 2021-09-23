---
layout: default
title: "RETIRED Doctor API service instance is down"
type: Alert
runbook-name: "api.doctor-api.down"
description: "This alert will be triggered if the api_doctor_api service is not work properly."
service: tip-api-platform
tags: api_doctor_api, apis
link: /apiplatform/api.doctor-api.down.html
---

## Purpose
This alert will be triggered if the Doctor API service is not working properly.


## Technical Details
Doctor API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-doctor-api%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Users of the Doctor API will be unable to reach the service.


## Instructions to Fix
1. Verify if Doctor API is indeed down
   - Depends on which environment is failing, refer to [API Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) for the proper URL, and do curl command on it, e.g.
     `curl {{site.data[site.target].oss-apiplatform.links.doctor-api-prod.link}}`
    - The reply should be  
      ```
      {"href":"{{site.data[site.target].oss-apiplatform.links.doctor-api-prod.link}}","code":0,"description":"The API is available and operational."}
      ```
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.

2. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-doctor-api%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl get po -napi -lapp=api-doctor-api`
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)

3. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-doctor-api --since=5m`  
    If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

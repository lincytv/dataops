---
layout: default
title: Low usage detected for Incident Management/concerns API
type: Alert
runbook-name: api.incidentmgmt-api.lowusage
description: "This alert indicates that there is a very low number of incoming requests on Incident Management/concerns API."
service: tip-api-platform
tags: tip, kafka, consumer
link: /apiplatform/api.incidentmgmt-api.lowusage.html
---

## Purpose
Troubleshoot issue when there is a very low number of incoming requests on Incident Management /concerns API.


## Technical Details
Incident Management API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances of the API running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-incident-management%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

This alert indicates that there is a very low number of incoming requests on Incident Management /concerns API.

Root cause may be:

- Incident Management instances are no longer dispatched.
- Heartbeat test has stopped (which should not happen) and no end user requests are sent to Incident Management /concerns API.


## User Impact
This is **CRITICAL** to be operational at all times as the whole TIP depends on this service to be running correctly. Any new incidents sent to TIP will not get to ServiceNow, having a direct customer impact.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Verify IM API health
   - In a terminal, execute  
   `curl {{site.data[site.target].oss-apiplatform.links.incidentmgmtapi-api-prod.link}}`
    - The reply should be  
      ```
	  {
  "service": "tip_incidentmgmtapi",
  "version": 1,
  "health": [
    {
      "plan": "Free",
      "status": 0,		                        <==== "status:" 0  means service is operational
      "serviceInput": "healthcheck",
      "serviceOutput": "service operational",
      "responseTime": 8091
    }
  ],
  "apiservicestat": {
    "ServiceStartTime": "2018-06-18T15:26:33Z",
    "ServiceHostname": "api-incident-management-85f4649d8f-k4n2k",
    "ServiceIPAddress": "172.30.169.101",
    "ServiceInterfaces": "127.0.0.1/8 (lo),172.30.169.101/32 (eth0)",
    "ServiceCatalogStatus": "unknown",
    "ServiceCatalogCode": 0,
    "ServiceCatalogStatusTime": "",
    "ServiceCatalogExtStatus": "",
    "ServiceCatalogExtCode": 0,
    "ServiceCatalogExtStatusTime": "",
    "BackgroundServiceStatus": "ServiceNow connectivity: OK",  <==== connectivity to SNow should be "OK"
    "BackgroundServiceCode": 200,
    "BackgroundServiceStatusTime": "2018-06-28T10:23:11Z",
    "InfoStatsIntervalStart": "2018-06-28T10:06:35Z",
    "InfoStatsIntervalEnd": "2018-06-28T10:16:35Z",
    "InfoMaxResponseTime": 0,
    "InfoRequestCount": 89,
    "PostStatsIntervalStart": "2018-06-28T10:06:35Z",
    "PostStatsIntervalEnd": "2018-06-28T10:16:35Z",
    "PostMaxResponseTime": 602,
    "PostRequestCount": 2,
    "PatchStatsIntervalStart": "2018-06-28T10:06:35Z",
    "PatchStatsIntervalEnd": "2018-06-28T10:16:35Z",
    "PatchMaxResponseTime": 8091,
    "PatchRequestCount": 11
  }
}
```

    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.  

2. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-incident-management%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl get po -napi -lapp=api-incident-management`
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)  

3. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-incident-management -c api-incident-management --since=5m`  
  

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

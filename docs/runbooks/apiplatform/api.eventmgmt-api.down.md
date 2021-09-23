---
layout: default
title: "API Platform - Event Management API is down"
type: Alert
runbook-name: "api.eventmgmt-api.down"
description: "This alert will be triggered when all instances of the Event Management API service went down"
service: tip-api-platform
tags: api-eventmgmt, apis
link: /apiplatform/api.eventmgmt-api.down.html
---

## Purpose
This alert is triggered when Event Management API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
Event Management API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-eventmgmt%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Users of the Event Management API will be unable to reach the service.


## Instructions to Fix
1. Verify if Event Management API is indeed down
   - In a terminal, if the alert is for production, execute `curl {{site.data[site.target].oss-apiplatform.links.eventmgmt-api-prod.link}}`
     and if the alert is for staging, execute `curl {{site.data[site.target].oss-apiplatform.links.eventmgmt-api-stage.link}}`
    - The reply should be something like
      ```
      {
      "clientId":"eventmgmtapi",
      "description":"Event and correlation management for Bluemix",
      "version":"0.0.1",
      "categories":["eventmgmt"],
      "events":{"href":"https://pnp-api-oss.cloud.ibm.com/eventmgmtapi/api/eventmgmt/events"},
      "event":{"href":"https://pnp-api-oss.cloud.ibm.com/eventmgmtapi/api/eventmgmt/event"},
      "events_flatten":{"href":"https://pnp-api-oss.cloud.ibm.com/eventmgmtapi/api/eventmgmt/cicd/events_flatten"},
      "events_sql":{"href":"https://pnp-api-oss.cloud.ibm.com/eventmgmtapi/api/eventmgmt/cicd/events_sql"}
      }
      ```
    - If you do get JSON data returned, this means the API service is up and running. PagerDuty alert should get resolved by itself after a short period; otherwise go to step 2.

2. Check if Event Management API is registered in API Catalog
   - Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   - Go to the **API Management** panel, in **API Catalog** tab, see if you can find the `eventmgmtapi` in the **API Catalog** table. If yes, then repeat step 1; otherwise wait for a couple of minutes to see if the API can re-register itself to the API Catalog. If you still do not see the `eventmgmtapi` in the Client ID column after a few minutes, go to next step.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/api_management/api_catalog2.png){:width="640px"}

3. See if it is Doctor Backend outages
   - If you are also seeing alerts for other Doctor outages at the same time. Then most likely it is related to Doctor fabric router issue, then please contact [{{doctor-critical-alerts-l2-name}}]({{doctor-critical-alerts-l2-link}}) to restart Doctor fabric router. After the Doctor fabric router is restarted, the problem may not be self-healed instantly, wait for half an hour and retry step 1.<br>

4. Restart Event Management API service
   - Go to **CI & CD** panel. Enter `doctor_eventcorrelation` in `Continuous Deployment` field.
   - Select each instance one at a time.
   - Click on the `restart service` action button.


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

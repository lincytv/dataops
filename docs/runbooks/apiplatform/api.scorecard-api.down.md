---
layout: default
title: "API Platform - Scorecard API is down"
type: Alert
runbook-name: "api.scorecard-api.down"
description: "This alert will be triggered when all instances of the Scorecard API service went down"
service: tip-api-platform
tags: api-scorecard, apis
link: /apiplatform/api.scorecard-api.down.html
---

## Purpose
This alert is triggered when Scorecard API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
Scorecard API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-scorecard%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Users of the Scorecard API will be unable to reach the service.


## Instructions to Fix
1. Verify if Scorecard API is indeed down
   - In a terminal, if the alert is for production, execute `curl {{site.data[site.target].oss-apiplatform.links.scorecard-api-prod.link}}`
     and if the alert is for staging, execute `curl {{site.data[site.target].oss-apiplatform.links.scorecard-api-stage.link}}`
    - The reply should be something like
      ```
      {
      "clientId":"scorecard",
      "description":"The Segments and Tribes API provides information about the associations between Segments, Tribes, and Services as well as compliance for the services.",
      "categories":["segmenttribe"],
      "segments":{"href":"https://pnp-api-oss.cloud.ibm.com/scorecard/api/segmenttribe/v1/segments"},
      "tribes":{"href":"https://pnp-api-oss.cloud.ibm.com/scorecard/api/segmenttribe/v1/tribes"},
      "services":{"href":"https://pnp-api-oss.cloud.ibm.com/scorecard/api/segmenttribe/v1/services"},
      "production_readiness":{"href":"https://pnp-api-oss.cloud.ibm.com/scorecard/api/segmenttribe/v1/production_readiness"
      }
      ```
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.

2. Check if Scorecard API is registered in API Catalog
   - Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   - Go to the **API Management** panel, in **API Catalog** tab, see if you can find the `scorecard` in the **API Catalog** table. If yes, then repeat step 1; otherwise wait for a couple of minutes to see if the API can re-register itself to the API Catalog. If you still do not see the `scorecard` in the Client ID column after a few minutes, go to next step.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/api_management/api_catalog2.png){:width="640px"}

3. See if it is Doctor Backend outages
   - If you are also seeing alerts for other Doctor outages at the same time. Then most likely it is related to Doctor fabric router issue, then please contact [{{doctor-critical-alerts-l2-name}}]({{doctor-critical-alerts-l2-link}}) to restart Doctor fabric router. After the Doctor fabric router is restarted, the problem may not be self-healed instantly, wait for half an hour and retry step 1.<br>

4. Restart Scorecard API service
   - Go to **CI & CD** panel. Enter `doctor_scorecard` in `Continuous Deployment` field.
   - Select each instance one at a time.
   - Click on the `restart service` action button.


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

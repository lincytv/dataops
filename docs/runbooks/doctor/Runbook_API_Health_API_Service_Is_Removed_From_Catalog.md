---
layout: default
description: Describe if an API service is not responding, and/or the API service has just been removed from the API catalog
title: RETIRED API Health API service is removed from catalog
service: doctor
runbook-name: API Health API service is removed from catalog
tags: oss, bluemix, doctor, api, health
link: /doctor/Runbook_API_Health_API_Service_Is_Removed_From_Catalog.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose

This alert will be triggered if an API service is found not responding, and the API service has just been removed from the API catalog.

## Technical Details

If an API service is removed from the API catalog, we need to find out why the API service was not responding. If it is just intermittent network issue, the API service will do self-healing by re-registering itself to the catalog.

## User Impact

If an API service is removed from all the API catalog instances, and the API service failed to re-register itself to the catalog, then user can no longer call any of the APIs from that API service.


## Instructions to Fix

1. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).

2. Go to the **API Management** panel, in **API Catalog** tab, see if you can find the client id mentioned in the PagerDuty details. If yes, go to next step; otherwise wait for a couple of minutes to see if the API can re-register itself to the API Catalog. If you still do not see the client id after a few minutes, restart the API service (see [Restart API Service](#restart-api-service) section below), and wait for 5 minutes.

3. If you do see the client id in the **API Catalog** table, then do curl to the url specified in `Source Info` column. For example, if the client id is "eventmgmtapi", then do<br>
`curl -XGET {{doctor-rest-apis-link}}/eventmgmtapi/api/info`<br>
If JSON data is returned in the response, this means the API service is up and running, you can resolve the PagerDuty alert. If ServiceNow incident was created, also resolve the ServiceNow incident.<br>
If there is error in the curl command, go to next step.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/api_management/api_catalog.png){:width="640px"}

4. Check the log of the API service (see [Check API Service Log](#check-api-service-log) section), and try to restart the API service (see [Restart API Service](#restart-api-service)  section) if you have not done so.<br>
If the client ID is "eventmgmtapi" or "scorecard", and you are also seeing Doctor outages at the same time. Then most likely it is related to Doctor fabric router issue, then please contact [{{doctor-critical-alerts-l2-name}}]({{doctor-critical-alerts-l2-link}}) to restart Doctor fabric router. After the Doctor fabric router is restarted, the problem may not be self-healed instantly, wait for half an hour and retry step 3.<br>
If the client ID is not "eventmgmtapi" and "scorecard",  and you did not find anything wrong from the log, and after restarting the API service, it still does not help, escalate the alert to level 2 of [{{tip-api-platform-policy-name}}]({{tip-api-platform-policy-link}}) (see the link and contact one of the people in the level 2).

5. Please note that this PagerDuty alert is not coming from TIP and is not coming from New Relic, you have to manually resolve this alert, and manually resolve ServiceNow incident at https://watson.service-now.com/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_userpref_module%3Db55fbec4c0a800090088e83d7ff500de%26sysparm_query%3Dactive%3Dtrue%5EEQ%26active%3Dtrue%26sysparm_clear_stack%3Dtrue. You can find the ServiceNow incident number in the PagerDuty alert.

## Restart API Service

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Go to **CI & CD** panel.
* Enter the corresponding service name from the table below in `Continuous Deployment` field.
* Select each instance one at a time.
* Click on the `restart service` action button.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_apicatalog_restart.png){:width="640px"}

```
 Client id                           | Service Name     
 ------------------------------------|--------------------------
 authapi                             | api_key_service  
 catalog                             | doctor_apicatalog
 doctorapi                           | api_doctor_api
 eventmgmtapi                        | doctor_eventcorrelation
 incidentmgmtapi, incidentmgmtxapi   | tip-IncidentMgmtAPI
 scorecard                           | doctor_scorecard
 subscription                        | subscription_api
                                     |
 api_health                          | api_health_monitor

```
## Check API Service Log

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Go to **CI & CD** panel.
* Enter the corresponding service name of the client id in `Continuous Deployment` field as described in [Restart API Service](#restart-api-service) section.
* Find the `Environment` that the API Service is running on.
* Go to **Remote Command**.
* Select that environment.
* Run the following command:<br>
  - `docker logs  <Service Name> --tail 100`

## Where to find metric in NewRelic

If the API service is not `eventmgmtapi` and `scorecard`, then you can find their metric data in NewRelic
https://insights.newrelic.com/accounts/1387904/dashboards/565366<br>
You can also find individual API service metric data from APM of NewRelic, below is the application name for each API service:<br>
```
 Client id                           | App Name     
 ------------------------------------|--------------------------
 authapi                             | Key Service
 catalog                             | API Catalog
 doctorapi                           | Doctor Service
 incidentmgmtapi, incidentmgmtxapi   | Incident Management API
 subscription                        | SubscriptionAPI
                                     |
 api_health                          | API Health

```
## Where the source code is located

If you need to look at the source code to investigate the issue, the table below shows the location of source code:<br>
```
 Client id          | Source Location     
 -------------------|---------------------------------------------------------------------------------------
 authapi            | https://github.ibm.com/cloud-sre/ToolsPlatform/tree/master/KeyServiceApi
 catalog            | https://github.ibm.com/cloud-sre/ToolsPlatform/tree/master/ApiCatalog
 doctorapi          | https://github.ibm.com/cloud-sre/ToolsPlatform/tree/master/DoctorServiceApi
 eventmgmtapi       | https://github.ibm.com/BlueMix-Fabric/doctor/tree/master/lib/services/eventcorrelation
 incidentmgmtapi    | https://github.ibm.com/cloud-sre/ToolsPlatform/tree/master/IncidentMgmtApi
 scorecard          | https://github.ibm.com/BlueMix-Fabric/doctor/tree/master/lib/services/scorecard
 subscription       | https://github.ibm.com/cloud-sre/SubscriptionAPI
                    |
 api_health         | https://github.ibm.com/cloud-sre/tip-api-health

```

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

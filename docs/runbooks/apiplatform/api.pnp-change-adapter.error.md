---
layout: default
title: "PnP Change Adapter down and other issues"
type: Alert
runbook-name: "api.pnp-change-adapter.error"
description: "This alert will be triggered when the PnP Change Adapter did not work properly"
service: tip-api-platform
tags: api-pnp-change-adpater
link: /apiplatform/api.pnp-change-adapter.error.html
---

## Purpose
Alerts will be triggered when PnP Change Adapter is not responding and/or NewRelic is not receiving metrics.

## Technical Details
The PnP Change Adapter will pull maintenance records from RTC and ServiceNow,then post the records to nq2ds queue.



## User Impact
Pnp database will be missing maintenance records from RTC and ServiceNow.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

This runbook is for many incidents that triggered by `pnp-change-adapter` . Please look for the title of the incident below, and follow the instructions in the runbook link.



### PnP change adapter down

   - `api-pnp-change-adpater_down`

   please follow the runbook to check if the pnp-change-adapter service is down.[PnP Change adapter down]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-change-adapter.down.html)



### ServiceNow API down

   - `api-pnp-change-adapter_getSNowFailed`
   - `api-pnp-change-adapter_getSnowCmdbCisFailed`
   - `api-pnp-change-adapter_getSnowEnvFailed`

   There are 3 different URLs for different tables in each environment. These 3 tables' name are **change_request**,**cmdb_ci** and **u_environment**.

   If ServiceNow is involved, check to make sure that ServiceNow API is working.  Please check if the alert comes from Production or Staging in the incident details. If you see `_prd` in the New Relic condition name, then it is production alert, for staging, it is `_stg`. Then obtain the required token and ServiceNow URL for different tables from [ServiceNow-URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/ServiceNow-URLs.html).

   For example, there is one alert which condition name is `api-pnp-change-adapter_getSNowFailed:eu-de:2:SLD6:prd`.
   It means there is something wrong when pnp-change-adapter tried to call the Production ServiceNow URL to get the "change_request" table. In this case, you need to execute the following command to check if the URL indeed down.

   ```
   curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/change_request?sysparm_query=u_environmentISNOTEMPTY^state%21=3^ORclosed_at%3Ejavascript:gs.beginningOfLast30Days%28%29^u_outage_duration%3Ejavascript:gs.getDurationDate%28%270%200:0:0%27%29&sysparm_offset=0&sysparm_limit=1
   ```

   If the request doesn't work,  check if there is something wrong with [ServiceNow](https://watson.service-now.com). Then try to restart the api-pnp-change-adapter service. If the issue still exists, please reassign the PagerDuty incident to tip-api-platform level 2.


### PnP Change adapter Parse data failed

   - `api-pnp-change-adapter_parseDoctorFailed`
   - `api-pnp-change-adapter_parseSNowFailed`
   - `api-pnp-change-adapter_parseSnowCmdbCisFail`
   - `api-pnp-change-adapter_parseSnowEnvFailed`

   Check the log(follow **Check logs in logDNA** section below) for the specific message that it was trying to unmarshal into data struct.
    - If the alert is `api-pnp-change-adapter_parseDoctorFailed`,please check log if there is any error when calling Doctor API. If so, please follow the [Doctor API failed]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-doctor-rtc-api.down.html)
    - If the alert is one of the last 3 alerts above, please check if there is any error when calling ServiceNow. If so, please follow the **ServiceNow API Down** section.
    - Try to restart the api-pnp-change-adapter service.
     In the terminal, execute `kubectl oss pod delete -l app=api-pnp-change-adapter -n api`.


### PnP Change adapter query db failed

   - `api-pnp-change-adapter_db_failed`

   Verify that Postgres is up and running and check if there are any current Postgres related alerts  [PostgreSQL / HAProxy service down and other issues]({{site.baseurl}}/docs/runbooks/apiplatform/api.postgres.down.html)

   Check the log(follow **Check logs in logDNA** section below) if there were any startup errors in connection.
   Check the logs for specific message. If the errors are api-pnp-change-adapter coding issues, then reassign the PagerDuty incident to tip-api-platform level 2.


### PnP Change adapter post msg failed

   - `api-pnp-change-adpater_mqPostFailed`

   Verify that RabbitMQ is up and running.Check if there is any RabbitMQ alert, if so, please follow the runbook [PnP RabbitMQ down]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html).

  Check that the configuration for RabbitMQ is correct. Check the log to see if there were any startup errors in connection.


### Check logs in logDNA

   - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
   - The logs should give some indication on what the problem is.
   - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
   - In each region, in a cluster, execute  
    `kubectl logs  -n api -l app=api-pnp-change-adpater -c api-pnp-change-adpater  --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.api-platform-prd.name}}]({{site.data[site.target].oss-slack.channels.api-platform-prd.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-stg.name}}]({{site.data[site.target].oss-slack.channels.api-platform-stg.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-dev.name}}]({{site.data[site.target].oss-slack.channels.api-platform-dev.link}})  

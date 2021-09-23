---
layout: default
title: "API Platform - PnP Resource Adapter has failed"
type: Alert
runbook-name: "api.pnp-resourceadapter.fail"
description: This alert will be triggered when there is a failure in the PnP Resource Adapter
service: tip-api-platform
tags: api-pnp-resourceadapter, apis
link: /apiplatform/api.pnp-resourceadapter.failed.html
---

## Purpose
There are multiple failure conditions that could cause these alerts to be generated:
- Posting resource or incident data to MQ
- Encrypting the payload
- Retrieving HTTP data from ServiceNow

## Technical Details
The PnP Resource Adapter(PRA) is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running.

The PRA will run automatically at 1 AM EST every day.  It collects
   - the resources from the global and OSS catalogs
      - combines the data out of the available data from those services
      - encrypts the data and passes it to the Rabbit MQ
   - the incident, case and change data from ServiceNow
      - validates the data is correct
      - combines the data from other tables in ServiceNow to create the data required
      - encrypts and pushes the data to the RabbitMQ    

The resource and ServiceNow data do not represent runtime dependencies.   The resource data changes rarely and the ServiceNow data is only really relevant in cases where the data needs to be recreated or validated to make sure data is up to date.

## New Relic
You can view the history and statistics of these problems by navigating to the bottom of the link below.   The sections are named "API Failures by ..."

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/759503?filters=%255B%257B%2522key%2522%253A%2522monitorName%2522%252C%2522value%2522%253A%2522resource-adapter%2522%252C%2522like%2522%253Atrue%257D%255D)

## User Impact
Resource or ServiceNow data could be out of date or not populated


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

- Before proceeding, [check Slack - {{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there is a reason for this issue

 | Incident Title | Runbook Link |
   | -------------- | ------------ |
   | api-pnp-resource-adapter failed in posting to MQ  | [MQ issues]({{page.url}}#encryption-or-mq-posting-errors) |
   | api-pnp-resource-adapter failed in encryption| [Encryption issues]({{page.url}}#encryption-or-mq-posting-errors) |
   | api-pnp-resource-adapter failed in http get from ServiceNow | [ServiceNow issues]({{page.url}}#servicenow) |
   | api-pnp-resource-adapter is down | [api.pnp-resourceadapter.down]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-resourceadapter.down.html) |


### Encryption or MQ Posting errors
 For failures in encryption or posting to MQ, check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-resource-adapter -c pi-pnp-resource-adapter --tail=50`  


Resolution is likely a failure in other components (for example the rabbit MQ or the vault).   Identify the problem component and take necessary actions to fix the issue there.  

For example if the MQ server is not responding, can you determine the cause (i.e. bad network resolution, the service is actually not available, bad connection or use [the MQ runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html)).  If it is not obvious what the problem or resolution is then [restart problem pod and escalate]({{page.url}}#after-remediation-steps) if that doesn't resolve it.


### ServiceNow
 If ServiceNow is involved, check to make sure that ServiceNow API is working.   Obtain [the necessary token credentials]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html)

     - incidents
        curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/incident?sysparm_query=resolved_at%3Ejavascript%3Ags.endOfThisMonth()%5EORresolved_atISEMPTY&sysparm_limit=1
     - case
        curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/sn_customerservice_case?sysparm_query=resolved_at%3Ejavascript%3Ags.endOfThisMonth()%5EORresolved_atISEMPTY&sysparm_limit=1
     - change
        curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/change_request?sysparm_query=u_environmentISNOTEMPTY^state%21=3^ORclosed_at%3Ejavascript:gs.beginningOfLast30Days%28%29^u_outage_duration%3Ejavascript:gs.getDurationDate%28%270%200:0:0%27%29&sysparm_offset=0&sysparm_limit=1

  If the request doesn't work, then [escalate]({{page.url}}#after-remediation-steps) directly.  Otherwise, try [restarting the pod]({{page.url}}#after-remediation-steps).


## After remediation steps

   Once all the issues have been resolved, use the command below torestart the PRA by killing the pod.   It will automatically restart and run an import.   It should be able to complete the process in less than 5 minutes without errors.

    - `kubectl oos pod delete api-pnp-resource-adapter -n api`

   If the steps above did not resolve the problem then reassign the PagerDuty incident to **tip-api-platform level 2.**



## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

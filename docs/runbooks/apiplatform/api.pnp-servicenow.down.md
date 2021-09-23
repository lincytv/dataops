---
layout: default
title: "API Platform - ServiceNow is down"
type: Alert
runbook-name: "api.pnp-servicenow.down"
description: This alert will be triggered when ServiceNow is not available
service: tip-api-platform
tags: api-pnp-servicenow, apis
link: /apiplatform/api.pnp-servicenow.down.html
---


## Purpose
This alert is triggered when ServiceNow is not available

{% capture cloud-newrelic-monitoring-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.slack }}{% endcapture %}
{% capture cloud-newrelic-monitoring-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.name }}{% endcapture %}
{% capture cloud-newrelic-monitoring-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.userid }}{% endcapture %}
{% capture cloud-newrelic-monitoring-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.notesid }}{% endcapture %}

## User Impact
ServiceNow is relied upon by the following services
   - Resource Adapter
   - Subscription Consumer
   - NQ2DS
   - PnP Hooks

Additionally most of the other services have an indirect realtime relationship to ServiceNow.  So if ServiceNow goes down much of the PnP functionality will be compromised.

## New Relic
You can view the history and statistics of these problems by navigating to the bottom of the link below.   The sections are named "API Failures by ..."

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/759503?filters=%255B%257B%2522key%2522%253A%2522monitorName%2522%252C%2522value%2522%253A%2522resource-adapter%2522%252C%2522like%2522%253Atrue%257D%255D)


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

- Before proceeding, [check Slack - {{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there is a reason for this issue

   1. First test the ServiceNow API on your local machine. Use a REST client like Postman or CURL to check that the ServiceNow API is working. Obtain [the necessary token credentials]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html)
      ```
         incidents:
         curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/incident?sysparm_query=resolved_at%3Ejavascript%3Ags.endOfThisMonth()%5EORresolved_atISEMPTY&sysparm_limit=1  

         case:
         curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/sn_customerservice_case?sysparm_query=resolved_at%3Ejavascript%3Ags.endOfThisMonth()%5EORresolved_atISEMPTY&sysparm_limit=1

         change:
         curl  -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/change_request?sysparm_query=u_environmentISNOTEMPTY^state%21=3^ORclosed_at%3Ejavascript:gs.beginningOfLast30Days%28%29^u_outage_duration%3Ejavascript:gs.getDurationDate%28%270%200:0:0%27%29&sysparm_offset=0&sysparm_limit=1
      ```

         Expect a response to look something like this:
         ```
            {
            "result": [
            {
                  "u_affected_activity": "",
                  "parent": {
                     "link": "https://watson.service-now.com/api/now/table/task/ea8143d7db0683c0da1ed11c5e961927",
                     "value": "xxx"
                  },
                  "u_tribe": {
                     "link": "https://watson.service-now.com/api/now/table/u_tribe/8f4b1fc5db8903008799327e9d961974",
                     "value": "xxx"
                  },
                  "upon_reject": "cancel",
                  ...

        ```        

      If the requests do not work, then [escalate immediately]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-servicenow.down.html#escalation) directly.

   2. If the requests work locally, then make sure that the requests work in the server environment. This can be done by entering into the subscription pod and running the curl commands from step 1

        ```
        kubectl get po|grep subscription
        kubectl exec -it api-pnp-subscription-<pod id> -- sh
        curl -H 'Authorization: Bearer <TOKEN>' https://watson.service-now.com/api/now/table/incident?sysparm_query=resolved_at%3Ejavascript%3Ags.endOfThisMonth()%5EORresolved_atISEMPTY&sysparm_limit=1
        ```       
      If the request fails but step 1 shows that the service is available then it would be an issue for [the TF team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html) to look into.

   3. Lastly validate that ServiceNow traffic is moving or being held up.  This can be done by reviewing the logs or submitting the same requests in the shell environment of the server.   The PnP Hooks server is a good service to use to monitor activity

      - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
      - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
         - In each region, in a cluster, execute  
            `kubectl logs -napi -lapp=api-pnp-hooks -c api-pnp-hooks --since=15m`  
            
            Below is an example of what a log entry from ServiceNow should look like
            ```
            2018/12/04 23:21:05.988275 snowIncidents.go:24: Invoking SNow Incidents
            2018/12/04 23:21:05.988348 handleMessage.go:24: Raw message: { "operation": "insert", "sys_id": "Hexadecimal Value Here", "number": "INC0000001-us-east", "sys_created_on": "2018-11-22 10:50:20", "incident_state": "New", "u_disruption_ended": "2018-11-22 10:50:11", "u_disruption_began": "2018-11-22 10:25:08", "priority": "Sev - 1", "u_status": "Confirmed CIE", "short_description": "PnP Heartbeat - NewRelic Syntetics", "description": "", "cmdb_ci": "pnp-api-oss", "comments": "", "sys_updated_on": "2018-12-04 23:21:05", "u_environment": "IBM Public US-SOUTH (YP)", "u_description_customer_impact": "PnP heatbeat", "u_current_status": "", "u_affected_activity": "Availability", "crn": [ "crn:v1:bluemix:public:pnp-api-oss:us-east:::pnp-incident:" ], "instance": "newrelic"}
            2018/12/04 23:21:05.990396 snowIncidents.go:34: successfully produced incident to RabbitMQ
            ```


## Escalation
  - Check [IBM ServiceNow Slack channel]({{site.data[site.target].oss-slack.channels.velocity-config.link}}) for any messages about this outage.  If not, raise an inquiry.
  - Create a Severity 1 [incident](https://watson.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D-1%26sysparm_query%3Dactive%3Dtrue%26sysparm_stack%3Dincident_list.do%3Fsysparm_query%3Dactive%3Dtrue) in ServiceNow.
   - The Configuration Item of the incident should be 'servicenow'
   - Add 'michael_lee@us.ibm.com' to the watchlist (In the Notes section of the incident)


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

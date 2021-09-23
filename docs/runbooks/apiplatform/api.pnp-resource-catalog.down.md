---
layout: default
title: "API Platform - PnP Resource Catalog is down"
type: Alert
runbook-name: "api.pnp-resource-catalog.down"
description: This alert will be triggered when the resource catalog service is not available
service: tip-api-platform
tags: api-pnp-resource-catalog, apis
link: /apiplatform/api.pnp-resource-catalog.down.html
---

## Purpose
This alert is triggered when Resource Catalog is not available

{% capture cloud-newrelic-monitoring-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.slack }}{% endcapture %}
{% capture cloud-newrelic-monitoring-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.name }}{% endcapture %}
{% capture cloud-newrelic-monitoring-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.userid }}{% endcapture %}
{% capture cloud-newrelic-monitoring-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.notesid }}{% endcapture %}


## Technical Details
The Resource Catalog is used by the PnP Resource Adapter to obtain the resource records that will be used by the PnP services.  The sync activity is run once a day at 1 AM


[The NewRelic synthetic](https://synthetics.newrelic.com/accounts/1926897/monitors/c9367985-a0e8-4d39-aaff-dcb731c658d5/results) tracks the health of the resource catalog.


## User Impact
Resource data could be out of date or not populated


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

When getting this alert, please check the slack channel [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) if there is any upgrade going on.


1. Verify if Resource Catalog API is not responding by running a curl command.
 - In a terminal, execute
   ```
   curl  'https://resource-catalog.bluemix.net/api/v1'
   ```
 - It should normally return a JSON list of all the available resources.


2. Try the curl command above on your local machine as well as in the different Kube regions.   If it works in any of the regions or on your local machine, then the problem is network related.  We will need to determine why the service cannot connect to the catalog url.

Document the issue the connection errors finding the errors

3. Check logs in logDNA and document the connection errors. Then reassign the PagerDuty incident to **tip-api-platform level 2.**
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-resource-adapter -c api-pnp-resource-adapter --since=15m`  
    If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  


4.  If the curl commands are not able to connect to the resource catalog, we will need contact the global catalog team.  
  - Create a Severity 1 [incident](https://watson.service-now.com/nav_to.do?uri=%2Fincident.do%3Fsys_id%3D-1%26sysparm_query%3Dactive%3Dtrue%26sysparm_stack%3Dincident_list.do%3Fsysparm_query%3Dactive%3Dtrue) in ServiceNow.
  - The Configuration Item of the incident should be 'globalcatalog'
  - Add 'michael_lee@us.ibm.com' to the watchlist (In the Notes section of the incident)


## After remediation steps

   If all the issues have been resolved, use the command below to restart the Resource Adapter in any of the production environments by killing the pod.   It will automatically restart and run an import.   It should be able to complete the process in less than 5 minutes without errors.

    - `kubectl oss pod delete pod -l app=api-pnp-resource-adapter -n api`


If the steps above did not resolve the problem then reassign the PagerDuty incident to **tip-api-platform level 2.**





## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

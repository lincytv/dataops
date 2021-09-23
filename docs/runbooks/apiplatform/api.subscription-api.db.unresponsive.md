---
layout: default
title: Subscription API unable to contact PostgresSQL
type: Alert
runbook-name: "api.subscription-api.db.unresponsive"
description: "Subscription API is unable to contact the PostgresSQL database."
service: tip-api-platform
tags: subscription API, subscription Consumer, scorecard, Key Service API, Postgresql
link: /apiplatform/api.subscription-api.db.unresponsive.html
---

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

{% capture sosat-tools-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.slack }}{% endcapture %}
{% capture sosat-tools-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.name }}{% endcapture %}
{% capture sosat-tools-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.userid }}{% endcapture %}
{% capture sosat-tools-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.notesid }}{% endcapture %}

## Purpose

Troubleshoot and resolve issues with Subscription API not being able to contact PostgresSQL database.

## Technical Details

Subscription API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 2 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-sosat.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-subscription-api%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

The way the monitoring is set up in this case is that for every GET request to `{{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}}`, the database connectivity is tested and reported to NewRelic. If NewRelic does not receive this heartbeat, this alert is triggered.

### New Relic Metrics

[API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-subscription-api%2522%257D%255D)

## User Impact

Users and the Subscription Consumer will not be able to query Subscription API. Users will be unable to make changes to their subscriptions. This should not impact the Subscription Consumer as it holds a copy of all subscription in-memory, it is only impacted if the Subscription Consumer pods are restarted (which is when the consumer queries Subscription API the first time for all subscriptions).

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check whether Subscription API is responding
    - `curl {{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}}`

    The reply should be:  
    `{"href":{{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}},"code":0,"description":"API is available and operational"}`
    If you get this reply then at least one pod is working and the database connectivity is working. New Relic maybe not be querying `/subscription/healthz` or not receiving metrics. The next step we can check if NewRelic is receiving metrics from any of the pods running Subscription API.

2. Check NewRelic graph in the open Incidents
    - Open [{{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1387904/incidents]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1387904/incidents) and find the open incident and click on it. A graph will be shown on the right-hand side of the screen. It should be higher than 0 (zero). If it is then the issue should resolve by itself and the incident should close itself.
    - If the graph still shows 0 (zero) at any part of the graph in the last 15min, the incident will not get resolved.
        - There are 2 possibilities:
        1. New Relic is not querying `/subscription/healthz`, and so metrics are not being sent to NewRelic.  If something is wrong with New Relic, check the [status page of New Relic]({{site.data[site.target].oss-apiplatform.links.new-relic-status.link}}). You should see all operational.
        2. The connection to the database is not healthy. We'll address this in step 3.

3. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-subscription-api%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl get po -napi -lapp=api-subscription-api`
        - You should see 2 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Healthz_Path.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure. See [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)

4. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute   
    `kubectl logs -napi -lapp=api-subscription-api -c api-subscription-api --since=5m`  
      

If Subscription API is not working after these steps, contact {{site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name}} or {{site.data[site.target].oss-contacts.contacts.sosat-tools.name}}, emails below.

## Contacts

**PagerDuty**
* Production [{{site.data[site.target].oss-sosat.links.sosat-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-critical-alerts.link}})
* Dev or Test [{{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.sosat-monitor-prod.name}}]({{site.data[site.target].oss-slack.channels.sosat-monitor-prod.link}})  

**Runbook Owners**
* {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}
* {% include contact.html slack=sosat-tools-slack name=sosat-tools-name userid=sosat-tools-userid notesid=sosat-tools-notesid %}

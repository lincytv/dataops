---
layout: default
title: Subscription API is unable to initialize services and tribes cache
type: Alert
runbook-name: "api.subscription-api.services-cache-failed"
description: "Subscription API is unable to initialize services and tribes cache"
service: tip-api-platform
tags: subscription API, subscription consumer, Postgresql, gcor
link: /apiplatform/api.subscription-api.services-cache-failed.html
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

Troubleshoot and resolve issues with Subscription API not being able to initialize services and tribes cache.

## Technical Details

Subscription API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 2 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-sosat.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-subscription-api%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

When this alert is triggered it means that Subscription API could not initialize the cache that holds services and tribes, which are retrieved from GCOR Services API. The cache is used to validate whether a service or tribe name is valid or not. This has low impact to the overall functionality of the Subscription API.  

### New Relic Metrics

[API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-subscription-api%2522%257D%255D)

## User Impact

This impacts only the query filter in the subscription. So users will not be able to update or create subscriptions using the query filter attributes `tribe_name`and `service_name`.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html), and find the link for Subscription API  
    - Look for `failed to initialize gcor cache` in the logs, if a very recent entry is found then this means the cache has not been built yet  
    - The specific error to the call to GCOR API is found just before the `failed to initialize gcor cache` entry. See what the error is, it should indicate the cause of the problem  
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-subscription-api -c api-subscription-api --since=5m`  
    If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  

What you need to search for are entries that contains `gcor_cache.go`, the error message will be printed.
The probable reason for the cache not initializing is some network issue or with the GCOR API.

If the problem is with the GCOR API, an alert should be open in NewRelic Alerts for the GCOR API. Follow instructions provided in the runbook linked in the incident.

If the problem is related to the network, test if you are able to reach Subscription API, try the following link:
[{{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}}]({{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}})

The reply should be:  
    `{"href":{{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}},"code":0,"description":"API is available and operational"}`

If the response is different then something is up with Subscription API, which should have another alert open in NewRelic, which should be worked out.

If you see that the issue persists in the logs, and you are able to reach Subscription API successfully then contact {{site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name}} or {{site.data[site.target].oss-contacts.contacts.sosat-tools.name}}, emails below.

## Contacts

**Runbook Owners**
* {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}
* {% include contact.html slack=sosat-tools-slack name=sosat-tools-name userid=sosat-tools-userid notesid=sosat-tools-notesid %}

---
layout: default
title: API Platform component down in Kubernetes
type: Alert
runbook-name: api-platform-component-down-in-k8s
description: "API Platform component down in Kubernetes"
service: tip-api-platform
tags: tip,kibana,logstash,elastic
link: /apiplatform/api-platform-component-down-in-k8s.html
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
This alert is triggered if an API Platform component no longer has any running pods in an Armada cluster. In each region, there are two or more pod instances running depending on the API.

## Technical Details
API Platform components are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`.

NRQL monitors have been set up in New Relic to monitor various pods (representing API Platform components) in certain kubernetes clusters. In this case, no pods seem to be running the specific API Platform component.

New Relic alerts policies that are monitoring Kube pods using NRQL conditions:
1. [oss_api_platform_k8s_dev](https://alerts.newrelic.com/accounts/1926897/policies/238302)
2. [oss_api_platform_k8s_stg](https://alerts.newrelic.com/accounts/1926897/policies/247899)
3. [oss_api_platform_k8s_prd](https://alerts.newrelic.com/accounts/1926897/policies/247900)

## User Impact
If no pods are running for the API, the API will not be reachable in that region so this alert is critical to resolve.

## Instructions to Fix

The following are the components monitored and their associated runbooks with more detailed instructions to fix:

 - [api-api-catalog](api.catalog-api.down.html)
 - [api-key-service](api.key-service-api.down.html)
 - [api-incident-management](api.incidentmgmt-api.down.html)
 - [api-subscription-api](api.subscription-api.unresponsive.html)
 - [api-event-management](api.eventmgmt-api.down.html)
 - [api-scorecard](api.scorecard-api.down.html)

It is important NOT to manually resolve a New Relic incident.

Fix the problem at its source (the application), and the New Relic incident will resolve itself.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.api-platform-prd.name}}]({{site.data[site.target].oss-slack.channels.api-platform-prd.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-stg.name}}]({{site.data[site.target].oss-slack.channels.api-platform-stg.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-dev.name}}]({{site.data[site.target].oss-slack.channels.api-platform-dev.link}})  

**Runbook Owners**
* {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}
* {% include contact.html slack=sosat-tools-slack name=sosat-tools-name userid=sosat-tools-userid notesid=sosat-tools-notesid %}

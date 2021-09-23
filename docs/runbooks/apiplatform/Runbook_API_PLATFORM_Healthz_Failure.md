---
layout: default
title: API PLATFORM Healthz Failures
type: Alert
runbook-name: "Runbook_API_PLATFORM_Healthz_Failure"
description: "API PLATFORM Healthz Failures"
service: tip-api-platform
tags: api-api-catalog,api-doctor-api,api-incident-management,api-key-service_healthz,api-subscription-api
link: /apiplatform/Runbook_API_PLATFORM_Healthz_Failure.html
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
This alert is triggered if the NewRelic PING or API synthetic monitors for an API Platform component have failed.

## Technical Details
API Platform components are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are two or more pod instances running depending on the API.

PING and API synthetic monitors have been set up in New Relic to monitor the healthz url of API Platform components in each region (i.e. the URL tested is the regional URL for the API component so we know the test is calling the correct region).

New Relic alerts policies that contain the PING and API synthetic alert conditions:
1. [oss_api_platform_synthetics_dev](https://alerts.newrelic.com/accounts/1926897/policies/266967)
2. [oss_api_platform_synthetics_stg](https://alerts.newrelic.com/accounts/1926897/policies/266968)
3. [oss_api_platform_synthetics_prd](https://alerts.newrelic.com/accounts/1926897/policies/266970)

## User Impact
The API component may not be reachable or functioning correctly so this alert is critical to resolve.

## Instructions to Fix

The following are the components monitored and their associated runbooks with more detailed instructions to fix:

 - [api-api-catalog](api.catalog-api.down.html)
 - [api-key-service](api.key-service-api.down.html)
 - [api-incident-management](api.incidentmgmt-api.down.html)
 - [api-subscription-api](api.subscription-api.unresponsive.html)
 - [api-event-management](api.eventmgmt-api.down.html)
 - [api-scorecard-backend](api.scorecard-pod-down-in-k8s.html)
 - [api-scorecard](api.scorecard-api.down.html)
 - [api-gcor-api](api.scorecard-pod-down-in-k8s.html)
 - [api-pnp-status-api](api.pnp-status.down.html)
 - [api-pnp-subscription-api](api.pnp-subscription-api.down.html)
 - [api-pnp-hooks-api](api.pnp-hooks-api.down.html)
 - [api-edb-ingestor-api](api.edb-api-healthz.failed.html)
 - [api-edb-mapping-api](api.edb-api-healthz.failed.html)
 - [api-edb-processing-status-api](api.edb-api-healthz.failed.html)
 - [api-edb-audit-api](api.edb-api-healthz.failed.html)

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

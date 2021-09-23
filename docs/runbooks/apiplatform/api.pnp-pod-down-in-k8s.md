---
layout: default
title: API Platform - PnP component down in Kubernetes
type: Alert
runbook-name: api.pnp-pod-down-in-k8s.md
description: "API Platform - PnP component down in Kubernetes"
service: tip-api-platform
tags: tip, pnp
link: /apiplatform/api.pnp-pod-down-in-k8s.html
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
This alert is triggered if one or more pods of an API Platform PnP component is down. In each region, there are one or more pod instances running depending on the component.

## Technical Details
API Platform PnP components are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`, except for api-pnp-db-cleaner which is only deployed to `us-east`.

NRQL monitors have been set up in New Relic to monitor pods for each PnP component in each region, and there are also NR API scripts set up to monitor each component globally, except for API components.

New Relic alerts policies that are monitoring Kube pods using NR API scripts globally (sev 1):
1. [oss_pnp_k8s_global_prd]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/policies/357448)
2. [oss_pnp_k8s_global_stg]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/policies/357363)

New Relic alerts policies that are monitoring Kube pods using NRQL conditions by region (sev 2):
1. [oss_pnp_k8s_prd]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/policies/320343)
2. [oss_pnp_k8s_stg]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/policies/320342)


## User Impact
Whenever you see `everywhere` in the incident title, it is a sev 1 alert, it indicates that no pods are running for that specific PnP component in any region, this kind of alert is critical to resolve.

If only one region is down for a component, that component should still be able to function, except for api-pnp-db-cleaner, which is only deloyed to `us-east`.

## Instructions to Fix

If it is a sev 2 alert, then check the slack channel [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) if there is any upgrade going on.  

The following are the components monitored and their associated runbooks with more detailed instructions to fix:

 - [api-pnp-bspn-loader](api.pnp-bspn-loader.down.html)
 - [api-pnp-case-api](api.pnp-case.down.html)
 - [api-pnp-change-adapter](api.pnp-change-adapter.down.html)
 - [api-pnp-db-cleaner](api.pnp-db-cleaner.failed.html)
 - [api-pnp-deadletter-consumer](api.pnp-deadletter-consumer.down.html)
 - [api-pnp-hooks-api](api.pnp-hooks-api.down.html)
 - [api-pnp-maintenance-status-consumer](api.pnp-maintenance-status-consumer.down.html)
 - [api-pnp-notifications-adapter](api.pnp-notifications-adapter.down.html)
 - [api-pnp-notifications-consumer](api.pnp-notifications-consumer.failed.html)
 - [api-pnp-nq2ds](api.pnp-nq2ds.down.html)
 - [api-pnp-resource-adapter](api.pnp-resourceadapter.down.html)
 - [api-pnp-status-api](api.pnp-status.down.html)
 - [api-pnp-status-consumer](api.pnp-status-consumer.down.html)
 - [api-pnp-subscription-api](api.pnp-subscription-api.down.html)
 - [api-pnp-subscription-consumer](api.pnp-subscription-consumer.failed.html)



It is important NOT to manually resolve a New Relic incident.

Fix the problem at its source, and the New Relic incident will resolve itself.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.api-platform-prd.name}}]({{site.data[site.target].oss-slack.channels.api-platform-prd.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-stg.name}}]({{site.data[site.target].oss-slack.channels.api-platform-stg.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-dev.name}}]({{site.data[site.target].oss-slack.channels.api-platform-dev.link}})  

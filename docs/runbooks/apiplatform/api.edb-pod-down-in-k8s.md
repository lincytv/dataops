---
layout: default
title: API Platform - EDB component down in Kubernetes
type: Alert
runbook-name: api.edb-pod-down-in-k8s.md
description: "API Platform - EDB component down in Kubernetes"
service: tip-api-platform
tags: tip, edb
link: /apiplatform/api.edb-pod-down-in-k8s.html
---

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

## Purpose
This alert is triggered if one or more pods of an API Platform EDB component is down. In each region, there are one or more pod instances running depending on the component.

## Technical Details
API Platform EDB components are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`.

NRQL monitors have been set up in New Relic to monitor pods for each EDB component in each region, and there are also NR API scripts set up to monitor each component globally, except for API components.

New Relic alerts policies that are monitoring Kube pods using NR API scripts globally (sev 1):
1. [oss_edb_k8s_global_prd]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/424807)
2. [oss_edb_k8s_global_stg]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/424758)

New Relic alerts policies that are monitoring Kube pods using NRQL conditions by region (sev 2):
1. [oss_edb_k8s_prd]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/418509)
2. [oss_edb_k8s_stg]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/418506)


## User Impact
Whenever you see `everywhere` in the incident title, it is a sev 1 alert, it indicates that no pods are running for that specific EDB component in any region, this kind of alert is critical to resolve.

If only one region is down for a component, that component should still be able to function.

## Instructions to Fix

If it is a sev 2 alert, then check the slack channel [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) if there is any upgrade going on.  

The following are the components monitored and their associated runbooks with more detailed instructions to fix:
 - [api-edb-adapter-cie](api.edb-adapter-cie.error.html)
 - [api-edb-adapter-dry-run](api.edb-adapter-dryrun.error.html)
 - [api-edb-adapter-metrics](api.edb-adapter-metrics.error.html)
 - [api-edb-adapter-metrics-backup](api.edb-adapter-metrics.error.html)
 - [api-edb-adapter-sysdig](api.edb-adapter-sysdig.error.html)
 - [api-edb-adapter-tip](api.edb-adapter-tip.error.html)
 - [api-edb-audit](api.edb-audit.error.html)
 - [api-edb-ingestor](api.edb-api-healthz.failed.html)
 - [api-edb-mapping-api](api.edb-api-healthz.failed.html)
 - [api-edb-mapping-consumer](api.edb-mapping-consumer.error.html)
 - [api-edb-processing-status](api.edb-api-healthz.failed.html)



It is important NOT to manually resolve a New Relic incident.

Fix the problem at its source, and the New Relic incident will resolve itself.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

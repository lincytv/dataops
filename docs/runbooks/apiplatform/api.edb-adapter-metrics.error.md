---
layout: default
title: "EDB Metrics Adapter down and other issues"
type: Alert
runbook-name: "api.edb-adapter-metrics.error"
description: "This alert will be triggered when the EDB Metrics Adapter did not work properly"
service: tip-api-platform
tags: api-edb-adapter-metrics, edb, metrics, sysdig
link: /apiplatform/api.edb-adapter-metrics.error.html
---

## Purpose
Alerts will be triggered when EDB metrics adapter is not responding and/or NewRelic is not receiving metrics.

## Technical Details
api-edb-adapter-metrics collects rolling availability data. api-edb-adapter-metrics-backup collects daily availability data. api-edb-adapter-metrics-sysdig sends availability data as platform metrics.  They all share the same base code (under edb-adapter-metrics), while deployed using different configurations. There should only be 1 instance of `api-edb-adapter-metrics-backup` running across all regions (currently set to only run in `us-south` on production and `us-east` on staging). There should only be 1 instance of `api-edb-adapter-metrics-sysdig` running across all regions (currently set to only run in `us-south` on production and `us-east` on staging). Its dependencies include RabbitMQ, MongoDB, and Redis.

## User Impact
If any of its dependencies go down, metrics data will not be collected and processed accurately.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### `edb-Mongo-Error` is not null in NR Transaction `edb-adapter-metrics-EventLoop` or `edb-adapter-metrics-EventLoopDaily`
Verify that Cloudant is up, see [API Platform - EDB Cloudant has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-cloudant.down.html)

### `edb-Redis-Send-Error` is not null in NR Transaction `edb-adapter-metrics-recordMetrics`
Verify that Redis is up, see [API Platform - EDB Redis has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-redis.down.html)

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-edb-adapter-metrics -c api-edb-adapter-metrics --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)
   - In us-south (production) or us-east (staging), execute  
    `kubectl logs  -n api -l app=api-edb-adapter-metrics-backup -c api-edb-adapter-metrics-backup --tail=50` or
    `kubectl logs  -n api -l app=api-edb-adapter-metrics-sysdig -c api-edb-adapter-metrics-sysdig --tail=50`



If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

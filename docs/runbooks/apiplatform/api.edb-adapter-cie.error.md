---
layout: default
title: "EDB CIE Adapter down and other issues"
type: Alert
runbook-name: "api.edb-adapter-cie.error"
description: "This alert will be triggered when the EDB CIE Adapter did not work properly"
service: tip-api-platform
tags: api-edb-adapter-cie, edb, adapter, cie
link: /apiplatform/api.edb-adapter-cie.error.html
---

## Purpose
Alerts will be triggered when CIE adapter is not responding and/or NewRelic is not receiving metrics for this application.

## Technical Details
api-edb-adapter-cie processes CIE data sent in by service teams. Its dependencies include RabbitMQ, MongoDB, and Redis.

## User Impact
If any of its dependencies go down, CIE data sent in by service teams will not be collected and processed accurately.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### `edb-Mongo-Error` is not null in NR Transaction
Verify that MongoDB is up, see [API Platform - EDB MongoDB has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-mongodb.down.html)

### `edb-adapter-cie-postStatusErr` is not null in NR Transaction
Verify that Redis is up, see [API Platform - EDB Redis has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-redis.down.html)

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

### Check logs

   - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-edb-adapter-cie  -c api-edb-adapter-cie --tail=50` (The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)



If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

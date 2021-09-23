---
layout: default
title: "API Platform - PostgresDB failover monitoring"
type: Alert
runbook-name: "api.postgres-monitor.failed"
description: "This alert will be triggered if the OSS PostgresDB servers failed over"
service: tip-api-platform
tags: apis, apigateway
link: /apiplatform/api.postgres-monitor.failed.html
---
{% capture tip-api-platform-1-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.slack }}{% endcapture %}
{% capture tip-api-platform-1-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.name }}{% endcapture %}
{% capture tip-api-platform-1-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.userid }}{% endcapture %}
{% capture tip-api-platform-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.notesid }}{% endcapture %}

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

## Purpose
This alert will be triggered if the OSS PostgresDB servers failover (primary becomes slave and slave becomes primary).

## Technical Details
The [api-postgres-monitor](https://github.ibm.com/cloud-sre/api-postgres-monitor) program runs on both of the OSS Postgres servers and reports which server is primary and which server is slave to NewRelic. If this cluster status changes (i.e. there is a failover), NewRelic will alert.

## User Impact
- Should not impact users
- However, we need to ensure investigate why the former primary Postgres server failed and ensure it recovers correctly so that the failover can automatically happen again in the future if needed

## Instructions to Fix
1. Confirm whether a failover actually has occurred by checking the cluster states in the [OSS PostgresDB Status ](https://insights.newrelic.com/accounts/1926897/dashboards/986134) NewRelic dashboard.
2. If a failover has occurred, recover the former primary server using [https://ibm.ent.box.com/file/341004580814](https://ibm.ent.box.com/file/341004580814) and update the alert conditions in NewRelic to reflect which server is now primary and which server is now slave
3. If a failover did not occur, investigate why there was a cluster state change

## Notes and Special Considerations

None

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

---
layout: default
title: RETIRED API Platform - api-postgres-monitor program instance is down
type: Alert
runbook-name: "api.postgres-monitor.down"
description: "This alert is triggered when NewRelic is not receiving metrics from the api-postgres-monitor program"
service: tip-api-platform
tags: apis, apigateway
link: /apiplatform/api.postgres-monitor.down.html
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
This alert is triggered when NewRelic is not receiving metrics from the api-postgres-monitor program anymore.

## Technical Details
The [api-postgres-monitor](https://github.ibm.com/cloud-sre/api-postgres-monitor) program runs on both of the OSS Postgres servers and reports which server is primary and which server is slave to NewRelic. The api-postgres-monitor program sends a transaction to NewRelic approximately once every 5 minutes. If NewRelic stops receiving transactions from the api-postgres-monitor program, this alert will be raised.

## User Impact
If the api-postgres-monitor programs are no longer running, our team will not be alerted if a database failover occurs.

## Instructions to Fix
1. Verify whether the api-postgres-monitor programs are running or not
   - Log onto the Postgres VMs (see the [How to access the OSS Postgres and HAProxy servers](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/ibm/API_Platform_Postgres.html) runbook)
   - Change to root: `sudo -i`
   - Execute the following command to check the status of the program: `systemctl status api-postgres-monitor`
   - Check the log file: `cat /opt/ibm/api-postgres-monitor/api-postgres-monitor.log`
2. If the programs are running and there are no errors, check the following URL to see NewRelic is having temporary problems (i.e. alert is a false positive)
   - [https://status.newrelic.com](https://status.newrelic.com)

## Notes and Special Considerations

None

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

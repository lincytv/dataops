---
layout: default
title: "RETIRED - API Platform - Kong monitor container instance is down"
type: Alert
runbook-name: "RETIRED - api.kong-monitor.down"
description: "RETIRED - This alert is triggered when NewRelic is not receiving metrics from the api-kong-monitor containers"
service: tip-api-platform
tags: apis, apigateway
link: /apiplatform/api.kong-monitor.down.html
---

**Kong has been removed as it's no longer needed - see [github issue](https://github.ibm.com/cloud-sre/ToolsPlatform/issues/9975)**

{% capture tip-api-platform-1-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.slack }}{% endcapture %}
{% capture tip-api-platform-1-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.name }}{% endcapture %}
{% capture tip-api-platform-1-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.userid }}{% endcapture %}
{% capture tip-api-platform-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.notesid }}{% endcapture %}

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

## Purpose
This alert is triggered when NewRelic is not receiving metrics from the api-kong-monitor containers anymore.

## Technical Details
The [api-kong-monitor](https://github.ibm.com/cloud-sre/api-kong-monitor) container runs in each of the staging and production api-kong pods in the `api` namespace of the OSS Kube instances. The api-kong-monitor container sends a transaction to NewRelic approximately once every 5 minutes. If NewRelic stops receiving transactions from the api-kong-monitor container, this alert will be raised.

## User Impact
If the api-kong-monitor containers are no longer running, our team will not get an early warning if Kong loses it's connection to the Kong PostgresSQL database.

## Instructions to Fix
1. Check the logs of the api-kong-monitor containers in LogDNA to ensure they are running and for any errors
   - See [wiki page](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/How-to-view-Armada-log-on-LogDNA) for information on how to access and view K8s logs on LogDNA
   - Go to LogDNA Instance: [IBM Cloud Log Analysis with LogDNA-OSS IKS](https://app.us-south.logging.cloud.ibm.com/ext/ibm-sso/22ac4e2ebc)
   - There is a api-kong-monitor view for staging and production under the `API PLATFORM` category in LogDNA
2. If the containers are running and there are no errors, check the following URL to see NewRelic is having temporary problems (i.e. alert is a false positive)
   - [https://status.newrelic.com](https://status.newrelic.com)

## Notes and Special Considerations

None

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

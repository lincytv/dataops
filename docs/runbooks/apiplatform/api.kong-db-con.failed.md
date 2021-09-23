---
layout: default
title: "RETIRED - API Platform - Kong DB connection failed"
type: Alert
runbook-name: "RETIRED - api.kong-db-con.failed"
description: "RETIRED - This alert will be triggered if the Kong database can not be reached"
service: tip-api-platform
tags: apis, apigateway
link: /apiplatform/api.kong-db-con.failed.html
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
This alert will be triggered if the Kong PostgresSQL database can not be reached by the api-kong-monitor container that is running in one or more of the staging or production api-kong pods.

## Technical Details
The [api-kong-monitor](https://github.ibm.com/cloud-sre/api-kong-monitor) container runs in each of the staging and production api-kong pods in the `api` namespace of the OSS Kube instances. The api-kong-monitor container tries to ping and run a simple SQL query against the Kong PostgresSQL database every 5 minutes. If this test fails, a NewRelic alert is created.

## User Impact
- **HIGH IMPACT**
- Calls to API Platform, TIP, EDB, PnP, and Doctor APIs through Kong may start to fail
- Kong can survive without a database for a period of time, but the Kong cache can be invalidated at which time API calls will start to fail

## Instructions to Fix

1. Check whether you are receiving other PagerDuty incidents like the API Catalog /healthz not being reachable
   - If you are, this alert is already causing an impact
2. If the problem is isolated to one region, one temporary solution while the problem is being investigated is to remove the region (origin pool) from the CIS-PnP-Stage or CIS-PnP-Prod CIS configurations under the OSS Account in https://cloud.ibm.com
3. Check the logs of the api-kong-monitor containers in LogDNA for any errors
   - See [wiki page](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/How-to-view-Armada-log-on-LogDNA) for information on how to access and view K8s logs on LogDNA
   - Go to LogDNA Instance: [IBM Cloud Log Analysis with LogDNA-OSS IKS](https://app.us-south.logging.cloud.ibm.com/ext/ibm-sso/22ac4e2ebc)
   - There is a api-kong-monitor view for staging and production under the `API PLATFORM` category in LogDNA

## Notes and Special Considerations

These alerts should be treated as high priority as they can impact multiple OSS services such as TIP, PnP, and EDB.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

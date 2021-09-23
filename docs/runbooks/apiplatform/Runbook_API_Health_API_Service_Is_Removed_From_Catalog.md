---
layout: default
description: "Runbook API Health API Service Is Removed From Catalog"
title: "Runbook API Health API Service Is Removed From Catalog"
service: tip-api-platform
runbook-name: "Runbook API Health API Service Is Removed From Catalog"
tags: oss, bluemix, doctor, tip-api-platform, api
link: /apiplatform/Runbook_API_Health_API_Service_Is_Removed_From_Catalog.html
type: Alert
---

{% capture tip-api-platform-1-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.slack }}{% endcapture %}
{% capture tip-api-platform-1-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.name }}{% endcapture %}
{% capture tip-api-platform-1-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.userid }}{% endcapture %}
{% capture tip-api-platform-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.notesid }}{% endcapture %}

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

# API Health - API service is removed from catalog

## Purpose
This alert will be triggered if an API service is found not responding and the API service has just been removed from the API catalog.

## Technical Details
If an API service is removed from the API catalog, we need to find out why the API service was not responding. If it is just an intermittent network issue, the API service will do self-healing by re-registering itself to the catalog.

## User Impact
If an API service is removed from all the API catalog instances, users can no longer call any of the APIs from that API service.

## Instructions to Fix

1. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).

2. Go to the API Management panel, in API Catalog tab, see if you find the client id mentioned in the PagerDuty details. If not, go to step 4.

3. If yes, try to do curl to the url specified in Source Info column of the client id. If data is returned in the response, this means the API service is up and running, you can resolve the PagerDuty alert. Otherwise, go to step 4.

4. Escalate the alert to level 2 of the [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}). (Contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} and {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-1-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %})

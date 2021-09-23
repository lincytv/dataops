---
layout: default
description: "RETIRED Echometer URL Down Failure."
title: RETIRED Echometer URL Down Failure
service: tip-api-platform
runbook-name: "Echometer URL Down Failure"
tags: oss, bluemix, doctor, blink, Echometer, api platform, api, tip-api-platform
link: /apiplatform/Runbook-Echometer-URL-Down-Failure.html
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

{% capture scorecard-1-slack %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.slack }}{% endcapture %}
{% capture scorecard-1-name %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.name }}{% endcapture %}
{% capture scorecard-1-userid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.userid }}{% endcapture %}
{% capture scorecard-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.notesid }}{% endcapture %}
{% capture scorecard-2-slack %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.slack }}{% endcapture %}
{% capture scorecard-2-name %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.name }}{% endcapture %}
{% capture scorecard-2-userid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.userid }}{% endcapture %}
{% capture scorecard-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.notesid }}{% endcapture %}

## Purpose

This alert will be triggered if the service monitored by Echometer cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

When the service is cloud based:

1. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}})

2. Double check the URL status:

   - Click on "Echometer" in the Wukong navigator.
   - Search for the environment or service name from the PagerDuty incident.
     - Type the environment name in the search box.
     - Press "Enter".
   - Verify that the `STATUS` of the URL is 0.
   - If the `STATUS` is 0, resolve the incident.
   - If status is 1, then continue to next step.

3. If the status is 1, and the problem is with one of the following APIs, escalate the alert to level 2 of the [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}) (contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %}, or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}):
   - API Catalog (api_catalog_service)
   - Doctor API (api_doctor_api)
   - Incident Management API (incidentmgmt or incidentmgmtapi)
   - Key Service (api_key_service)
   - Kong (kong)
   - Subscription API (subscriptionapi)

4. If the status is 1, and the problem is with one of the following APIs, open the url in a browser or open a terminal and run curl `URL`. If you get a return of *ok*, resolve the incident. Otherwise, escalate the alert to level 2 service contact.
    - Scorecard (level 2 contact: (contacts: {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, or {% include contact.html slack=scorecard-2-slack name=scorecard-2-name userid=scorecard-2-userid notesid=scorecard-2-notesid %}))

5. If the status is 1, and the problem is NOT with one of the APIs from steps 3 or 4 above, navigate to **Doctor Keeper** using the navigation.

6. Use the filter input box to find the Environment.

7. Click **SSH**. An SSH session opens in a new tab.
   - If the SSH session does NOT open in a new tab, check to see if the environment has been decommissioned. Go to *Doctor Portal Governance-> Handover Management* to check it.
   - If the environment has not been decommissioned, and the keeper status is yellow, this is typically a network issue. Please contact the network on call and send a message to the [{{site.data[site.target].oss-slack.channels.sre-platform-onshift.name}}]({{site.data[site.target].oss-slack.channels.sre-platform-onshift.link}}) Slack channel.
   - If the environment has been decommissioned, remove the /healthz check for the environment from Echometer by using the following steps and then resolve the incident:
     - Click Echometer in the Wukong navigator.
     - Search for the environment from the PagerDuty incident.
     - Click the Delete button.

7. At the prompt, enter: `su <YOUR_SSO_ID>`, where `<YOUR_SSO_ID>` is your Doctor SSO ID.

8. Enter `sudo su` When prompted for your password, enter your Doctor SSO Password.

9. Enter `docker ps`

10. Enter `docker restart doctor_backend`

11. Verify that the URL from the PagerDuty incident is reachable:
   - Click on Echometer in the Wukong navigator.
   - Search for the environment from the PagerDuty incident.
   - Verify that the STATUS of the URL is 0.
     **NOTE:** You may have to wait ~5 minutes for Echometer to check the URL again.
   - If the STATUS is 0, resolve the incident.

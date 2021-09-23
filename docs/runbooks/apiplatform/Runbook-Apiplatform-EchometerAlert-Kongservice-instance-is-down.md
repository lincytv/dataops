---
layout: default
title: "RETIRED API Platform - Echometer alert: Kong service is down"
type: Alert
runbook-name: "Runbook-Apiplatform-EchometerAlert-Kongservice-instance-is-down"
description: "This alert will be triggered if the doctor_kong or api_gateway did not work properly."
service: tip-api-platform
tags: apis, doctor, apigateway
link: /apiplatform/Runbook-Apiplatform-EchometerAlert-Kongservice-instance-is-down.html
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
This alert will be triggered if the doctor_kong or api_gateway does not work properly.

## Technical Details
There is one deployment of doctor_kong service. Kong api_gateway has 5 instances on softlayer, they are started by `docker swarm`.

### Detail

## User Impact
- Users cannot see APIs and API users on the wukong API Management.
- APIs registered in apigateway don't work and won't be redirected to the right upstream url.

## Instructions to Fix
1. Check API and API user displayed on wukong portal.
    - Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
    - Go to panel `API Management`, check the lists of `API` tab and `API User` tab. If there is no data, `doctor_kong` service may be down.
2. Find out the reason why doctor_kong was down.
    - Then go to `CI&CD`, search `doctor_kong` in the _Continuous Deployment_.
    - Copy the Environment name and Navigate to the `Doctor Keeper` on the left-hand side bar, Search for the impacted envirtonment, and click SSH. A console window will open for the environment's Doctor VM.
    - Login with your SSO ID: use `su <YOUR_SSO_ID>`, and switch to root: `sudo -i`.
    - Call `curl http://localhost:4587/kong/apis` on host VM, doctor_kong works well when got a list of apis. If there is no any apis retrieved, use `docker logs --tail 100 doctor_kong` the see the errors.
3. Try to recover the service.
    - Use `docker restart doctor_kong` to restart the doctor_kong service. Wait for several minutes.
    - Re-call `curl http://localhost:4587/kong/apis` to see the result.
    - If there is still no data and then escalate the alert to level 2 of the tip-api-platform policy contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} for help.
4. Check kong if doctor_kong service is ok.
    - Go to Wukong panel `KONG Management`, to check the kong-instance status. As long as anyone of Kong instance node is up, it means the API user will succeed to call the API via Kong and API manageement will retrieve `APIs` and `API user` successfully. In case any server node is down, please notify level 2 (go to step 5) to get their attention since there is impact on Kong's high availability.
5. If the restart button doesn't work, or you find any other errors, escalate the alert to level 2 of the tip-api-platform policy contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} for help.

## Notes and Special Considerations

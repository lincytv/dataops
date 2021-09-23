---
layout: default
description: This Runbook is for Doctor service is down.
title: Runbook Doctor service is down
service: PostgreSQL
runbook-name: Runbook Doctor service is down
tags: oss, bluemix, doctor
link: /doctor/Runbook_Doctor_service_down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This alert is triggered when healthz API of doctor service is failed.

## Technical Details
Healthz API is to monitor if services are running well.

## User Impact
If healthz failed, it indicates the service maybe down.

## Instructions to Fix
You can find service name from Alert title.

|alert title|service name|healthz API|
|:-----|:-----|:-----|
|certmanagement_healthcheck_failed|certmanagement|https://pnp-api-oss.cloud.ibm.com/certmanagement/healthz|

Please follow these steps, replace **service name** and **healthz API** according to the servicename in alert title.

1. Verify if the service is indeed down
 - In a terminal, execute
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>'  -i <healthz API>
   ```
 - It should return ok. If it failed, then continue the step2.

2. Check if the service is running.   
3. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
4. Go to the **CI & CD** panel.
5. In the **Continuous Deployment** section.
6. Type in **service name**.
7. Go to "Remote Command" , find the server and run `docker restart **service name**`

**If any questions, please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %}.**


---
layout: default
title: "Doctor PNP API down"
type: Alert
runbook-name: "doctor-pnp-api.down"
description: "This alert will be triggered when doctor pnp api did not work properly"
service: doctor, pnp
tags: pnp
link: /doctor/doctor-pnp-api.down.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This alert is triggered when this API is not responding or get errors.

## Technical Details
The Doctor API (https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/pnp/healthz) is used by PnP to get maintenance records from Doctor(actually Doctor will get them from RTC). It is provided by **Doctor Pnp Service**.

## User Impact
If the API is not responding or getting errors, PnP will not get maintenance records from RTC. Users who use the PnP APIs will also not get maintenance records.

## Instructions to Fix

1. Verify if Doctor API is indeed down
 - In a terminal, execute
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>'  -i 'https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/pnp/healthz'
   ```
 - It should return ok. If it failed, then continue the step2.

2. Check if the **doctor_pnp** service is running.   
3. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
4. Go to the **CI & CD** panel.
5. In the **Continuous Deployment** section.
6. Type in `doctor_pnp`.
7. Go to "Remote Command" , find the server and run `docker restart doctor_pnp`


**Runbook Owners**
* csschen@cn.ibm.com

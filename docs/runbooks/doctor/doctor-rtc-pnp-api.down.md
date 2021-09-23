---
layout: default
title: "Doctor RTC API down"
type: Alert
runbook-name: "doctor-rtc-pnp-api.down"
description: "This alert will be triggered when doctor rtc api did not work properly"
service: doctor, rtc
tags: rtc
link: /doctor/doctor-rtc-pnp-api.down.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}


#### Notes: The API was migrated to Doctor Dlt service.

## Purpose
This alert is triggered when this API is not responding or get errors.

## Technical Details
The Doctor API (https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/get_drs_from_db_to_pnp) is used by PnP to get maintenance records from Doctor(actually Doctor will get them from RTC). It is provided by **Doctor Dlt Service**.

## User Impact
If the API is not responding or getting errors, PnP will not get maintenance records from RTC. Users who use the PnP APIs will also not get maintenance records.

## Instructions to Fix

1. Verify if Doctor API is indeed down
 - In a terminal, execute
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>'  -i 'https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/get_drs_from_db_to_pnp'
   ```
 - It should return numbers of miantenance records without any error. If it failed, then continue the step2.

2. Check if the **doctor_dlt** service is running.   
3. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
4. Go to the **CI & CD** panel.
5. In the **Continuous Deployment** section.
6. Type in `doctor_dlt`.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor_dlt.png){:width="640px"}
7. Go to "Remote Command" , find the server and run `docker restart doctor_dlt`


**Runbook Owners**
* {% include contact.html slack=cloud-newrelic-monitoring-slack name=cloud-newrelic-monitoring-name userid=cloud-newrelic-monitoring-userid notesid=cloud-newrelic-monitoring-notesid %}

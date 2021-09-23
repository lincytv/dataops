---
layout: default
title: "RETIRED Doctor RTC API down"
type: Alert
runbook-name: "api.pnp-doctor-rtc-api.down"
description: "This alert will be triggered when doctor api that the PnP Change Adapter used did not work properly"
service: tip-api-platform
tags: api-doctor-rtc-api
link: /apiplatform/api.pnp-doctor-rtc-api.down.html
---

{% capture cloud-newrelic-monitoring-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.slack }}{% endcapture %}
{% capture cloud-newrelic-monitoring-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.name }}{% endcapture %}
{% capture cloud-newrelic-monitoring-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.userid }}{% endcapture %}
{% capture cloud-newrelic-monitoring-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.notesid }}{% endcapture %}


## Purpose
This alert is triggered when Doctor RTC API is not responding or get errors.

## Technical Details
The Doctor API (https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/get_drs_from_db_to_pnp) is used by PnP to get maintenance records from Doctor(actually Doctor will get them from RTC). It is provided by Doctor RTC Service.

## User Impact
If the API is not responding or getting errors, PnP will not get maintenance records from RTC. Users who use the PnP APIs will also not get maintenance records.

## Instructions to Fix

1. Verify if Doctor API is indeed down
 - In a terminal, execute
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>'  -i 'https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/get_drs_from_db_to_pnp'
   ```
 - It should return numbers of miantenance records without any error. If it failed, then continue the step2.

2. Check if the Doctor RTC service is running.
 - Double check the URL status: `curl  https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/rtc/healthz`
 - If the healthz URL failed, please continue the step 3.
 - If it returns `ok`, it means the service is running.  There may be something wrong with `/get_drs_from_db_to_pnp` API, Contact {% include contact.html slack=cloud-newrelic-monitoring-slack name=cloud-newrelic-monitoring-name userid=cloud-newrelic-monitoring-userid notesid=cloud-newrelic-monitoring-notesid %} to check the issue.


3. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
4. Go to the **CI & CD** panel.
5. In the **Continuous Deployment** section.
6. Type in `doctor_rtc`.
![]({{site.baseurl}}/docs/runbooks/apiplatform/images/doctor_rtc.png){:width="640px"}
7. Restart the service instances listed in the table, by clicking on the icon under the **Action** column.

8. If the service is running and the above two APIs are reachable, then restart **api-pnp-change-adapter** service to import the records again.
  - `kubectl oss pod delete -l app=api-pnp-change-adapter -napi `
9. If this alert still exists, escalate to doctor team [{{site.data[site.target].oss-slack.channels.oss-doctor.name}}]({{site.data[site.target].oss-slack.channels.oss-doctor.link}}) .



**Runbook Owners**
* {% include contact.html slack=cloud-newrelic-monitoring-slack name=cloud-newrelic-monitoring-name userid=cloud-newrelic-monitoring-userid notesid=cloud-newrelic-monitoring-notesid %}

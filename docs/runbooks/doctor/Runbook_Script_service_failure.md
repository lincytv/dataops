---
layout: default
description: Runbook Script service failure
title: RETIRED Runbook Runbook Script service failure
service: Script
runbook-name: Runbook Script service failure
tags: oss, bluemix, doctor
link: /doctor/Runbook_Script_service_failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}


## Purpose
This alert will be triggered if the Doctor Script service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact
Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

1. Double check the URL status:
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>'  -i '{{doctor-rest-apis-link}}/doctorapi/api/doctor/script/healthz'
   ```
   If it return `ok`, it means the service is healthy, the alert will be resolved automatically in 30 mins. If not, please go to next step.

   Notes:
    * Replace the `<ApiKey>` with your own api key .

2. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Go to the **CI & CD** panel.
4. In the **Continuous Deployment** section.
5. Type in `doctor_script`.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_script.png){:width="640px"}
6. Restart the service instances listed in the table, by clicking on the icon under the **Action** column.
7. If this alert still existed, escalate to doctor team


## Notes and Special Considerations
   {% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: Runbook Doctor Security Service Down
title: RETIRED Runbook Doctor Security Service Down
service: doctor_security
runbook-name: Runbook Doctor Security Service URL Down
tags: oss, bluemix, doctor, doctor_security
link: /doctor/Runbook_Security_Service_Down_Watson_Health.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the Doctor security service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. **doctor_security** service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

1. Double check the URL status:

   ```
   curl -X GET -k -H 'Authorization: <ApiKey>' -H 'MODERATE-TENANT: <Env_name>' -i '{{doctor-rest-apis-link}}/doctorapi/api/doctor/security/firecall/healthz'
   ```
   If it return `ok`, then you can resolve the alert. If not, please go to next step.

   > **Notes:**
    * Replace the `<ApiKey>` with your own api key, you can get it from [{{doctor-portal-name}} profile info]({{doctor-portal-link}}/#/profile/info) for [more info about ApiKey]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)
    * Replace the `<Env_name>` with the environment name reported in the alert. For example, `security_healthcheck_failed:WATSON_HEALTH_HIPAA`, the environment is `WATSON_HEALTH_HIPAA`.

2. Restart doctor_security on wukong portal  
   - Login to [{{wukong-portal-name}}]({{wukong-portal-link}})
   - Select **Remote Command**.
   - Find the environment reported in the alert.
   - Restart the service container reported in the alert, for example:

      ```docker restart doctor_security```

     * To check the logs if there is any error. Run the curl command in step 1 again.
     * If it return `ok`, resolve the alert.
   
   - If it still can not be fixed, snooze this alert and send the failed env to {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} 

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

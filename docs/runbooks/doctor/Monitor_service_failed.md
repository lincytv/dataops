---
layout: default
description: A list of tips and techniques useful for Doctor on-call duties
title: Monitor service failed
service: doctor
runbook-name: Monitor service failed
tags: oss, bluemix, runbook, oncall, ssh, Jumpbox
link: /doctor/Monitor_service_failed.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose

This alert will be triggered if the Doctor monitor micro-service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected, especially Handover process.

## Instructions to Fix


1. Double check the URL status:
   ```
   curl -X GET -k -H 'Authorization: <ApiKey>' -i 'https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/monitor/healthz'
   ```
   If it return `ok`, then you can resolve the alert. If not, please go to next step.

   Notes:
    * Replace the `<ApiKey>` with your own API Key from [{{doctor-portal-name}} -> Account]({{doctor-portal-link}}/#/profile/info).

   ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/get_api_key.png){:width="640px"}


3. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).

   - Select **CI/CD**.
   - Input `doctor_monitor` under **Continuous Deployment** and the service details will be shown
   - Restart the service container reported in the alert by click the ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/refresh_btn.png){:width="20px"} button under **Action** column:

     * Waiting for 2 minutes,Run the curl command in step 1 again.
     * If it return `ok`, resolve the incident.

   - If it still can not be fixed,  Escalate the alert  in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}).

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

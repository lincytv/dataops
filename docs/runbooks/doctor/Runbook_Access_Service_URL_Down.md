---
layout: default
description: Runbook Access Service URL Down
title: Runbook Access Service URL Down
service: doctor_access
runbook-name: Runbook Access Service URL Down
tags: oss, bluemix, doctor, blink, doctor_access
link: /doctor/Runbook_Access_Service_URL_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose

This alert will be triggered if the Doctor access service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

**Notes**:
     We are not allowed to touch Watson environments(some environments like WATSON_*), if getting the alerts for Watson environments, please contact  **Murat.Zh@ibm.com**  who is from Watson team in slack and let Watson team know about it.


1. Double check the URL status:

   ```
   curl -X GET -k -H 'Authorization: <ApiKey>' -H 'MODERATE-TENANT: <Env_name>' -i '{{doctor-rest-apis-link}}/doctorapi/api/doctor/access/healthz'
   ```
   If it return `ok`, then you can resolve the alert. If not, please go to next step.

   > **Notes:**
    * Replace the `<ApiKey>` with your own api key, you can get it from [{{doctor-portal-name}} profile info]({{doctor-portal-link}}/#/profile/info) for [more info about ApiKey]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)
    * Replace the `<Env_name>` with the environment name reported in the alert. For example, `access_service_failed.2.D_YS0`, the enironment is `D_YS0`.

2. Check the environment.
   - Check to see if the environment has been decommissioned.
    * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
    * Select **Governance**
    * Select **Handover Management**
    * User the search box, to find the alert environment.
    * Check the environment.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/hand_over_to_customer.png){:width="640px"}
   - If the environment has been decommissioned.
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/decommissioned_env.png){:width="640px"}
   - Contact {% include contact.html slack=cloud-newrelic-monitoring-slack name=cloud-newrelic-monitoring-name userid=cloud-newrelic-monitoring-userid notesid=cloud-newrelic-monitoring-notesid %} to remove the environment from the healthz check list.


3. If the environment has not been decommissioned  
   - Login to [{{wukong-portal-name}}]({{wukong-portal-link}})
   - Select **Remote Command**.
   - Find the environment reported in the alert.
   - Restart the service container reported in the alert, for example,:

      ``docker restart doctor_access``

     * To check the logs if there is any error. Run the curl command in step 1 again.
     * If it return `ok`, resolve the alert.
   - If the **Doctor Keeper** status is yellow, this is typically a network issue. Please contact the network on call and send a message to the [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/inactive_env.png){:width="640px"}
   - If it still can not be fixed,  Escalate the alert in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}).


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

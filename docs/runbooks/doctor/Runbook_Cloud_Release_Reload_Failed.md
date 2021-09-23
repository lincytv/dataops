---
layout: default
description: This alert is triggred when Cloud release loading failed.
title: RETIRED Runbook Cloud Release Reload Failed
service: doctor_backend, doctor_cloud
runbook-name: Runbook_Cloud_Release_Reload_Failed
tags: oss, bluemix, doctor, doctor_backend
link: /doctor/Runbook_Cloud_Release_Reload_Failed.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the Doctor backend(or cloud) service monitored by New Relic cannot be reached.

**For dedicated/local environment,this alert will be resolved automatically in 30 minutes.
Please go ahead this runbook if auto-resolve failed for dedicated/local environment**


## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.
  4. The configuration of BOSH is changed

## User Impact
Metric data cannot be shown ,either Doctor page or ace console
Bosh instances cannot be loaded
Deployment information cannot be shown
Users who are using the functionality provided by this service will be affected.

## Instructions to Fix


1. Double check the URL status:

   ```
   curl -X GET -k -H 'Authorization: <ApiKey>' -H 'MODERATE-TENANT: <Env_name>' -i '{{doctor-rest-apis-link}}/doctorapi/api/doctor/cloud/releases'
   ```
   If it returns `200` and check if the release info is showing in the page like the following picture. if yes, you can resolve the alert.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud_release.png){:width="640px"}

   If it returns `404` and the release info is not loading, the doctor_backend(or doctor_cloud) service is down, go to next step.

   > **Notes:**
    * Replace the `<ApiKey>` with your own api key, you can get it from [{{doctor-portal-name}} profile info]({{doctor-portal-link}}/#/profile/info) for [more info about ApiKey]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)
    * Replace the `<Env_name>` with the environment name reported in the alert. For example, `no_release:D_YS0::d-ys0:dedicated::us-south`, the enironment is `D_YS0`.

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
   - Restart the service container reported in the alert, for example, ``docker restart doctor_backend`` Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html) if you cannot find the doctor_backend container.

     * To check the logs if there is any error  `docker logs doctor_backend --tail 50`.
     * Run the curl command in step 1 again.
         - If it return `200` and the release data is showing in the above page, resolve the alert.
   - If the **Doctor Keeper** status is yellow, this is typically a network issue. Please contact the network on call and send a message to the [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/inactive_env.png){:width="640px"}


4. If restarting backend or cloud service does not fix the problem.

    * Check if **UAA** and **CredHub** is deployed by using [How to enable BOSH_CLI to UAA]({{site.baseurl}}/docs/runbooks/doctor/Runbook_How_to_enable_bosh_cli_to_uaa.html) runbook.

    * Check **doctor_backend** or **doctor_cloud** logs if you see something like the follow:
      ```
      [2019-03-29 10:44:45 +0000] ERROR: VaultHelper-get_decrypt_value:Failed to get vault token as timeout,error: execution expired
      [2019-03-29 10:44:45 +0000] INFO: VaultHelper-decrypt:Failed to get decrypt value, rety
      [2019-03-29 10:44:50 +0000] ERROR: VaultHelper-get_decrypt_value:Failed to get vault token as timeout,error: execution expired
      ```
      The problem is with Vault and at this point there is nothing else you can do but wait until Vault recovers. There is a [Git issue 7072](https://github.ibm.com/cloud-sre/ToolsPlatform/issues/7072) issue to removed a dependency from Vault.

5. If the issue still can not be fixed,  escalate the alert to level 2 or ask help in slack channel [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}})

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

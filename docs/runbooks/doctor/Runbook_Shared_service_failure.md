---
layout: default
description: Runbook Shared service failure
title: RETIRED Shared service failure
service: Datahub
runbook-name: Shared service failure
tags: oss, bluemix, doctor
link: /doctor/Runbook_Shared_service_failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose
This alert will be triggered if the Doctor Shared services monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact
Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

1. Double check the URL status, for example:
   ```
   curl -X GET -k -H 'Authorization:<DOCTOR_APIKEY>'  -i '{{doctor-rest-apis-link}}/doctorapi/api/doctor/<shared_service_name>/healthz'
   ```
   If it return `200` , it means the service works well, the alert will be resolved automatically in 15 mins. If not, please go to next step.

   > **Notes:** <br>
   1. To get your **DOCTOR_APIKEY** check [How to get your API Key]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html}}) runbook.
   2. Replace the `<shared_service_name>` with the _service name_ reported in the alert. For example, `datahub_service_healthcheck_failed`, the service is `datahub`. in this case the URL will `{{doctor-rest-apis-link}}/doctorapi/api/doctor/datahub/healthz`<br><br>
   **If the curl command failed, verify the shared service URI**
   3. To find the shared service URI follow the next steps:
   * Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   * Select **API Management** from the left side menu.
   * Select the **API** tab.
   * Type the service name and click on **Search**.
   * From the list of values look for any entry in the **API Name** column that contains **healthz**.
   * Copy the value from the **URI** column and add it to `{{doctor-rest-apis-link}}`.
   * For example for the **datahub**, the URI is `/doctorapi/api/doctor/datahub/healthz`.
    - The complete URL will be `{{doctor-rest-apis-link}}/doctorapi/api/doctor/datahub/healthz`
   * Another example look for share service **deployment**, the URI is `/deployment_env_healthz`
    - The URL will be `{{doctor-rest-apis-link}}/deployment_env_healthz`
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/api_management/api_search_uri.png){:width="640px"}

   /Users/alejandro/Documents/GitHub/cloud-sre_runbooks/docs/runbooks/doctor/images/wukong/api_management/api_search_uri.png

2. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Go to the **CI & CD** panel.
4. In the **Continuous Deployment** section.
5. Type the service name , for example, `doctor_datahub`.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_datahub.png){:width="640px"}
6. Restart the service instances listed in the table, by clicking on the icon under the **Action** column.
7. If this alert still existed, escalate to doctor team.


## Notes and Special Considerations

   {% include {{site.target}}/tips_and_techniques.html %}

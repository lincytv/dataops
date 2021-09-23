---
layout: default
description: This alert will be triggered if calling healthz API of an API service failed in API Health monitoring.
title: API Health - Healthz Failed
service: healthz
runbook-name: "API Health - Healthz Failed"
tags: oss, bluemix, doctor, healthz
link: /doctor/Runbook_API_Health_Healthz_Failed.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose
This alert will be triggered if calling healthz API of an API service failed in API Health monitoring. It could be the healthz API is not responding, or the response status code is not 200, or there is an error in the call.

## Technical Details
If a call to healthz of an API service failed, we need to find out why it failed.

## User Impact
User might have problem in calling other APIs from that API service.

## Instructions to Fix

### Step 1.
Try to call healthz API, you can find the url from the {{doctor-alert-system-name}} alert.

For example:
  `$ curl -XGET {{doctor-rest-apis-link}}/catalog/api/catalog/healthz`

  If you see something like below returned, then healthz api is working fine, you can resolve the alert; otherwise go to next step.

  ```
  {"href":"https://pnp-api-oss.cloud.ibm.com/catalog/api/catalog/healthz","code":0,"description":"The API is available and operational."}
  ```

### Step 2.
  * Login to [{{wukong-portal-name}}]({{wukong-portal-link}})
  * Go to the **CI & CD** panel.
  * In the **Continuous Deployment** section.
  * Type in the corresponding microservice name of the failed API service.
  | API    | Microservice     |
  | :------------- | :------------- |
  | authapi       | api_key_service |
  |catalog|doctor_apicatalog|
  |doctorapi|api_doctor_api|
  |incidentmgmtapi|tip-IncidentMgmtAPI|



  >**Note:** Find the API service that failed in the {{doctor-alert-system-name}} alert.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/pd/api_service_failed.png){:width="640px"}
  * Hit **Enter** to see if the microservice is running.



### Step 3.
  - Restart the service instances listed in the microservice table one at a time.
    - Click on the checkbox of the instance.
    - Click in the icon from the Action colunm.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_apicatalog_restart.png){:width="640px"}
  - Wait for 5 minutes.
  - Try step 1 again.
  - If the curl still fails, continue this runbooks.
### Step 4 for API catalog only.
  - Enter doctor_apicatalog's container using your SSO ID(--Pending on SSO account for doctor VMs)
    - Click on the hiperlink of each environment such as **DOCTOR_MBUS4**.
    - It will open a SSH session.
    - Log in using your SOS ID.
    >**Note:** If you SSO does not work try **Remote Command**.

    - Check the DB connection:
      `nc 10.112.157.236 5432 -v`
    - The output should be
      `Connection to 10.112.157.236 5432 port [tcp/postgresql] succeeded!`.
    1. If succeeded.
      - Go to step 5, it's probably not the DB connection issue.
    2. Otherwise.
      - Contact the network oncall `@cybot whois oncall` in [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.
      - Try whether the public IP works:
        `nc 159.8.170.87 5432 -v`.
        - If the public IP also fails, post a message in the [{{sosat-monitor-prod-name}}]({{sosat-monitor-prod-link}}) Slack channel, and also open an incident targeting the network team. (TBD)
        - If the public IP connection succeeds while the private IP fails, switch to the public IP as a workaround, and then switch back to the private IP after it recovers.
           1. Enter doctor_apicatalog's container.
           2. Use VIM to edit /.hostconfig.json.
           3. Modify the DB host from the private IP to the public IP.
           4. Exit the container.
           5. `docker restart doctor_apicatalog`.
           6. Since Kong is using the same DB, Kong will also be down after its cache expires in some time. So, if the network's estimated recovering time is over one hour, post a message in the [{{sosat-monitor-prod-name}}]({{sosat-monitor-prod-link}}) Slack channel to get management team's approval for Kong configuration change, and go to the next step for escalation. (Once approved, Kong's DB connection configuration must also be changed to the public IP.)

### Step 5 Escalate the alert to level2.
- Go to[{{tip-api-platform-policy-name}}]({{tip-api-platform-policy-link}}) (see the link and contact one of the people in level 2 support).

### Step 6. Please remember to resolve ServiceNow incident manually.
- Go to [ServiceNow](https://watson.service-now.com/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_userpref_module%3Db55fbec4c0a800090088e83d7ff500de%26sysparm_query%3Dactive%3Dtrue%5EEQ%26active%3Dtrue%26sysparm_clear_stack%3Dtrue).
- You can find the ServiceNow incident number in the {{doctor-alert-system-name}} alert `ServiceNow Incident: `.
- If there is no ServiceNow incident number shown in the {{doctor-alert-system-name}} alert, it is most likely that Incident Management Api failed to create ServiceNow incident due to 500 (internal) or 502 (bad gateway) errors.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

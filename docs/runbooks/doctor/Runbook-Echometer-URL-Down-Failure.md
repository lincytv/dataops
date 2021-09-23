---
layout: default
description: Echometer URL Down Failure.
title: Echometer URL Down Failure
service: echometer
runbook-name: "Echometer URL Down Failure"
tags: oss, bluemix, doctor, blink, Echometer
link: /doctor/Runbook-Echometer-URL-Down-Failure.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the service monitored by Echometer cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

{% if site.target == "ibm" %}
{% include_relative _ibm-includes/echometer-down-note.html %} __________________________
{% endif %}

When the service is cloud based:

1. Login to [{{wukong-portal-name}}]({{wukong-portal-link}})

2. Double check the URL status:

   - Click on **Echometer** in the Wukong navigator.
   - Search for the environment or service name from the {{doctor-alert-system-name}} incident.
     - Type the environment name in the search box.
     - Press **Enter**.
   - Verify that the `STATUS` of the URL is `0`.
   - If the `STATUS` is `0`, resolve the incident.
   - If `STATUS` is `1`, then continue to next step.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/check_status.png)

3. If the `STATUS` is `1`, and the problem is with one of the following APIs:
   - API Catalog (api_catalog_service)
   - Doctor API (api_doctor_api)
   - Incident Management API (incidentmgmt)
   - Key Service (api_key_service)
   - Kong (kong)
   - Subscription API (subscriptionapi)

    Escalate the alert to level 2 of the [{{tip-api-platform-policy-name}}]({{tip-api-platform-policy-link}}) (contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %}, or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %})

4. If the `STATUS` is `1`, and the problem is with one of the following APIs:
    - Scorecard (level 2 contact: (contacts: {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, or {% include contact.html slack=scorecard-2-slack name=scorecard-2-name userid=scorecard-2-userid notesid=scorecard-2-notesid %})
    - Servicedb (level 2 contact: {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %})

    Open the url in a browser or open a terminal and run curl `URL`. If you get a return of **ok**, resolve the incident. Otherwise, escalate the alert to level 2 service contact.

5. If the `STATUS` is `1`, and the problem is NOT with one of the APIs from steps 3 or 4 above, navigate to **Doctor Keeper** using the navigation.

6. Use the filter input box to find the Environment.

7. Click **SSH**. An SSH session opens in a new tab.
   - If the SSH session does NOT open in a new tab.
   - Check to see if the environment has been decommissioned.
    * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
    * Select **Governance**
    * Select **Handover Management**
    * User the search box, to find the alert environment.
    * Check the environment.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/hand_over_to_customer.png)
   - If the environment has not been decommissioned, and the keeper status is yellow, this is typically a network issue. Please contact the network on call and send a message to the [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/inactive_env.png)
   - If the environment has been decommissioned.
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/decommissioned_env.png)
   - Remove the /healthz check for the environment from **Echometer** by using the following steps and then resolve the incident:
       - Click **Echometer** in the Wukong navigator.
       - Search for the environment from the PagerDuty incident.
       - Click the **Delete** button.
       ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/healthz.png)


8. At the prompt, enter: `su <YOUR_SSO_ID>`, where `<YOUR_SSO_ID>` is your Doctor SSO ID.

9. Enter `sudo su` When prompted for your password, enter your Doctor SSO Password.

10. Enter `docker ps`

11. Enter `docker restart doctor_backend`
    Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
    if you cannot find the **doctor_backend** container.

12. Verify that the URL from the {{doctor-alert-system-name}} incident is reachable:
   - Click on **Echometer** in the Wukong navigator.
   - Search for the environment from the {{doctor-alert-system-name}} incident.
   - Verify that the `STATUS` of the URL is `0`.
     >**NOTE:** You may have to wait ~5 minutes for Echometer to check the URL again.
   - If the `STATUS` is `0`, resolve the incident.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

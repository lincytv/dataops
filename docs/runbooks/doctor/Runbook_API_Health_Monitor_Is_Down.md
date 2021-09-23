---
layout: default
description: Runbook API Health Monitor Is Down
title: Runbook API Health Monitor Is Down
service: api
runbook-name: Runbook API Health Monitor Is Down
tags: oss, bluemix, doctor
link: /doctor/Runbook_API_Health_Monitor_Is_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_sosat_constants.md%}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose
This alert will be triggered if {{new-relic-portal-name}} did not receive any transactions from the API Health monitoring for a certain period of time.

## Technical Details
If {{new-relic-portal-name}} did not receive any transactions from API Health monitoring, it could be that the API Health monitoring is down, or there is a network issue that needs investigation.

## User Impact
API Health monitoring monitors the health of the API Catalog and API services. If the API Health monitoring is down, we do not know if the API Platform is in a healthy state or not.

## Instructions to Fix

1. Go to
[{{service-now-name}}]({{service-now-link}}/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_userpref_module%3Db55b4ab0c0a80009007a9c0f03fb4da9%26sysparm_clear_stack%3Dtrue) and open a new ServiceNow incident manually to record this issue.
2. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Go to the **CI & CD** panel.
4. In the **Continuous Deployment** section.
5. Type in `api_health_monitor`.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/api_health_monitor_ip.png){:width="640px"}
6. Try to ping the IP of the service instance listed in the table.
![]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/ping_pi_health_monitor_ip.png){:width="640px"}
  * If you can ping the IP address, go to next step; otherwise contact the network team [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}).
7. Restart the service instance listed in the table, by clicking on the icon under the **Action** column.
8. In the {{doctor-alert-system-name}} alert.
  * Find the _incident_acknowledge_url_.
  * Go to this url, and wait for about 10 minutes to see if the {{new-relic-portal-name}} incident status is changed to _Closed_ automatically.
    * If yes, you can resolve the {{doctor-alert-system-name}} alert; otherwise, go to next step.
9. Escalate the alert to level 2 of the [tip-api-platform policy]({{site.data[site.target].oss-doctor.links.doctor-alert-system.link}}/escalation_policies#P7EPQAO). Contact one of the people in the level 2, e.g. {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}).
10. Please note that this {{doctor-alert-system-name}} alert is coming from {{new-relic-portal-name}} and is not coming from TIP. When the issue is resolved, click on the _incident_url_ link in the {{doctor-alert-system-name}} to ensure that the {{new-relic-portal-name}} incident is closed, then resolve this {{doctor-alert-system-name}} alert, and also manually resolve {{service-now-name}} incident.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

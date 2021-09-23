---
layout: default
description: Metrics data is older than two hours. Check your IBM Cloud Doctor configuration and connection.
title: Metrics data is older than two hours
service: doctor
runbook-name: Metrics data is older than two hours
tags: doctor
link: /doctor/Runbook_Metrics_data_is_older_than_two_hours.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
--

## Purpose

Below are instructions to fix a _Metrics data is older than two hours_ Pager Duty incident or Slack question.


![]({{site.baseurl}}/docs/runbooks/doctor/images/ace_console/MetricsDataIsOlder2hrs.png){:width="640px"}

## Instructions to Fix

>**Note:** If you see errors in this section: ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/DoctorChecksInAdminConsole.png){:width="320px" } <br>use the follow runbook first [Ops Admin Console Doctor Check Failed]({{site.baseurl}}/docs/runbooks/doctor/Runbook-Ops-admin-console-doctor-check-failed.html)

Determine if this is a Doctor's issue in the following way:

### 1. login doctor agent via ssh.

### 2. If this is diego environment
- curl -X GET http://localhost:[PORT]/cloud/app/cell_usage
- For example: ```curl -X GET http://localhost:4569/cloud/app/cell_usage```
- Then go to [check point 1](#check-point-1).
- If the curl command fails then check the follow runbooks and try again.
  - [Cloud resource usage APIs]({{site.baseurl}}/docs/runbooks/doctor/Runbook_cloud_resource_usage_APIs.html)
  - [Cloud usage is delay]({{site.baseurl}}/docs/runbooks/doctor/Runbook_cloud_usage_is_delay.html)

### 3. If this is DEA environment
- curl -X GET http://localhost:[PORT]/cloud/app/dea_usage
- For example: ```curl -X GET http://localhost:4569/cloud/app/dea_usage```
- Then go to [check point 1](#check-point-1).

### 4. Other
- curl -X GET http://localhost:[PORT]/cloud/instance/v1
- For example: ```curl -X GET http://localhost:4569/cloud/instance/v1```
- Then go to [check point 2](#check-point-2).


### Check point 1:
- Make sure the "last_update_time" is within 2 hours.

![]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/Usage_cell.png){:width="640px"}


### Check point 2:
- Make sure the "time" is within 2 hours.
![usage_instance.png]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/Usage_short_instance.png){:width="640px"}


>**Note:** If the **time** and **last_update_time** is within 2 hours, then this is not a Doctor's issue,
Please contact Ops Console team ({% include contact.html slack=admin-console-slack name=admin-console-name userid=admin-console-userid notesid=admin-console-notesid %},  or {% include contact.html slack=admin-console-2-slack name=admin-console-2-name userid=admin-console-2-userid notesid=admin-console-2-notesid %}).

## Notes and Special Considerations

Check your email inbox to see if you receive the test email. May take up to ~5 minutes.
{% include {{site.target}}/tips_and_techniques.html %}

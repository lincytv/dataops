---
layout: default
description: Cloud Usage is Delay alert
title: Cloud Usage Is Delay
service: doctor
runbook-name: Runbook cloud usage is delay
tags: doctor
link: /doctor/Runbook_cloud_usage_is_delay.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select **Scheduler Task** from the left side menu.
* Select the environment mentioned in the alert.
  * Stop and then start these scheduler tasks for this environment:
  * refresh_app_statistics_info_new
  * refresh_app_statistics_info_new4
  * refresh_app_statistics_info_new5
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/usage_scheduertask.png){:width="700px"}
* After 5 minutes, run remote command to check the _last_update_time_.
  - Select **Remote Command** from the left side menu.
  - Search for the environment.
  - Check the environment box.
  - Run `curl -X GET http://localhost:4569/cloud/app/cell_usage`
  - Make sure the _last_update_time_ is within 1 hour.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/usage_remotecommand.png){:width="700px"}

  {% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
  {{ note_backend_port  | markdownify }}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

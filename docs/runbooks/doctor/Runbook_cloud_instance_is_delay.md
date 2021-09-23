---
layout: default
description: Cloud Instance is Delay alert
title: Cloud Instance Is Delay
service: doctor
runbook-name: Runbook cloud instance is delay
tags: doctor, cloud
link: /doctor/Runbook_cloud_instance_is_delay.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select **Scheduler Task** from the left side menu.
* Select the environment mentioned in the alert.
* Stop and then start these scheduler tasks for this environment:
  - refresh_cloud
  - refresh_app_statistics_info_new
  - refresh_app_statistics_info_new4
  - refresh_app_statistics_info_new5
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/restart_task.png)
* After 5 minutes, run remote command to check the _time_.
  - Select **Remote Command** from the left side menu.
  - Search for the environment.
  - Check the environment box.
  - Run `curl -X GET http://localhost:4569/cloud/instance/v1`
  - Make sure the _time_ is within 1 hour.

  ![usage_instance.png]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/usage_instance.png){:width="700px"}

  {% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
  {{ note_backend_port  | markdownify }}


## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

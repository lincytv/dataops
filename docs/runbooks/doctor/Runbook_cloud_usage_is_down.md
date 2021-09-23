---
layout: default
description: Cloud Usage is Down alert
title: Cloud Usage Is Down
service: backend
runbook-name: Runbook cloud usage is down
tags: doctor,backend
link: /doctor/Runbook_cloud_usage_is_down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select **CI & CD** from the left side menu.
* On the **Continuous Deployment** field, input _doctor_backend_.
Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the _doctor_backend_ container.
* Select the environment mentioned in the alert using the check box.
* Stop and then start _doctor_backend_ for the environment, using the **Action** icon.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_backend_restart.png)
* After 5 minutes, run remote command to check the _last_update_time_.
  - Select **Remote Command** from the left side menu.
  - Search for the environment.
  - Check the environment box.
  - Run `curl -X GET http://localhost:4569/cloud/app/cell_usage`
  - Make sure the _last_update_time_ is within 1 hour.


Restart _doctor_backend_. After 5 minutes, run remote command to check the _last_update_time_. Make sure the _last_update_time_ is within 1 hour.

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/usage_remotecommand.png){:width="700px"}

{% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
  {{ note_backend_port  | markdownify }}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: What's up with the doctor_backend Container?
title: DECOMMISSIONED Doctor Backend Service
service: doctor
runbook-name: "Doctor Backend"
tags: docker, doctor_backend
link: /doctor/Doctor_backend_container.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

# What is the doctor_backend container?
The doctor_backend container runs in the Doctor Agent in each environment.
It provides services described
[here]({{site.baseurl}}/docs/runbooks/doctor/Runbook_St_Admcnsl_doctorChk_Ops_admin_console_doctor_check_failed.html) and
[here]({{site.baseurl}}/docs/runbooks/doctor/Runbook_App_and_User_page_function_not_work.html).
In some environments it is called **doctor_cloud**.
If your runbook asks you to look for the **doctor_backend** and you cannot find it, then perhaps its an environment which uses the name **doctor_cloud**.

## Which environments use the name doctor_cloud?
To find which environments use the name **doctor_cloud**:
1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
2. Click **CI & CD** in the navigation menu.
3. Search for the instances of service **doctor_cloud**.  The environments using this name are shown:

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_cloud_service.png){:width="640px"}

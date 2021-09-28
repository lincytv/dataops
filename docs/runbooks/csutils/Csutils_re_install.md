---
layout: default
description: What's up with the csutils_backend Container?
title: DECOMMISSIONED csutils Backend Service
service: csutils
runbook-name: "Csutils Re-install"
tags: csutils, csutils_re_install
link: /csutils/csutils_re_install.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

# How Do we Reinstall Csutils?
The doctor_backend container runs in the Doctor Agent in each environment.
It provides services described
[here]({{site.baseurl}}/docs/runbooks/csutils/Runbook_St_Admcnsl_csutilsChk_Ops_admin_console_csutils_check_failed.html) and
[here]({{site.baseurl}}/docs/runbooks/csutils/Runbook_App_and_User_page_function_not_work.html).
In some environments it is called **csutils_cloud**.
If your runbook asks you to look for the **csutils_backend** and you cannot find it, then perhaps its an environment which uses the name **csutils_cloud**.

## Which environments use the name csutils_cloud?
To find which environments use the name **csutils_cloud**:
1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
2. Click **CI & CD** in the navigation menu.
3. Search for the instances of service **csutils_cloud**.  The environments using this name are shown:

![]({{site.baseurl}}/docs/runbooks/csutils/images/wukong/cicd/csutils_cloud_service.png){:width="640px"}

---
layout: default
description: EU Emergency Process Stop Polling Pending USAM Request
title: EU Emergency Process Stop Polling Pending USAM Request
service: doctor
runbook-name: EU Emergency Process Stop Polling Pending USAM Request
tags: oss, bluemix, doctor
link: /doctor/Runbook_EU_Emergency_Process_Stop_Polling_Pending_USAM_Request.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

1. As EUaccess service depends on the {{usam-short}} system.
  - Check if the {{usam-short}} system is down by accessing [{{usam-name}}]({{usam-link}}).
  - If you can access and login it should be fine. Go to step 2. Otherwise alert [{{eu-emerg-approvers-name}}]({{eu-emerg-approvers-link}}) that {{usam-short}} is down.

2. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Select **CI & CD** from the left side menu.
4. Search out service `doctor_euaccess`, these instances should be run on **{{doctor-service1-name}}** and **{{doctor-service2-name}}**.
5. Restart listed environments one by one, please, by clicking on the icon under the *Action* column.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_euaccess.png)
6. After all instances of `doctor_euaccess` are restarted, go to the **Scheduler Task** page.
7. Restart the following scheduler jobs. You can do so by clicking on _Stop_, then after it changes to _Start_, click on _Start_.

   * `EUAccess_SOS_Access_Check`
   * `Refresh_USAM_EU_EMERG_GROUP`   
   * `Refresh_USAM_Prigrp_User`   
   * `Refresh_Pending_USAM_Request`   

8. If the alert happens again.
   * Go to the [{{wukong-portal-name}}]({{wukong-portal-link}}).
   * Select **CI & CD** from the left side menu.
   * Restart the service `doctor_shared_scheduler`.   

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

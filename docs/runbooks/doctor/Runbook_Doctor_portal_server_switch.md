---
layout: default
description: Runbook Doctor portal server is down
title: Runbook Doctor portal server is down
service: doctor portal
runbook-name: Runbook Doctor portal server is down
tags: oss, bluemix, doctor, portal
link: /doctor/Runbook_Doctor_portal_server_switch.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This runbook used for switch Doctor portal server for CIS

## Technical Details

  1. Has access permission to cloud.ibm.com
  2. Has access permission to IBM cloud CIS service for Doctor

## User Impact

Users who are using browser to access doctor.cloud.ibm.com will be failed.

## Instructions to Fix

a. Login cloud.ibm.com with w3 ID.

![]({{site.baseurl}}/docs/runbooks/doctor/images/cloud_console.jpg){:width="640px"}

b. Click **Services** on dashboard Resource Summary part.

![]({{site.baseurl}}/docs/runbooks/doctor/images/services.jpg){:width="640px"}

c. Input "cis-doctor" under Name column to filter the result,then click CIS-Doctor.

![]({{site.baseurl}}/docs/runbooks/doctor/images/cis-doctor.jpg){:width="640px"}

d. Click **Load Balancers**.

![]({{site.baseurl}}/docs/runbooks/doctor/images/load_balancers.jpg){:width="640px"}

click the three dots,click Edit,the Global Load Balancer for Doctor domain will be shown.

![]({{site.baseurl}}/docs/runbooks/doctor/images/balancer_edit.jpg){:width="640px"}

e. Switch the Poolname which indicates the region by click the up/down arrow icon,the Poolname with priority One will accept the Doctor portal requests,please ensure the pollname in the region is working before promote it to priority One.Click **Apply Changes** to finish the priority change.

![]({{site.baseurl}}/docs/runbooks/doctor/images/change_priority.jpg){:width="640px"}


## Notes and Special Considerations

If cann't access "CIS-Doctor" services,please contact yujunjie@cn.ibm.com for access permission.

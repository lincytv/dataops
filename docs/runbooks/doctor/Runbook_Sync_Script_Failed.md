---
layout: default
description: This alert indicates a failure when transferring the scripts from ibm github script repository to target environment bosh cli VM.
title: Doctor Sync Script Failed
service: doctor
runbook-name: "Doctor Sync Script Failed"
tags: oss, bluemix, bbo, Sync_Script_Failed, ansible
link: /doctor/Runbook_Sync_Script_Failed.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

When you receive this alert, it means the scripts (e.g. autoscaling scripts) that were transferred from the IBM GitHub script repository to the target environment bosh cli VM failed.

## Technical Details

The transfer job implemented by Ansible.

## User Impact

The scripts which are used to run on the target environment VMs are not the latest and may have failed.

## Instructions to Fix

To fix this issue, follow the steps below:

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
{% include_relative _{{site.target}}-includes/tip_ssh.md %}

* Execute `curl http://localhost:4569/cloud/hello`

    If running the command returns {"result":"success"}, then execute the command: `ls -ld /opt/ansible/scripts`
and check whether the date is the same as other environments which return sync script success.

* If the date is not the same.
  - login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **CI & CD** from the left menu.
  - Click the **Sync Script Repository** button on the line that begins with **Sync:**.
  - Wait 2 minutes and then repeat steps 1 and 2.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/sync.png){:width="700px"}

* If the date is the same, resolve this alert.


## Notes and Special Considerations
   {% include {{site.target}}/tips_and_techniques.html %}

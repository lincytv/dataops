---
layout: default
description: Failed to Complete Selfhealing Scheduler Task Reset Root Password
title: Failed to Complete Selfhealing Scheduler Task Reset Root Password
service: doctor
runbook-name:  Runbook Failed To Complete Selfhealing Scheduler Task
tags: oss, bluemix, doctor
link: /doctor/Runbook_Failed_To_Complete_Selfhealing_Scheduler_Task.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

## Technical Details

## User Impact

## Instructions to Fix

### 1. Restart the BBO agent for the environment in the {{doctor-alert-system-name}} title.
   1. Logon to the [{{wukong-portal-name}}]({{wukong-portal-link}}).
   2. Go to the **CI & CD** page
   3. Enter `bbo_agent` as below.
   4. The BBO agent list will be displayed.   
   ![BBO_Agent_1]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/bbo_agent_restart_1.png){:width="700px"}
   5. Find the BBO agent for that environment.
   6. Click the **Restart** button.
   ![BBO_Agent_2]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/bbo_agent_restart_2.png){:width="700px"}
   7. Click the **Refresh** button. ![BBO_Agent_2]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/refresh_btn.png){:width="40px"} to check the `State` of the BBO agent that was restarted.
   8. Verify that it was restarted successfully.
      >***NOTE:*** It may take a couple minutes before `State` is updated.

   9. If the BBO agent can't be restarted successfully.
      * SSH to the Doctor agent Virtual Machine in that environment.
      * Restart the BBO agent manually with the command `docker restart bbo_agent`.
      {% include_relative _{{site.target}}-includes/tip_ssh.md %}

### 2. Run the Selfhealing scheduler task manually.  
   1. Logon to [{{doctor-portal-name}}]({{doctor-portal-link}}).
   2. Go to **Diagnose**.
   3. Select **Selfhealing**.
   4. Switch to **Schedule Jobs**.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_jobs.png){:width="640px"}
   5. Find the job by name as listed in the {{doctor-alert-system-name}} title _Reset root password_.
   6. Click the button in the **Logs** column.
   7. Select the environment that is listed in the {{doctor-alert-system-name}} title from the dropdown list.
   ![Selfhealing_job_1]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/selfhealing_schedule_job.png){:width="700px"}  
   8. A popup window will be shown.
   9. On the popup window, click the button **Run One-time**.
   ![Selfhealing_job_2]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/selfhealing_schedule_job_2.png){:width="700px"}
   10. Check the output log. If the operation failed please send an email to {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: Creating Self-healing Schedule Jobs
title: Self-healing Schedule Jobs
service: doctor
runbook-name: Self-healing Schedule Jobs
tags: oss, bluemix, doctor, firecall
link: /doctor/Runbook_Selfhealing_Schedule_Jobs.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

##  Steps to creating a Self-healing Schedule Job
1. Log in to [{{doctor-portal-name}}]({{doctor-portal-link}}).
2. Select the menu **Diagnose**.
3. Select **Self-healing**.
4. Select **Schedule Jobs** from dropdwon list.
5. Click the **Create** button. A modal named _Create New Scheduled Running Script_ will be displayed.
  * **Title:** Input the schedule job name.
  * **Description:** Input the description of the schedule job.
  * **Action Type:** Select an _Action Type_.
  * **Script:** Input the _Relative Path_ of a script.
  * **Parameters:** Input the parameter name and select the variable which is passed into the script.
  * **Scheduler Type:** Choose the Scheduler Type (Interval or Cron) and input the corresponding value .
  * **Enable on:** Choose one or more environments for the schedule job to run on.
  * **Post Action:** Set the action after the script log output if needed.
6. Click the **Submit** button.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_job_top_half.png){:width="640px"}
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_job_bottom_half.png){:width="640px"}
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/test_job.jpg)

## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

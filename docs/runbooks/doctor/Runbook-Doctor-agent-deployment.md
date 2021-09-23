---
layout: default
description: Runbook Doctor agent deployment.
title: Doctor Agent Deployment
service: doctor
runbook-name: Doctor agent deployment
tags: oss, bluemix, doctor, blink
link: /doctor/Runbook-Doctor-agent-deployment.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

## Purpose

Doctor Agent Deployment.

## Technical Details

Deployed by {{ucd-portal-name}}.

## User Impact

Users on-boarding their service to the OSS Ops Platform.

## Instructions to Fix

Check JML for _bluemix_doctor_agent_public_ip_ and _bluemix_doctor_agent_public_port_. If these keys and associated values are not present, reach out to the Doctor team  [{{oss-doctor-name}}]({{oss-doctor-link}}) or check `git log` for the repo to see if they were removed.

Check JML for _doctor_blink_port_. If it's not present, run A0216.

### Run {{ucd-portal-short}} process A2600

* Go to [{{ucd-portal-name}}]({{ucd-portal-link}}).

* Select **Applications** from the top list.

* Search for **Bluemix-End2End**.
![]({{site.baseurl}}/docs/runbooks/doctor/images/ucd/bluemix-end2end.png){:width="640px"}

* Find your environment.
      {% include_relative _{{site.target}}-includes/tip_find_ucd_env.md %}

* Click the **Play** button (triangle pointing to right with circle around it).
![]({{site.baseurl}}/docs/runbooks/doctor/images/ucd/play_script.png){:width="640px"}

* Uncheck **Only changed Versions** option.

* Select Process: A2600: Deploy doctor agent
![UCD run process]({{site.baseurl }}/docs/runbooks/doctor/images/ucd/run_process.png){:width="649px" height="495px"}

* If using a snapshot:
  - Select snapshot name
  - Choose component version: DoctorAgent: **3.805**

* Submit

## Verification:

Open Doctor status and confirm your environment is listed.

1. Wait about 10 minutes after UCD process success.
2. Open [{{doctor-status.name}}]({{doctor-status.link}})

![doctor status]({{ site.baseurl }}/docs/runbooks/doctor/images/status.png){:width="641px" height="347px"}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

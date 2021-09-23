---
layout: default
description: Configure Self-Healing
title: Configure Self-Healing
service: selfhealing
runbook-name:  Runbook configure selfhealing
tags: doctor
link: /doctor/Runbook_configure_selfhealing.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

Estimation: 20 Minutes.

## Purpose

Below are the steps to configure Doctor for self-healing.

## Rule Management

### Add new rule  

  * Once you have configured {{doctor-alert-system-name}} in Event Manager to receive the {{doctor-alert-system-name}} incidents by Doctor, you can add a self-healing rule to handle {{doctor-alert-system-name}} incidents automatically.  

    1. Log in to [{{doctor-portal-name}}]({{doctor-portal-link}}).
    2. Navigate to **Diagnose**.
    3. Select **Self-healing**.
    4. Click on **Create**. to add the rule.
    5. The following rule creation panel will open.
    6. Input all the fields required.
    7. **Submit**.
   ![Add_rule_1]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/add_rule_1.png){:width="700px"}
   ![Add_rule_2]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/add_rule_2.png){:width="700px"}
   ![Add_rule_3]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/add_rule_3.png){:width="700px"}

   >**Note:** The _Parameters_ section will change depending of the action type selected

  * By default, self-healing provides the following out-of-the-box action types that can be triggered by the {{doctor-alert-system-name}} incident.

  | Action Type     | Display Name     | Handler |
  | :------------- | :------------- |:------------- |
  | script | Exec Script Using BBO      | BBOScriptExecutionHandler       |
  | ansible_script | Exec Script Using Ansible | AnsibleScriptExecutionHandler |
  | BBO | Run BBO | BBOHandler |
  | reassign_to_user | Reassign User | PDUserAssignHandler|
  | set_escalate_polic | Reassign Escalation Policy | PDEscalationHandler |
  | auto_resolve | Auto Resolve | AutoResolveHandler|
  | ds_incident_route | Route CDS Incident| CDSIncidentRouteHandler|
  |rest_api | Invoke REST API | RestAPIHandler|
  | create_rtc_workitem | Create RTC Workitem | RTCHandler|
  | github_issue | Create Github Issue | GithubHandler|
  | slack	| Send To Slack | SlackHandler|
  | ansible_playbook | Exec Ansible Playbook | AnsibleScriptExecutionHandler|
  | password_expire | Create Defect For Password Expire | QradarPasswordExpireHandler|
  | pd | Create PagerDuty Incident | PDIncidentHander|
  |local_script | Exec Local Script On Doctor Agent | LocalScriptExecutionHandler|
  | send_mail | Send Mail | MailHandler|
  | reset_doctor_2fa | Reset Doctor 2FA | DoctorReset2FAHandler|



  * If you need custom actions for special cases you have two options:  

    1. Implement a custom action handler by referring to {% if site.target=='ibm' %} [Guide for how to implement Doctor Self-healing custom action handler]({{repos-bluemix-fabric-link}}/doctor/wiki/docs/Guide for how to implement Doctor Self-healing custom action handler.docx){% else %} [Guide for how to implement Doctor Self-healing custom action handler]({{site.baseurl}}/docs/runbooks/doctor/docs/Guide for how to implement Doctor Self-healing custom action handler.docx) {% endif %}.

    2. Implement a new micro-service and expose a _REST API_, then use the existing action type _Invoke REST API_ to call it.

      >**Note:** Some fields support regular expression input. Runtime will extract the value from the {{doctor-alert-system-name}} incident in the body using the regular expression. The regular expression input should be embraced by `/` like `/[\s\S]*([0-9]+)[\s\S]*/`, and the past embraced by parenthesis will be extracted.

## Rule Management

### Simulate rule   

  * You can test the added rule by using **Simulate**.

  1. Log in to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  2. Navigate to **Diagnose**.
  3. Select **Self-healing**.
  4. Click on **Simulate**.
  5. Input a {{doctor-alert-system-name}} incident/TIP Event.
  6. If {{doctor-alert-system-name}} incident.
      - Input the {{doctor-alert-system-name}} domain.
  7. Click the **Retrieve** button, to get the incident/event content.
  8. Click the **Match** button to list all the matched rules.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/simulate_rule_match.png){:width="700px"}
  9. If you want to trigger the matched rule, click the **Trigger** button.   
  ![Simulate_rule]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/simulate_rule.png){:width="700px"}   

## Scheduler Jobs  


  1. Log in to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  2. Navigate to **Diagnose**.
  3. Select **Self-healing**.
  4. Click **Schedule Jobs** from the dropdown menus on the right panel.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_jobs.png){:width="700px"}
  5. Click **Create** to add a new scheduler job.
  6. The following panel will open.
  7. Input all the required fields.
  8. Click **Submit**.
  ![Add_scheduler_job]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/add_schedule_job.png){:width="700px"}   

## Use Doctor PD services as SRE Bot

In some cases, an alert is not necessary to be escalated to SRE in case it can be fixed by automation. But we still need the alert history, so we can leverage the Doctor SRE bot.

![Doctor bot]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/doctor_bot.png){:width="700px"}  

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

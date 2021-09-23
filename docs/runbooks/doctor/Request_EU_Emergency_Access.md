---
layout: default
description: EU Emergency Requesting Access Process.
title: "EU Emergency Requesting Access Process"
service: doctor
runbook-name: EU Emergency Requesting Access Process
tags: oss, doctor, AccessHub. EU, Emergency
link: /doctor/Runbook_EU_Emergency_Request_Access_Process.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
\_\_

## Purpose

The IBM EU cloud imposes restrictions in relation to the operators having the possibility of accessing and managing Cloud resources. Standard/persistent access is allowed only to European operators (which means employees of any IBM European Union Nation). Any other access can be allowed only through an emergency process, which used to be based on USAM, and now has been moved to AccessHub. Any emergency access to the EU Cloud requested by non-EU personnel will be temporary (revoked after 2 hours). Please visit the [Process Overview](https://pages.github.ibm.com/ibmcloud/Security/guidance/AccessHub-EUCloud.html#process-overview) page on the IBM Public Cloud Security for more information.

This runbook is to provide the steps required to request access to an EU Managed Environment, which can be identified by the EU green dot on Doctor home page, I.e `YP_FRANKFURT)`.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor_eu_managed.jpg){:width="450px"}

If any non-EU personnel attempts to SSH to the environment from Doctor, will recieve a poppup window indicating the process you need to follow as outlined below.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_eu_permission_denied.jpg){:width="450px"}

## How to request access

- Login to [{{access-hub-name}}]({{access-hub-link}}/) with your W3ID.
- Click on the `Request or Manage Access` tab on the home page.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_request_access.png){:width="450px"}

- Under `ALL APPLICATIONS` Search for `BMX-PIM1-TOOLS`.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_input_application.png){:width="450px"}

- If you already have access to other groups for this application, click on `Modify Existing Access`, if not, click `Add To Cart`
- Click the `Checkout` button.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_checkout.png){:width="450px"}

- Search for the required EU emergency group. For the OSS team, we need to request `ibm-cloud-ops-platform_frayp_Blink_eu_emerg` group. Then select `+ ADD` and `Next` on the bottom of the page.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_eu_select_group.jpg){:width="450px"}

- Fill in the require Business Justification for requesting emergency access to EU Cloud systems. Instructions on how to do so can be found [here](https://pages.github.ibm.com/ibmcloud/Security/guidance/AccessHub-EUCloud-business-justification.html) and [here](https://ibm.ent.box.com/notes/238959050795?s=ynjzv8y39teohs9b2tnd7tqgtbtb1s5t).

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_eu_bus_justification.jpg){:width="450px"}

* Here is an example business justification:

  ```
  Id: 20150440
  url: https://ibm.pagerduty.com/incidents/P183NI7
  type: incident
  severity: non-blocking
  text: Access to this environment by IBM personnel from outside the European Union is required to investigate a non-blocking incident for BBO alert.  Access to the system is needed to investigate this issue and take corrective action as needed.
  ```

  `Please ensure that you do not change the spacing between the key work (such as **type:**) and the value (such as **Incident**) since your request may not be processed.`

- Select `Submit`, your request will then be reviewed/approved by the EU approvers. You can review the status and/or request updates on [{{oss-slack-eu-emerg-approvers-name}}]({{oss-slack-eu-emerg-approvers-link}}) slack channel.
- Any emergency access to the EU Cloud requested by non-EU personnel will be temporary (revoked after 2 hours). Doctor will still be the automation tool for processing such emergency requests.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

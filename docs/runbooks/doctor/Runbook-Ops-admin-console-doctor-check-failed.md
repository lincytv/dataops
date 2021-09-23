---
layout: default
description: Alert Received For Ops Admin Console Doctor Check Failure.
title: Ops Admin Console Doctor Check Failed
service: doctor
runbook-name: Ops admin console doctor check failed
tags: oss, ops admin, doctor
link: /doctor/Runbook-Ops-admin-console-doctor-check-failed.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose
This Runbook is to resolve alerts about Ops admin console doctor check failures.

## Technical Details
This type of alert often reassigned by SRE to us.

The content is as follows:
Bluemix Alert SEV3 - ***(env).fabric.admcnsl_chk.bmxDoctorTransactionCounts : st_admcnsl_doctorChk (Ops admin console doctor check failed)***

## User Impact

## Instructions to Fix

### 1. Log into the Doctor agent of the environment which mentioned in the alert.

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
__

### 2. Run these apis on Doctor agent in step 1.

  * `curl -X GET http://127.0.0.1:4569/cloud/app/dea_usage`  
  * `curl -X GET http://127.0.0.1:4569/cloud/app/cell_usage`  
  * `curl -X GET http://127.0.0.1:4569/cloud/monitor/network/usage/hourly`  

### 3 If step 2 results are all success

  * Go to [{{doctor-portal-name}} -> Blink]({{doctor-portal-link}}/#/proxy_blink).
  * Find the listed in the alert _(env).fabric.._
  * Click the ACE(IBM) button in column ACE Console.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_agent_2.png){:width="640px"}
  * Add /check in the url which opened, for example:
    - [https://console.gcc.ca-east.bluemix.net/check](https://console.gcc.ca-east.bluemix.net/check).
  * Check the result in the new open page.
    - If the result are all success, resolve the alert.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/DoctorChecksInAdminConsole.png){:width="600px"}

### If step 2 results are failed

  * Restart `doctor_backend` by `docker restart doctor_backend` on agent VM
  * Or use **Remote Command** for more info [check]({{site.baseurl}}/docs/runbooks/doctor/Runbook_cloud_usage_is_down.html)
  * Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html) if you cannot find the **doctor_backend** container.
  * Try step 2 again.
    - If step 2 still fails then try the follow runbooks and try step 2 again.
      - [Cloud resource usage APIs]({{site.baseurl}}/docs/runbooks/doctor/Runbook_cloud_resource_usage_APIs.html)
      - [Cloud usage is delay]({{site.baseurl}}/docs/runbooks/doctor/Runbook_cloud_usage_is_delay.html)
  * For [Metrics data is older than two hours]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Metrics_data_is_older_than_two_hours.html)


## Notes and Special Considerations

Sometimes it's caused by memory or disk being full check [Disk Usage is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html), if disk is not an issue check [boshcli runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Bosh_Cli_SSH_Metrics_ibm_allenvs_infra_sshTunnel.html).
If you have other problems, please contact {% include contact.html slack=admin-console-slack name=admin-console-name userid=admin-console-userid notesid=admin-console-notesid %} in admin console team.


{% include {{site.target}}/tips_and_techniques.html %}

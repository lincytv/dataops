---
layout: default
description: SSO ID is for accessing all Bluemix and services VMs, here are the process.
title: Request SSO ID
service: doctor
runbook-name: "Request SSO ID"
tags: oss, ssh, Jumpbox, SSO
link: /doctor/Request_SSO_ID.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

Estimation: 5 Minutes.

SSO ID is for accessing all Bluemix and services VMs, here are the process

1. Access the {{usam-name}} request page: [{{usam-short}}]({{usam-link}}).
2. Select **Request system access**, from the left side menu.
3. On the **Search for:** field enter system: {{usam-oss-system}}.
4. Click on **Search**.
5. Under **_System Search Results_**, check the box.
6. Click on **Submit**.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/sso_id_1.png)
7. On the **Userid:**, specify the ID you want to get access to (if your intranet id looks like the follow: {{usam-id-example}} use **john** as userid).
8. Click on the **_[+]_** of {{usam-oss-privilege}} to request a personal ID on the staging or production environment (both if you need access to both environments).
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/sso_id_2.png)
9. Select the group you need to join (depending on your team membership: please see the tables in the [Request access to Bluemix envs with personal IDs]({{usam.bluemix-envs-table}}) document for more details). If you work on Doctor on-call, you probably will want to request access to the following groups:
    - {{usam-doctor-stage-dev-ops}}
    - {{usam-doctor-prod-dev-ops}}
    - {{usam-doctor-prod-dev-ops-l}}

    >Make sure to specify the userid for each system you selected, and to enter a business justification in the related fields.

9. Fill the business justification for each group
Submit your request using the **Submit** button.

**NOTE** <br>
* If you already have a request/approved access using your **Userid** (from step 7), use the next steps instead:

  * Go to [{{usam-short}}]({{usam-link}}).
  * Click on **Manage Your Userids**.
  * Click on **Manage Groups/Privileges** for the **Userid** (from step 7).
  * Follow steps 8 and 9.
  * Click on **Request Access**.
  
* Need to reset your SSO password, use this [link](https://password.sos.ibm.com/default.aspx)

Once you submit the request, it will be approved by
{% include contact.html slack=usam-bluemix-envs-slack name=usam-bluemix-envs-name userid=usam-bluemix-envs-userid notesid=usam-bluemix-envs-notesid%} and
{% include contact.html slack=usam-bluemix-envs-alt-slack name=usam-bluemix-envs-alt-name userid=usam-bluemix-envs-alt-userid notesid=usam-bluemix-envs-alt-notesid%}. If approved, you'll receive an email from the tool, containing information about your access.

You'll get a temporary password that you need to change.
[To change your password, click here]({{usam-chg-pwd}})

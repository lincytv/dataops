---
layout: default
description: The access to this server is controlled through ldap authentication.Here is the process to apply the access.
title: Request CLI access
service: doctor
runbook-name: "Request CLI access"
tags: oss, ssh, Jumpbox, CLI
link: /doctor/Request_CLI_access.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

Estimation: 5 Minutes.

{{bosh-cli-link}} is the SSH entry in {{ibm-blue-zone-name}}, The access to this server is controlled through ldap authentication. Here is the process to apply the access,

1. Access the {{usam-name}} request page: [{{usam-short}}]({{usam-link}}).
2. Select **Request system access**, from the left side menu.
3. On the **Search for:** field enter system: **_{{usam-system-cli}}_**.
4. Click on **Search**.
5. Under **_System Search Results_**, check the box.
6. Click on **Submit**.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/ucd_id_1.png)
7. Specify your intranet id (_{{usam-id-example}}_) as user id in the request.
8. Click on the **_[+]_** of   **{{usam-cli-privilege-l1}}**
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/cli_id_2.png)
9. Click on the **_[+]_** of   **{{usam-cli-privilege-l2}}**
10. Click on the check box for  "_{{usam-group-jumpbox-ops}}_" group.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/cli_id_3.png)
11. Click on the check box for  "_{{usam-group-jumpbox-user}}_" group.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/cli_id_4.png)
12. Fill the business justification for each group
Submit your request using the **Submit** button.

 

**NOTE** <br>
* If you already have a request/approved access using your internet id use the next steps instead:
    * Go to [{{usam-short}}]({{usam-link-home}}).
    * Click on **Manage Your Userids**.
    * Click on **Manage Groups/Privileges** for the intranet id (from step 7).
    * Follow steps 8-10.
    * Click on **Request Access**.
    * If you see an error message check your [Pending requests]({{usam-link}}../../MyUseridsPending) before to try to create a new request.

---
layout: default
description: How to requet UCD access.
title: Request UCD access
service: UCD
runbook-name: "Request UCD access"
tags: oss, ssh, Jumpbox, UCD,SSO
link: /doctor/Request_UCD_access.html
type: Informational
---

1. Access the {{site.data[site.target].oss-doctor.links.usam.name}} request page: [{{site.data[site.target].oss-doctor.links.usam.short}}]({{site.data[site.target].oss-doctor.links.usam.link}}).
2. Select **Request system access**, from the left side menu.
3. On the **Search for:** field enter system: **_{{site.data[site.target].oss-doctor.links.usam.system-cli}}_**.
4. Click on **Search**.
5. Under **_System Search Results_**, check the box.
6. Click on **Submit**.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/ucd_id_1.png)
7. On the **Userid:**, specify the ID you want to get access to (e.g.: _{{site.data[site.target].oss-doctor.links.usam.id-example}}_).
8. Click on the **_[+]_** of   **{{site.data[site.target].oss-doctor.links.usam.ucd-privilege-l1}}**
9. Click on the **_[+]_** of   **{{site.data[site.target].oss-doctor.links.usam.ucd-privilege-l2}}**
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/ucd_id_2.png)
10. Click on the **_[+]_** of **Bluemix-UCD--Class-Test--BM ...**
    * Click on the check box for **Bluemix-UCD--Class-Test--BM-Developer** and add your business justification
11. Click on the **_[+]_** of **Bluemix-UCD--Class-General1--BM ...**
    * Click on the check box for **Bluemix-UCD--Class-General1--BM-Developer** and add your business justification.
![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/ucd_id_3.png)
12. Fill the business justification for each group
Submit your request using the **Submit** button.

**NOTE** <br>
* If you already have a request/approved access using your **Userid** (from step 7), use the next steps instead:

  * Go to [{{site.data[site.target].oss-doctor.links.usam.short}}]({{site.data[site.target].oss-doctor.links.usam.link}}).
  * Click on **Manage Your Userids**.
  * Click on **Manage Groups/Privileges** for the **Userid** (from step 7).
  * Follow steps 8-11.
  * Click on **Request Access**.
  * If you see an error message check your [Pending requests]({{site.data[site.target].oss-doctor.links.usam.link}}../../MyUseridsPending) before to try to create a new request.

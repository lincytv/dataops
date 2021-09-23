---
layout: default
description: Request access the Privileged ID Management (PIM)
title: Request access to the Privileged ID Management (PIM) in AH
service: tip-api-platform
runbook-name: Request access to the Privileged ID Management (PIM) in AH
tags: oss,AccessHub,pim,PIM,access
link: /apiplatform//Request_PIM_Access_In_AH.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

Privileged ID Management (PIM) access is managed by AccessHub, below are the steps for requesting access

- Login to [{{access-hub-name}}]({{access-hub-link}}/) with your W3ID
- Click **Request or Manage Access** on the home page.

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/accesshub_request_access.png){:width="640px"}

- In the application search bar, input **SOS IDMgt** in search box

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/ah_brand_system_sosidmgt.jpg){:width="640px"}

- If you already have some access to a group of this application, you just need to click **Manage Access**, if not you need to click **Request New Account** button

* Select your account name and click modify
* In the Brand Type, select `BU430-OTDev`

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/ah_brand.jpg){:width="640px"}

**NOTE: If you require the addition or modification of secrets, please contact one the following team members:**

- {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}
- {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}


- Click **Add** button next to add groups and search for the **BU430-OTDev-PIM-Developers** or **BU430-OTDev-PIM-ServiceAdmins** group if requesting for service admins. Select the group you want.    

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/ah_pim_group.jpg){:width="640px"}

- Input business justification then click **Submit** button. Justification can be such `on call operations for OSS API Platform`


- Click on View Status to review your request


- After your request is approved, you can find it on **Applications** page

## Runbook Owners

- {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

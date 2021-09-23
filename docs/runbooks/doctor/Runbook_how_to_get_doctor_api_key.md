---
layout: default
description: Describe how to get your API Key
title: How to get your API key
service: doctor
runbook-name: Runbook how to get doctor api key
tags: doctor
link: /doctor/Runbook_how_to_get_doctor_api_key.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## Get your API Key

  * Log on to the  [{{doctor-portal-name}}]({{doctor-portal-link}}).
  * Click your ID to open the preference page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-1.png){:width="640px"}
  * Click on **Account**.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-2.png){:width="640px"}
  * Get the **API Key** on the user profile page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/get_api_key.png){:width="640px"}
  * If API Key is empty, click on the **Create**, to generate a new one.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/create_api_key.png){:width="640px"}.

  If you see
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/dont_have_apiplatform_group.png){:width="640px"}
  
  * Go to USAM: https://usam.svl.ibm.com:9443/AM/idman/AddSystemAccess

  * Search for the system "USAM-PIM1-BMX"

  * Specify your Intranet ID in the request

  * Select group "BMXDoctor-Operator-Apiplatform"

  * Submit your request

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

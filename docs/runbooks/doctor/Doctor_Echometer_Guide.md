---
layout: default
description: Doctor Echometer Guide
title: Doctor Echometer Guide
service: doctor
runbook-name: Doctor Echometer Guide
tags: wukong, echometer
link: /doctor/Doctor_Echometer_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}



1. Prepare
    Add a API in your service for check:
    e.g. We have a `healthz` API in _IAM_, _user_, _cloud_ service. And will return **ok**, code as below:

    ```
     get '/healthz' do
        return "ok"
      end
    ```
    Of course you can define your output based on your requirement.
2. Quick Start

  * Login in [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Find the **Echometer** option at the bottom of the left bar.
  * Click the **Add URL** button in the upper left corner of the page.
  * Add the corresponding content to the new pop-up page.
    - **URL:** The URL you want to monitor (**required**).
    - **Service:** The kind of service that your url belongs to(**required**).
    - **Env:** This option applies to service in agent. It must be a json array, e.g.:       
    _["D_DYS1","D_CAPGEMINI_TEST","YS1_LONDON","YS1_DALLAS"]_
    - **Expect Response Code:** The HTTP response code your URL should return.(required)
    - **Expect Response Result:** The HTTP response body your URL should return.
    - **PagerDuty Service Key:** The {{doctor-alert-system-name}} key that will be used for send {{doctor-alert-system-name}} alert.
    - **Echometer Instance:** Which _Echometer_ you choose to monitor your URL.
      * If you don’t know which one to choose, just leave it blank. Basically if the URL IP is {% if site.target =='ibm' %}10.x.x.x{% else %} <<your IP here>>{% endif %}
      * The instance should be _instance_service_zone_.
    - **Alert Type:** Currently it only supports {{doctor-alert-system-name}}.
    - **Whether to take Recovery Action:** `YES` - It will restart service when it gets incorrect status.
    - **Whether to send recovery notification:** `YES` - It will send {{doctor-alert-system-name}} alert to indicate that the service is recovered
    - **Whether to take action immediately:** `NO` - It will waiting for some time to retry then take actions if the status is still not good.
    - **Runbook link:** Customized Runbook link, if empty it will use the default one: `https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook-Echometer-URL-Down-Failure.html`
*	Click the **Add** button, you will see the URL added on the page.
* Click the **Refresh** button to see the URL status.  
  - `STATUS 0:  URL is normal`
  - `STATUS 1:  URL is down`

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/add_url.png)

## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: EU Emergency Process USAM API Invoke Failure
title: EU Emergency Process USAM API Invoke Failure
service: euaccess
runbook-name: EU Emergency Process USAM API Invoke Failure
tags: oss, bluemix, doctor,euaccess
link: /doctor/Runbook_EU_Emergency_Process_USAM_API_Invoke_Failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

1. As EUaccess service depend on {{usam-short}} system, so take following action to check if {{usam-short}} system down or {{usam-short}} API work well
   - a. Accessing [{{usam-name }}]({{usam-link}}).
   - If you **can not*** access {{usam-short}} home page please go to slack channel [{{eu-emerg-approvers-name}}]({{eu-emerg-approvers-link}}) and post a message about {{usam-name }} down, **and snooze the incident and resolve it after {{usam.short}} is covered** , otherwise go to step 1.b  
   - b. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   - Navigate to page **EU Emergency Admin**.
   - Click button **Test USAM API**.
   - If test failed go to step 2, otherwise you can close pagerduty alert for now and to see if alert will be triggered again, maybe just intermittent problem

2. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Select **CI & CD** from the left side menu.
4. Search out service `doctor_euaccess`, these instances should be run on **{{doctor-service1-name}}** and **{{doctor-service2-name}}**.
5. Restart listed environments one by one, please, by clicking on the icon under the *Action* column.
6. If all action taken and still get alert later, login {doctor-service2-rtp-name}}, {{doctor-service1-name}} & {{doctor-service2-name}}
   - a. Run command 'ping usam.svl.ibm.com' on both VMs, if not reachable it may caused as RTP DNS server issue, you can try to add '9.30.63.23  usam.svl.ibm.com' into /etc/hosts and restart `doctor_euaccess` by `docker restart doctor_euaccess`
   - b. Also run `docker restart usam_rest_client` on the VMs.

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_euaccess.png)

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

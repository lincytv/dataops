---
layout: default
description: This Runbook is for PagerDuty alerts when the blink is down for watson environment.
title: Doctor Blink sretools.blink is Down
service: blink_agent
runbook-name: Doctor Blink Service is Down for watson environment
tags: oss, bluemix, doctor, blink, blink_agent, docker
link: /doctor/Runbook_Doctor_Blink_Watson_Env.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

## Purpose

This alert happens when blink does not work on watson environments.

## Instructions to Fix

### Verify if the tunnel is ok

  - Log on a mbus server(mbus1/mbus2/mbus3).
  - Run `nc -v 10.124.116.109 <Port>`

  **TIP:** To find the port.

 |Env name|Port|
 |:----|:-----|
 |WATSON_CMPRD|48516|
 |WATSON_CSFDEV|48511|
 |WATSON_DDEV|48515|
 |WATSON_FRAPRD|48507|
 |WATSON_LONPRD|48521|
 |WATSON_PPRD|48509|
 |WATSON_PSTG|48510|
 |WATSON_SBPRD|48514|
 |WATSON_SKPRD|48518|
 |WATSON_SYDPRD|48508|
 |WATSON_TOKPRD|48522|
 |WATSON_TRPRD|48513|
 |WATSON_ICD|48525|
 |WATSON_SEOPRD|48527|

<br>
<br>
  If the output is like this `Connection to 10.124.116.109 port 45001 [tcp/*] succeeded!`, then blink is work now, you can just resolve this incident.

  If the output is like this `nc: connectx to 10.124.116.109 port 45001 (tcp) failed: Connection refused`, please refer to next step.

  >**Note:** If you don't see the environment/port or the port number isn't correct; follow the steps described here [Step 7 To verify that the blink agent has started and working]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Doctor_Blink_ibm_allenvs_network_doctor_blink.html#step-7-to-verify-that-the-blink-agent-has-started-and-working) **Step 7.3 Make sure blink is using the correct port**  to get the correct port number.

### Restart blink_agent

  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
  - Select **CI & CD**
  - Search for `blink_agent` under `Continuous Deployment`.
  - Find the target environment.
  - Verify if the state of blink_agent is `Up xxx`, if not, click `Restart Service` button.
  - Verify the tunnel as step1 , if still get `Connection refused` error, please post a message to slack channel #watson-on-doctor or send a direct message to @ssymes.




## Notes and Special Considerations

 If any questions, please contact {% include contact.html slack=cloud-software-dev-slack name=ccloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} or {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid %}.

 {% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: Runbook VM register failure
title: Runbook Runbook VM register failure
service: CipherKeeper
runbook-name: Runbook Runbook VM register failure
tags: oss, bluemix, doctor
link: /doctor/Runbook_VM_register_failure.html
type: Alert
---

{% include {{site.target}}/load_oss_sosat_constants.md%}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose
This alert will be triggered if VM register endpoint down or VM registration failure

## Technical Details
VM register service is used to deploy doctor keys, enable firecall accounts or root account.

## User Impact
VM register endpoint down or VM registration failure may block mod_vm process

## Instructions to Fix

1. Go to
[{{service-now-name}}]({{service-now-link}}/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_userpref_module%3Db55b4ab0c0a80009007a9c0f03fb4da9%26sysparm_clear_stack%3Dtrue) and open a new ServiceNow incident manually to record this issue.
2. Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Go to the **CI & CD** panel.
4. In the **Continuous Deployment** section.
5. Type in `oss_cipherkeeper`.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/vm_register_failure.png){:width="640px"}
6. Restart the service instance listed in the table, by clicking on the icon under the **Action** column.
7. If this alert still existed, escalate to doctor team


## Notes and Special Considerations
   {% include {{site.target}}/tips_and_techniques.html %}

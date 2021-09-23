---
layout: default
description: This runbook will guide Doctor operator how to reload Doctor agent.
title: How to work with GRE for BoshCli upgrade on local environment
service: admin
runbook-name: How to work with GRE for BoshCli upgrade on local environment
tags: oss, bluemix, boshcli, doctor, agent,local
link: /doctor/Runbook_how_to_work_with_GRE_for_BoshCli_upgrade_on_Local_environment.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}


## Purpose
 This runbook will guide Doctor operator how to work with GRE for boshCli upgrade on local environment.

## Technical Details
  Doctor agent/blink is running on two boshcli systems for local environments , when boshcli system is planned to upgrade, it will be shut down for minutes.  Since GRE is using vCenter to manage local system, and vCenter is accessed via Doctor blink proxy, so during the shutdown of one system ,we need to make sure that the other one is working , so that GRE can login vCenter then power on the upgraded boshcli


## User Impact
n/a

## Instructions  
1. Verify two boshcli have deployed all Doctor services and working , at least including  access, blink, backend , security...
- note:  if the system is L_RBCSCC or L_RBCGCC, need to follow [this runbook](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/ibm-only/Runbook_For_L_RBCSCC_Manual_Command_For_Starting_Doctor_Agent_Service.html) to start service manually
2. Stop  blink service on one boshcli
3. Enable Doctor proxy on you browser
4. Access  https://vcenter._$[domain-name]_/  ,the domain name can be found at Doctor->access->blink
5. Verify if the page is accessible
6. Start blink and stop another one, repeat step 4 & 5



## Notes and Special Considerations

If any issue of blink, please contact Qi ZM Guo/China/IBM

{% include {{site.target}}/tips_and_techniques.html %}

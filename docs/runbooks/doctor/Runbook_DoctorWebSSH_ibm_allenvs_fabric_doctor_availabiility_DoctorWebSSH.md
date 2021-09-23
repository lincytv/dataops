---
layout: default
description: Doctor Web SSH Alert
title: Doctor Web SSH is Down
service: webssh
runbook-name: Runbook Doctor Web SSH ibm allenvs fabric doctor availability Doctor Web SSH
tags: oss, bluemix, doctor, Web, SSH
link: /doctor/Runbook_DoctorWebSSH_ibm_allenvs_fabric_doctor_availabiility_DoctorWebSSH.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose

This Runbook resolves the alert for Doctor Web SSH not working as expected.

## Technical Details

Doctor Web SSH is built on a native SSH tunnel that relies on network connectivity between the Doctor agent and the Doctor message bus.   

## User Impact

The user can't log in to the target VM with Web SSH from Doctor portal.

## Instructions to Fix

### Step 1 Login to the VM that has the doctor agent

  {% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}

  {% include_relative _{{site.target}}-includes/tip_ssh.md %}

### Step 2 Check network status

   - Go to [{{repos-bluemix-fabric-name}} doctor-configuration]({{repos-bluemix-fabric-link}}/doctor-configuration/tree/master/config).
   - Find the .yml of the environment e.g. _taishan_dedicated_bnsf.yml_.
   - Open the yml, find **ssh_hub**,it's ssh hub IP address.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/cloud_ssh_hub.png){:width="640px"}
   - Run `nc <ssh_hub_ip_address 22 -w 3`.
   - Then run `echo $?`.
      - If the result is `0`, that means network is ok.
        * Restart doctor_access service by command `docker restart doctor_access`.
      - If the result is anything other than `0`, there is a network issue.
        * Wait 5 minutes (in the event that the network issue is intermittent) and then run the `nc` command again.
        * If the `nc` command still returns anything other than `0`, open a defect and assign it to the doctor team, {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

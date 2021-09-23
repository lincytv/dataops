---
layout: default
description: A list of tips and techniques useful for Doctor on-call duties
title: Deploy certificates on doctor agent
service: doctor
runbook-name: DECOMMISSIONED - Deploy certificates on doctor agent
tags: oss, bluemix, runbook, cert
link: /doctor/Deploy-certificates-on-doctor-agent.html
type: Informational
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}


## Purpose
This is use to create or regenerate certificates on a doctor environment.

## Test

## Technical Details

Need to have access to the VM and able to sudo



## Instructions to Fix

1. Logon into the target VM, Use SSH from [{{wukong-portal-name}}]({{wukong-portal-link}}/) or [{{doctor-portal-name}}]({{doctor-portal-link}}).

2. Verify certificates
  - Rename authorized_keys file on target VM
    - `cd /home/doctor/.ssh/`
    - `mv authorized_keys authorized_keys.bak`, need to change it back after verification, if no authorized_keys under this folder, just skip this step.
  - SSH to target VM with key

  - Logon doctor agent.
    - `docker exec -it doctor_security bash`
    - `cd /opt/ansible/`
    - `ssh-agent bash`
    - `ssh-add doctor_key` (or taishan_key)
    - `cd /home/doctor/.ssh/`
    - `mv authorized_keys authorized_keys.bak`
    - `ssh -A doctor@x.x.x.x` , replace the IP to doctor agent IP, if you can SSH to the target IP without password, then cert is ok on this IP.

 3. Upgrade **doctor_security** to the latest version.
    - From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
    - Select **CI & CD** from the left side menu.
    - Search **doctor_security**, check the version of new environment, if the version is not the latest version, upgrade it.
 4. Sync the script repository.
    - Check if the cert_checker.sh is exist on doctor agent.
      - From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
      - Select **Remote Command** from the left side menu.
      - Select the doctor agent of new environment, run the following command.
        - `ls /opt/ansible/scripts/doctor_scripts/cert_checker.sh` If there is no this script, follow the next step  to sync the script.
    - Sync script on [{{wukong-portal-name}}]({{wukong-portal-link}}/) portal.
      - From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
      - Select **CI & CD** from the left side menu.
      - Click on **Sync Script Repository**, it will sync scripts on all environments, need to wait several miniutes.
 5. Deploy cert to doctor agent.
   - From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
   - Select **Remote Command** from the left side menu.
   - Select the doctor agent of new environment
   - `curl localhost:4693/security/firecall/cert/check_by_ip -d '{"email": "xxx@cn.ibm.com", "ips": ["x.x.x.x"], "regenerateca": "true", "restartssh": "true", "groupkey": <group key>}'`
   > Replace the IP to doctor agent ip.

 6. Create signed public key on doctor agent.
   - From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
   - Select **Remote Command** from the left side menu.
   - Select the doctor agent of new environment
   - `curl localhost:4693/security/firecall/agent/cert/check -d '{"email": "xxx@cn.ibm.com","regenerate_cert": "true", "public_key": <public key>,"group_key":<group key>}'`

   > Get the **public_key** and **group_key** from [here](https://github.ibm.com/cloud-sre/doctor_runbook_private/blob/master/certificates_doctor_agent_keys) if you don't have access to the git repo, contact: {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or in slack channel: <a href="{{oss-doctor-link}}">{{oss-doctor-name}}


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

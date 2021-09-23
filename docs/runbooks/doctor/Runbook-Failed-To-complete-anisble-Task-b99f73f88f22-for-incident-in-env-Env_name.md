---
layout: default
description: Failed To complete Ansible Task b99f73f88f22.
title: Failed To complete Ansible Task b99f73f88f22
service: doctor
runbook-name: "Failed To complete Ansible Task b99f73f88f22"
tags: oss, bluemix, doctor, blink, ansible
link: /doctor/Runbook-Failed-To-complete-anisble-Task-b99f73f88f22-for-incident-in-env-Env_name.html
type: Alert
---


## Purpose

Resolve alert with incident body:

```
fatal: [x.x.x.x: UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: Permission denied (publickey,password).\r\n", "unreachable": true}
```

## Technical Details

## User Impact

## Instructions to Fix

1. Log in to the agent VM of the impacted environment, and connect to the container `doctor_backend` with the command `docker exec -it doctor_backend bash`.
Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.
2. Go to `/etc/ansible/hosts` and search for the IP in the error message above, you may see a line like:
```
x.x.x.x ansible_user=<user> ansible_become_pass=xxxxxx ansible_ssh_private_key_file=/opt/ansible/xxxx
```
3. Run the command `ssh -i /opt/ansible/xxxx  <user>@x.x.x.x` to test if the user and private key in step 2 are correct (this should fail) then switch to another key under `/opt/ansible/`. If another key works, change the `/etc/ansible/hosts` to the correct key path.
4. Change the yml config of the environment with correct ssh key path and commit to config repository. If the IP in error message is `boshcli`, you need to change `ope > ansible > script_repo > ssh_key`, if not change `ope > ansible > target > ssh_key`.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

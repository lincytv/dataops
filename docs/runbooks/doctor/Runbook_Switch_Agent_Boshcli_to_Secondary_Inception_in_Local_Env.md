---
layout: default
description: Once primary agent/boshcli in local env can not be accessed, switch to secondary inception
title: Switch agent boshcli to secondary inception in local env
service: doctor
runbook-name: "Runbook - Switch to agent/boshcli to secondary inception in local env"
tags: agent/boshcli, Secondary, Runbook,Doctor, Inception
link: /doctor/Runbook_Switch_Agent_Boshcli_to_Secondary_Inception_in_Local_Env.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## Purpose
Once primary agent/boshcli in local env can not be accessed, we need to switch to secondary inception

## Technical Details
1. Edit the bosh_cli ip in doctor configuration
2. Restart doctor_backend, doctor_scriptengine, doctor_security
3. Add the bbo_agent config if there is not configuration and restart, or restart it directly


## User Impact
NA

## Instructions to Fix

1. Edit [doctor-configuration]({{doctor-config-repo-link}}) file taishan_local_xxxxx.yml,
switch the ip in bosh_cli and bosh_cli_backup,   

change
```
bosh_cli: {{bosh-cli-ip}}
bosh_cli_backup: {{bosh-cli-ip_backup}}
```
to  
```
bosh_cli: {{bosh-cli-ip_backup}}  
bosh_cli_backup: {{bosh-cli-ip}}
```
change
```
script_repo:  
            ip:{{bosh-cli-ip}}
```
to
```
script_repo:  
            ip: {{bosh-cli-ip_backup}}  
```

2. In [{{wukong-portal-name}} > Doctor Keeper]({{wukong-portal-link}}) page, search environment name and SSH.

3. Run `docker ps` to list all doctor container and run `docker restart <container_name>` for
+ doctor_backend
+ doctor_scriptengine
+ doctor_security

4. Restart bbo_agent
+ If there is bbo_agent, run `docker restart bbo_agent`.

+ If there is not bbo_agent, find the similar config for bbo_agent in other environment in path {{doctor-compose-path}}, paste to current {{doctor-compose-file-name}},
```
bbo_agent:
    command: port_num config_name https_same_to_doctor_access
    container_name: bbo_agent
    environment:
    - GROUP_KEY=xxxxxxxxxxxxxxxxxxxx
    image: xxxxxxxxxxxxxxxxx
    mem_limit: 1500000000
    network_mode: host
    restart: always
    stdin_open: true
    tty: true
    volumes:
    - /opt/bbo/data:/opt/bbo/data
```
change `command: port_num config_name https_same_to_doctor_access` for current environment, restart the bbo_agent with  `{{doctor-compose-cmd}}`

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

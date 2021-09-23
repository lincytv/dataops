---
layout: default
description: This alert will be triggered if consul agent started on Doctor agent was down.
title: Consul agent is down
service: consul
runbook-name: Consul agent is down
tags: consul_agent
link: /doctor/Runbook_ibm_env4_lon_fabric_diego_consul_check_st_consulAgent_check_consul_agent_is_down.html
type: Alert
---


{% include {{site.target}}/load_oss_doctor_constants.md%}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose
This alert will be triggered if consul agent started on Doctor agent was down

## Technical Details
There is consul agent started on Doctor agent, it was started automatically during startup of container **doctor_backend**. It's for get status of cf consul cluster and show it on **Instance** tab of [{{doctor-portal-name}} Cloud page]({{doctor-portal-link}}/#/cloud) of each environment.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/details.png)


## User Impact
Consul status shown on Doctor portal will not update to date.

## Instructions to Fix
1. Logon [{{wukong-portal-name}}]({{wukong-portal-link}}) portal.
2. SSH logon to Doctor agent of that environment mentioned in {{doctor-alert-system-name}} alert.
3. `sudo -i` to get root privilege.
4. Run `docker exec -it doctor_backend bash`.
Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.
5. You will jump into container **doctor_backend**.
3. Run `ps -ef | grep consul`.
  * If no consul process.
    - Run commnad `/opt/taishan/tools/web_console/scripts/consul_agent.sh /opt/logs/consul/config/consul.json` to started it.
4. Run `ps -ef | grep consul` to confirm consul process has started.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

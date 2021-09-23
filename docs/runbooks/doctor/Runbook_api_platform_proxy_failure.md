---
layout: default
description: How to solve the API platform proxy issue.
title: Recover the API Platform proxy
service: doctor
runbook-name: Recover the API Platform proxy
tags: oss, doctor
link: /doctor/Runbook_api_platform_proxy_failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

# Recover the API Platform proxy

## Purpose
Once the API Platform in Armada works but the Nginx proxy to expose it doesn't work, follow this guide.

## User Impact
When the proxy doesn't work, requests cannot be sent to API Platform.

## Instructions to Fix

For the dev env (pnp-api-oss.dev.cloud.ibm.com), which is exposed by Nginx on 10.154.65.173/9.66.246.38:

1. See which IP of the Nginx server is not working. You can use `https://9.66.246.38/catalog/api/info` and `https://10.154.65.173/catalog/api/info`; or set `<9_or_10_IP> pnp-api-oss.dev.cloud.ibm.com` in your /etc/hosts file and use `https://pnp-api-oss.dev.cloud.ibm.com/catalog/api/info`.

    - If the 10 IP works while the 9 IP doesn't, check whether `ssh [your SSO username]@9.66.246.38` works from your local machine terminal.
        - If you can SSH to 9.66.246.38, then it might be a network configuration issue, try `ifconfig eth0 mtu 1300` on 9.66.246.38.
        - If you cannot SSH to 9.66.246.38, `ssh [your SSO username]@10.154.65.173` from a Softlayer host, and check the routing table using `netstat -rn`. If the output contains no `9.0.0.0` destination, add it using `route add -net 9.0.0.0 netmask 255.0.0.0 gw 10.154.65.1`, and check whether 9.66.246.38 can be SSHed. If it still doesn't work, contact the network team for help.

    - If both IPs fail, try SSH or ping 10.154.65.173 from a Softlayer host.
        - If SSH works, check the Nginx configuration.
        - If SSH/ping fails, the VM might need a hard reboot.

---
layout: default
description: How to solve the LDAP proxy issue.
title: Recover the LDAP proxy
service: doctor
runbook-name: Recover the LDAP proxy
tags: oss, doctor
link: /doctor/Runbook_ldap_proxy_down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

# Recover the LDAP proxy

## Purpose
Once the LDAP proxy doesn't work, follow this guide to fix it.

## Technical Details
Softlayer VMs and Armada pods might not access LDAP APIs since the LDAP server is in the bluezone. Thus, 2 proxies (`10.154.65.173:1636` and `10.190.54.106`) are used to access LDAP APIs.

## User Impact
When the proxy doesn't work, requests from Softlayer VMs or Armada pods cannot be sent to the LDAP server.

## Instructions to Fix

#### Option 1

Ask the LDAP client to config to automatically switch to one of the other proxy, if have not already done so.

#### Option 2
Try to fix the proxy problem.

SSH to a proxy using your SSO credential.
Do `ssh [your SSO username]@<9_IP_of_the_proxy>` from your local machine terminal. (9 IP mappings: 10.154.65.173/9.66.246.38, 10.190.54.106/9.66.242.229).
  - If you cannot SSH to the 9 IP, try to SSH to the proxy using the 10 IP. (Go to [WuKong](https://wukong.cloud.ibm.com/#/) -> Doctor Keeper, start a ssh session from any of the DOCTOR_SERVICE_* listed. Do `ssh [your SSO username]@<10_IP_of_the_proxy>`
      - If it also failed, go to Doctor to check the VM's status, and reboot it if necessary. (If you do not have the privilege to reboot it, contact {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} during North America time, or Slack channel [{{oss-doctor-name}}]({{oss-doctor-link}}) during China time.)
      - If it succeeded, it means the private 10 IP is ok, and the problem only exists in the 9 IP:
          - For 10.154.65.173/9.66.246.38, check the VM's routing table using `netstat -rn`. If the output contains no `9.0.0.0` destination, add it using `route add -net 9.0.0.0 netmask 255.0.0.0 gw 10.154.65.1`, and check the proxy's 9.66.246.38 IP again. If the 9.66.246.38 IP still doesn't work, contact the network team for help.
          - For 10.154.65.173/9.66.246.38, contact the network team for help.
  - If you can SSH to the 9 IP, the problem might exist in the tunnel deamon, or the monitor in Armada. contact {% include contact.html slack=tip-api-platform-5-slack name=tip-api-platform-5-name userid=tip-api-platform-5-userid notesid=tip-api-platform-5-notesid %}.

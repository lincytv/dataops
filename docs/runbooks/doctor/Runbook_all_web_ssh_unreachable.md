---
layout: default
description: How to fix the issue of all web ssh unreachable
title: web ssh unreachable
service: doctor
runbook-name: All web ssh unreachable
tags: oss, bluemix, doctor, gre
link: /palente/Runbook_all_web_ssh_unreachable.html
type: issue
---

{% include {{site.target}}/load_oss_contacts_constants.md %}

## Technical Detail
When  web ssh is unreachable (opens a blank window but no any response)  on all environments , it might be caused by Webtty is not working ，need to restart it.  

## Steps to fix
1. login 9.42.74.244(DOCTOR_RTP_SSHHUB) using your w3 id
2. run command : Sudo supervisorctl restart wetty

## Prereq:
1. Request access for USAM group : ibm-cloud-ops-platform_portal-devops_operator 
2. Contact  {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} to create the id in associated system

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

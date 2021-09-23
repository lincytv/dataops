---
layout: default
description: RETIRED - This Runbook is for PagerDuty alerts when PostgreSQL server is down.
title: RETIRED - Doctor PostgreSQL server is Down
service: PostgreSQL
runbook-name: RETIRED - Doctor PostgreSQL Server is Down
tags: oss, bluemix, doctor, PostgreSQL, pg
link: /doctor/Runbook_Doctor_PostgreSQL_Server_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

## Purpose

This alert happens when doctor PostgreSQL server is down.

## User Impact
If PostgreSQL server is down, doctor db can't be accessed any more.

## Instructions to Fix

Please verify if PostgreSQL server is down, if so, you need to contact doctor team.

  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
  - Select **Remote Command**
  - Search a server which is in service account such as mbus1, mbus2 or mbus3
  - Input `nc -v <host> <port> -w 5`, replace `<host>` and `<port>` with the real one get from details of the incident
  - Click `Run`
  - If you get success, it indicates PostgreSQL server is ok now, you can resolve this incident.
  - If you get Error like this `Execute shell command error`, it indicates PostgreSQL server maybe down, or there are some network issue of PostgreSQL server.

**Please run `nc` command 3 times, if all failed, contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} directly. If they are not online, please make emergency call to CDL team.**

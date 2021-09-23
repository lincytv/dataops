---
layout: default
description: RETIRED -  This Runbook is for PagerDuty alerts when PostgreSQL connections exceed the max connections.
title: RETIRED - Doctor PostgreSQL connections exceed
service: PostgreSQL
runbook-name: RETIRED - Doctor PostgreSQL connections exceed
tags: oss, bluemix, doctor, PostgreSQL, pg
link: /doctor/Runbook_Doctor_PostgreSQL_Connections.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

## Purpose

This alert happens when the connections to PostgreSQL server with doctor user exceed the max connections.

## User Impact
If PostgreSQL connections is exceeded, doctor db can't be accessed with `doctor` user any more.

## Instructions to Fix

Please restart `reportcollector` service on wukong portal.

  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
  - Select **Remote Command**
  - Search following servers and choose all of them: `DOCTOR_RTP_SERVICE1`,`DOCTOR_RTP_SERVICE2`,`DOCTOR_SERVICE1_LIT`
  - Input `docker restart reportcollector`, then click `Run`.
  - Input `docker ps|grep reportcollector`, then click `Run`, verify if `reportcollector` is just restarted.

**Please DO NOT resolve this incident manually, it will be resolved automatically in 40 minutes, if it's not resolved, please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} directly. If they are not online, please make emergency call to CDL team.**

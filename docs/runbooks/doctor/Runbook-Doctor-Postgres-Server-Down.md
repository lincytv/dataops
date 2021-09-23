---
layout: default
description: RETIRED - When this issue occurs, it means that postgres server can not be connected.
title: RETIRED - Doctor Postgres Server Down
service: postgres db
runbook-name: RETIRED - Doctor Postgres Server Down
tags: oss, bluemix, postgres, doctor, vm
link: /doctor/Runbook-Doctor-Postgres-Server-Down.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

Please directly contact {% include contact.html slack=bosh-director-slack name=bosh-director-name userid=bosh-director-userid notesid=bosh-director-notesid %} or {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %} or {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %}. If they are not online, please make emergency call to CDL team.

---
layout: default
description: RETIRED - This Runbook is for PagerDuty alerts when the PgSQL Standby Node is down.
title: RETIRED - PgSQL Standby Node is down
service: N/A
runbook-name: "RETIRED - PgSQL Standby Node is down"
tags: oss, bluemix, doctor, Postgresql, PgPool, HaProxy
link: /doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Standby_Down.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
{% include {{site.target}}/load_pgsql_constants.md %}
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

## Purpose

This alert happens when PgSQL Standby Node is down.

## User Impact

Usually, PgSQL standy node down won't impact anything.

## Contacts

Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}


## Details

{% include {{site.target}}/pgsql_servers.md %}

If you got any incidents as below:
- Postgres Standby node ping failure alerts


Please follow this runbook to deal with the incidents.

## Instructions to Fix

### Step 1 Inform the focal about the incident.

Please [contact](#contacts) with the focal, inform them about the incident. Reassign the PD incident to the contact and let them know it Please.
> Focal pints need to use the follow [documentation](https://ibm.ent.box.com/file/574470465943)

## Notes and Special Considerations
If the problem is not resolved contact a member from the [contacts](#contacts) section.
{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: RETIRED - This Runbook is for PagerDuty alerts when the PgSQL Primary Node is down.
title: RETIRED - PgSQL Primary Node is down
service: N/A
runbook-name: "RETIRED - PgSQL Primary Node is down"
tags: oss, bluemix, doctor, Postgresql, PgPool, HaProxy
link: /doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Primary_Down.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_pgsql_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

## Purpose

This alert happens when PgSQL Primary Node is down.

## User Impact

This alert indicates that PgSQL clusters will not be able to be connected any more.

## Contacts

Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}


## Details

{% include {{site.target}}/pgsql_servers.md %}

If you got any incidents as below:
- Postgres Primary node ping failure alerts


Please follow this runbook to deal with the incidents.

## Instructions to Fix

### Step 1 Verify if the PgSQL Cluster Prod is down.

Run the following commands.


   ```
curl -i -X GET "http://{{osspgproxy1-private-ip}}:5777/CheckHASystemHealth"

curl -i -X GET "http://{{osspgproxy2-private-ip}}:5777/CheckHASystemHealth"

   ```

   If you got return message (anyone of the HaProxy nodes) like this:

   ```
    HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 140
    Server: Werkzeug/0.14.1 Python/2.7.12
    Date: Tue, 30 Oct 2018 01:52:21 GMT

    Tue Oct 30 01:52:21 2018: ********PgSQL Writing is functional********
    Tue Oct 30 01:52:21 2018: ********PgSQL Reading is functional********
   ```
   That means the current HaProxy node is alive and the whole DB cluster is OK. You can close the incident.

or

follow the step 2.

### Step 2 Inform the focal about the incident.

Please [contact](#contacts) with the focal, inform them about the incident. Reassign the PD incident to the contact and let them know it Please.
> Focal pints need to use the follow [documentation](https://ibm.ent.box.com/file/574470465943)


## Notes and Special Considerations
If the problem is not resolved contact a member from the [contacts](#contacts) section.
{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: RETIRED -  This Runbook is for PagerDuty alerts when the PgSQL clusters Prod HaProxy Primary Node is Down.
title: RETIRED -  ONCALL NEED ACTIONS TO CHANGE DNS MAPPING IMMEDIATELY -- PgSQL clusters Prod HaProxy Primary Node is Down
service: N/A
runbook-name: "RETIRED -  PgSQL clusters Prod HaProxy Primary Node is Down"
tags: oss, bluemix, doctor, Postgresql, PgPool, HaProxy
link: /doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Primary_Down.html
type: Alert
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**


{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_pgsql_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

ONCALL NEED ACTIONS TO CHANGE DNS MAPPING IMMEDIATELY --- This alert happens when HaProxy Primary Node **{{osspgproxy1-private-ip}}/{{osspgproxy1-public-ip}}** is down.

## User Impact

This alert indicates that PgSQL clusters will not be able to be connected any more.

## Contacts

Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}


## Details

{% include {{site.target}}/pgsql_servers.md %}

If you got any incidents (includes IP **{{osspgproxy1-private-ip}}**) as below:
- HaProxy Primary node ping failure alerts
- Postgres HAProxy primary Synthetic ping alerts
- Postgres HAProxy primary HealthCheck alerts

Please follow this runbook to deal with the incidents.

## Instructions to Fix

### Step 1 Verify if the HaProxy primary node is down.

- Using you SSO credentials, login to **{{osspgproxy1-private-ip}}** IVM using [{{doctor-portal-name}} look up]({{doctor-portal-link}}/#/ip_lookup).
- Run the following commands.

   ```
curl -i -X GET "http://{{osspgproxy1-private-ip}}:5777/CheckHASystemHealth"

   ```

   If you got return message like this:

   ```
    HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8
    Content-Length: 140
    Server: Werkzeug/0.14.1 Python/2.7.12
    Date: Tue, 30 Oct 2018 01:52:21 GMT

    Tue Oct 30 01:52:21 2018: ********PgSQL Writing is functional********
    Tue Oct 30 01:52:21 2018: ********PgSQL Reading is functional********
   ```

   That means the current HaProxy node is alive and the whole DB cluster is OK.

You can close the incident.

### Step 2 If you get errors on step 1.

Please contact with the focal, inform them about the incident. Reassign the PD incident to the contact and let them know it Please.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}

Inform the focal to change the *DNS IP* mapping:

**How to change the DNS IP mapping:**
1. Login in [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
2. Select **{{oss-account-full-name}}** account.
3. From **Services**.<br>
![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/services/services.png){:width="640px"}
4. Select **CIS-OSS-Prod** instance.
5. From the left side menu select **Reliability**.
6. Then select **DNS**.
7. Search for **pg**.<br>
![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/services/cis/cis_reliability_load_dns.png){:width="640px"}
8. Select the record with **{{osspgproxy2-private-ip}}** under the column *Value* (the living HaProxy node's IP - HaProxy standby node's IP).
9. Click on the three dots and select **Edit**.
10. Enter the new IP address.
11. Click on **Update Record**.

## Notes and Special Considerations

If the problem is not resolved contact a member from the [contacts](#contacts) section.
{% include {{site.target}}/tips_and_techniques.html %}

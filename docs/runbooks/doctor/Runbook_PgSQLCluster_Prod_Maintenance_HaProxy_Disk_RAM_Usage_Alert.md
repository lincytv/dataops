---
layout: default
description: RETIRED -  This Runbook is for PagerDuty alerts when the HaProxy Disk or RAM usage is high.
title: RETIRED -  HaProxy Disk or RAM usage is high.
service: N/A
runbook-name: "RETIRED -  HaProxy Disk or RAM usage is high"
tags: oss, bluemix, doctor, Postgresql, PgPool, HaProxy
link: /doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Disk_RAM_Usage_Alert.html
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

This alert happens when HaProxy Disk or RAM usage is high.

## User Impact

Usually, if the server still is running, there is no impact for using.

## Contacts

Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}


## Details

{% include {{site.target}}/pgsql_servers.md %}

If you got any incidents as below:
- HaProxy Disk or RAM usage is high alert


Please follow this runbook to deal with the incidents.

## Instructions to Fix

### Step 1 Check the PgSQL Cluster Prod status.

Run the following commands.

Check the HaProxy primary node usage:

   ```
curl -i -X GET "http://{{osspgproxy1-private-ip}}:5777/CheckHaProxySystemUsageInfo/<threshold>"

e.g. curl -i -X GET "http://{{osspgproxy1-private-ip}}:5777/CheckHaProxySystemUsageInfo/85"
   ```

Check the HaProxy standby node usage:

   ```
curl -i -X GET "http://{{osspgproxy2-private-ip}}:5777/CheckHaProxySystemUsageInfo/<threshold>"

e.g. curl -i -X GET "http://{{osspgproxy2-private-ip}}:5777/CheckHaProxySystemUsageInfo/85"
   ```

   If you got return message like this:

   ```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 726
Server: Werkzeug/0.14.1 Python/2.7.12
Date: Wed, 31 Oct 2018 08:11:39 GMT
{
  "alertTrigger": 0,
  "boot_time": "2018-10-10 03:20:14",
  "diskiocount.read_count": 1997255,
  "diskiocount.write_count": 969191,
  "diskusage.free": 101807919104,
  "diskusage.percent": 1.9,
  "diskusage.total": 103762382848,
  "diskusage.used": 1937686528,
  "mem.active": 433410048,
  "mem.available": 8095674368,
  "mem.buffers": 121569280,
  "mem.cached": 469954560,
  "mem.free": 7590170624,
  "mem.inactive": 169422848,
  "mem.percent": 3.3,
  "mem.shared": 3510272,
  "mem.total": 8370008064,
  "mem.used": 188313600,
  "memswap.free": 2112741376,
  "memswap.percent": 1.6,
  "memswap.sin": 29147136,
  "memswap.sout": 2150047744,
  "memswap.total": 2146758656,
  "memswap.used": 34017280
}
   ```

    Check the fields "mem.percent", "diskusage.percent" and "alertTrigger", if the values are less than threshold you set up, the "alertTrigger" value would be 0. Please close the incident.

or
    if the values are greater than threshold you set up, the "alertTrigger" value would be 1. Please follow the step 2.

Follow runbook [PgSQLCluster Prod Maintenance PgSQL Disk RAM Usage Alert.]({{site.baseurl}}/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.md)


## Notes and Special Considerations
If the problem is not resolved contact a member from the [contacts](#contacts) section.
{% include {{site.target}}/tips_and_techniques.html %}

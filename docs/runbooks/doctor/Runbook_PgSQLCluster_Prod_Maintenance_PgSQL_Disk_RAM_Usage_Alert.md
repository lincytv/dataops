---
layout: default
description: RETIRED - This Runbook is for PagerDuty alerts when the PgSQL Disk or RAM usage is high.
title: RETIRED - PgSQL Disk or RAM usage is high.
service: N/A
runbook-name: "RETIRED - PgSQL Disk or RAM usage is high"
tags: oss, bluemix, doctor, Postgresql, PgPool, HaProxy
link: /doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html
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

This alert happens when PgSQL Disk or RAM usage is high.

## User Impact

Usually, if the server still is running, there is no impact for using.

## Contacts

Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

* For CDL
    - {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}
    - {% include contact.html slack=cloud-newrelic-monitoring-slack name=cloud-newrelic-monitoring-name userid=cloud-newrelic-monitoring-userid notesid=cloud-newrelic-monitoring-notesid %}
* For NA
    - {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}
    - {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}
    - {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}

## Details

  {% include {{site.target}}/pgsql_servers.md %}

<br><br>
* If you got any incidents containing the following **api-pnp-db-cleaner pgSQL primary/standby IP 1/2 system disk/ram usage**, Please follow this runbook to deal with the incidents.

## Instructions to Fix

### Step 1 Check the PgSQL Cluster Prod status.

* You will get two PD's one for primary IP 1 and one for standby IP2.
* From [{{doctor-portal-name}}]({{doctor-portal-link}}).
* Select **Home** from the left side.
* From the type list box select **SERVICE** or use the search  text box and type **SERVICE**.
* **YP_SERVICE** will be listed.
* Click on **YP_SERVICE**.
* From the **Details** section select **IaaS** tab.
* Use the search text box and type the server IP from the PD.
    - e.g. `Description: api-pnp-db-cleaner pgSQL standby IP 2 system disk/ram usage high.` <br>
    `http://{{osspgproxy2-private-ip}}:5777/CheckPgSQLSystemUsageInfo/pgslave/threshold shows usage is high.` <br>
    Where **{{osspgproxy2-private-ip}}** is the IP address of the proxy server.
* With the IP address from the previous step, use the table [Postgres servers](#postgres-servers), get
  the correspondent *osspgX.bluemix.net* IP address, if the proxy reporter was **{{osspgproxy2-private-ip}}** then it corresponds to **osspgproxy2.bluemix.net** it the postgres server is: **osspg2.bluemix.net** and the IP is: **{{osspg2-private-ip}}**, for this example, this is IP ,**{{osspg2-private-ip}}**, that is going to be use in the following steps.
* Open a SSH session using the **SSH Console**.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/SSH_console.png){:width="640px"}
* Use your SSO account to login.
> If you can't access with your SSO contact a person from the [contacts](#contacts) section.
* Then `sudo -i` to change to root.
* Check the PgSQL primary node usage
    * `curl -i -X GET "http://<IP>:5777/CheckPgSQLSystemUsageInfo/pgmaster/<threshold>"`
        - e.g. `curl -i -X GET "http://{{osspgproxy1-private-ip}}:5777/CheckPgSQLSystemUsageInfo/pgmaster/85"`
* Check the PgSQL standby node usage
    * `curl -i -X GET "http://<IP>:5777/CheckPgSQLSystemUsageInfo/pgslave/<threshold>"`
        - e.g. `curl -i -X GET "http://{{osspgproxy2-private-ip}}:5777/CheckPgSQLSystemUsageInfo/pgslave/85"`

    >Where `<threshold>` is a number such as 85,90... that represents the percentage of usage you would like to check
* For each  curl command you will get an output like the follow:


   ```
      HTTP/1.0 200 OK
      Content-Type: application/json
      Content-Length: 743
      Server: Werkzeug/0.14.1 Python/2.7.12
      Date: Wed, 07 Nov 2018 07:07:20 GMT
      {
        "alertTrigger": 0,
        "boot_time": "2018-10-10 03:34:18",
        "diskiocount.read_count": 855144,
        "diskiocount.write_count": 9916990,
        "diskusage.free": 3235510292480,
        "diskusage.percent": 13.4,
        "diskusage.total": 3934492254208,
        "diskusage.used": 499097636864,
        "mem.active": 38014595072,
        "mem.available": 64663113728,
        "mem.buffers": 172032000,
        "mem.cached": 65429491712,
        "mem.free": 291229696,
        "mem.inactive": 26155794432,
        "mem.percent": 3.7,
        "mem.shared": 718249984,
        "mem.total": 67145539584,
        "mem.used": 1252786176,
        "memswap.free": 1577336832,
        "memswap.percent": 23.0,
        "memswap.sin": 10928128,
        "memswap.sout": 485167104,
        "memswap.total": 2047864832,
        "memswap.used": 470528000
      }
   ```

* For both outputs, check the fields  **mem.percent**, **diskusage.percent** and **alertTrigger**, if their values are less than threshold you use in the curl command, the **alertTrigger** value would be `0`, then close the incident.
* If the values **mem.percent**, **diskusage.percent** are greater than threshold you use in the curl command, the **alertTrigger** value would be `1`. Please follow the step 2.
>**Note:** If at least one of the outputs shows `"alertTrigger": 1` you need to do step 2.

### Step 2 Remove old archives files

>This process will be executed in both {{osspg1-private-ip}} and {{osspg2-private-ip}}

* Connected from the previous step as root.
* `su - postgres`
>Make sure you type the command as shown there are spaces between su , - and postgres
* `cd /opt/postgresql/9.6.10/archive`
* `ls -lt |more`
* Select a filename created in  the last two or three hours, the file name will look like **00000009000007CD0000004E**
* run this command: `pg_archivecleanup -d /opt/postgresql/9.6.10/archive <fileName> >> /tmp/pg_archivecleanup.log 2>&1`
> Replace `<fileName>` with the file name from previous step
* Depending of the number of files to clean it will run for one or two minutes.
* Once completed, older files including the one you selected, should be removed from `/opt/postgresql/9.6.10/archive`
* If the files did not get removed check the log file at /tmp/pg_archivecleanup.log, report any error to one of the [contacts](#contacts)
* if not error try again the curl commands both commands should show now `"alertTrigger": 0`

## Notes and Special Considerations
If the problem is not resolved contact a member from the [contacts](#contacts) section.
{% include {{site.target}}/tips_and_techniques.html %}

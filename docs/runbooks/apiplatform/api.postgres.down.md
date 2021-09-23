---
layout: default
title: "RETIRED - PostgreSQL / HAProxy service down and other issues"
type: Alert
runbook-name: "RETIRED - api.postgres.down"
description: "RETIRED - This alert will be triggered if the PostgreSQL or HAProxy did not work properly."
service: tip-api-platform
tags: apis, postgres, pgsql, haproxy
link: /apiplatform/api.postgres.down.html
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**


{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_api_constants.md%}
{% include {{site.target}}/load_pgsql_constants.md%}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose
Alerts will be triggered if PostgreSQL Primary or Standby nodes, or HAProxy Primary and Standby nodes cannot be pinged, or health check APIs return failure, or these server nodes have high disk or memory usage.
The pinging and health checking of PostgreSQL and HAProxy Primary and Standby nodes are performed in api-pnp-db-cleaner component in us-east. If api-pnp-db-cleaner pod is down in `us-east`, there will be **api-pnp-db-cleaner - no pnp-postgres-ping data,
api-pnp-db-cleaner - no pnp-haproxy-ping data, or api-pnp-db-cleaner down** alert opened for tip-api-platform team.

## Technical Details
PostgreSQL server has auto-failover enabled, and is supported by Technical Foundation Team. High availability is guaranteed from its database layer perspective.
Even if the primary region of PostgreSQL cluster is outage, auto-failover will be auto recovered around 10 seconds without any change required from the client service side.
If you receive any alerts related to PostgreSQL or HAProxy, other than the alerts related to high disk / ram usage, the auto-failover may recover some of the alerts,
however you still have to follow the instructions in one of the runbooks below based on the alerts that you received.

## User Impact
- Users has problem in accessing PostgreSQL database.
- Any service that is rely on PostgreSQL database will be impacted.

## Instructions to Fix
This runbook is for many incidents that are related to PostgreSQL database issues. Please look for the title of the incident in the table below, and follow the instructions in the runbook link.

| Incident Title | Runbook Link |
| -------------- | ------------ |
| api-pnp-db-cleaner ping of primary postgress node failed | [PgSQL Primary Node is down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Primary_Down.html) |
| api-pnp-db-cleaner ping of standby postgress node failed | [PgSQL Standby Node is down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Standby_Down.html) |
| api-pnp-db-cleaner haproxy primary node health check failed | [PgSQL clusters Prod HaProxy Primary Node ({{osspgproxy1-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Primary_Down.html) |
| api-pnp-db-cleaner haproxy primary system health check failed | [PgSQL clusters Prod HaProxy Primary Node ({{osspgproxy1-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Primary_Down.html) |
| api-pnp-db-cleaner ping of primary haproxy port 1 failed | [PgSQL clusters Prod HaProxy Primary Node ({{osspgproxy1-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Primary_Down.html) |
| api-pnp-db-cleaner ping of primary haproxy port 2 failed | [PgSQL clusters Prod HaProxy Primary Node ({{osspgproxy1-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Primary_Down.html) |
| api-pnp-db-cleaner haproxy standby node health check failed | [PgSQL clusters Prod HaProxy Standby Node ({{osspgproxy2-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Standby_Down.html) |
| api-pnp-db-cleaner haproxy standby system health check failed | [PgSQL clusters Prod HaProxy Standby Node ({{osspgproxy2-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Standby_Down.html) |
| api-pnp-db-cleaner ping of standby haproxy port 1 failed | [PgSQL clusters Prod HaProxy Standby Node ({{osspgproxy2-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Standby_Down.html) |
| api-pnp-db-cleaner ping of standby haproxy port 2 failed | [PgSQL clusters Prod HaProxy Standby Node ({{osspgproxy2-private-ip}}) is Down](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Standby_Down.html) |
| api-pnp-db-cleaner haproxy primary node disk/ram usage high | [HaProxy Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner haproxy standby node disk/ram usage high | [HaProxy Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner haproxy primary node get disk/ram usage failed | [HaProxy Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner haproxy standby node get disk/ram usage failed | [HaProxy Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_HaProxy_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL primary IP 1 system disk/ram usage high | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL primary IP 2  system disk/ram usage high | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL standby IP 1 system disk/ram usage high | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL standby IP 2 system disk/ram usage high | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL primary IP 1 get system disk/ram usage failed | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL primary IP 2 get system disk/ram usage failed | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL standby IP 1 get system disk/ram usage failed | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |
| api-pnp-db-cleaner pgSQL standby IP 2 get system disk/ram usage failed | [PgSQL Disk or RAM usage is high](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_PgSQLCluster_Prod_Maintenance_PgSQL_Disk_RAM_Usage_Alert.html) |


## Contacts

**PagerDuty**
* [{{oss-apiplatform-pagerduty-name}}]({{oss-apiplatform-pagerduty-link}})

**Slack**
* [{{oss-slack-api-platform-prd-name}}]({{oss-slack-api-platform-prd-link}})  
* [{{oss-slack-api-platform-stg-name}}]({{oss-slack-api-platform-stg-link}})  
* [{{oss-slack-api-platform-dev-name}}]({{oss-slack-api-platform-dev-link}})  


Please contact with Bluemix Doctor Level 2 who is on call.
And inform who can access to PgSQL clusters Prod environment.

{% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}, {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

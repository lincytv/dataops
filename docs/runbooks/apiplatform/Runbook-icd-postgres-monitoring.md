---
layout: default
title: OSS IBM Cloud Databases for PostgreSQL Monitoring runbook
type: Alert
runbook-name: icd-postgres-monitoring
description: "OSS IBM Cloud Databases for PostgreSQL Monitoring runbook"
service: tip-api-platform
tags: ICD, icd, postgres, postgreSQL, replica, read-only, disk, cpu
link: /apiplatform/Runbook-icd-postgres-monitoring.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Overview

This runbook provides details for resolving ICD PostgreSQL alerts and steps associated with promoting a read-only-replica to a leader in case of an outage. One Primary instance in `us-south` for production environment, one instance for Staging and a read-only-replica in us-east. Get a list of instances from [here]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_Platform_ICD_Postgres.html#postgressql-instances).


PostgreSQL Production and Staging Disk, CPU, Memory and number of connections are currently monitored by Sysdig instance [IBM Cloud Monitoring with Sysdig-EDB-Prod-us-south](https://us-south.monitoring.cloud.ibm.com/#/default-dashboard/ibm_databases_for_postgresql?last=3600). Notification will be sent directly to PagerDuty (Production only) and [{{oss-slack-oss-postgres-sysdig-name}}]({{oss-slack-oss-postgres-sysdig-link}}) slack channel.


**Related alerts:**

- [ICD Postgres Disk at 80% - Prd](#icd-postgres-disk-usage)
- [ICD Postgres Disk at 90% - Prd](#icd-postgres-disk-usage)
- [ICD Postgres Memory at 80% - Prd](#icd-postgres-memory-usage)
- [ICD Postgres Memory at 90% - Prd](#icd-postgres-memory-usage)
- [ICD Postgres CPU usage 90% - Prd](#icd-postgres-cpu-usage)
- [ICD Postgres CPU usage 80% - Prd](#icd-postgres-cpu-usage)
- [ICD Postgres Connection limit at 200 - Prd](#icd-postgres-connection-limit)
- [ICD Postgres Connection limit at 230 - Prd](#icd-postgres-connection-limit)
- [ICD Postgres Disk at 90% - Stg](#icd-postgres-disk-usage)
- [ICD Postgres Memory at 90% - Stg](#icd-postgres-memory-usage)
- [ICD Postgres CPU usage 90% - Stg](#icd-postgres-cpu-usage)
- [ICD Postgres Connection limit at 230 - Stg](#icd-postgres-connection-limit)


## ICD Postgres Disk usage

The current ICD PostgreSQL instance has been provisioned with 5 GB disk space/member and its setup with autoscale by 10% every 15 minutes. The deployment comes with free backup storage equal to the total disk space and does not count towards our usage. With the size of the database being around 4GB, we do not anticipate to see the alert often. You can view the allocated Disk Usage from Resource tab in the instance.

- Check the Disk usage in Sysdig by viewing the `Disk used percent` panel.
   - [Databases for PostgreSQL - Prod Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/449f9c7b-de88-83273-491f-b0be-00359d43f416?last=3600)
   - [Databases for PostgreSQL - Stg Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/63ed297c-862b-83893-4ff7-ab37-a7bc5eaa990b?last=3600)

- If you receive an alert, please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

## ICD Postgres Memory usage

The current ICD PostgreSQL instance has been provisioned with 4GB RAM/member and its setup with autoscale by 10% every 15 minutes, so we do not anticipate to see the alert often. You can view the allocated Disk Usage from Resource tab in the instance.

- Check the Memory usage in Sysdig by viewing the `Memory used percent` panel:
  - [Databases for PostgreSQL - Prod Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/449f9c7b-de88-83273-491f-b0be-00359d43f416?last=3600)
  - [Databases for PostgreSQL - Stg Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/63ed297c-862b-83893-4ff7-ab37-a7bc5eaa990b?last=3600)

- if you receive an alert, please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

## ICD Postgres CPU usage

The current ICD PostgreSQL instance has been provisioned with 3 Dedicated Cores/member, so we do not anticipate to see the alert often. You can view the allocated Disk Usage from Resource tab in the instance.

- Check the CPU usage in Sysdig by viewing the `Avg CPU used` panel:
  - [Databases for PostgreSQL - Prod Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/449f9c7b-de88-83273-491f-b0be-00359d43f416?last=3600)
  - [Databases for PostgreSQL - Stg Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/63ed297c-862b-83893-4ff7-ab37-a7bc5eaa990b?last=3600)

* if you receive an alert, please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

## ICD Postgres Connection limit

At provision, Databases for PostgreSQL sets the maximum number of connections to PostgreSQL database to `115`. `15` connections are reserved for the superuser to maintain the state and integrity of the database, and 100 connections are available for us and the applications. We have adjusted our instances connection limit to `250` to accommodate the needs of our services. You can check the connection limit from the ibmclouddb database using pgAdmin or psql with: `SHOW max_connections;`

If the number of connections to the database exceeds the `250` connection limit, new connections fail and return an error.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/icd_connections_error.jpg){:width="400px"}

**How to resolve**

- Check the number of connections in Sysdig by viewing the `Total connections per member` panel:
  - [Databases for PostgreSQL - Prod Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/449f9c7b-de88-83273-491f-b0be-00359d43f416?last=3600)
  - [Databases for PostgreSQL - Stg Overview](https://us-south.monitoring.cloud.ibm.com/#/shared/dashboard/63ed297c-862b-83893-4ff7-ab37-a7bc5eaa990b?last=3600)


- You may also query `pg_stat_database` from ibmclouddb database using pgAdmin or psql with `SELECT count(distinct(numbackends)) FROM pg_stat_database;`
- Break down the connections by database, `SELECT datname, numbackends FROM pg_stat_database ORDER BY numbackends DESC;`
- Based on the result from above command, list the connection details from the specific database with large number of connections. I.e. `SELECT * FROM pg_stat_activity WHERE datname='pnp_dev';`
- If you find specific connection, you can terminate it using the following instructions:

  - `SELECT pg_cancel_backend(pid);` pg_cancel_backend cancels a connection's current query without terminating the connection, and without stopping any other queries that it might be running.
  - `SELECT pg_terminate_backend(pid);` pg_terminate_backend stops the entire process and closes the connection.

* There is an option to [kill all connections](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-managing-connections#killing-all-connections) from the UI or using psql, however this is **NOT recommended** as it will disrupt anything that is connected to the deployment.

* if you receive an alert, this may mean we have some problems with the services/pods failing to connect to the database and can cause the service not to release the connection. If this occurs, we need to further investigate please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

## Runbook Owners

- {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}
- {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

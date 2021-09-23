---
layout: default
title: How to create and promote an ICD PostgreSQL instance a read-only-replica to a Leader
type: Informational
runbook-name: icd-postgres-promote-read-replica
description: "How to create and promote an ICD PostgreSQL instance a read-only-replica to a Leader"
service: tip-api-platform
tags: ICD, icd, postgres, postgreSQL, replica, read-only
link: /apiplatform/Runbook-icd-promote-postgres-read-replica.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Overview

This runbook provides steps associated with creating and promoting a read-only-replica to a leader in case of an outage. A list of instances are available [here]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_Platform_ICD_Postgres.html#postgressql-instances). For more information on ICD PostgreSQL, please review the following [runbook]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_Platform_ICD_Postgres.html).


## Create a read-only-replica

A read-only replica is set up to replicate all of your data from the leader deployment to the replica deployment using asynchronous replication. As the name implies, read-only replicas support read transactions and can be used to balance databases that have both write-heavy and read-heavy operations. The read-only replica has a single PostgreSQL data member. For more information, visit [IBM Cloud](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-read-only-replicas) documentation.

**From UI**

- Login to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}/) with your W3 ID
- Select `{{oss-account-account}}`
- Select Resources > Services > Click on Databases for PostgreSQL instance
- Select Settings > Create Read-Only Replicas

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/icd_create_replica.jpg){:width="640px"}

- Fill in the information ensuring that you use an identifiable name, select a region that is not in the same region as the Leader instance and click Create

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/icd_create_replica_form.jpg){:width="400px"}

**Cloud Databases CLI**

The [Cloud Databases CLI](https://cloud.ibm.com/docs/databases-cli-plugin?topic=databases-cli-plugin-cdb-reference#install_cli) plug-in offers extra methods of accessing the capabilities of the Cloud Databases services. You can use Cloud Databases CLI to manage and connect to IBM Cloud Databases for PostgreSQL. In order to manage the database, first you must install the plugin with these [instructions] ](https://cloud.ibm.com/docs/databases-cli-plugin?topic=databases-cli-plugin-cdb-reference#installing-the-cloud-databases-cli-plug-in). Provisioning is handled by the [Resource Controller](https://cloud.ibm.com/apidocs/resource-controller/resource-controller)

- Login to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}/) with your W3 ID
- Select Resources > Services > Click on Databases for PostgreSQL instance
- On the Overview page, make a note of the ID. I.e. `crn:v1:bluemix:public:databases-for-postgresql:us-south:a/0bb4d59c58f057ca240dd82f9bc42eb3:a2fb6b53-3b32-4721-bdff-e51cf305a50d::`
- From a local terminal window, run the following command:

```
ibmcloud resource service-instance-create <<name-of-the-replica> databases-for-postgresql standard <<region> -p \ '{ "remote_leader_id": "<<instance-id-from-above>>:",
  "members_memory_allocation_mb": "<<memory-in-mb",
  "members_disk_allocation_mb": "<<disk-in-mb>>"
}'
```

Example:

```
ibmcloud resource service-instance-create OSS_Test_pg_read_only databases-for-postgresql standard us-east -p \ '{
  "remote_leader_id": "crn:v1:bluemix:public:databases-for-postgresql:us-south:a/0bb4d59c58f057ca240dd82f9bc42eb3:a2fb6b53-3b32-4721-bdff-e51cf305a50d::",
  "members_memory_allocation_mb": "8192",
  "members_disk_allocation_mb": "131072"
}'
```

- The minimum size of a read-only replica is 2 GB RAM and 10 GB of disk.


## Promote a read-only-replica to a Leader

A [PostgreSQL](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-high-availability) instance is created with a `Leader` and a `Replica`. Both members contain a copy of your data by using asynchronous replication, with a distributed consensus mechanism to maintain cluster state and handle failovers. The failover is automatic between the `Leader` and `Replica` and once the leader is back online, it takes over again. We have extended the high-availability to more regions using Two [read-only replicas](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-read-only-replicas) in the `us-east` and `eu-de`.

If something happens to the leader deployment or there's an outage in the region it's deployed in, a read-only replica can be promoted to a stand-alone cluster and start accepting writes from your application. Once a read-only replica is promoted to a leader, it cannot be de-promoted and it becomes the main instance.

**From UI**

- Login to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}/) with your W3 ID
- Select `{{oss-account-account}}`
- Select Resources > Services > Click on Databases for PostgreSQL instance
- Select Settings > Read-Only Replicas> Select gear icon (Manage Instance) next the replica name

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/icd_read_replica.jpg){:width="400px"}

- Once the Read-Only Replicas loads, Select Settings > Read-Only Replicas > Promote Read-Only Replica button

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/icd_promote_read_replica.jpg){:width="400px"}

**Cloud Databases CLI**

- To promote a read-only-replica using the CLI, ensure you have the plugin installed with these [instructions] ](https://cloud.ibm.com/docs/databases-cli-plugin?topic=databases-cli-plugin-cdb-reference#installing-the-cloud-databases-cli-plug-in)

- On the Overview page of the replica, make a note of the ID.
  I.e. `crn:v1:bluemix:public:databases-for-postgresql:us-south:a/0bb4d59c58f057ca240dd82f9bc42eb3:a2fb6b53-3b32-4721-bdff-e51cf305a50d::`
- From a local terminal window, run the following command:

`ibmcloud cdb read-replica-promote "<<replica-id>>" --skip-initial-backup`

Example

```
ibmcloud cdb read-replica-promote "crn:v1:bluemix:public:databases-for-postgresql:us-east:a/0bb4d59c58f057ca240dd82f9bc42eb3:1f96e563-2fcd-4906-933f-7f3044161029::" --skip-initial-backup
```

Using the `--skip-initial-backup` will allow for the task to be completed faster as we do not need an immediate back since the read-only-replica already sync'ed to the leader

## Runbook Owners

- {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}
- {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

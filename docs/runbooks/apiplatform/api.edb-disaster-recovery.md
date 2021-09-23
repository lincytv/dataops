---
layout: default
title: "EDB Disaster Recovery"
type: Informational
runbook-name: "api.edb-disaster-recovery"
description: "Steps to perform for disaster recovery or db failures"
service: tip-api-platform
tags: api-edb-disaster-recovery
link: /apiplatform/api.edb-disaster-recovery.html
---

## Purpose
Follow this runbook to recover EDB from a disaster or database failures.

## Technical details

High availability is supported for multi zone.  
- [Redis high availability](https://cloud.ibm.com/docs/services/databases-for-redis?topic=databases-for-redis-high-availability#high-availability)
- [MongoDB high availability](https://cloud.ibm.com/docs/databases-for-mongodb?topic=databases-for-mongodb-high-availability)

The Redis and MongoDB databases used by EDB are in a single multi zone region.  If there is a full outage or database failures in that region, we need to restore a backup to another region, update the secrets that hold the database connection and redeploy the affected charts.

## Restore MongoDB instance

As of the latest update of this document, the active production and staging MongoDB instances are provisioned in us-south region.  In case of failures in us-south we will use a restored instance in the us-east region.

There are Jenkins jobs that run at midnight UTC which back up the MongoDB production and staging instances in the active region and restores them into backup instances on the backup region.

Steps:

1. Rename the existing backup instance from `edb-mongodb-backup-prod` to `Databases for MongoDB-EDB Production-<region>` or from `edb-mongodb-backup-staging` to `Databases for MongoDB-EDB Staging-<region>` depending on the affected environment.
If the backup instance does not exist, is corrupt or otherwise unusable, provision a new MongoDB instance in the backup region named `Databases for MongoDB-EDB Staging-<region>` or `Databases for MongoDB-EDB Production-<region>` from the latest backup available in the active region for the affected environment (staging or production). See [restoring-a-backup](https://cloud.ibm.com/docs/databases-for-mongodb?topic=cloud-databases-dashboard-backups#restoring-a-backup).
2. Go to the Settings for the renamed instance and generate a password for the admin account and capture it as it will be needed for updating the secret in vault.
3. Capture the `Public mongodb endpoint` from the Overview tab which will be used to update the secret in vault.
4. Update Jenkins jobs listed below so that the default parameter values match the new active/backup region and dbnames.
  - [BackupRestoreEDBMongoDBProduction](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/BackupRestoreEDBMongoDBProduction/configure)
  - [BackupRestoreEDBMongoDBStaging](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/BackupRestoreEDBMongoDBStaging/configure)

## Restore Redis instance

As of the latest update of this document, the active production and staging Redis instances are provisioned in us-south region.  In case of failures in us-south we will restore an instance in the us-east region.

There are Jenkins jobs that run periodically (hourly on production and every 6 hours on staging) which back up the Redis production and staging instance running in the active region.

Steps:

1. Provision a new Redis instance in the backup region named `Databases for Redis-EDB Staging-<region>` or `Databases for Redis-EDB Production-<region>` from the latest backup available in the active region for the affected environment (staging or production).  See [restoring-a-backup](https://cloud.ibm.com/docs/databases-for-redis?topic=cloud-databases-dashboard-backups#restoring-a-backup).
2. Go to the Settings for the new instance and generate a password for the admin account and capture it as it will be needed for updating the secret in vault.
3. Capture the `Public rediss endpoint` from the Overview tab which will be used to update the secret in vault.
4. Update Jenkins jobs listed below so that the default parameter values match the new active region and dbnames.
  - [BackupEDBRedisProduction](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/BackupEDBRedisProduction/configure)
  - [BackupEDBRedisStaging](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/BackupEDBRedisStaging/configure)


## Update secrets in vault

Update any of the affected secrets listed below using vault:

```
vault write <vault path> 'value=<new value>' 'about=<some information such as update time, updated by>'
```

Staging
- /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/edb/mongodb/ussouth.key
- /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/edb/redis/ussouth.key

Production
- /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/edb/mongodb/ussouth.key
- /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/edb/redis/ussouth.key

## Redeploy charts

The following list of charts should be redeployed to the affected environment(s) after the vault secrets have been updated.

- api-edb-adapter-metrics
- api-edb-adapter-metrics-backup
- api-edb-processing-status
- api-edb-adapter-tip
- api-edb-adapter-metrics-sysdig
- api-edb-adapter-sysdig

- api-edb-cleanup
- api-edb-mapping-api
- api-edb-subscription-api
- api-issuetracker
- api-issuecreator-backend
- api-edb-audit
- api-edb-adapter-actiontracker
- api-edb-adapter-cie
- api-edb-hooks
- api-edb-cie-api
- api-edb-hooks-consumer

Run Jenkins [DeployCharts](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/EDB/job/DeployCharts/build?delay=0sec) job for each region and environment as required by updating the default parameter values as required.

### Warning!!
Other potentially affected applications regarding MongoDB secrets and chart redeployment we need to consider:
- ciebot
- issue creator/tracker
- certificate manager

## Validate

Check the logs to see if there are any errors and that transactions are flowing nicely.

{% include_relative _{{site.target}}-includes/edb-logdna.md %}

{% include_relative _{{site.target}}-includes/edb-ingestor-redirect.md %}

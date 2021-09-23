---
layout: default
title: "API Platform - EDB Cloudant has errors"
type: Alert
runbook-name: "api.edb-cloudant.down"
description: "Addresses issues with Cloudant as it pertains to EDB components."
service: tip-api-platform
tags: edb, cloudant
link: /apiplatform/api.edb-cloudant.down.html   
---

## Instructions to Fix

### Test connection to Cloudant
The first thing to check is if there is an issue with Cloudant.

1. Check the status of affected Cloudant instance by logging into the dashboard URL. See this [runbook]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/Cloudant_for_OSS.html) for details.
2. Check logs in [LogDNA](https://app.us-south.logging.cloud.ibm.com/ext/ibm-sso/f544afde9f) for any errors.
3. EDB data is stored in several databases. For your reference, here is the DB to service mapping:

| Database                 | EDB Service                |
|--------------------------|----------------------------|
| edb-audit                | edb-audit                  |
| edb-daily-metrics        | edb-adapter-metrics-backup |
| edb-rolling-metrics      | edb-adapter-metrics-backup |
| edbmaps                  | edb-mapping-api            |
| action_record            | edb-adapter-actiontracker  |
| edbcies                  | edb-cie-api                |
| edbsubscriptionresources | edb-subscription-api       |
| edbsubscriptions         | edb-subscription-api       |

## Notes and Special Considerations

### Opening an issue with the Cloudant team
A support ticket/case should be opened in IBM Cloud for the specific Cloudant instance.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

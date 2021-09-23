---
layout: default
title: "API Platform - EDB MongoDB has errors"
type: Alert
runbook-name: "api.edb-mongodb.down"
description: "Addresses issues with MongoDB as it pertains to EDB components."
service: tip-api-platform
tags: edb, mongodb
link: /apiplatform/api.edb-mongodb.down.html   
---

## Instructions to Fix

### Test connection to MongoDB
The first thing to check is if there is an issue with MongoDB.

1. Get a MongoDB client. For GUI based, recommendation is [MongoDB Compass](https://www.mongodb.com/products/compass).
2. Get MongoDB credentials from PIM.
    - Dev: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43287/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43287/general)
    - Staging: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43289/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43289/general)
    - Production: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43288/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43288/general)
3. Login to MongoDB. If you are using MongoDB Compass, copy just the first URL (starting from `mongodb://` and end at the port number), open MongoDB Compass and it should recognize that you have a MongoDB URL in the clipboard.

    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/edb_mongodb_compass_detect.png){:width="640px"}

    Click `Yes` and make sure the settings look similar to the screenshot below:

    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/edb_mongodb_compass_settings.png){:width="640px"}
    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/edb_mongodb_compass_settings_more.png){:width="640px"}
   
   To get certificate, copy the value of the certificate (begins with `-----BEGIN CERTIFICATE-----` and end with `-----END CERTIFICATE-----` and which can be found in the Notes section of PIM Console) into a file on your machine.
   Browse for this file and select it for `Certificate Authority` field in MongoDB Compass.
4. Check logs in [LogDNA](https://app.us-south.logging.cloud.ibm.com/ext/ibm-sso/f544afde9f) for any errors.
5. EDB data is stored in database `edb`. At time of writing, for your reference, here is the DB collections mapping:

| Collection        | EDB Component              |
| ----------------- | -------------------------- |
| audit             | edb-audit                  |
| edbDailyMetrics   | edb-adapter-metrics-backup |
| edbRollingMetrics | edb-adapter-metrics        |
| edbmaps           | edb-mapping-api            |

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/edb_mongodb_compass_collections.png){:width="640px"}

## Notes and Special Considerations

### Opening an issue with the ICD team
A ticket should be opened in IBM Cloud for the specific ICD MongoDB instance.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

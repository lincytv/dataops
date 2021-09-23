---
layout: default
title: "API Platform - EDB Redis has errors"
type: Alert
runbook-name: "api.edb-redis.down"
description: "Addresses issues with Redis as it pertains to EDB components."
service: tip-api-platform
tags: edb, redis
link: /apiplatform/api.edb-redis.down.html   
---

## Instructions to Fix

### Test connection to Redis
The first thing to check is if there is an issue with Redis.

1. Get [Redli](https://github.com/IBM-Cloud/redli) from [https://github.com/IBM-Cloud/redli/releases](https://github.com/IBM-Cloud/redli/releases)
2. Get Redis credentials from PIM. 
  - Dev: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43284/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43284/general)
  - Staging: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43286/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43286/general)
  - Prod: [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43285/general](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43285/general)
3. Login to Redis via Redli: `./redli -u <VALUE FROM PREVIOUS STEP>`
4. If successful, you should see something like `Connected to 4.0.10`
5. A sample command you can execute is `info keyspace` to see how many keys are currently stored in each DB. At time of writing, for your reference, here is the DB mapping:

| DB Number | EDB Component                                   |
| --------- | ----------------------------------------------- |
| 1         | edb-adapter-tip                                 |
| 2         | edb-adapter-metrics, edb-adapter-metrics-backup |
| 3         | edb-processing-status                           |
| 4 		    | edb-adapter-sysdig-ausyd 						            |
| 5			    | edb-adapter-sysdig-eude						              |
| 6 		    | edb-adapter-sysdig-eugb 						            |
| 7 		    | edb-adapter-sysdig-useast 					            |
| 8 		    | edb-adapter-sysdig-ussouth 					            |
| 9			    | edb-adapter-sysdig-default 					            |


## Notes and Special Considerations

### Opening an issue with the Compose team
A ticket should be opened in IBM Cloud for the specific ICD Redis instance.

## Contacts

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

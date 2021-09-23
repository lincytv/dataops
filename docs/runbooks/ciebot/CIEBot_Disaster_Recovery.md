---
layout: default
title: CIEBot Disaster Recovery Runbook
type: Informational
runbook-name: CIEBot Disaster Recovery Runbook
description: "Steps to perform for disaster recovery or db failures"
service: ciebot
tags: ciebot-disaster-recovery
link: /ciebot/CIEBot_Disaster_Recovery.html
---

## Purpose
Follow this runbook to recover CIEBot from a disaster or database failures.

## Technical details

CIEBot production bot `ciebot` is deployed in 3 regions: us-east, us-south and eu-de; HA is setup via CIS with a global interface. When one of region is down, all request will switch to another region automatically, no manual action is required.  
- [CIEBot regional deployment diagram](https://github.ibm.com/cloud-sre/oss-platform-architecture/blob/master/topology/images/CIEBOT_Regional_Container.png)

The Cloudant databases used by CIEBot production are in a single multi zone region(us-south).  If there is a full outage or database failures in that region, we need to restore a backup to another region, update the secrets that hold the database connection and redeploy the affected charts.

CIEBot staging bot `cietest` is not deployed in multi region(us-east only), but `cietest1` is HA enabled. Only when us-east is down, we need to follow below steps to restore Cloudant DB for `cietest1` and notify `cietest` user to use `cietest1` temporally.

## Restore Cloudant instance

CIEBot shares database instances with EDB. Refer to [EDB disaster recovery runbook ](../piplatform/api.edb-disaster-recovery.md) for actions to take when a Cloudant database is down.

## Update secrets in vault

Update any of the affected secrets listed below using vault:

```
vault write <vault path> 'value=<new value>' 'about=<some information such as update time, updated by>'
```

Staging
- /generic/crn/v1/staging/local/tip-oss-flow/global/apiplatform/edb/cloudant_url_standard
- /generic/crn/v1/staging/local/tip-oss-flow/global/apiplatform/edb/cloudant_apikey_standard

Production
- /generic/crn/v1/internal/local/tip-oss-flow/global/apiplatform/edb/cloudant_url_standard
- /generic/crn/v1/internal/local/tip-oss-flow/global/apiplatform/edb/cloudant_apikey_standard

## Redeploy charts

The following list of charts should be redeployed to the affected environment(s) after the vault secrets have been updated.

oss-chart git repo : https://github.ibm.com/cloud-sre/oss-charts

Staging: 
- For bot `cietest` :
   - ciebot-bots-handler
   - ciebot-bots-slack-consumer
   - ciebot-bots-incoming-webhook
   - ciebot-bots-miscellaneous-commands-processor

- For bot `cietest1` :
   - ciebot-cietest1-handler
   - ciebot-cietest1-slack-consumer
   - ciebot-cietest1-incoming-webhook
   - ciebot-cietest1-miscellaneous-commands-processor

Production: 
- For bot `ciebot`
    - ciebot-ciebot-handler
    - ciebot-ciebot-slack-consumer
    - ciebot-ciebot-incoming-webhook
    - ciebot-ciebot-miscellaneous-commands-processor

Steps: 
1. Update the value of version in Chart.yaml in oss-chart for above charts,
2. Commit the change to github
3. Create PR, waiting for build succeed in development, then merge the change to staging


## Validate

Check the logs to see if there are any errors and that transactions are flowing nicely.
Verify ciebot in slack if it's responding for any command 

## Reference
[Configuring IBM Cloudant for cross-region disaster recovery](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-configuring-ibm-cloudant-for-cross-region-disaster-recovery)

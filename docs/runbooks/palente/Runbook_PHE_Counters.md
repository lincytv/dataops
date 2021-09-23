---
layout: default
description: PHE Counters
title: PHE Counters
service: palente
runbook-name: PHE Counters
tags: oss, palente
link: /palente/Runbook_PHE_Counters.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}


## Purpose
PHE use counters to determine if pCIE creation/updating process is working well.

## Technical Details
PHE has 2 counters, one is `rawCounter` which count total number of pCIEs being created or updated in the past one hour, this includes PHE heartbeat pCIEs. Another one is `realCounter` which only count total number of pCIEs being created or updated for IBM Cloud Services.

### Heartbeat pCIEs
PHE randomly generate test data points for test CIs (`palante-test-1`, `palante-test-2`,`palante-test-2`) every 15 mins. The data points may trigger pCIE being created/updated. These pCIEs are used as PHE heartbeat check. We expect at least 1 pCIE is being created or updated every one hour. This means `rawCounter` must be >= 1 every hour.

### IBM Cloud Services pCIEs
Based on our statistics, PHE may create or update 3-10 pCIEs within a day. We haven't set `realCounter` alert yet, we will collect more data to determine the proper alert count.

## User Impact
If `rawCounter` is less than 1 per hour, there maybe something wrong in the process of creating/updating pCIEs. It may affect PHE to create/update pCIE to real IBM Cloud services.

## Instructions to Fix
1. Heartbeat pCIE is driven by test data point. We need to make sure generating test data point is turned on. Currently only us-east production is enabled test data. Go to logDNA, select PALANTE->OSS-CSD(Palante), filter `us-east_OSSProd`, search `Random test mode `, you should see log shows `Random test mode enabled` with other settings like below
```
    Dec 3 13:09:43 api-oss-csd-76b7867c97-pn5t8 api-oss-csd 18:09:43 WRN Random test mode enabled clear_percent=50 create_percent=5 num_locations=16 refresh_interval=1m0s save_to_elk=true 
```

If log shows `Random test mode disabled`, go to oss-charts/api-oss-csd, open useast-production-values.yaml, check if any of the variables `randomtest_*` is set to `-1`
    - If there is `-1`, change variable settings as below and redeploy us-east production pod
    ```
    randomtest_refresh_interval: 15m
    randomtest_create_percent: 5
    randomtest_clear_percent: 50
    randomtest_num_locations: 16
    randomtest_save_to_elk: false
    ```

After redeployed, check logDNA to see if log shows `Random test mode enabled`, if not, please contact PHE team. If test data is enabled, snooze the alert to see if problem can be resolved.

2. If variables are all ok in previous step, search `Finished refresh of report` in logDNA us-east_OSSProd, within past 1 hour, there should be at least one row of log has `num_OrangeOrYellow`>0 and `num_heartbeat`>0. If not, pls contact PHE team

```
Dec 3 13:20:42 api-oss-csd-76b7867c97-pn5t8 api-oss-csd 18:20:42 INF Finished refresh of report [us-east] created_CIEs=[] num_OrangeOrYellow=2 num_Processed_OrangeOrYellow=2 num_heartbeat=2 num_rows=135 num_skipped=0 updated_CIEs=["INCxxx","INCxxxx"]

```

3. If you do find log with `num_OrangeOrYellow` and `num_heartbeat` > 0, expand the log row, click on `view in context` to see logs before it. If you see any error log related to POST or PATCH `https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns`, please report PHE team with the error or contact TIP team for help.

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

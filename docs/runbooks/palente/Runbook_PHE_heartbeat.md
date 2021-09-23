---
layout: default
description: PHE heartbeat
title: PHE heartbeat
service: palente
runbook-name: PHE heartbeat
tags: oss, palente, phe
link: /palente/Runbook_PHE_heartbeat.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
To make sure PHE create/update pCIE work flow is working properly.

## Technical Details
PHE has 3 test CIs: *palante-test-1*, *palante-test-2* and *palante-test-3*. In production environment, the pCIEs created by PHE for these test CIs are `heartbeat pCIEs`. PHE generates random test metrics to trigger `create or update pCIE` condition every hour, and add a `PHE work note` to the heartbeat pCIEs, or if a test CI's heartbeat pCIE is resolved, a new heartbeat pCIE will be opened. The heartbeat pCIE is resolved after being opened for a week, a new one should be open after previous one being resolved for an hour.

## User Impact
A missing heartbeat could indicate something wrong in PHE work flow and may affect a real pCIE being opened or updated.

## Instructions to Fix

1. Manually check heartbeat pCIEs on [ServiceNow](https://watson.service-now.com/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_query%3Dcmdb_ciSTARTSWITHpalante-test-%5Eu_status%3D20%5EORDERBYDESCsys_updated_on%26sysparm_first_row%3D1%26sysparm_view%3D) If the latest updated time in pCIEs listed is within an hour, this may be a false alarm.

2. If the latest update on heartbeat pCIEs is over an hour
  - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
  - Select the **PALANTE**, then **OSS-CSD(Palante)**
  - Search for `Finished refresh of report`, you should see logs like
  >
     Nov 26 12:35:14 api-oss-csd-56ccb677cc-vhb4n api-oss-csd 17:35:14 INF Finished refresh of report [us-east] created_CIEs=[] num_OrangeOrYellow=1 num_Processed_OrangeOrYellow=1 num_heartbeat=1 num_rows=158 num_skipped=0 updated_CIEs=[INC2823328]

   - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/finished_report_refresh.png){:width="600px"}
   - In the past one hour, there should be at least one of this log contains none 0 `num_heartbeat`. If can't find a log shows `num_heartbeat` more than 0, there maybe something wrong with randomly generated test metrics. Follow the contact details to contact [Pa'lente team](#palente-contact-information).

3. If the log shows `num_heartbeat` more than 0, this means PHE does generated test metrics.
   * Check if `num_Processed_OrangeOrYellow` and `num_skipped` are not 0 (you may filter LogDNA to `us-east` as this is primary region)
      - If they are not 0 and `num_skipped` equals to `num_Processed_OrangeOrYellow`, this means PHE processed test metrics and found a resolved pCIE.
   * Check in step 1 if we have a recently resolved heartbeat pCIE (within 1 hour)
      - If yes, wait for a longer time to see if a new pCIE is created. (This should be very rare, because we still send heartbeat when find an inactive pCIE)

4. If `num_heartbeat` and `num_Processed_OrangeOrYellow` are not 0, and `num_skipped` is 0, this means PHE did try to process heartbeat metrics, but didn't update or create any pCIE. Please contact [Pa'lente team](#palente-contact-information).

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

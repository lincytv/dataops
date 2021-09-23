---
layout: default
description: PHE Healthz
title: PHE Healthz
service: palente
runbook-name: PHE Healthz
tags: oss, palente, phe
link: /palente/Runbook_PHE_Healthz.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
Use to check the health of the pa'lente service

## Technical Details
PHE runs cycles about a minute each to produce a *report* that contains a bunch of *Rows*, one for each service and each location, with a *status* that reflects the best assessment from the Summarizers over whether there is an issue or not (Red/Orange/Yellow/LogOnly/Suspicious/Green).

At the end of each cycle a New Relic transition is created. The expectation is at least to see six cycles/transactions completed at each region every ten minutes. If the number of cycles/transactions is lower than six, then New Relic will trigger an alert.


## User Impact

PHE service might be down and it will affect the auto-generation of pCIE

## Instructions to Fix


1. Get the region and environment from the alert inside the details like the follow:
    ```
    Description: Violated New Relic condition: oss_csd_healthz_summarizers. Description:
    PHE Healthz did not meet the number of cycles in the expected period of time, it might be problem with the PHE service

    Region: us-east
    Environment: prod
    ```

2. Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
  - Select the **PALANTE**, then **OSS-CSD(Palante)**
  - Filter out the region
  - Search for `Finished refresh of report`
  - If you see logs like below consistently generated every minute or so, PHE is still running normally, snooze the alert, it should be resolved soon something like the follow:
  - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/finished_report_refresh.png){:width="600px"}
  - If you don't see `Finished refresh of report` log in recent 5 minutes
    - Search for latest `Sidecar available`, and check the following logs to see if pod is restarting.
    - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/sidecar.png){:width="600px"}
    - PHE usually takes 15 mins to load all TIP related data
    > Sometimes if there is high volume of incidents in the past 3 days, the time could be longer.
      If you don't see any error in the following logs and new logs are keep generating,
      snooze the alert for an hour to wait for pod to be fully started.
  - If the alert is not resolved within 1 hour, Please contact [Pa'lente team](#palente-contact-information).

3. Re-start the api-oss-csd pod using the kdep [How to restart Pa'lente Service]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

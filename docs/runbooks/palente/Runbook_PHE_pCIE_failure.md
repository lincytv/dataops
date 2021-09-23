---
layout: default
description: Describe the steps to follow when PHE failed to create a pCIE
title: pCIE failure alert
service: palente
runbook-name: pCIE failure alert
tags: oss, palente, phe
link: /palente/Runbook_PHE_pCIE_failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
To make sure PHE creating/updating pCIE work flow is working properly.

## Technical Details
PHE calls TIP incident management API to create/update (POST/PATCH) CIE in ServiceNow. This alert is triggered when incident management API returns error.

## User Impact
An error during creating or updating a CIE might affect PHE reporting protencial issue happen in a service.

## Instructions to Fix

1. Check [pCIEs errors Dashboard](https://one.newrelic.com/launcher/dashboards.launcher?pane=eyJuZXJkbGV0SWQiOiJkYXNoYm9hcmRzLmRhc2hib2FyZCIsImVudGl0eUlkIjoiTVRreU5qZzVOM3hXU1ZwOFJFRlRTRUpQUVZKRWZHUmhPamcyT0RFNCIsInVzZURlZmF1bHRUaW1lUmFuZ2UiOmZhbHNlLCJpc1RlbXBsYXRlRW1wdHkiOmZhbHNlLCJzZWxlY3RlZFBhZ2UiOiJNVGt5TmpnNU4zeFdTVnA4UkVGVFNFSlBRVkpFZkRFMU56RXhOREkiLCJlZGl0TW9kZSI6dHJ1ZSwiaXNTYXZpbmdFZGl0Q2hhbmdlcyI6ZmFsc2V9&platform[accountId]=1926897&platform[$isFallbackTimeRange]=false), check the error(s) message(s), if you see several errors in a short period of time.  
  - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
  - Select the **PALANTE**, then **OSS-CSD(Palante)**
  - If the alert is `oss_csd_pcie_failed_prd`, search for `payload`, 
   - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/pcieCreateUpdateError.png){:width="600px"}
  
  - Otherwise search for `A key word` from any New Relic recorded errors during the time of the alert.
   - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/finished_report_refresh.png){:width="600px"}
   - If you see a lot of 500 or 429 [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services) pod.
   - If the error continues after restarting contact [Pa'lente team](#palente-contact-information).
2. If you see a single error and the alert does not get auto resolved, manually resolve it.
  - Open the URL of the alert provided in [{{doctor-alert-system-name}}]({{doctor-alert-system-link}})
  - ![]({{site.baseurl}}/docs/runbooks/palente/images/pd/newrelic_alert_id.png){:width="600px"}
  - It will direct you to the NewRelic alert, from there, manually close the alert.
  - ![]({{site.baseurl}}/docs/runbooks/palente/images/newrelic/manually_close_alert.png){:width="600px"}
  > At this time this alert needs to be manually resolved, we are working to resolved this issue


## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

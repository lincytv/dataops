---
layout: default
description: PHE MongoDB Awareness
title: PHE MongoDB Awareness
service: palente
runbook-name: PHE MongoDB Awareness
tags: oss, palente, mongoDB
link: /palente/Runbook_PHE_MongoDB_Awareness.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
PHE connect to MongoDB for collecting EDB metrics and configuration rules. This alert make sure the connection from PHE to MongoDB is healthy.

## Technical Details
PHE connects to 2 MongoDB collections:

  - `edb` for collecting EDB metrics
  - `csd` for collecting configuration rules

Before collecting data from tables, PHE ping DB to check connection. If ping failed, it will try to recreate the connection and ping again. Alert will be triggered by three consecutive failures.

>Note: You can see the healthz of the database at [Pa'lente Dashboard](https://one.newrelic.com/launcher/dashboards.launcher?pane=eyJuZXJkbGV0SWQiOiJkYXNoYm9hcmRzLmRhc2hib2FyZCIsImVudGl0eUlkIjoiTVRreU5qZzVOM3hXU1ZwOFJFRlRTRUpQUVZKRWZHUmhPamcyT0RFNCIsInVzZURlZmF1bHRUaW1lUmFuZ2UiOmZhbHNlLCJpc1RlbXBsYXRlRW1wdHkiOmZhbHNlLCJlZGl0TW9kZSI6ZmFsc2UsImlzU2F2aW5nRWRpdENoYW5nZXMiOmZhbHNlLCJzZWxlY3RlZFBhZ2UiOiJNVGt5TmpnNU4zeFdTVnA4UkVGVFNFSlBRVkpFZkRFMU5qTTVPRGMifQ==&platform[accountId]=1926897&platform[$isFallbackTimeRange]=false)

## User Impact
If failure happens to `edb`, PHE will not be able to collect EDB rolling metrics.
If failure happens to `csd`, PHE will not be able to load latest configuration rules. However, unless there is a recent rule change, otherwise, PHE should still be able to function with cached rules.

## Instructions to Fix
1. If there are other `MongoDB` related alerts at the same time, the problem may be caused by MongoDB issue, we can snooze the alert and monitor for a longer time.
2. [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
- Select the **PALANTE**, then **OSS-CSD(Palante)**
- Search for `ping DB client`.
  - if the error log is mixed with `Ping DB client passed`, it could be a network glitch, we can snooze the alert and monitor for 5 - 10 minutes.
  - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/DBping.png){:width="600px"}
3. If `MongoDB: Failed to ping DB client` continuously show up in the log for more than 5 minutes, [try to restart the pod]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services) with the error in that region.

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
Include the contacts for escalation when applicable.

{% include {{site.target}}/palente_tips.html %}

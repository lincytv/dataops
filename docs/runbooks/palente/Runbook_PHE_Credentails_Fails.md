---
layout: default
description: Describe the steps to follow when the credentials to connect to TIP IM API failed preventing PHE to connect and create a pCIE
title:  PHE Credentials failed
service: palente
runbook-name: PHE Credentials failed
tags: oss, palente, tip
link: /palente/Runbook_PHE_Credentials_Fails.html
type: Information
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}


## Purpose
This alert is triggered when the Palante Heuristics Engine (PHE) has failed to refresh get **tip-yp** key value from the environment variables. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
The PHE calls the Elastic ingestor on a regular interval and supports retrying the call to the Elastic ingestor 5 times. If, after 5 retries, the Elastic ingestor still returns an error this alert is fired. The Elastic ingestor itself makes calls to the _TIP Elasticsearch_ instance running in the same cluster to get _TIP_ alert data. Based on this data, the Elastic ingestor creates data points and calls the Palante hybrid store to store the data points both within an in-memory data store and in the _TIP Elasticsearch_ instance running in the same cluster (just under a different _Elasticsearch_ index).

## User Impact
More than 5 failed refreshes may indicate an underlying issue in the PHE or perhaps with the _TIP Elasticsearch_ instance running in the same cluster. Consequently, the PHE will be unable to open or update a real pCIE.

## Instructions to Fix
1. Step by step instructions for fixing the problem.
2. If applicable include the following:
    - How to restore the service to normal operations from an end-user perspective.
    - How to do root cause analysis.
    - How to repair the service to a normal configuration, if needed.
3. Conclude with the expected outcome of the instructions.

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
Include the contacts for escalation when applicable.

{% include {{site.target}}/palente_tips.html %}

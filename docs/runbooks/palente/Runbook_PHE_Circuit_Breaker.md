---
layout: default
description: PHE Circuit Breaker
title: PHE Circuit Breaker
service: palente
runbook-name: PHE Circuit Breaker
tags: oss, palente, tip
link: /palente/Runbook_PHE_Circuit_Breaker.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}


## Purpose
PHE is continuously monitoring and reporting heath status of a service. For services in **allowlist**, PHE will create/update pCIE if confidence value in primary summarizer metric is over 50. For any PHE created pCIE, AVM will manually handle it first. To prevent flooding the IMAPI, ServiceNow, and ultimately the AVM team with a large number of pCIEs in a short period of time, PHE set max of 3 pCIEs it can create within an hour as a circuit breaker.

## Technical Details
PHE keeps track of the latest 3 pCIEs it created in a first in first out stack. Before creating a pCIE, PHE checks timestamp of the first pCIE in the stack to see if it is over an hour. If it is created one hour ago, PHE will continue to create the new pCIE, remove the first one from the stack, and put the newly created one in. If the first one is created less than an hour ago, PHE will send circuit break alert and log the pCIE to slack channel instead of creating in ServiceNow.

## User Impact
Services in **allowlist** may not have pCIE created.

## Instructions to Fix

1. First check slack channel [{{slack-palante-pcie-automation-name}}]({{slack-palante-pcie-automation-link}}) to make sure a pCIE with similar timestamp is logged.

2. Inform AVM team Slack([{{slack-toc-avm-name}}]({{slack-toc-avm-link}})) that because of circuit break alert, there will be pCIE for **allowlisted** service being logged instead of created.

3. Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
  - Select the **PALANTE**, then **OSS-CSD(Palante)**
  - Filter out the region
  - Search for `reached pCIE creation upper limit`
  - Will see an error like the follow:
  > Dec 12 12:39:17 api-oss-csd-7d665d5b5b-4zkkr api-oss-csd 17:39:17 ERR reached pCIE creation upper limit: maximum [3] pCIEs within an hour, a pCIE for service [devopsinsights] is logged at slack channel

4. Go to ServiceNow to check [latest pCIEs created by PHE](https://watson.service-now.com/nav_to.do?uri=%2Fincident_list.do%3Fsysparm_query%3Du_detection_source%3DMonitoring%20Tool%5Eu_monitoring_situation%3DCreated%20by%20PHE%26sysparm_first_row%3D1%26sysparm_view%3D)
  - If the 3rd latest pCIE is NOT created within 1 hour, this could be a false alarm and there may be something wrong with PHE cache list, please contact [Pa'lente team](#palente-contact-information).
  - If it is created within 1 hour, check each pCIE's `Opened` timestamp.
    - If the pCIEs are created reasonably in the past one hour, monitor the situation for 30 mins.
    - If the alert is not resolved within 1 hour, or receive more alerts, please contact [Pa'lente team](#palente-contact-information).

> Note: If multiple pCIEs are created within short time period, contact [Pa'lente team](#palente-contact-information).

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

---
layout: default
description: PHE Individual Trans Loops
title: PHE Individual Trans Loops
service: palente
runbook-name: PHE Individual Trans Loops
tags: oss, palente, phe
link: /palente/Runbook_PHE_Individual_Trans_Loops.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}


## Purpose
This alert is triggered when the PHE has failed to refresh one or more of the following components 5 or more times. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
The PHE has 6 different types of refresh loops running concurrently at regular  intervals to collect data. The PHE will allow for 5 retries for each failed refresh. If the number of failed refreshes reaches more than 5, it will trigger a [{{doctor-alert-system-name}}]({{doctor-alert-system-link}}) alert.

## User Impact
More than 5 failed refreshes may indicate an underlying issue in the PHE or perhaps with an API or database. Consequently, the PHE will be unable to open or update a real pCIE. In the event the issue is unrelated to PHE, the team responsible for the failing component should be notified accordingly (ex. EDB failure).

## Instructions to Fix
This is the parent runbook which gives a high level overview of the problem. Below is a list of runbook links with more details in respective to the alert. Please navigate to the correct runbook according to the received alert.
* [TIP](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_TIP_Ingestor.html)
* [Summarizer + CIE Generation](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_Summarizers.html)
* [OSS Registry](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_OSS_Registry.html)
* [ServiceNow](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_ServiceNow.html)
* [Elastic](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_ELK_Ingestor.html)
* [EDB](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/palente/Runbook_PHE_EDB_Ingestor.html)

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

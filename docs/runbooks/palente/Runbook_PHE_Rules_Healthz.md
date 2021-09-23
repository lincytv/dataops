---
layout: default
description: PHE Rules Healthz
title: PHE Rules Healthz
service: palente
runbook-name: PHE Rules Healthz
tags: oss, palente, phe
link: /palente/Runbook_PHE_Rules_Healthz.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
To determine the health of the Pa'lante Rules API service.

## Technical Details
The PHE operates by utilizing a set of rules that are stored in a database. The rules API is used to validate and load any new or updated rules into the databse. The API is mainly called whenever a new PR containing new/updated rules is submitted to the `oss-phe-rules` repository. The PR will trigger the CICD pipeline to call this validation API in order to validate against the new/updated rules. When the PR is merged into the master branch, the `load` operation of the API will be called to load the new/updated rules into the database.

## User Impact
If the API is down and fails to load new rules into the database, it may prevent PHE from operating properly without the new rules that accomodate the new code changes for the PHE.

## Instructions to Fix
1. Restart the  `api-oss-csd-rules` pod using kdep [How to restart Pa'lante Services]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}
---
layout: default
description: PHE failed to load configuration rules
title: PHE Configuration Rule
service: palente
runbook-name: PHE Configuration Rules
tags: oss, palente, tip
link: /palente/Runbook_PHE_Config_Rule_Error.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}


## Purpose
This alert is triggered when the Palante Heuristics Engine (PHE) has failed to load configuration rules from MongoDB 5 or more times. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
PHE configuration rules are stored on MongoDB database `csd`, collection `rules`. PHE loads configuration rules from MongoDB once service is started and every hour, this make sure PHE is up to date with the latest rules. There are 2 possible failures: failed to connect to MongoDB, or failed to load rules.

### How does rule get changed
All configuration rule files are stored in repo [oss-phe-rules](https://github.ibm.com/cloud-sre/oss-phe-rules). Changes merged to `master`, `staging` or `development` branch will trigger build to upload the rules to corresponding MongoDB. For more details, please reference to Readme in the repository.
When user create or merge PR in **oss-phe-rules**, the PR is validated/loaded by service `api-oss-csd-rule`. This service is using the same build as `api-oss-csd`. This make sure that rules saved to MongoDB by `api-oss-csd-rule` are valid for `api-oss-csd`

## User Impact
If the failure happen when PHE is starting, this will block all consequence processes, we need to resolve the problem ASAP. If the failure happen during reload rule time, PHE can still run with cached rules.

## Instructions to Fix
1. Determine if the failure is caused by MongdoDB connection or rule validation:
    - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
    - Select the **PALANTE**, then **OSS-CSD(Palante)**
    - Filter out the region report in the alert
    - Search for latest log `Starting refresh loop for configuration files`, expand and view in context
    - If error logs are related to MongoDB, please reference to [MongoDB Awareness runbook]({{site.baseurl}}/docs/runbooks/palente/Runbook_PHE_MongoDB_Awareness.html)
    - If error logs are like `Error parsing config file (custom info for this Metric)`, please proceed to the next step

2. If PHE fail to load rules from DB, it could because production PHE has not been deployed with latest build, while new rules are already loaded to production DB:
    - Check with palante team or TIP team to see if there is new `api-oss-csd` production build going on, if yes, snooze alert. Once production build is done, the alert should be resolved automatically.
    - If there is no ongoing production build, please contact palante team to validate and reload prodution rule.

3. If PHE database `csd` or PHE table `rules` in database `csd` is missing, please reference to [API Platform - EDB MongoDB has errors]({{site.baseurl}}/docs/runbooks/apiplatform/api.edb-mongodb.down.html) to connect to target MongoDB using MongoDB client
    - Create database `csd` if it is missing
    - Reference to [PHE Rules API swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/csdrules.yaml&no-proxy), get `osssc@us.ibm.com` APIKey based on [How to rotate credentials for Scorecard Function ID]({{site.baseurl}}/docs/runbooks/apiplatform/scorecard-FID-credential-rotation.html), use PHE Rules API to load rules to target MongoDB. 
    
## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

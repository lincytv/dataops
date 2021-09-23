---
layout: default
description: This alert is triggered when the Palante Heuristics Engine (PHE) has failed to refresh it's cache of OSS registry data or EDB certification data 21 or more times
title: PHE OSS Registry
service: palente
runbook-name: PHE OSS Registry
tags: oss, palente, tip
link: /palente/Runbook_PHE_OSS_Registry.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
This alert is triggered when the Palante Heuristics Engine (PHE) has failed to refresh it's cache of OSS registry data or EDB certification data 21 or more times. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
The PHE calls the OSS registry and EDB MongoDB on a regular interval to refresh it's cache of data from these two sources. Support is in place to retry the calls 21 times. If, after 21 retries, the calls still fail this alert is fired.

## User Impact
More than 21 failed refreshes may indicate an underlying issue in the PHE or perhaps with the OSS registry or EDB MongoDB. Impacts:
- If the PHE has not been able to load this data at least once since it was started, certain metric selectors will not be available for all services
- If the PHE has been able to load this data at least once, then there can be delay in PHE picking up new or updated services from the OSS registry and EDB MongoDB and applying certain metric selectors to the updated services

## Instructions to Fix
* **1.** The first step is to determine what error is being returned by the TIP ingestor. There are four possible different ways to obtain the error:
{% include ingestor_log.md name="OSS Registry Errors" %}
* **2.** The next step really depends on the error retrieved from 1 above. Here are some examples of possible errors and how to resolve them:

   **Problems connecting to production OSS registry (production Global Catalog)**

   - `Cannot get IAM token for Global Catalog (OSS entries):could not get IAM access token from API key for entry \"catalog-yp\" (HTTP GET error from IAM): Error in HTTP POST for IAM Token  (url=https://iam.cloud.ibm.com/identity/token): HTTPError code=400 Bad Request : {\"errorCode\":\"BXNIM0415E\",\"errorMessage\":\"Provided API key could not be found\" ...`
       - The IAM API key stored in the **SECRETKEY_catalog-yp** environment variable is no longer valid
       - Re-deploy the api-oss-csd pod in the problem region using the kdep, [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services), to ensure that the latest API key from Vault is available in the **SECRETKEY_catalog-yp** environment variable, e.g. `kdep useast-production-values.yaml`
       - If the problem is still occurring, a new API key will need to be created and stored in Vault:
          - If {% include contact.html slack=palente-scorecard-id-owner-slack name=palente-scorecard-id-owner-name userid=palente-scorecard-id-owner-userid notesid=palente-scorecard-id-owner-notesid %} is available, ask {{palente-scorecard-id-owner-name}} to generate a new API key for the scorecard function id
          - If {{palente-scorecard-id-owner-name}} is not available, generate an API key under the production or staging IBM - PNPServe account in the [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}) console using your id or another functional id you have access to
          - Temporarily, update the Vault entry for the **SECRETKEY_catalog-yp** environment variable with the new key and re-deploy the api-oss-csd pod in the problem regions using the kdep, [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services), command
          - Notify the [Pa'lente team](#palente-contact-information) of any changes

    - `Cannot get IAM token for Global Catalog (OSS entries): could not get IAM access token from API key for entry "catalog-yp" (empty response from IAM)`
       - This indicates that the call to production IAM to generate a token from the API key stored in the **SECRETKEY_catalog-yp** environment variable was successful, but IAM did not send an access token
       - Check the [#iam-adopters](https://ibm-cloudplatform.slack.com/archives/C0NLB2W3B) Slack channel to see if others are reporting similar problems. If not ask for help on the [#iam-adopters](https://ibm-cloudplatform.slack.com/archives/C0NLB2W3B) Slack channel.

    - `Error in HTTP GET for Catalog.OSS  (url=https://globalcatalog.cloud.ibm.com/api/v1?_offset=0&include=metadata.other.oss:metadata.other.oss_segment:metadata.other.oss_tribe:metadata.other.oss_environment&q=kind:oss_segment+kind:oss_tribe+kind:oss+kind:oss_environment): HTTPError code=XXX Not Found : X`
       - Call from the OSS registry code to the production Global Catalog failed with a `XXX` error code
       - Check the [#global-catalog-issues](https://ibm-cloudplatform.slack.com/archives/C8147V4PK) Slack channel to see if others are reporting similar problems. If not ask for help on the [#global-catalog-issues](https://ibm-cloudplatform.slack.com/archives/C8147V4PK) Slack channel.

    **Problems connecting to production EDB MongoDB**

    - `failed to connect to DB`
       - Creating a connection to or pinging the EDB MongoDB instance has failed
       - Additional information regarding the problem should be available in LogDNA (see link and details in step 1 above)
       - Try searching LogDNA for the following types of error strings to get a better idea of the problem occurring:
          - `Cannot get credentials edb-yp for MongoDB [edb] - disabled: X`
          - `MongoDB: Failed to create DB client for [edb]`
          - `MongoDB: Failed to connect to DB`
          - `MongoDB: Failed to ping DB client, reconnect: X`
          - `MongoDB: Failed to ping DB client`
      - Check whether there are any active EDB PagerDuty incidents as well and follow the associated runbooks
      - If there are no active EDB PagerDuty incidents, follow the [API Platform - EDB MongoDB has errors](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.edb-mongodb.down.html) runbook
      - If nothing helps up to this point, [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)

    **Problems pulling data from production EDB MongoDB**

    - Mongo DB error (error can vary depending on the problem)
       - Additional information regarding the problem should be available in LogDNA (see link and details in step 1 above)
       - Try searching LogDNA for the following types of error strings to get a better idea of the problem occurring:
          - `Collection [edbMetricsCertification] find failed: X`
          - `EDB Ingestor: Error occured while collecting data from edbMetricsCertification. Retry after X second`
          - `mongoDBUtils: Find data from collection`
          - `mongoDBUtils: Failed to process data for MetricsRolling`
          - `mongoDBUtils: Failed to process data for MetricsCertification`
          - `mongoDBUtils: Failed to process data for Rule`
          - `mongoDBUtils: unknown type: X`
          - `mongoDBUtils: DB Cursor error`
      - Check whether there are any active EDB PagerDuty incidents as well and follow the associated runbooks
      - If there are no active EDB PagerDuty incidents, follow the [API Platform - EDB MongoDB has errors](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.edb-mongodb.down.html) runbook
      - If nothing helps up to this point, [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)

* **3.** The problem is going to resolve when the appropriate `OSS Registry Error` widget from step 1 no longer shows any recent errors. If you are stuck, reach out to the [Pa'lente team](#palente-contact-information).

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

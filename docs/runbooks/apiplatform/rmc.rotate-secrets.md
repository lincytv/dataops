---
layout: default
title: "How to rotate secrets of the RMC Operations page, backend, and jobs"
type: Informational
runbook-name: "rmc.rotate-secrets"
description: "How to rotate secrets of the RMC Operations page, backend, and jobs"
service: oss-platform-registry
tags: rmc, operations-ui
link: /apiplatform/rmc.rotate-secrets.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose
This runbook should be used when the secrets used by the RMC Operations page, api-operations-backend service, and/or osscatimporter and osscatpublisher cronjobs need to be rotated.

## How to rotate secrets used in the RMC Operations page

**Secrets Table:**

| Number | VAULT__moduleName |  VAULT__environment | VAULT__secretKey    | VAULT__secretValue                                           |
| ------ | ----------------- | ------------------- | ------------------- | ------------------------------------------------------------ |
| 1      | oss               |   devtest           | actionTrackerAPIKey |  osstest@us.ibm.com stage PnPServe IAM API key from Shane    | 
| 2      | oss               |   test              | actionTrackerAPIKey |  c3cvmwgl@ca.ibm.com prod PnPServe IAM API key from Shane    | 
| 3      | oss               |   devtest           | certMgmtApiKey      |  scorecar@cn.ibm.com prod IAM API key from Emma              |
| 4      | oss               |   test              | certMgmtApiKey      |  scorecar@cn.ibm.com prod IAM API key from Emma              |
| 5      | oss               |   devtest           | certMgmtApiKeyNew   |  osssc@us.ibm.com prod IAM API key from Emma                 |
| 6      | oss               |   test              | certMgmtApiKeyNew   |  osssc@us.ibm.com prod IAM API key from Emma                 |
| 7      | oss               |   devtest           | edbAuditAuthKey     |  Same IAM API key as 2 above                                 |
| 8      | oss               |   test              | edbAuditAuthKey     |  Same IAM API key as 2 above                                 |
| 9      | oss               |   devtest           | gcorAuthApiKey      |  Same IAM API key as 1 above                                 |
| 10     | oss               |   test              | gcorAuthApiKey      |  Same IAM API key as 1 above                                 |
| 11     | oss               |   devtest           | gcorIamApiKey       |  osscat@us.ibm.com stage IAM API key from Dan                |
| 12     | oss               |   test              | gcorIamApiKey       |  osscat@us.ibm.com stage IAM API key from Dan                |
| 13     | oss               |   devtest           | iamApiKey           |  operations-ui operator service id stage API key from Shane  |
| 14     | oss               |   test              | iamApiKey           |  operations-ui operator service id stage API key from Shane  |
| 15     | oss               |   devtest           | slackAtReviewers    |  id of @ossreviewertest (not rotatable)                      |
| 16     | oss               |   test              | slackAtReviewers    |  id of @oss-onboarding-reviewers (not rotatable)             |
| 17     | oss               |   devtest           | slackWebhookURL     |  Webhook for [onboarding](https://api.slack.com/apps/A011CCWAADU/incoming-webhooks) Slack app from Emma or Shane |
| 18     | oss               |   test              | slackWebhookURL     |  Webhook for [onboarding](https://api.slack.com/apps/A011CCWAADU/incoming-webhooks) Slack app from Emma or Shane |
| 19     | oss               |   devtest           | tipTokenAuthKey     |  Same IAM API key as 2 above                                 |
| 20     | oss               |   test              | tipTokenAuthKey     |  Same IAM API key as 2 above                                 |

**Process:**

1. For each secret in the Secrets Table above:
    - Generate a new secret value
    - Follow the instructions [here](https://github.ibm.com/console-pipeline/docs/tree/master/helm#confidential) to change the secret value
    - Ask someone else on the team (Shane, Emma, Gabriel, Du Qian, or Gu Yue) to approve the secret change on the [#bld-oss](https://ibm-cloudplatform.slack.com/archives/CLZ03TRPF) Slack channel 
2. Run a replan of the oss service by opening the [Jenkins oss replan](https://wcp-console-jenkins.swg-devops.com/job/replan/job/oss/) build, clicking 'Build with Parameters', and then clicking BUILD
3. Open the RMC Operations page for an RMC resource in the [RMC devtest instance](https://dev.console.test.cloud.ibm.com/onboarding) and ensure that it loads fine
4. Promote the latest test oss build to the test environment by opening the [Jenkins oss promote](https://wcp-console-jenkins.swg-devops.com/job/promote/job/oss/build?delay=0sec) build, setting the RELEASE field to same value as the CURRENT_ONDECK_RELEASE and then clicking BUILD
5. Open the RMC Operations page for an RMC resource in the [RMC test instance](https://test.cloud.ibm.com/onboarding/dashboard) and ensure that it loads fine
6. Delete all the old secret values from there various sources
7. Do a quick re-test of the RMC Operations page in the devtest and test instances

## How to rotate operations-ui secrets in PIM:

There is currently only one secret: [BU430-OTDev > BU430-OTDev-PIM-ServiceAdmins > operations-ui > BSS account API](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/43304)

To rotate, ask Shane to generate a new staging IAM API key and set in PIM.

## How to rotate secrets used by the api-operations-backend service:

**Secrets Table:**

| Number | Secret Name (in charts)  | Description                                                                    | Vault Value                                                                                   |
| ------ | ------------------------ | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 1      | ACCEPTED_TOKEN           | Used by the RMC team to call the api-operations-backend API                    | Hard coded token - do not rotate. Migrating to accept IAM API keys and tokens.                |
| 2      | API_PLATFORM_API_KEY     | Used by the OSS IAM breakGlass to test IAM health                              | osstest@us.ibm.com (dev/staging) or c3cvmwgl@ca.ibm.com (prod)                                |
| 3      | BGCACHE_MASTER_KEY       | Used to decrypt OSS IAM breakglass data from TIP Elasticsearch                 | See OSS IAM breakglass cache secret rotation runbook (TBA) or contact Rui or Shane            |
| 4      | CLOUD_SERVICE_API_KEY    | Used by the iam-authorize library code to check with IAM if user is authorized | API key owned by the 'pnp-api-oss operator service id' in the IBM - PNPServe account from Ken |
| 5      | IAMKeyForWrite           | Used to write OSS records to the staging Global Catalog                        | osscat@us.ibm.com stage IAM API key from Dan                                                  |
| 6      | NR_LICENSE               | Used to write data to NewRelic using NewRelic APM                              | https://docs.newrelic.com/docs/accounts/accounts-billing/account-setup/new-relic-license-key/ |
| 7      | SECRETCREDENTIALS_es_key | Used to connect to TIP Elasticsearch                                           | See the [How to rotate secrets for OSS IAM breakglass](./iam.bg.rotate-secrets.html) runbook or contact Shane |

**Process:**

1. Unless there are different instructions in the table above, for each secret in the Secrets Table above, generate a new secret value
2. Reploy api-osscatalog charts in dev, staging, and production by making a change to the api-operations-backend charts (and any other charts that use the same Vault paths)
3. Delete the old secret values

## How to rotate secrets used by the osscatimporter and osscatpublisher cronjobs:

**Secrets Table:**

| Number | Secret Name (in charts) | Description                                                                                            |  Vault Value                                                               |
| ------ | ----------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| 1      | catalog_yp              | Used to read and write production Global Catalog records & EDB records from the Scorecard backend API  | osscat@us.ibm.com prod IAM API key from Dan                                |
| 2      | catalog_ys1             | Used to read and write staging Global Catalog records                                                  | osscat@us.ibm.com stage IAM API key from Dan                               |
| 3      | cos_iam_key             | Used to check emergency break in Cloud Object Storage and write logs, reports, etc to COS              | Service creds of Cloud Object Storage-Shared instance in OSS Cloud account |
| 4      | osscat_service_yp       | Used to get service information from production IAM (/v2/services API)                                 | osscat@us.ibm.com prod IAM API key from Dan                                |
| 5      | rmc-staging             | Used to call RMC backend APIs to get RMC resource information                                          | operations-ui operator service id stage API key from Shane                 |
| 6      | servicenow_watson       | Used to get configuration management (CI) information from production ServiceNow                       | Obtain SN token from Courtney Richards (SN Velocity team)                  |
| 7      | slack_token             | Used to post results to the #osscatalog-updates and #osscatalog-updates-test Slack channels            | ossbot Slack application token from Jing, Kun, or Shane                    |

**Process:**

1. For each secret in the Secrets Table above, generate a new secret value
2. Reploy api-osscatalog charts in dev, staging, and production by making a change to the api-osscatalog charts (and any other charts that use the same Vault paths)
3. Delete the old secret values

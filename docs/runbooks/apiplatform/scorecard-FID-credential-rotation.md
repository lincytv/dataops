---
layout: default
description: How to rotate credentials of Scorecard Function ID
title: How to rotate credentials for Scorecard Function ID
service: tip-api-platform
runbook-name: How to rotate credentials for Scorecard Function ID
tags: oss, scorecard, runbook
link: /apiplatform/scorecard-FID-credential-rotation.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose
This runbook is used as reference when need to update Scorecard function ID `osssc@us.ibm.com` credentials, such as W3ID password or API keys.

**W3ID** osssc@us.ibm.com

**Manager** Shawn Bramblett

**Owner** Emma Zhang

## Change W3ID password
W3ID password need to be changed every 3 months. FID owner or manager can update password in [sso link](https://w3idprofile.sso.ibm.com/password/nonperson_id_entry.wss)

After new password is set, contact Ali to update the password record in PIM

## IAM APIKeys
IAM API key need to be rotate every 1 year. 
Scorecard FID manages 3 sets of staging and production APIKeys for Scorecard, EDB and IssueCreator.

### To generate new APIKey:

1. Login to [IBM Cloud](https://cloud.ibm.com) using FID w3id credential (contact Emma or Shawn for 2FA verification)

2. Switch to `PNPServe` account

3. Go to [manage IAM API Key page](https://cloud.ibm.com/iam/apikeys) to generate new keys (for staging, go to [test IBM Cloud](https://test.cloud.ibm.com/iam/apikeys)). DO NOT delete old key at this point.

4. Inform service owner about the change (Scorecard: Emma Zhang, EDB: Irma Sheriff, RMC: Shane)

### To update APIKey in service:

1. Test new APIKeys with curl command locally to make sure new keys work fine before updating any vault value.

2. Get vault path from oss-charts. Use following table as reference, but double check oss-charts in case the table is out of date.

| Service       | Vault path                                                       | 
| :------------- | :------------------------------------------------------------- |
| Scorecard (api-scorecard-backend, api-gcor-api)  | generic/crn/v1/dev/local/tip-oss-flow/global/scorecard/IAM_APIKEY (production APIKEY) |
|   | generic/crn/v1/dev/local/tip-oss-flow/global/scorecard/IAM_APIKEY_STAGING (staging APIKEY) |
|   | generic/crn/v1/dev/local/tip-oss-flow/global/scorecard/CERT_IAM_APIKEY (production APIKEY) |
|   | generic/crn/v1/staging/local/tip-oss-flow/global/scorecard/IAM_APIKEY (production APIKEY) |
|   | generic/crn/v1/staging/local/tip-oss-flow/global/scorecard/IAM_APIKEY_STAGING (staging APIKEY) |
|   | generic/crn/v1/staging/local/tip-oss-flow/global/scorecard/CERT_IAM_APIKEY (production APIKEY) |
|   | generic/crn/v1/internal/local/tip-oss-flow/global/scorecard/IAM_APIKEY (production APIKEY) |
|   | generic/crn/v1/internal/local/tip-oss-flow/global/scorecard/IAM_APIKEY_STAGING (staging APIKEY) |
|   | generic/crn/v1/internal/local/tip-oss-flow/global/scorecard/CERT_IAM_APIKEY (production APIKEY) |
| PHE (api-oss-csd) | generic/crn/v1/dev/local/tip-oss-flow/global/oss-csd/catalog_yp (staging APIKEY) |
|   | generic/crn/v1/dev/local/tip-oss-flow/global/oss-csd/tip_yp (staging APIKEY) |
|   | generic/crn/v1/staging/local/tip-oss-flow/global/oss-csd/catalog_yp (staging APIKEY) |
|   | generic/crn/v1/staging/local/tip-oss-flow/global/oss-csd/tip_yp (staging APIKEY) |
|   | generic/crn/v1/internal/local/tip-oss-flow/global/oss-csd/catalog_yp (production APIKEY) |
|   | generic/crn/v1/internal/local/tip-oss-flow/global/oss-csd/tip_yp (production APIKEY) |
| EDB (api-edb-adapter-dry-run, api-edb-adapter-metrics, api-edb-adapter-metrics-backup, api-edb-adapter-metrics-sysdig, api-edb-adapter-sysdig, api-edb-adapter-tip, api-subscription-api, api-edb-stale-metrics-subscription) | /generic/crn/v1/internal/local/tip-oss-flow/global/edb/scorecard_iam_api_key (production APIKey) |
|   | /generic/crn/v1/staging/local/tip-oss-flow/global/edb/scorecard_iam_api_key (staging APIKey) |
|   | /generic/crn/v1/dev/local/tip-oss-flow/global/edb/scorecard_iam_api_key (staging APIKey) |
| Issue Creator |   TBD | 


3. Update vault value with new APIKey
    ```
    vault write <vault path> 'value=<new value>' 'about=<some information such as update time, updated by>'
    ```

4. Deploy service
    For dev and staging environment, developer can update `version` value in `Chart.yaml` file to a minor version change, and merge the change to oss-charts master branch to trigger a new deployment. 
    
    For production environment, the change in oss-charts will be pushed to production by TIP team afterwards, if you need to have the change deployed immediately, please contact Shane or Irma or anyone who has kube admin role.
    
5. Check logDNA to make sure new key works

### To update APIKey in Scorecard UI and RMC UI:
1. Follow the doc in [helm Confidential](https://github.ibm.com/console-pipeline/docs/tree/master/helm#confidential) to update any credentials. Starting with `devtest` first, and test on [scorecard devtest site](https://dev.console.test.cloud.ibm.com/scorecard)

2. Test [scorecard pages](https://cloud.ibm.com/scorecard) or [staging scorecard pages](https://test.cloud.ibm.com/scorecard)

3. Test [RMC pages](https://test.cloud.ibm.com/onboarding/dashboard)


After verify new key works, go to https://cloud.ibm.com/iam/apikeys to lock old keys, and eventually delete keys after new keys are used no problem for a while.
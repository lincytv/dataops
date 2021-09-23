---
layout: default
description: How to rotate credentials For EDB
title: How to rotate credentials for EDB
service: tip-api-platform
runbook-name: How to rotate credentials for EDB
tags: oss, edb, runbook, secrets, vault
link: /apiplatform/How_To/Rotate_EDB_Secrets.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose
This runbook is used as reference when secrets need to be rotated for Event Data Broker (EDB).

EDB uses API Keys for various functional userids and external services which need to be rotated yearly.

## IBM Cloud Database credentials

Credentials for ICD Redis, MongoDB and RabbitMQ must also be [rotated](https://ibm.ent.box.com/notes/745961725563). 


## Change Functional W3ID passwords

W3ID passwords need to be changed every 3 months. Functinal ID owner or manager can [change](https://w3idprofile.sso.ibm.com/password/nonperson_id_entry.wss) the password.

| W3ID |  Manager | Owner   | 
| ----------------- | ------------------- | ------------------- | 
| ossedb@us.ibm.com | Shawn Bramblett | Irma Sheriff |
| c3cvnhb3@ca.ibm.com | Eugene Kharlamov | Irma Sheriff |
| osssc@us.ibm.com | Shawn Bramblett | Emma Zhang |
| scorecar@cn.ibm.com | Eugene Kharlamov | Emma Zhang |



## IAM APIKeys
IAM API keys need to be rotated once a year. 


### List of secrets requiring rotation

| Environment |  Secret Owner | Vault Path    | About                                           |
| ----------------- | ------------------- | ------------------- | ------------------------------------------------------------ |
| dev | ServiceId-beb8144a-eb61-4bef-8625-457f1bafdad6 | /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/edb/sysdig/supertenant.key | Contains API key supertenant-apikey for Service ID sysdig-supertenant on account 2117538 |
| staging | ServiceId-beb8144a-eb61-4bef-8625-457f1bafdad6 | /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/edb/sysdig/supertenant.key | Contains API key supertenant-apikey for Service ID sysdig-supertenant on account 2117538 |
| prod | ServiceId-beb8144a-eb61-4bef-8625-457f1bafdad6 | /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/edb/sysdig/supertenant.key | Contains API key supertenant-apikey for Service ID sysdig-supertenant on account 2117538 |
| dev | ossedb@us.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/edb/iam/ossedb.key | Contains test apikey for ossedb account used for synthetic provisioning tests |
| staging | ossedb@us.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/edb/iam/ossedb.key | Contains test apikey for ossedb account used for synthetic provisioning tests |
| prod | ossedb@us.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/edb/iam/ossedb.key | Contains test apikey for ossedb account used for synthetic provisioning tests |
| dev | osssc@us.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/edb/scorecard_iam_api_key | Public test IAM API key owned by the osssc@us.ibm.com user and used by edb to access GCOR api |
| staging | osssc@us.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/edb/scorecard_iam_api_key | Public test IAM API key owned by the osssc@us.ibm.com user and used by edb to access GCOR api |
| prod | osssc@us.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/edb/scorecard_iam_api_key | Public IAM API key owned by the osssc@us.ibm.com user and used by edb to access GCOR api |
| dev | scorecar@cn.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/scorecard/PNP_SERVE_APIKEY | Used for calling Ingestor |
| staging | scorecar@cn.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/scorecard/PNP_SERVE_APIKEY | Used for calling Ingestor |
| prod | scorecar@cn.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/scorecard/PNP_SERVE_APIKEY | Used for calling Ingestor |
| dev | c3cvnhb3@ca.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey | EDB PNPServe test IAM key used to authenticate against EDB APIs |
| dev | c3cvnhb3@ca.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey-secondary | EDB PNPServe IAM key used to authenticate against EDB APIs |
| staging | c3cvnhb3@ca.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey | EDB PNPServe test IAM key used to authenticate against EDB APIs |
| staging | c3cvnhb3@ca.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey-secondary | EDB PNPServe IAM key used to authenticate against EDB APIs |
| prod | c3cvnhb3@ca.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey | EDB PNPServe test IAM key used to authenticate against EDB APIs |
| prod | c3cvnhb3@ca.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/edb/pnpserve/c3cvnbh3/public-iam-apikey-secondary | EDB PNPServe IAM key used to authenticate against EDB APIs |
| dev | ossedb@us.ibm.com | /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/edb/iam/pnpserve/ossedb.key | Contains apikey for ossedb account used for edb stale data notifications |
| staging | ossedb@us.ibm.com | /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/edb/iam/pnpserve/ossedb.key | Contains apikey for ossedb account used for edb stale data notifications |
| prod | ossedb@us.ibm.com | /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/edb/iam/pnpserve/ossedb.key | Contains apikey for ossedb account used for edb stale data notifications |

### To generate a new APIKey:

1. Login to [IBM Cloud](https://cloud.ibm.com) using FID w3id credential.

2. Go to [manage IAM API Key page](https://cloud.ibm.com/iam/apikeys) to generate new keys (for staging, go to [test IBM Cloud](https://test.cloud.ibm.com/iam/apikeys)). DO NOT delete the old key at this point.

### To update the APIKey in relevant EDB components:

1. Use the table above as a reference, but double check vault paths in oss-charts in case the table is out of date.


2. Update relevant vault value with the new APIKey being rotated.
    ```
    vault write <vault path> 'value=<new value>' 'about=<information about the secret>'
    ```

3. Deploy service
    Search oss-charts with the vault path to find all components that need to be redeployed.  The developer can update the `version` value in the `Chart.yaml` file to a minor version change, and merge the change to oss-charts staging branch to trigger a new deployment. 
       
4. Check logDNA for any authentication errors.

5. After you have verified the new key works, go to https://cloud.ibm.com/iam/apikeys to lock the old keys. If after a few days there are no issues, delete the keys.

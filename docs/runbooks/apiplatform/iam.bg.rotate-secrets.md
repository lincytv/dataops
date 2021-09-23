---
layout: default
title: "How to rotate secrets for OSS IAM breakglass"
type: Informational
runbook-name: "iam.bg.rotate-secrets"
description: "How to rotate secrets for OSS IAM breakglass"
service: tip-api-platform
tags: iam, breakglass, cache, iam-authorize
link: /apiplatform/iam.bg.rotate-secrets.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose

This runbook should be used when the secrets for the OSS IAM breakglass functionality need to be rotated. These secrets are used by multiple services such as tip-hooks, pnp-hooks, edb-ingestor, etc.

## How to rotate the TIP Elasticsearch secrets

OSS IAM breakglass information is read from the TIP Elasticsearch instance in the same cluster at startup, and is written to the TIP Elasticsearch instance in the same cluster periodically. In order for services like tip-hooks etc to connect to TIP Elasticsearch, the services need access to a user id and password with access to TIP Elasticsearch. This section provides instructions on how to rotate this password in the development, staging, and production environments.

Note that in order to perform the following steps, you will need access to change the c3cvsc90@ca.ibm.com (bgesstage) functional id password for development and staging, and the c3cvsc92@ca.ibm.com (bgesprod) functional id password for production. The admin of these functional ids can be looked up in Bluepages.

**Steps**

1. Create a new password, but do not change in w3 yet

2. Set password2 (`yyyy` value below) to the new password in Vault (so `xxxx` will contain the old password, and `yyyy` will contain the new password):

    Dev:
    ```
    vault write /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/shared/elk/elasticsearch_json 'value=@creds.json' 'about=Credentials used to log into TIP Elasticsearch instance within the cluster.'
    ```

    Staging:
    ```
    vault write /generic/crn/v1/staging/local/tip-oss-flow/global/otdev/shared/elk/elasticsearch_json 'value=@creds.json' 'about=Credentials used to log into TIP Elasticsearch instance within the cluster.'
    ```

    Production:
    ```
    vault write /generic/crn/v1/internal/local/tip-oss-flow/global/otdev/shared/elk/elasticsearch_json 'value=@creds.json' 'about=Credentials used to log into TIP Elasticsearch instance within the cluster.'
    ```

    creds.json (for dev and staging):
    ```
    {
        "enabled":"true",
        "url":"http://tip-elasticsearch-elasticsearch-client.tip.svc.cluster.local:9200",
        "user1":"c3cvsc90@ca.ibm.com",
        "password1":"xxxx",
        "user2":"c3cvsc90@ca.ibm.com",
        "password2":"yyyy"
    }
    ```

    creds.json (for production)
    ```
    {
    "enabled":"true",
        "url":"http://tip-elasticsearch-elasticsearch-client.tip.svc.cluster.local:9200",
        "user1":"c3cvsc92@ca.ibm.com",
        "password1":"xxxx",
        "user2":"c3cvsc92@ca.ibm.com",
        "password2":"yyyy"
    }
    ```

3. Find all services that use the OSS IAM break glass support by searching the oss-charts repository for "/local/tip-oss-flow/global/otdev/shared/elk/elasticsearch_json"

    Example command:
    ```
    grep -rl "/local/tip-oss-flow/global/otdev/shared/elk/elasticsearch_json" . | sed 's|^./||' | sed 's|/development-values.yaml||' | sed 's|/staging-values.yaml||' | sed 's|/production-values.yaml||' | uniq | sort
    ```

4. Update the `lst` environment variable definition below with the services found in step 3, and re-deploy all pods in dev and staging, or production (**ensure you use the correct oss-charts branch - staging or production!**):

    ```
    cd ~/git/oss-charts
    declare -a lst=(api-api-catalog api-auth-proxy api-bastion-api api-edb-adapter-actiontracker api-edb-audit api-edb-cie-api api-edb-hooks api-edb-ingestor api-edb-mapping-api api-edb-mapping-consumer api-edb-processing-status api-edb-subscription-api api-gcor-api api-incident-management api-issuecreator-backend api-operations-backend api-pnp-hooks api-pnp-ops-api api-pnp-status api-pnp-subscription api-scorecard-backend api-subscription-api tip-hooks)
    ./re-deploy-by-region-env.sh -e development -r ussouth -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e development -r useast -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e development -r eude -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e staging -r ussouth -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e staging -r useast -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e staging -r eude -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e production -r useast -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e production -r ussouth -b <SN_TICKET_NUM> -l "${lst[@]}"
    ./re-deploy-by-region-env.sh -e production -r eude -b <SN_TICKET_NUM> -l "${lst[@]}"
    ```

    Note: If a pod can not be updated because continuous deployment is disabled, manually update the Kube secret that holds the elasticsearch password and then delete all the pods to force the pods to pickup the updated secret. Rough steps:
    ```
    1. kubectl describe pod -napi ...
    2. kubectl get secret -napi ... -o yaml > secret.yaml
    3. base64 --input creds.json
    4. Update the base64 encoded secret value in the secret.yaml file
    5. kubectl apply -f secret.yaml
    6. kubectl delete pod ...
    ```

5. Verify:
    - No incidents in NewRelic or PagerDuty
    - No errors in LogDNA with the following strings:
        - "Bulk indexer received an error writing data to Elasticsearch"
        - "Bulk indexer received a 401 Unauthorized error writing data to Elasticsearch"

6. If unexpected incidents or authorization errors are found in step 5 above and the problem can not be determined, revert the changes made and reach out to the team for help.

7. Change the password in w3 and wait for email that password was successfully change
    - Note that it is normal to see some bulk indexer errors after the password is changed in w3 when the services automatically move from password1 to password2
    - Can search LogDNA for the following text to see when the password switches are being made by the code: "received a 401 Unauthorized error writing data to Elasticsearch"

8. Repeat step 2 but this time update the password1 value (`xxxx` value) to the new password (so both `xxxx` and `yyyy` will be the new password)

9. Repeat step 4 to redeploy

10. Repeat step 5 to verify

**Note** that before changes can be made to the OSS staging or production environments, a production ServiceNow Change record needs to be opened for each environment. Text like the following can be used for the SN Change record:

```
Explanation of Impact During Change Implementation: No impact

Purpose / Goal: Rotating TIP Elasticsearch password used by OSS staging services for OSS IAM breakglass

Description & Plan:
1. Create new password but do not set yet
2. Update password2 in Vault to the new password
3. Re-deploy pods that use password
4. Set new password (make effective)
5. Update password1 in Vault to the new password
6. Re-deploy pods that use password

Backout plan:

Undo deployment changes
```

## How to rotate the OSS IAM break glass encryption key

TBA. Talk with Rui or Shane in the meantime.

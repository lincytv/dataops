---
layout: default
description: TIP Ingestor
title: TIP Ingestor
service: palente
runbook-name: TIP Ingestor
tags: oss, palente, tip
link: /palente/Runbook_PHE_TIP_Ingestor.html
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
This alert is triggered when the Palante Heuristics Engine (PHE) has failed to refresh TIP sources 5 or more times. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
The PHE calls the TIP ingestor on a regular interval and supports retrying the call to the TIP ingestor 5 times. If, after 5 retries, the TIP ingestor still returns an error this alert is fired. The TIP ingestor itself makes calls to the OSS Incident Management (IM) API to get incident data from ServiceNow. Based on this data, the TIP ingestor creates data points and calls the Palante hybrid store to store the data points both within an in-memory data store and in the _TIP Elasticsearch_ instance running in the same cluster.

## User Impact
More than 5 failed refreshes may indicate an underlying issue in the PHE or perhaps with the IM API. Consequently, the PHE will be unable to open or update a real pCIE.

## Instructions to Fix
* **1.** The first step is to determine what error is being returned by the TIP ingestor. There are four possible different ways to obtain the error:
{% include ingestor_log.md name="TIP Ingestor Errors" %}
* **2.** The next step really depends on the error retrieved from 1 above. Here are some examples of possible errors and how to resolve them:

    **Configuration problem**

    - `Cannot get key "tip-yp" for TIP IM API - disabled: cannot find entry "tip-yp" in keyfile`:
        - There is a problem with the api-oss-csd charts: the **SECRETKEY_tip-yp** environment variable is missing from the value is missing from the [api-oss-csd deployment.yaml]({{api-oss-csd-charts-link}}/templates/deployment.yaml) file
        - Look for recent changes to the [api-oss-csd charts]({{api-oss-csd-charts-link}}), reverse the changes, and re-deploy the api-oss-csd pod using kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)

    - `Error in HTTP GET for TIP Incidents (sev*/confirmed-cie/1.00h)  (url=https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns?_limit=100&create_start=2020-12-07T21:53:05Z&create_end=2020-12-07T22:53:05Z&incident_state=confirmed-cie): HTTPError code=401 Unauthorized : {"message":"Unauthorized"}`
        - The value of the **SECRETKEY_tip-yp** environment variable in the [api-oss-csd charts](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/api-oss-csd) is no longer valid
        - As a temporary fix, find the Kube secret name associated with the **SECRETKEY_tip-yp** environment variable by running the `kubectl describe pod -napi -l app=api-oss-csd` command, see [How to get a kube secret]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-get-a-kube-secret)
        - Get the yaml for the secret: `kubectl get secret -n api auto-configured-secret-from-vault-xxxx -o yaml > secret.yaml`
        - Generate an API key under the production or staging IBM - PNPServe account in the [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}) console using one of the users identified in the `ID_SWITCH_FROM` property in the api-incident-management [values.yaml](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/api-incident-management/values.yaml) file
        >If you can't access the APIKEY at IBM - PNPServe account please contact {% include contact.html slack=palente-sme-elk-slack name=palente-sme-elk-name userid=palente-sme-elk-userid notesid=palente-sme-elk-notesid %} or {% include contact.html slack=tip-api-platform-manager-slack name=tip-api-platform-manager-name userid=tip-api-platform-manager-userid notesid=tip-api-platform-manager-notesid %}
        - Base64 encode your API key by running: `echo 'API_KEY' | base64`
        - Update the data.value value in the secret.yaml file with the Base64 encoded API key
        - Update the Kube secret with the API key by running: `kubectl apply -f secret.yaml`
        - Notify the [Pa'lente team](#palente-contact-information) of the change

    - `LookupMetricConfig(): no default configuration for Metric X`
        - There may be a problem loading the metric configuration files
        - [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services) pod.

    **Network Problem calling the Incident Management API**

    - `Error in HTTP GET for TIP Incidents (sev*/confirmed-cie/1.00h)  (url=https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns?_limit=100&create_start=2020-12-07T21:58:07Z&create_end=2020-12-07T22:58:07Z&incident_state=confirmed-cie): Get https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns?_limit=100&create_start=2020-12-07T21:58:07Z&create_end=2020-12-07T22:58:07Z&incident_state=confirmed-cie: dial tcp 104.20.227.112:443: connect: connection refused`
        - Generate an API key under the production or staging IBM - PNPServe account in the [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}) console depending on the alert environment
        - Try running the following command depending on the environment and region to see if you get a failure:
            ```
            curl -H "Authorization: $API_KEY" "https://us-east.pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns?_limit=1&severity=1&active=both"
            ```
        - If you don't see a failure, try running the same command in the api-oss-csd container of the api-oss-csd pod running in the environment and region that reported the problem
        - If you still don't see a failure, the alert should clear
        - If you do see a failure, there is most likely a problem with Kube or the networking in general. Check the health of the Kube cluster.

    **Incident Management API returning error**

    - `Error in HTTP GET for TIP Incidents (sev*/confirmed-cie/1.00h)  (url=https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi1/api/v1/incidentmgmt/concerns?_limit=100&create_start=2020-12-07T22:00:49Z&create_end=2020-12-07T23:00:49Z&incident_state=confirmed-cie): HTTPError code=500`
       - Generate an API key under the production or staging IBM - PNPServe account in the [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}) console depending on the alert environment
       - Try running the following command depending on the environment and region to see if you get a failure:
            ```
            curl -H "Authorization: $API_KEY" "https://us-east.pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns?_limit=1&severity=1&active=both"
            ```
       - If you don't see a failure, the alert should clear
       - If you do see a failure, reach out to the TIP team on the [{{oss-slack-cto-oss-tip-internal-name}}]({{oss-slack-cto-oss-tip-internal-link}}) Slack channel for help
       - If you are not getting a response on the Slack channel, open a incident in production [{{service-now-name}}]({{service-now-link}}) under the `tip-oss-flow` service (configuration item) to cause the TIP team to be paged out

    **Problems saving to Elasticsearch**

    - `Error occurred trying to save data point into the Elasticsearch data store. Cause: Error occurred marshalling input for bulk indexing`
        - This is a problem in the oss-csd code
        - If the alert does not clear, [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services) 

    - `Error occurred trying to save data point into the Elasticsearch data store. Cause: Error occurred adding item to bulk indexer`
        - This is most likely a problem in the oss-csd code or the Elasticsearch library it uses
        - If the alert does not clear, [Try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services) pod.

* **3.** The problem is going to resolve when the appropriate `TIP Ingestor Error` widget from step 1 no longer shows any recent errors. If you are stuck, reach out to the [Pa'lente team](#palente-contact-information).

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

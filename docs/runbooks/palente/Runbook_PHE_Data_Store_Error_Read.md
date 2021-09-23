---
layout: default
description: PHE Data Store Error Read
title: PHE Data Store Error Read
service: palente
runbook-name: PHE Data Store Error Read
tags: oss, palente, phe
link: /palente/Runbook_PHE_Data_Store_Error_Read.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
This alert is triggered when the Palante Heuristics Engine (PHE) has failed to read from Elasticsearch three or more times over a 5 minute period. Use this runbook to confirm and resolve this issue accordingly.

## Technical Details
The PHE makes Elasticsearch read calls in the following scenarios:
1. To initially populate historic data points in the PHE hybrid data store by reading data from the `csd*` index
2. To display historic data points in the internal PHE dashboard by reading data from the `csd*` index
3. To create +1 data points by reading +1 alerts from the TIP `alerts-*` index

## User Impact
Scenarios 1 and 2 from above do not impact the end user. Scenario 3 can impact the end user, however, as not obtaining +1 data can mean that the PHE is delayed in creating one or more pCIEs and/or may completely miss creating one or more pCIEs.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

* **1.** The first step is to determine what error is being returned by the Elasticsearch code. There are four possible different ways to obtain the error (you will also be able to obtain the name of the Elasticsearch index where that the error occurred against in the `PHE- ELASTICSEARCH- INDEX` column of the NewRelic dashboard):  
{% include datastore_log.md name="Read Errors (Prod)" %}
* **2.** The next step really depends on the error retrieved from 1 above. Here are some examples of possible errors and how to resolve them:

    **Configuration problem**

    - `Elasticsearch is disabled`
      - The value of the **SECRETCREDENTIALS_es_key** environment variable in the [api-oss-csd charts]({{api-oss-csd-charts-link}}) is either missing **(A)** or has the `enabled` property set to _false_ **(B)**
      - Find the Kube secret name associated with the **SECRETCREDENTIALS_es_key** environment variable by running the `kubectl describe pod -napi -l app=api-oss-csd` command, you will see a line like the follow:
      ```
        SECRETCREDENTIALS_es_key:    <set to the key 'value' in secret
        'auto-configured-secret-from-vault-78e540401d2fc83af685d938548eb47eaa1442c34995c784ad9894abeb5a83f7'>  Optional: false
      ```
      - **A.** If the Kube secret name can not be found
        - Look for recent changes to the [api-oss-csd charts]({{api-oss-csd-charts-link}})
        - Reverse the changes
        - Re-deploy the api-oss-csd pod using the kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)
      - **B.** If the Kube secret name can be found
        - Get the secret [How to get a kube secret]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-get-a-kube-secret)
        - If `"enabled":"true"` is missing from the secret.yaml/json file or is set to _false_
        - Add `"enabled":"true"` to the secret.yaml/json  file
        - Update the Kube secret with the API key by running:
          - `kubectl apply -f secret.yaml` / `kubectl apply -f secret.json`
        - Notify the [Pa'lente team](#palente-contact-information) of the change

    - `entry "es-key" in keyfile does not contain a "X"` _[where X = user1, password1, user2, or password2]_
        - The value of the **SECRETCREDENTIALS_es_key** environment variable in the [api-oss-csd charts]({{api-oss-csd-charts-link}}) is missing a property
        - Compare the value of the **SECRETCREDENTIALS_es_key** environment variable with another working region of the same environment
          - For example, if the problem is in production _us-east_, try looking at the value in production _us-south_
        - If the value in the working region is different
          - Re-deploy the api-oss-csd pod in the problem region using the kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)
        - Notify the [Pa'lente team](#palente-contact-information) of the change

    **Problems reading from Elasticsearch**

    - `Could not cast response of call to Elasticsearch to PostReponse`
        - This is most likely a transient problem, wait five minutes to see if the problem stops, if the problem persists.
          - [Try restarting the api-oss-csd ]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)

    - `Unexpected status code:401`
        - There is a either a problem with _LDAP_ proxy that the _TIP Elasticsearch_ instance uses to authentic users or a problem with the user name and passwords used to connect to Elasticsearch
        - Compare the value of the **SECRETCREDENTIALS_es_key** environment variable with another working region of the same environment.
          - For example, if the problem is in production _us-east_, try looking at the value in production _us-south_
        - Re-deploy the api-oss-csd pod in the problem region using the kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)
        - If the 401 error persists, follow the [Contacting the TIP team for Elasticsearch help](#contacting-the-tip-team-for-elasticsearch-help) steps below to contact the TIP team for help in determining if there is a problem with _Elasticsearch_ or with the _LDAP_ proxy used by _Elasticsearch_
        - If it is determined that the password may be invalid, contact {% include contact.html slack=palente-sme-elk-slack name=palente-sme-elk-name userid=palente-sme-elk-userid notesid=palente-sme-elk-notesid %} to verify that the password for the _c3cvsc93@ca.ibm.com_ (dev and staging) or _c3cvsc94@ca.ibm.com_ (production) user.
        - If a new password is needed, contact either {% include contact.html slack=palente-sme-elk-slack name=palente-sme-elk-name userid=palente-sme-elk-userid notesid=palente-sme-elk-notesid %} or {% include contact.html slack=tip-api-platform-manager-slack name=tip-api-platform-manager-name userid=tip-api-platform-manager-userid notesid=tip-api-platform-manager-notesid %} can create a new password
          - The Vault entry for the **SECRETCREDENTIALS_es_key** environment can then be updated
          - Then the api-oss-csd pods re-deployed in the problem region using the kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)
        - Notify the [Pa'lente team](#palente-contact-information) of any changes

    - `Unexpected status code:403`
        - The *c3cvsc93@ca.ibm.com* (dev and staging) or *c3cvsc94@ca.ibm.com* (production) user no longer has permission to read from the TIP `alerts-*` index in the _TIP Elasticsearch_ instance in the same region as the problem api-oss-csd pod
        - This is most likely a permission problem with the _TIP Elasticsearch_ instance itself
        - Follow the [Contacting the TIP team for Elasticsearch help](#contacting-the-tip-team-for-elasticsearch-help) steps below to contact the TIP team for help

    - `Unexpected status code:xxx`
        - This could be a problem due to a recent code update to the api-oss-csd code or configuration, some bad data in Elasticsearch, or a problem with _TIP Elasticsearch_ instance, wait five minutes to see if the problem stops
        - If the problem persists, try [restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)
        - Look for recent changes to the [api-oss-csd charts]({{api-oss-csd-charts-link}})
          - Reverse the changes, and re-deploy the api-oss-csd pod using the kdep [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)
        - If reversing the changes does not help, follow the [Contacting the TIP team for Elasticsearch help](#contacting-the-tip-team-for-elasticsearch-help) steps below to contact the _TIP_ team for help
        - Notify the [Pa'lente team](#palente-contact-information) of any changes

* **3.** The problem is going to resolve when the `Read Errors (Prod)` widget from step 1 no longer shows any recent errors. If you are stuck, reach out to the [Pa'lente team](#palente-contact-information).

## Contacting the TIP team for Elasticsearch help

- Reach out to the _TIP_ team on the [{{oss-slack-cto-oss-tip-internal-name}}]({{oss-slack-cto-oss-tip-internal-link}}) Slack channel for help ({% include contact.html slack=sosat-lead-eng-slack name=sosat-lead-eng-name userid=sosat-lead-eng-userid notesid=sosat-lead-eng-notesid %} is the main contact for _Elasticsearch_ on the _TIP_ team)
- If you are not getting a response on the Slack channel and need an urgent response, open a incident in production [{{service-now-name}}]({{service-now-link}}) under the `tip-oss-flow` service (configuration item) to cause the _TIP_ team to be paged out

## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}

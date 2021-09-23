---
layout: default
description: PHE Healthz Liveness
title: PHE Healthz Liveness
service: palente
runbook-name: PHE Healthz Liveness
tags: oss, palente, phe
link: /palente/Runbook_PHE_Healthz_Liveness.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
This alert is triggered whenever the PHE's Healthz endpoint is not repsonding.

## Technical Details
PHE is deployed in 2 regions, `us-south` and `us-east`. In `us-south` there are 2 instances running; one in staging and the other in production. On a single production instance is deployed to `us-east`. A healthz endpoint exists to verify PHE's liveness.


## User Impact
If the PHE is down, we will be unable to detect possible service outtages across IBM Cloud.


## Instructions to fix
1. Verify that the PHE Healthz API is still responding succesfully 
- Visit the link or execute a curl command with the proper region and evironment set.
[Prod](https://us-south.pnp-api-oss.cloud.ibm.com/phengine/api/v1/phe/healthz) - `https://us-south.pnp-api-oss.cloud.ibm.com/phengine/api/v1/phe/healthz` 
[Staging](https://us-south.pnp-api-oss.test.cloud.ibm.com/phengine/api/v1/phe/healthz) - `https://us-south.pnp-api-oss.test.cloud.ibm.com/phengine/api/v1/phe/healthz`

- If you see:
```
{"href":"/api/v1/phe/healthz","code":0,"description":"The API is available and operational"}
```
- The PHE is still up and running and the alert should resolve soon. The alert might have been caused by dealys in the network. 
- Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.

- If the response is `no healthy upstream`, there is a problem and one should check the logs (proceed to next step).

2. Check the logs in LogDNA or Kubernetes
    - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
    - Select the **PALANTE**, then **OSS-CSD(Palante)**
    - Filter out the region
    - See if there have been any errors by filtering with level `ERR`.
    - The logs should give some indication on what the underlying problem is
    - If you are unable to see log in logDNA, you can access logs directly through Kubernetes instead by using the `kubectl` command
    - Execute `kubectl logs -napi -lapp=api-oss-csd -c api-oss-csd --tail 50`
    The `--tail 50` option indicates that it will get the last 50 lines of long entries of the pod, it can be changed or removed

3. To handle different types of errors in the log
    - For any ELK related error, please reference to [ELK Ingestor]({{site.baseurl}}/docs/runbooks/palente/Runbook_PHE_ELK_Ingestor.html)
        - `Unexpected status code:401`: Please contact Shane Cartledge in North America time, or DuQian in CDL time to check LDAP proxy connection.
    - For any Database related error, please reference to [PHE EDB Ingestor]({{site.baseurl}}/docs/runbooks/palente/Runbook_PHE_EDB_Ingestor.html)
    - For any TIP API related error, please reference to [TIP Ingestor]({{site.baseurl}}/docs/runbooks/palente/Runbook_PHE_TIP_Ingestor.html)
    - If there are any abnormal behaviours, Please contact [Pa'lente team](#palente-contact-information).

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
{% include {{site.target}}/palente_tips.html %}





---
layout: default
description: Runbook for Signing service down
title: How to recovery Signing Service
service: oss signing service
runbook-name: Runbook for Signing service down
tags: oss, signing service
link: /doctor/Runbook_how_to_recovery_signing_service.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the signing service is down, monitored by New Relic.

## Technical Details

The reason for this alert could be one of the following:
  1. ICD mongodb down.
  2. KeyProtect service not available.
  3. Network error


## User Impact

Users who need sign his/her ssh public key will failed.

## Instructions to Fix


1. Double check the URL status:

   ```
   https://pnp-api-oss.cloud.ibm.com/sshkeysigning/v1/certificates/healthz
   ```

2. If response code is 200, means it is running well. just leave the alert as it is, it will be closed soon.


3. If response code is not 200, delete the target pod,

find the target cluster from the PD alert description, for example:

```
Description: oss-sshkey-signing-us-east-staging: Violated New Relic condition: oss signing service down. Details: Monitor failed for location Washington, DC, USA. Policy
```

from the description, we will know the target cluster is us-east staging.

```ibmcloud login --sso``` 

```ibmcloud ks cluster config --cluster $target_cluster_id```

```kubectl get po -n api | grep api-oss-sshkey-signing | awk '{print $1}' | xargs kubectl delete po -n api```

ps: if you don't have access to target cluster/namespace, ask Jim to grant your access.


4. if you can not fix it, contact csschen@cn.ibm.com or bjyanzh@cn.ibm.com.

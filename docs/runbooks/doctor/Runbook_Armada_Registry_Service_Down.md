---
layout: default
description: Runbook Armada Registry Service Down
title: RETIRED Runbook Armada Registry Service Down
service: armada_registry
runbook-name: Runbook Armada Registry Service Down
tags: oss, bluemix, doctor, armada_registry
link: /doctor/Runbook_Armada_Registry_Service_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

The registry service is deployed in 3 regions in Armada production `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.

This alert will be triggered if the Doctor registry service in Armada production monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. Armada reloading
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix

1. Following the runbook [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2) to get into aramda region.

2. When you get into the region, then run `kubectl get po -n doctor` to get the pod.

3. Get into registry pod, `kubectl exec -it <registry_pod> -n doctor bash`

4. Check if the API is reachable.

   `curl 10.154.56.42:2379/version -i`

   if it returned `200`, the alert should be resolved. If it failed, the armada maybe is reloading. Wait for 30 minutes and try the above command again. If the API failed again, escalate the alert in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}) or send mail to **csschen@cn.ibm.com**.

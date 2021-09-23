---
layout: default
title: "Palente - PHE service memory utilization high"
type: Alert
runbook-name: "api-oss-csd-memory-high"
description: "This alert will be triggered when a PHE pod is using more than 80% or 90% of allocated memory"
service: palente
tags: oss, palente, tip
link: /palente/Runbook_api-oss-csd-memory-high.html
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
This alert is triggered when a PHE pod is using more than 80% or 90% of allocated memory

## Technical Details
PHE is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region.

The NewRelic dashboard [Palente Services Dashboard](https://one.newrelic.com/launcher/dashboards.launcher?pane=eyJuZXJkbGV0SWQiOiJkYXNoYm9hcmRzLmRhc2hib2FyZCIsImVudGl0eUlkIjoiTVRreU5qZzVOM3hXU1ZwOFJFRlRTRUpQUVZKRWZHUmhPamcyT0RFNCIsInVzZURlZmF1bHRUaW1lUmFuZ2UiOmZhbHNlLCJpc1RlbXBsYXRlRW1wdHkiOmZhbHNlLCJlZGl0TW9kZSI6ZmFsc2UsInNlbGVjdGVkUGFnZSI6Ik1Ua3lOamc1TjN4V1NWcDhSRUZUU0VKUFFWSkVmREUyTlRJNE5qUSIsImlzU2F2aW5nRWRpdENoYW5nZXMiOmZhbHNlfQ==&platform[accountId]=1926897&platform[filters]=IihuYW1lIGxpa2UgJ1BhXFwnbGVudGUnIG9yIGlkID0gJ1BhXFwnbGVudGUnIG9yIGRvbWFpbklkID0gJ1BhXFwnbGVudGUnKSI=&platform[$isFallbackTimeRange]=false) you can see all the details of all pods running in all regions and identify possible problems with the pods.



## User Impact
Many users and applications rely on this service. PHE won't be unable to create pCIE/CIE's if the service failed.
It is very important for this service to be up and running at all times.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Restart the api-oss-csd pods in the affected region/environment [try restarting the api-oss-csd]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-restart-palente-services)
    - Run the following command to delete/force restart all `api-oss-csd` pods in the cluster:
      `kubectl oss pod delete -l app=api-oss-csd -n api`
    - Wait approximately 10 minutes and the NR alert should clear automatically.
    - Deleting the pod will trigger a healthz alert(PagerDuty) of the affected region. Snooze the healthz alert, it will get resolved in a few minutes.

## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations

Include the contacts for escalation when applicable.

{% include {{site.target}}/palente_tips.html %}

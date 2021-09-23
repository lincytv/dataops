---
layout: default
title: "API Platform - PnP Notifications Adapter MQ Errors"
type: Alert
runbook-name: "api.pnp-notifications-adapter-mq.down"
description: "Runbook to drill into errors related to MQ via the Notifications Adapter"
service: tip-api-platform
tags: pnp, apis, notifications, mq
link: /apiplatform/api.pnp-notifications-adapter-mq.down.html   
---

## Purpose
The pnp-notification-mq-SendNotifications transaction provides information about transactions sending messages to the message queue.

This alert applies to appName=`api-pnp-notifications-adapter-*` and:
- Service now incidents with a title: `api-pnp-notifications-adapter failed in posting MQ`
- New Relic incidents with the title containing text: `api-pnp-notif-adapter_MQPostFail`

## Technical Details
Only one kind of error will occur

- Post failure - indicates that the adapter was unable to successfully post a message to the message queue.

## User Impact

When this issue occurs, it means that users will not be able to see new or updated Announcements or Security Notices.

This alert should be treated with medium priority as it can affect the notifications viewed.  The runbook should be followed to resolve the incident if at all possible, but in the event that it cannot be resolved completely, this should be ok to leave for resolution on the next business day because the security and announcement notifications do not indicate outages and will be automatically updated when the issue is resolved.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Step 1

Gather logs from the failing container.  See `Viewing Logs` from the Notes section below.  Look for any logs that contain "ERROR" indications.  Some specific errors that apply to this incident are:

- `ERROR (%s): Could not bulk load notifications. [%s]`
- `ERROR (%s): Could not compare load notifications. [%s]`

Where `%s` will be substituted with the function name and error text.  Gather this information for the following steps.

### Step 2

Use the message queue runbooks located in the following location to further debug message queue issues.

{{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html

### Step 3

If all of the above did not resolve the problem or open an incident, then reassign the PagerDuty incident to `tip-api-platform level 2`. Be sure to include the error information gathered above in the incident.

## Notes and Special Considerations

### Viewing Logs

Unfortunately at this time, our logDNA solution is not complete.  logDNA is dropping data after the data limit has been reached.  Therefore it will be necessary to find the system manually via kubectl commands.

Examination of the logs from the notification adapter container should provide a clue.  Issue command such as:
```
kubectl logs api-pnp-notifications-adapter-645c8bfb9f-88m87 -c api-pnp-notifications-adapter
```

Where `api-pnp-notifications-adapter-645c8bfb9f-88m87` is the pod name of the notification-adapter.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

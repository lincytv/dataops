---
layout: default
description: Softlayer Network DShared Service Vyatta Down
title: Softlayer Network DShared Service Vyatta Down
service: doctor
runbook-name: Runbook Softlayer Network DShared Service Vyatta Down
tags: oss, bluemix, doctor
link: /doctor/Runbook_Softlayer_Network_DShared_Service_Vyatta_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_slack_constants.md %}

## Purpose
Only the Network team can handle this incident, but this Runbook can tell you how to address this problem and find the correct person to resolve this issue.

## Background
Based on IBM Cloud Gen 1 design, there should be a network isolation between "Public" and "Dedicated/Local".

The Network team created a network zone for "Public" named "Service Zone", and another network zone for "Dedicated/Local" named "DShared Zone".

There are some firewall devices (Vyatta) between these two networks. The "Vyatta" here has HA failover.

>**Note:** But we still encounter the "Vyatta" down incident on 2018/01/12, because the Vyatta HA fail over is failed.

## Technical Details
How to address the incident Softlayer Network "DShared" -> "Service" Vyatta down.

1. Find any public environments in Doctor that are "Red".
2. From you IBM network.
  * If you cannot ping 9.66.246.4 (which is in Service Zone, Dal09) or 9.66.246.5 (which is in Service Zone, WDC01).
  * **But can** ping 9.66.246.2 (which is in DShared Zone, WDC01), 9.66.246.3 (which is in DShared Zone, LON02).

3. If 1 and 2, there is something wrong in the "vyatta" device. We need notify the network oncall about this incident (DShared -> Service vyatta has some problems), and ask them to fix this incident as soon as possible.

## Finding the network team on call

From Slack, `@cybot who is oncall` in the slack channel [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) and find _Bluemix Network Schedule_.
![]({{site.baseurl}}/docs/runbooks/doctor/images/slack/cybot_who_oncall_sre_bluemix_networt.png){:width="640px"}

## User Impact
Doctor user can not connect to some (not all) public environments (e.g. **YP_DALLAS**,**YS0_LONDON**).

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

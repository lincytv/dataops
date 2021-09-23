---
layout: default
title: "API Platform - Scorecard UI Frontend is down"
type: Alert
runbook-name: "Runbook_Scorecard_UI_Failure.md"
description: "Pinging Scorecard Frontend health check failed"
service: tip-api-platform
tags: scorecard
link: /apiplatform/Runbook_Scorecard_UI_Failure.html   
---

## Purpose
To resolve Scorecard UI issues.

## Technical Details
It is rare that the Scorecard UI is down, it could be `https://cloud.ibm.com` is down, then report the issue [{{site.data[site.target].oss-slack.channels.console-scorecard.name}}]({{site.data[site.target].oss-slack.channels.console-scorecard.link}}). If it is only the Scorecard pages not accessible, then notify tip-api-platform level 2.

## User Impact
User cannot access the Scorecard UI.

## Instructions to Fix

### Health check for Scorecard frontend


1. Find out from the incident if it is production or staging that is failing.
2. Run the appropriate command for production or staging, if you got 200 status code, then that means Scorecard frontend is healthy, New Relic should resolve the incident soon; otherwise go to next step.
   ```
   Production:
   curl -v https://cloud.ibm.com/scorecard/healthz
   
   Staging:
   curl -v https://test.cloud.ibm.com/scorecard/healthz
   ```
3. Report the issue to [{{site.data[site.target].oss-slack.channels.console-scorecard.name}}]({{site.data[site.target].oss-slack.channels.console-scorecard.link}}), and reassign the PagerDuty incident to tip-api-platform level 2.


## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.cto-sre-dashboard.name}}]({{site.data[site.target].oss-slack.channels.cto-sre-dashboard.link}})

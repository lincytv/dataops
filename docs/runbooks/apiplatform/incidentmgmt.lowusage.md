---
layout: default
title: Low usage detected for Incident Management/concerns API
type: Alert
runbook-name: incidentmgmt.lowusage
description: "This alert indicates that there is a very low number of incoming requests on Incident Management/concerns API."
service: tip-api-platform
tags: tip, tip-api-platform, incident management, api
link: /apiplatform/incidentmgmt.lowusage.html
---

## Monitor Details:
Link to monitor: [{{site.data[site.target].oss-sosat.links.new-relic.name}}]({{site.data[site.target].oss-sosat.links.new-relic.link}})

Condition: `sosat.tip.incidentmgmt.lowusage`

## Overview
This alert indicates that there is a very low number of incoming requests on Incident Management /concerns API.

Root cause may be:

- Incident Management instances are no longer dispatched.
- Heartbeat test has been stopped (which should not happen) and no end user requests are send to Incident Management /concerns API.

## Response:
1. Acknowledge the alert in New Relic using the Acknowledge Link.
In New Relic (APM) select the `Incident Management API` App and check the violations shown in "Application Activity" section.

2. View Incident Details

What do we need to look for to determine root cause?

Identify critical Incident Management server(s) not receiving requests (see instructions in section 'Validate not a False Positive').

Escalate to level 2.


### Validate not a False Positive

1. Open [{{site.data[site.target].oss-sosat.links.new-relic.name}}]({{site.data[site.target].oss-sosat.links.new-relic.link}}), go to APM and select `Incident Management API` App.
2. Select MONITORING / Transactions in the navigator on the left
3. Click on `/incidentmgmtapi/api/v1/incidentmgmt/concerns` , this displays dashboard for /concerns api
4. Click `Servers` and select a server
5. Graph `Throughput` shows requests per minute received for the selected server
6. Verify selected server is receiving requests. If server does not receive requests check if the server is a production server (critical). Servers used in staging environment are less critical. You can ignore development servers.
7. Goto step 4 (select different server), repeat until you verified all servers receive requests

![image]({{site.baseurl}}/docs/runbooks/apiplatform/images/incidentmgmt_howto_lowusage.jpg){: width="700px", height="403px"}


### Log Location

[TIP Incident Management API - Finding Logs in Kibana]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingLogsInKibana.html)

[TIP Incident Management API - Finding Detailed Service Logs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingDetailedServiceLogs.html)


## Escalation:

**Critical:** If you found (production) servers not receiving requests and you cannot resolve in 30 minutes, contact [API Platform Team](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/ibm/Contact_OSS_DEV_Team.html) 

## Additional Information:
The [SOS Email Dashboard]({{site.data[site.target].oss-sosat.links.new-relic-insight.link}}/accounts/1387904/dashboards/302521) may also be helpful.



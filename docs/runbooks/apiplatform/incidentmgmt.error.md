---
layout: default
title: Incident Management API service application error
type: Alert
runbook-name: incidentmgmt.error
description: "This alert indicates that an instance of the Incident Management API service has an application error."
service: tip-api-platform
tags: tip, tip-api-platform, api, incident management
link: /apiplatform/incidentmgmt.error.html
---

## Monitor Details:  
Link to monitor: [{{site.data[site.target].oss-sosat.links.new-relic.name}}]({{site.data[site.target].oss-sosat.links.new-relic.link}})

Condition: `sosat.tip.incidentmgmt.error`

## Overview
An instance of the TIP Incident Management API service (TIP IM) has an application error.
This error shows up in multiple monitors.

For detailed analysis, TIP IM provides an application level log that can be consulted to analyze errors like the above.

Root cause may be:  

- Invalid input
  - A request to update an incident in ServiceNow cannot be performed because this incident is not found in that particular ServiceNow instance.
  - Specifically, it can happen that TIP IM tries to lookup the sysId for the incident number and fails. This happens when previously created incidents are deleted by admin personal and clients still have the incident number, e.g. for retry mechanisms.
  - Also, switching ServiceNow instances can cause this to happen as incident numbers are unique within one instance.
- Dependent system not available
  - ServiceNow

## Response:
1. Acknowledge the alert in New Relic using the Acknowledge Link.
In New Relic (APM) select the `Incident Management API` App and check the the "Error rate" dashboard for the timeframe when the error(s) occurred.

2. View Incident Details

What do we need to look for to determine root cause?

According to the two categories from above the errors are either:
- 4xx for invalid input or bad requests, or
- 5xx for ServiceNow problems

The next level of detail can be found in [{{site.data[site.target].oss-sosat.links.activity-tracker.name}}]({{site.data[site.target].oss-sosat.links.activity-tracker.link}}). Open the predefined search `IncidentMgmt-Concerns` and select the timeframe from above. Each individual request should be logged with the its error code (reason.reasonCode).
In case invalid input is passed to TIP IM API, contacting the client requestor based on the information in Activity Tracker is required.

In case of ServiceNow not available check the current status using `{{site.data[site.target].oss-sosat.links.tip-incidentmgmtapi.link}}/healthcheck` and determine if the problem still exists (check info provided in field ```BackgroundServiceStatus```). In this case open a defect as described under section "ServiceNow" in `{{site.data[site.target].ghe.repos.cloud-sre.link}}/world-of-tip#servicenow`

For all cases it might be required to check the TIP IM API application logs. This document [How to TIP Incident Management API- Finding Logs in Kibana]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingLogsInKibana.html) describes ho to find them.

### Validate not a False Positive
In general check if the error shows up in two monitors. E.g. In case this showed up in the logs (Kibana), to verify that this is not a false positive, check if the request also shows in Activity Tracker with ( field `outcome` has value **other than** `succeed`).

### Log Location

[TIP Incident Management API - Finding Logs in Kibana link]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingLogsInKibana.html)

[TIP Incident Management API - Finding Detailed Service Logs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingDetailedServiceLogs.html)



## Escalation:
This depends also on the above defined categories:

In case the monitors detail that the backend (ServiceNow) is not available, this is:
**Critical:** If you cannot resolve in 30 minutes, contact Manager via PagerDuty. Also open a defect as outlined above. This pages the ServiceNow team.

In other cases it is:
**Low:** If you cannot resolve in 30 minutes email {{site.data[site.target].oss-sosat.contacts.sosat-support-contact.name}} [{{site.data[site.target].oss-sosat.contacts.sosat-support-contact.link}}](mailto:{{site.data[site.target].oss-sosat.contacts.sosat-support-contact.link}})


## Additional Information:
The [SOS Email Dashboard]({{site.data[site.target].oss-sosat.links.new-relic-insight.link}}/accounts/1387904/dashboards/302521) may also be helpful.

## Owners
* owner1@us.ibm.com
* owner2@ie.ibm.com

\(try to spread out coverage\)

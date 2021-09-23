---
layout: default
title: Incident Management API service down
type: Alert
runbook-name: incidentmgmt.down
description: "This alert indicates that an instance of the Incident Management API service went down and does not start/restart, or unexpectedly restarts."
service: tip-api-platform
tags: tip, tip-api-platform, api, incident management
link: /apiplatform/incidentmgmt.down.html
---

## Monitor Details:  

Link to monitor: [Echometer (in WuKong)]({{site.data[site.target].oss-doctor.links.wukong-portal.link}})

Condition: `sosat.tip.incidentmgmt.down`  (PD alert: Echometer URL Down Failure: Service: incidentmgmt)

## Overview

In this case an instance of the TIP Incident Management API service went down and does not start/restart, or unexpectedly restarts. Instructions also cover case of a newly created Incident Management docker image which fails to start.

Root cause may be:  
- Start Problems
- Runtime Problems
- New Docker image has issues

## Response:

What do we need to look for to determine root cause?

- The service runs in a container and is started by script ```startFromDocker.sh```. Logs written by the script are useful to detect runtime problems (e.g. unexpected restart of the service). Logfile ```incidentmgmt_console.log``` contains these logs. See document [How to TIP Incident Management API - Finding Detailed Service Logs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingDetailedServiceLogs.html) for instructions to get to the logfile.

- In case service went down and does not restart please follow instructions in [Analyzing Service Start/Restart Issue]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_AnalyzingServiceStartError.html)

- In case a newly created docker image does not start, try to deploy previously running version of the image, then following instructions in [Analyzing Service Start/Restart Issue]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_AnalyzingServiceStartError.html) to analyze start issue of new image.


### Validate not a False Positive

You have two options

1. open a browser enter `{{site.data[site.target].oss-sosat.links.tip-incidentmgmtapi.link}}/healthcheck` in the location bar.
2. open a terminal and run `curl {{site.data[site.target].oss-sosat.links.tip-incidentmgmtapi.link}}/healthcheck`

Response from 1. or 2. looks like example below. `status: 0` in health section indicates service is operational.
Section 'apiservicestat' includes additional status info.
```
{
	"service": "tip_incidentmgmtapi",
	"version": 1,
	"health": [{
			"plan": "Free",
			"status": 0,                         <==== "status:" 0  means service is operational
			"serviceInput": "healthcheck",
			"serviceOutput": "service operational",
			"responseTime": 1971
		}
	],
	"apiservicestat": {
		"ServiceStartTime": "2017-12-06T04:21:26Z",
		"ServiceHostname": "a0ba80bc8a23",
		"ServiceIPAddress": "172.18.0.5",
		"ServiceInterfaces": "127.0.0.1/8 (lo),::1/128 (lo),172.18.0.5/16 (eth0),fe80::42:acff:fe12:5/64 (eth0)",
		"ServiceCatalogStatus": "Catalog registration: OK",
		"ServiceCatalogCode": 200,
		"ServiceCatalogStatusTime": "2017-12-06T12:31:06Z",
		"BackgroundServiceStatus": "ServiceNow connectivity: OK",
		"BackgroundServiceCode": 200,
		"BackgroundServiceStatusTime": "2017-12-06T12:31:17Z",
		"InfoStatsIntervalStart": "2017-12-06T12:11:29Z",
		"InfoStatsIntervalEnd": "2017-12-06T12:21:29Z",
		"InfoMaxResponseTime": 0,
		"InfoRequestCount": 8,
		"PostStatsIntervalStart": "2017-12-06T12:11:29Z",
		"PostStatsIntervalEnd": "2017-12-06T12:21:29Z",
		"PostMaxResponseTime": 0,
		"PostRequestCount": 0,
		"PatchStatsIntervalStart": "2017-12-06T12:11:29Z",
		"PatchStatsIntervalEnd": "2017-12-06T12:21:29Z",
		"PatchMaxResponseTime": 1971,
		"PatchRequestCount": 12
	}
}

```
You can also check the NewRelic Monitoring Dashboard for Incident Management API:
`{{site.data[site.target].oss-sosat.links.new-relic.link}}/accounts/1387904/applications/63800548`



### Log Location
- For Kibana logs refer to document [How to TIP Incident Management API- Finding Logs in Kibana]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingLogsInKibana.html)

- For detailed logs refer to document [How to TIP Incident Management API - Finding Detailed Service Logs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/TIPIncidentManagement_FindingDetailedServiceLogs.html)


## Escalation:
**Critical:** If you cannot resolve in 30 minutes, contact Manager via PagerDuty

## Additional Information:
The [SOS Email Dashboard]({{site.data[site.target].oss-sosat.links.new-relic-insight.link}}/accounts/1387904/dashboards/302521) may also be helpful.

## Owners
* owner1@us.ibm.com
* owner2@ie.ibm.com

\(try to spread out coverage\)

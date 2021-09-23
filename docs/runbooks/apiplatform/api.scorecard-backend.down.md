---
layout: default
title: "API Platform - Scorecard Backend is down"
type: Alert
runbook-name: "api.scorecard-backend.down"
description: "This alert will be triggered if some endpoints of scorecard backend went down"
service: tip-api-platform
tags: api-scorecard, apis, backend, scorecard-backend
link: /apiplatform/api.scorecard-backend.down.html
---
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

## Purpose
This alert is triggered when Scorecard Backend API is not responding and/or NewRelic is not receiving metrics.

## Technical Details
Scorecard Backend API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 3 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-scorecard%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

Here is the API [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy)

## User Impact
[Scorecard UI Pages](https://cloud.ibm.com/scorecard) may not be able to show correctly. Users of the Scorecard Backend API will be unable to reach the specific endpoint.


## Instructions to Fix

### Check log in LogDNA
1. Login to [IBM Cloud](https://cloud.ibm.com) and switch to `OSS Account`

2. Goto [Logging](https://cloud.ibm.com/observe/logging) and click on `View LogDNA` of `LogDNA-OSS IKS`, this will open a new browser tab.

3. In left navigation bar, expand `SCORECARD` and select `api-scorecard-backend`

4. The view is preset to show only production log, you can switch to staging as you need.

5. If you see any exceptions or error in the log, please contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %} or {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}


### Check MongoDB connection
Running command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/healthz?isDBActive=true'
```
You should see a 200 OK response code with response like
```
{
    "href": "/api/v1/scorecardbackend/healthz",
    "code": 0,
    "description": "The API is available and operational."
}
```
If not, Scorecard backend may not connect to EDB mongoDB correctly. Please [check log in LogDNA](#Check-log-in-LogDNA) for any error and contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %} or {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}



### General issues

#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/getOSSRecords
Many APIs in scorecard backend rely on OSS records which is returned from GCOR API `https://pnp-api-oss.cloud.ibm.com/gcorapi/api/v1/gcor/scorecardData`.
To check if this API works, please run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/gcorapi/api/v1/gcor/scorecardData' \
  -H 'Authorization: <IAM_APIKEY>'
```
where `<IAM_APIKEY>` value can be get from `https://pimconsole.sos.ibm.com/SecretServer/app/#/home/folders/5138` under `PNPAPIKey - Prod`. (For staging API, use `ScorecardPNPServeAPIKey - stage`)

**Note:** For this specific API, you MUST use the APIKEY from vault, or you will get `unauthorized` error.

You should see a `200 OK` response code with response like
```
{
    "Segments": [
        {
            "schema_version": "1.0.14",
            ...

    "Tribes": [
        {
            "schema_version": "1.0.14",
            ...

    "Services": [
        {
            "schema_version": "1.0.14",
            ...

    "Environments": [
        {
            "schema_version": "1.0.11",
            ...

    "SegmentExtended": [
        {
            "schema_version": "1.0.14",
            ...

    "TribeExtended": [
        {
            "schema_version": "1.0.11",
            ...

    "ServiceExtended": [
        {
            "schema_version": "1.0.14",
            ...

    "EnvironmentExtended": [
        {
            "schema_version": "1.0.11",
            ...
}
```

If you receive 429 error code from GCOR API, this means the IAM_APIKEY used to query Global Cataglog is suspended, please contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, {% include contact.html slack=edb-admin-slack name=scorecard-1-name userid=edb-admin-userid notesid=edb-admin-notesid %} or {% include contact.html slack=oss-auth-slack name=oss-auth-name userid=oss-auth-userid notesid=oss-auth-notesid %} ASAP.

For other error code, check LogDNA `api-gcor-api` to see if there is any error and contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=oss-auth-slack name=oss-auth-name userid=oss-auth-userid notesid=oss-auth-notesid %}

If you received the expected data from GCOR, please run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/getOSSRecords' \
  -H 'Authorization: <IAM_APIKEY>'
```
To validate response, reference to [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy#/OSS%20Resources/get_scorecardbackend_api_v1_getOSSRecords)

If you didn't receive expected response, please [check log in LogDNA](#Check-log-in-LogDNA) and report error.


#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbAggregatedRollingMetrics?isNew=true
This API collects and processes EDB rolling metrics from EDB MongoDB and CIE data from PNP CIE and incident APIs, then returns the aggregated and rolling metrics.
Run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbAggregatedRollingMetrics?isNew=true' \
  -H 'Authorization: <IAM_APIKEY>'
```

You should see a `200 OK` response code with response like
```
{
    "provisioning": {
        "segmentAggregatedMetrics": {
            "58eda55b9babda00075a50d5": {
                "type": "provisioning",
                "ossinfo": {...},
                "aggregateMetric": {
                    "isAggregateToParent": true,
                    "last1h": 58.63,
                    "last4h": 58.63,
                    "last24h": 58.63,
                    "last7d": 71.18,
                    "last30d": 77.74
                },
                "rollingMetrics": [
                    {
                        "name": "Big Data Engines",
                        "ossid": "58eda55b9babda00075a50d5-58eda5669babda00075a50f8",
                        "location": "jp-tok",
                        "last1h": 100,
                        "last4h": 100,
                        "last24h": 100,
                        "last7d": 100,
                        "last30d": 100,
                        "servicenowIncidentsURL": "",
                        "last_update": "0001-01-01T00:00:00Z"
                    },
                    ...
                ]
            },
            ...
        },
        "tribeAggregatedMetrics": {
            "58eda55b9babda00075a50d5-58eda5669babda00075a50f1": {...},
            ...
        },
        "serviceRollingMetrics": {
            "aiopenscale": {
                "type": "provisioning",
                "ossinfo": {...},
                "aggregateMetric": {...},
                "rollingMetrics": [...]
            },
            ...
        }
    },
    "consumption": {
        "segmentAggregatedMetrics": {...},
        "tribeAggregatedMetrics": {...},
        "serviceRollingMetrics": {...}
    },
    "cie": {
        "segmentAggregatedMetrics": {...},
        "tribeAggregatedMetrics": {...},
        "serviceRollingMetrics": {...}
    }
}
```

Validate response data with [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy#/Availability/get_scorecardbackend_api_v1_edbAggregatedRollingMetrics)

1. If you see data problem in provisioning or consumption part, you need to check rolling metrics.
First, follow step to [check MongoDB connection](#check-mongodb-connection).

If mongoDB connection has no problem, run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbRollingAvailability' \
  -H 'Authorization: <IAM_APIKEY>'
```
to check EDB rolling metrics.

You should see a `200 OK` response code with response like
```
{
    "resources": {
        "provisioning": [
            {
                "service": "functions",
                "status": "GA",
                "entryType": "SERVICE",
                ...
            },
            ...
        ],
        "consumption": [
            {
                "service": "availabilitymonitoring",
                "status": "GA",
                "entryType": "SERVICE",
                "serviceOwner": {
                ...
            },
            ...
        ]
    }
}
```
or reference to [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy#/Availability/get_scorecardbackend_api_v1_edbRollingAvailability)

If you see response code 200, but data is empty or very little, please contact {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %} or {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}.

For other problem, please [check log in LogDNA](#Check-log-in-LogDNA) and report error.

2. If you see problem in `cie` part,
CIE data are collected by querying PNP concerns API. Please run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/incidentmgmtapi/api/v1/incidentmgmt/concerns' \
  -H 'Authorization: <IAM_APIKEY>'
```
to check if PNP concerns API is working as expected. Reference to [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/specs/incidentTIP.yaml&no-proxy#/default/get_api_v1_incidentmgmt_concerns) for response code and data model. If there is any problem, please contact {% include contact.html slack=oss-auth-slack name=oss-auth-name userid=oss-auth-userid notesid=oss-auth-notesid %} or {% include contact.html slack=oss-platform-architecture-slack name=oss-platform-architecture-name userid=oss-platform-architecture-userid notesid=oss-platform-architecture-notesid %}.

If PNP concerns API returned expected data, verify CIE data by running command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/MappedCIEAvailability' \
  -H 'Authorization: <IAM_APIKEY>'
```

You should see a `200 OK` response code with response like
```
{
    "resources": [
        {
            "service": "availabilitymonitoring",
            "status": "",
            "entryType": "",
            "segment": "Hybrid Cloud",
            "segmentID": "",
            "tribe": "AvailabilityMonitoring",
            "tribeID": "",
            "location": "us-south",
            "plan": "Lite",
            "component": "availabilitymonitoring",
            "lastUpdated": "2020-06-01T20:53:26.594349782Z",
            "last1d": [
                100,
                100,
                0
            ],
            "last7d": [
                100,
                100,
                0
            ],
            "last30d": [
                100,
                100,
                0
            ],
            "mttr": [
                0,
                0
            ],
            "last30dIncidents": null,
            "servicenowIncidentsURL": ""
        },
...
```
If not, please contact {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %} or {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}


#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbReportURLs
This API read availabilityReportURLs.json file from [scorecard backend repo](https://github.ibm.com/cloud-sre/scorecard-backend/blob/master/availabilityReportURLs.json). The file is manually updated, so most of the time, the API problem is caused by wrong json format.
1. Check if the file is in the expected location with valid json content.
```
{
    "segments": [
        {
            "name": "",
            "sysdig_url": ""
        },
        ...
    ],
    "tribes": [
        {
            "name": "",
            "segment": "",
            "sysdig_url": ""
        },
        ...
    ],
    "services": [
        {
            "name": "",
            "segment": "",
            "tribe": "",
            "sysdig_url": ""
        },
        ...
    ],
}
```
2. If not, please contact {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}
3. Otherwise, check LogDNA and report error.


#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/certHealthStatus
Services provide list of certificate management CRN when they onboard to IBM Cloud. They also need to follow [service framework document](https://pages.github.ibm.com/ibmcloud/Security/guidance/certificate_management.html#certificate-manager) to give Scorecard function id `scorecar@cn.ibm.com` read access to their certificate manamgement instance, otherwise their certificate health information will not be collected.

Scorecard backend run a scheduled job to look through each service and their certificate management CRNs, query certificate management API against each CRN to collect metadata and save to mongoDB.

1. First, follow step to [check MongoDB connection](#check-mongodb-connection)

2. If mongoDB connection is good, run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/certHealthStatus' \
  -H 'Authorization: <IAM_APIKEY>'
```
Verify response with [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy#/OSS%20Resources/get_scorecardbackend_api_v1_certHealthStatus).

If API doesn't return proper amount of data (should be same as number of services, which is currently over 900), most likely the daily job which update mongoDB is interupted. Delete only one of `us-east` pod, when the pod is recreated, the mongoDB will be repopulated.

For any other error, please [check log in LogDNA](#Check-log-in-LogDNA) and report error.

#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/serviceCertList
This is a wrapper API of Certificate Manager API to collect certificates of a service.
1. Get Certificate Manager CRNs of the service
Run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/gcorapi/api/v1/gcor/services/<ServiceName>' \
  -H 'Authorization: <IAM_APIKEY>'
```
or access [Scorecard page of the service](https://cloud.ibm.com/scorecard/resources/<SegmentName>/<TribeName>/<ServiceName>?env=production)

`Certificate Manager CRNs` is under `Compliance` section.

2. For each CRNs, encode CRN to URL format and run command
```
curl -X GET \
'https://us-south.certificate-manager.cloud.ibm.com/api/v3/<encodedCRN>/certificates' \
-H 'Authorization: Bearer <IAM_TOKEN>'
```
where `<IAM_TOKEN>` value can be get by running command
```
curl -X POST 'https://iam.cloud.ibm.com/identity/token' \
-H 'Accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'grant_type=urn:ibm:params:oauth:grant-type:apikey' \
--data-urlencode 'apikey=<IAM_APIKEY>'
```

If response code is not 200, please report `Service name` and `Certificate Manager CRN` to slack channel {% capture oss-slack-oss-onboarding-name %}{{site.data[site.target].oss-slack.channels.oss-onboarding.name}}{% endcapture %} {% capture oss-slack-oss-onboarding-link %}{{site.data[site.target].oss-slack.channels.oss-onboarding.link}}{% endcapture %} and @dalec

If you can get certificates returned for the provided CRN, but can't get it in scorecard API, please [check log in LogDNA](#Check-log-in-LogDNA) and report error.

#### https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbMetricsCertification
Services certify their EDB availability metrics on Scorecard UI, the certified info are saved to mongoDB. This API collects and returns EDB metrics certification info from mongodDB.
1. First, follow step to [check MongoDB connection](#check-mongodb-connection).

2. If mongoDB connection is good, run command
```
curl -X GET \
  'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/scorecardbackend/edbMetricsCertification' \
  -H 'Authorization: <IAM_APIKEY>'
```
Verify response with [swagger doc](http://sretools2.rtp.raleigh.ibm.com/swagger-ui/dist/index.html?url=/ossspecs/scorecardBackend-swagger.yaml&no-proxy#/Availability/get_scorecardbackend_api_v1_edbMetricsCertification).

If you didn't receive response code 200, please [check log in LogDNA](#Check-log-in-LogDNA) and report error.


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

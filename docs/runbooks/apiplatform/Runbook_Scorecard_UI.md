---
layout: default
title: "Scorecard UI Support"
type: Alert
runbook-name: "Runbook_Scorecard_UI.md"
description: "General Scorecard UI support"
service: scorecard
tags: scorecard
link: /apiplatform/Runbook_Scorecard_UI.html   
---

{% include {{site.target}}/load_oss_contacts_constants.md %}

## Purpose
To resolve Scorecard UI issues.

## Technical Details
It is rare that the Scorecard UI is down, it could be `https://cloud.ibm.com` is down, then report the issue [console-scorecard](https://ibm-cloudplatform.slack.com/messages/CGGEAH2AE). For any other Scorecard UI related problem, please reference to this doc.

## User Impact
Scorecard UI doesn't work as expected.

## Instructions to Fix

### Scorecard page is blank


1. Right click on the page and select `inspect` (Chrome) or `inspect element` (Firefox)
2. Go to `consoles` tab and see if there is any error
3. If you see any errors that may cause the blank page, please report to {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %}.

### Data is missing or not shown as expected

First need to verify if the data is returned from scorecard backend API.

   > **Notes:**

    * Replace the `<ApiKey>` with your own api key, you can get it from [{{doctor-portal-name}} profile info]({{doctor-portal-link}}/#/profile/info) for [more info about ApiKey]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)

    * Replace hostname to `pnp-api-oss.test.cloud.ibm.com` if test with staging site.


1. For cloud availability `Missed SLA` page, run command
```
curl -X GET \
'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/edbAggregatedRollingMetrics?isNew=true' \
-H 'Authorization: <APIKEY>'
```
2. For OSS Resources and Environment data, run command
```
curl -X GET \
'https://pnp-api-oss.cloud.ibm.com/scorecardbackend/api/v1/getOSSRecords' \
-H 'Authorization: <APIKEY>'
```
3. For issue creator, run command
```
curl -X GET \
'https://pnp-api-oss.test.cloud.ibm.com/issuecreator/api/v1/issuecreator/getWorkflows' \
-H 'Authorization: <APIKEY>'
```
4. For issue tracker services data, run command
```
curl -X GET \
'https://pnp-api-oss.test.cloud.ibm.com/issuecreator/api/v1/issuecreator/getSFServices' \
-H 'Authorization: <APIKEY>'
```
5. For issue tracker workflows data, run command
```
curl -X GET \
'https://pnp-api-oss.cloud.ibm.com/issuecreator/api/v1/issuecreator/getSFIssuesByPillar' \
-H 'Authorization: <APIKEY>'
```
6. For issue tracker workflows data of particular service/pillar, run command
```
curl -X POST 'https://pnp-api-oss.cloud.ibm.com/issuecreator/api/v1/issuecreator/getSFIssuesByPillarFilter' \
-H 'Authorization: <APIKEY>' \
-D '{
	"workflow": "Q3 2020 Currency",
	"serviceName": "appid",
	"pillar": "ARCH"
}'
```
7. For TIP onboard data, run command
```
curl -X GET \
'https://pnp-api-oss.test.cloud.ibm.com/scorecardbackend/api/v1/getTIPOnboardStatus' \
-H 'Authorization: <APIKEY>'
```
8. For Certificate Health report, run command
```
curl -X GET \
'https://pnp-api-oss.test.cloud.ibm.com/scorecardbackend/api/v1/certHealthStatus' \
-H 'Authorization: <APIKEY>'
```

If any of the CURL command returns error or wrong data, please reference to [scorecard backend runbook](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.scorecard-backend.down.html).

For issue creator or tracker related API (3, 4, 5, 6, 7), please contact Gabriel Avila.


If confirmed that data are returned correctly from backend API, proceed to the next step.

You need to use scorecard function id `scorecar@cn.ibm.com` for the following operations. Please visit `https://github.ibm.com/hongling/scorecard_credential` to get necessary credentials. If you don't have access, please contact: {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}, {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}, {% include contact.html slack=tip-api-platform-manager-slack name=tip-api-platform-manager-name userid=tip-api-platform-manager-userid notesid=tip-api-platform-manager-notesid %} or {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %}

tip-api-platform-manager

**staging site**
1. Login to `http://cloud.ibm.com` with account `scorecar@cn.ibm.com`
2. Switch account to `1308775 - Core Test`
3. Access kubernates cluster `cloud-test-dal-10` with namespace `devtest`
4. Check container logs to see if there is any error.

**production site**
1. Login to `http://cloud.ibm.com` with account `scorecar@cn.ibm.com`
2. Switch to account `1390033 - IBM`
3. Go to `https://cloud.ibm.com/observe/logging` and click on `View LogDNA`
4. In `All Apps`, type in `scorecard` and select `scorecard` to show only scorecard logs
5. Check logs to see if there is any error.

If you see any error in the above logs, please contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=tip-api-platform-3-slack name=tip-api-platform-3-name userid=tip-api-platform-3-userid notesid=tip-api-platform-3-notesid %}.



### Data is not updated or synced with latest change
Scorecard UI caches data returned from backend APIs.
1. Cloud Availability data is updated every hour.
2. OSS Records data is updated once a day.
3. TIP Onboard status is updated every hour.
4. Issue creator and tracker is updated every 10 minutes.


Especially OSS Records data, user may make change in ServiceNow or Doctor scorecard. For scorecard UI to show the updated information, we need to wait for Dan Julin to run the update script from oss catalog first, then wait for GCOR and scorecard backend API daily job to refresh the cache. If we want to sync the data right away, after confirmed oss catalog is updated, we can force update GCOR API and scorecard backend API by restart all the pods in all regions. Then submit a new scorecard UI build to staging or production.

---
layout: default
description: PHE ServiceNow
title: PHE ServiceNow
service: palente
runbook-name: PHE ServiceNow Ingestor
tags: oss, palente, servicenow
link: /palente/Runbook_PHE_ServiceNow.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}

## Purpose
PHE ServiceNow ingestor is used to collect change requests from ServiceNow.

## Technical Details
PHE ServiceNow ingestor query ServiceNow change request search API to get a list of change request IDs within certain time frame, then loop through those IDs and query change request read API to get details of each change request. The job is run every one hour.

For search API, PHE search for each of the 3 states: `New`, `Scheduled`, `Implement`, the start time will be one hour before current timestamp, and end time is current timestamp. The API will return change request IDs as an array.
```
https://watson.service-now.com/api/ibmwc/change/search?starttime=<start time>&endtime=<end time>&searchInProgress=true&state=<statue>
```

For read API, change request ID is the result returned from previous search API.
```
https://watsontest.service-now.com/api/ibmwc/change/<change request ID>/read
```

For details of the APIs, please reference to [ServiceNow change request API doc](https://watson.service-now.com/kb_view.do?sysparm_article=KB0011868)


## User Impact
If PHE fail to get change request, it may mistakenly create/update pCIE against a service which is having a disruptive change request.

## Instructions to Fix
1. If alert is about `ServiceNow_API_Query_Counter`, this means PHE is querying ServiceNow API too many times and reaching request limit.
ServiceNow allows 30,000 request/hour, the token will be suspended if over the limit.
There could be something wrong in PHE that cause it keep querying ServiceNow API.

  - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
  - Select the **PALANTE**, then **OSS-CSD(Palante)**
  - Search for `start loading all CR`.
    - Check the timestamp of the log.
    - ![]({{ site.baseurl }}/docs/runbooks/palente/images/logDNA/servicenow_request_exceed.png){:width="600px"}
    - If there is any pod that is not log once per hour.
    - Find the pod.
    - Filter LogDNA to show full log of the pod
    - If there is any error
    - Delete the pod and report [Pa'lente team](#palente-contact-information).

2. Unauthorized: if the error message in the alert mentions that API call is unauthorized, get the API token from vault `/generic/crn/v1/internal/local/tip-oss-flow/global/oss-csd/sn_yp` and try the following command:
```
curl 'https://watson.service-now.com/api/ibmwc/change/search?starttime=2020-11-18 00:00:00&endtime=2020-11-18 22:27:00&searchInProgress=true&state=Implement' \
-H 'Authorization: Bearer <token>'
```
  - If get unauthorized error, please contact [Pa'lente team](#palente-contact-information).


## Palente contact information
{% include {{site.target}}/palente_contact_info.md %}

## Notes and Special Considerations
Include the contacts for escalation when applicable.

{% include {{site.target}}/palente_tips.html %}

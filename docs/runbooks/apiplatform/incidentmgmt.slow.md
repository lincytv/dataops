---
layout: default
title: "Incident Management API experiencing slow response times"
type: Alert
runbook-name: incidentmgmt.slow
description: "Runbook to describe the response for slow response times from Incident Management API service."
service: tip-api-platform
tags: api, tip-api-platform, incident management
link: /apiplatform/incidentmgmt.slow.html
---

{% capture cloud-platform-dev-1-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.slack }}{% endcapture %}
{% capture cloud-platform-dev-1-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.name }}{% endcapture %}
{% capture cloud-platform-dev-1-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.userid }}{% endcapture %}
{% capture cloud-platform-dev-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.notesid }}{% endcapture %}

{% capture cloud-platform-dev-2-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.slack }}{% endcapture %}
{% capture cloud-platform-dev-2-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.name }}{% endcapture %}
{% capture cloud-platform-dev-2-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.userid }}{% endcapture %}
{% capture cloud-platform-dev-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.notesid }}{% endcapture %}

## Monitor Details:  

This is a [New Relic APM application metric monitor]({{site.data[site.target].oss-sosat.links.new-relic-alert.link}}/accounts/1387904/policies/146070?filterName=sosat.tip.incidentmgmt.slow)
```
Critical - Response time (web) > 5 secs for at least 5 mins
Warn - Response time (web) > 2 secs for at least 5 mins
```

## Overview

TIP Incident Management API service (TIP IM) has a built-in monitoring component and is monitored by external systems like NewRelic. IM periodically checks several operational aspects that the IM service depends upon.

As part of this monitoring, an increase of response times is detected (slow transactions). Each Incident Management service instance depends on a Service Now backend. The latter can experience slow responses.

Root cause may be:  

- Network connectivity problem
- Internal ServiceNow problem
- High rate of incoming requests

## Response:

1. Acknowledge the alert in New Relic using the Acknowledge Link.
   - In New Relic (APM) select `Incident Management API` Application.
   - Check 'Application activity' for warning or critical violations of 'sosat.tip.incidentmgmt.slow' condition. You may also check "Error rate" dashboard, 'Web transaction time' and 'Transactions' data shown for the timeframe when slow responses occurred.

2. Check Service Now Response times
   - Open [NewRelic applications]({{site.data[site.target].oss-sosat.links.new-relic.link}}/accounts/1387904/applications) page
   - Search for Incident Management API, click on it
   - Click on 'Transactions' on the left
   - Sort transactions by 'Most time consuming'
   - Click on `/incidentmgmtapi/api/v1/incidentmgmt/concerns` , this will display the App server breakdown. ServiceNow response times are shown.  
   [Here is a link directly to this]({{site.data[site.target].oss-sosat.links.new-relic.link}}/accounts/1387904/applications/63800548/transactions#id=5b225765625472616e73616374696f6e2f476f2f696e636964656e746d676d746170692f6170692f76312f696e636964656e746d676d742f636f6e6365726e73222c22225d)

3. Check for open ServiceNow issues

### Validate not a False Positive

- Open [NewRelic incidents]({{site.data[site.target].oss-sosat.links.new-relic-alert.link}}/accounts/1387904/incidents) page.
- Go to the `Open incidents` tab
- Search for `sosat.tip.incidentmgmt.slow`
- Verify there are no open incidents for this condition.  
[Here is a direct link to that search]({{site.data[site.target].oss-sosat.links.new-relic-alert.link}}/accounts/1387904/incidents?offset=0&text=sosat.tip.incidentmgmt.slow&type=open)


### Log Location
- n.a.

## Escalation:
**Critical:** If you cannot resolve in 30 minutes, contact Manager via PagerDuty

## Additional Information:


## Contacts
**PagerDuty**  
* Production [{{site.data[site.target].oss-sosat.links.sosat-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-critical-alerts.link}})
* Dev or Test [{{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.link}})

**Slack**  
* [{{site.data[site.target].oss-slack.channels.sosat-monitor-prod.name}}]({{site.data[site.target].oss-slack.channels.sosat-monitor-prod.link}})  

**Runbook Owners**  
* {% include contact.html slack=cloud-platform-dev-1-slack name=cloud-platform-dev-1-name userid=cloud-platform-dev-1-userid notesid=cloud-platform-dev-1-notesid %}
* {% include contact.html slack=cloud-platform-dev-2-slack name=cloud-platform-dev-2-name userid=cloud-platform-dev-2-userid notesid=cloud-platform-dev-2-notesid %}

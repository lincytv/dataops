---
layout: default
title: "RMC Operations UI Healthz Failure"
type: Alert
runbook-name: "rmc.operations-ui.healthz.failed"
description: "This alert will be triggered when calling the RMC Operations UI healthz API failed"
service: tip-api-platform
tags: rmc, operations-ui, oss, healthz
link: /apiplatform/rmc.operations-ui.healthz.failed.html
---

## Purpose
Alert will be triggered when the RMC Operations UI healthz API can not successfully be called.

## Technical Details
The operatons-ui service is deployed in test (staging) us-south and eu-gb IBM Cloud Console Kubernete instances. The operations-ui service has three replicas in the us-south region and two replicas in the eu-gb region.

An API synthetic monitor has been set up in New Relic to monitor the global healthz endpoint from multiple locations. This synthetic monitor calls the operations-ui endpoint in the test.cloud.ibm.com console instance. The operations-ui service is NOT deployed in the production cloud.ibm.com console instance.

#### Policy, Conditions, and Synthetics:
- Policy: [oss-platform-registry-prd](https://one.newrelic.com/launcher/nrai.launcher?platform[accountId]=1926897&pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjEyODQ3MDQifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ)
    - rmc-operations-ui-healthz-global.stg-Condition
        - [rmc-operations-ui-healthz-global-stg](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLmxlZ2FjeS1tb25pdG9yLXNldHRpbmdzIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRkbU9ETm1aVEk0TFRRNVpXTXRORGxqWXkxaFpXUTRMVGhsTVdKaVpHVXlZV1E0TmcifQ==&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRkbU9ETm1aVEk0TFRRNVpXTXRORGxqWXkxaFpXUTRMVGhsTVdKaVpHVXlZV1E0TmciLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5sZWdhY3ktbW9uaXRvci1zZXR0aW5ncyJ9fQ==&platform[accountId]=1926897&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)

## User Impact
If the operations-ui healthz API is not responding correctly, it means that there is most likely a problem with the RMC Operations page itself. This will impact IBMers who are trying to on-board new services or make changes to existing ones in the RMC UI.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

Note that you will need logging and metrics access for some of steps below. If you don't already have access, please:
- Request access following the [https://github.ibm.com/console-pipeline/docs/blob/master/logging-metrics/README.md](https://github.ibm.com/console-pipeline/docs/blob/master/logging-metrics/README.md) instructions
- Contact Shane Cartledge or Emma Zhang in North America time, or GuYue in CDL time for access help

### Steps

1. Check [New Relic status page](https://status.newrelic.com/) to see if there is an ongoing outage or maintenance. The alert may be a false alarm.
2. Open the incident in NewRelic, click the link for the synthetic name (rmc-operations-ui-healthz-global-stg), and then press the `Re-check` button to see if the problem is already fixed
3. Check whether the oss pods are running in the associated Kubernetes clusters by:
   - Logging into https://cloud.ibm.com
   - Selecting the `2149966 - acefrtlg acefrtlg's Account` account
   - Opening the `console-test-sysdig` Sysdig instance
   - Clicking `Explore` on the left navigator
   - Selecting `Services` in the first drop down
   - Selecting `Kubernetes Pod Overview` in the second drop down
   - Searching for `oss` and drilling down and selecting the `oss` service
   - Checking the `Pod Reference` view
4. Check the logs of the oss pods by:
   - Logging into https://cloud.ibm.com
   - Selecting the `2149966 - acefrtlg acefrtlg's Account` account
   - Opening the `console-test-logdna` LogDNA instance
   - Selecting `oss` under Apps
5. Check whether any recent changes have been delivered that may have caused a problem
6. If the pod is running fine and not logging any errors, the problem may be with Kubernetes or the network. Check the following Slack channels to see if there are known Cloud Console problems:
    - [#console-issues](https://ibm-cloudplatform.slack.com/archives/C6EA537U3)
    - [#console-cie](https://ibm-cloudplatform.slack.com/archives/CLJ4QQWNN)
7. Try restarting the `oss` pods by re-promoting the current test oss build:
   - Open the [Jenkins oss promote build](https://wcp-console-jenkins.swg-devops.com/job/promote/job/oss/build?delay=0sec)
   - Set the RELEASE field to same value as the last success build
   - Click `BUILD`
8. If you are stuck, reach out to Shane Cartledge, Emma Zhang, or GuYue depending on the time

## Contacts
**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [#oss-platform-onshift](https://ibm-cloudplatform.slack.com/archives/G01S292026S)

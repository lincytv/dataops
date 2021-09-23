---
layout: default
title: "RMC Operations UI Support"
type: Alert
runbook-name: "Runbook_Scorecard_UI.md"
description: "General RMC Operations UI Support"
service: operations-ui
tags: operations-ui
link: /apiplatform/Runbook_RMC_Operations_UI.html  
---

## Purpose

To resolve RMC Operations UI problems.

## Technical Details

It is rare that the RMC Operations UI is down, it could be the https://test.cloud.ibm.com console is down, then report the issue on the [console-issues](https://ibm-cloudplatform.slack.com/archives/C6EA537U3) Slack channel. It is also possible that RMC (https://test.cloud.ibm.com/onboarding) itself is down, then report the issue on the [rmc-adopters](https://ibm-cloudplatform.slack.com/archives/C5K3GQL6B) Slack channel. For detailed information about the RMC Operations UI, please see the [operations-ui wiki](https://github.ibm.com/cloud-sre/operations-ui/wiki).

## User Impact

If the RMC Operations UI is not working as expected, services may not be able to onboard or change their service details.

## Instructions to Fix

### Determine if the problem is in a backend API or the UI

1. Open the browser debug tools so that you can see the network traffic (F12 and then select the Network tab in Firefox)
2. Reload the RMC Operations page, recreate the problem, and look for errors in the Network tab
3. If there are errors on the Network tab, the problem is most likely in a backend API
4. If there are no errors on the Network tab, reload the page, recreate the problem, and this time look in the Console tab for errors
5. If there are errors in the Console tab but not the Network tab, the problem is most likely in the UI

### If the problem is in a backend API

Depending on the API call that is failing, there are different places you may need to check to get more information about the problem including who to contact for the failing API.

In general you will need to:
1. Inspect the RMC Operations UI server logs
2. Inspect the logs of the service that the RMC Opeartions UI server calls
3. Contact the owner of the API for help

Instructions on how to perform 1, 2, and 3 are available in the [Architecture and dependencies](https://github.ibm.com/cloud-sre/operations-ui/wiki/Architecture) wiki document.

### If the problem is in the UI

The problem was most likely just introduced by a recent update to the operations-ui code running on test.cloud.ibm.com. Check the [operations-ui v1.0](https://github.ibm.com/cloud-sre/operations-ui/tree/v1.0) commit history to see what has changed recently.

If the operations-ui code has not changed recently, reach out to the RMC team to see if they have made any changes recently. Contact [Robert Szaloki](https://w3.ibm.com/bluepages/profile.html?uid=ZZ03LF740) via Slack if he is available or the [rmc-adopters](https://ibm-cloudplatform.slack.com/archives/C5K3GQL6B) Slack channel if not.

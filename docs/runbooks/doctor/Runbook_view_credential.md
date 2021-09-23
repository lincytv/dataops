---
layout: default
description: How to resolve issues when viewing the credentials of an IBM Cloud environment and the credential field displays "bad encypt".
title: Incorrect/Missing Credentials for IBM Cloud Environment
service: doctor
runbook-name: "Incorrect/Missing Credentials for IBM Cloud Environment"
tags: oss, bluemix, doctor, credentials
link: /doctor/Runbook_view_credential.html
type: Alert
---


## Purpose

When viewing the credentials of a Bluemix environment (via clicking the "Eye" button), the credential field may display **"bad encrypt"**.

## Technical Details

Fetch credentials from the JML file and the customer cloud environment by integrating with JML on the Softlayer git server and calling the Softlayer API.

## User Impact

If this alert is triggered, a user will be unable to access the environment VM via BOSH cli, BOSH director, ccdb, or admin console.

## Instructions to Fix

In most cases, this will be resolved automatically within 30 minutes. The following instructions will fix the issue if we need to resolve it immediately.

1. Make sure the latest JML content can be fetched.
  - In the landing page, click the JML button of an environment, and make sure the JML content in the pop-up window contains the right credentials.

2. Retrieve the latest credentials of an environment.
  - Go to **Management -> Scheduler Task**. Underneath the specific environment, restart the task named **refresh_env_metadata**

3. Refresh the credentials in Doctor DB.
  1. If multiple environments need to refresh their credentials，go to **Management -> Scheduler Task**. Under Shared Scheduler Service, restart the task named *refresh_credentails*.
  2. If only one environment needs to refresh its credentials，go to **Inventory -> management**, click the  "Environment Info" button of the specific environment, click the "Sync" button, and then click "Save".

4. Validate the credentials.
  - On the landing page, click the "sync" button. After a successful sync (this may take up to 2 minutes) click the "eye" button of an environment to verify the credentials are displayed properly.


## Notes and Special Considerations
  {% include {{site.target}}/tips_and_techniques.html %}

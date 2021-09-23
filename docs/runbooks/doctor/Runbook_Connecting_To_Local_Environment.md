---
layout: default
description: Connecting to a Local Environment's VMware vSphere Web Client
title: Connecting to a Local Environment's VMware vSphere Web Client
service: doctor
runbook-name: Runbook connecting to local environment
tags: doctor
link: /doctor/Runbook_Connecting_To_Local_Environment.html
type: Informational
---

## Purpose

You may get a request from SREs trying to access the vSphere Web Client (or vCenter Client) of a customer's local environment.

## To get the vSphere Web Client URL

1. Load the VMware vSphere welcome page: `https://vcenter.<ENV_NAME>.bluemix.net/` e.g. `https://vcenter.scc.ca-east.bluemix.net/`

2. Click on the Log In to vSphere Web Client link. This will open a new page.

3. If the vSphere Web Client page opens successfully, you are all set and can provide this URL to the SRE.

4. If the vSphere Web Client page does NOT open successfully, try the following URL using the port from the unsuccessful URL: `https://vcenter.<ENV_NAME>.bluemix.net:<PORT_FROM_UNSUCCESSFUL_URL>/vsphere-client/`.

If this works, you are all set and can provide this URL to the SRE.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

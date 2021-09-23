---
layout: default
title: "EDB Synthetic Provisioning Issues"
type: Alert
runbook-name: "api.edb-synthetic-provisioning.error"
description: "This alert will be triggered when the EDB Synthetic Provisioning adapter fails to delete an instance it has provisioned"
service: tip-api-platform
tags: api-edb-synthetic-provisioning
link: /apiplatform/api.edb-synthetic-provisioning.error.html
---

## Purpose
Alerts will be triggered when the EDB Synthetic Provisioning adapter fails to delete an instance it has provisioned.

## Technical Details
The EDB Synthetic Provisioning adapter consumes from the edb.synthetic.provisioning queue as new provisioning requests are triggered by the edb metrics backup adapter.  The RC API is used to try and provision a service/plan/location.  If an instance already exists and is active, it will be deleted first.  After a successful provision, the instance will be deleted.


## User Impact
If EDB is unable to delete a provisioned instance it will be unable to perform a new provisioning test for the service, plan and location of the instance that failed to delete.

## Instructions to Fix

### `api-edb-adapter-synthetic-provision_error`

Manually try to delete the instance using ibmcloud cli.  

Obtain the GUID for the failing instance by viewing the NewRelic Dashboard named [EDB Synthetic Provisioning - Staging](https://insights.newrelic.com/accounts/1926897/dashboards/1564469) if the incident is for the staging environment or [EDB Synthetic Provisioning - Production](https://insights.newrelic.com/accounts/1926897/dashboards/1587171) for production and look at the `Delete Instance Failures` chart.

Logon to cloud using ossedb@us.ibm.com apikey.  Obtain this from PIM:

Staging:
- [PIM Secret](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46423/general)
- `ibmcloud login --apikey <password> -a https://test.cloud.ibm.com`

Production
- [PIM Secret](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46424/general)
- `ibmcloud login --apikey <password> -a https://cloud.ibm.com`


You can delete an instance of a service from the IBM Cloud CLI by running the following command:

`ibmcloud resource service-instance-delete <GUID>`

Replace GUID with the value obtained from the New Relic Dashboard above.

If the command fails to delete the instance, try to get some help from the [#rc-adaptors](https://ibm-cloudplatform.slack.com/archives/C4V9KLLEL) slack channel or open a support case.


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.edb.name}}]({{site.data[site.target].oss-slack.channels.edb.link}})

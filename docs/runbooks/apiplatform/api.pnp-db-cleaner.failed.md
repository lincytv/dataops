---
layout: default
title: "PnP DB Cleaner issues"
type: Alert
runbook-name: "api.pnp-db-cleaner.failed"
description: This alert will be triggered if DB Cleaner is down or did not work properly.
service: tip-api-platform
tags: db-cleaner
link: /apiplatform/api.pnp-db-cleaner.failed.html
---

## Purpose
Alerts will be triggered if DB Cleaner down or failed.

## Technical Details
The pinging and health checking of PostgreSQL and HAProxy Primary and Standby nodes are performed in pnp-db-cleaner component in production only, but these alerts are raised to Technical Foundation team and are supported by them.

api-pnp-db-cleaner also cleans up PnP database records for any closed incidents, maintenances, and notifications, archived resources, and expired subscriptions.
It also fixes any incidents, maintenances and watches that are not associated with a resource.

PnP DB Cleaner is deployed in 1 region in Armada `us-east` only, and there is only 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-db-cleaner%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)

## User Impact
- If api-pnp-db-cleaner is down, then pinging and health check to PostgreSQL and HAProxy cannot be performed.
- PnP incidents, maintenances and watches that are not associated with a resource are not fixed.
- Expired records in PnP database are not removed.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}



This runbook is for many incidents that triggered by `api-pnp-db-cleaner` . Please look for the title of the incident below, and follow the instructions there.

### PnP DB Cleaner down

   - `api-pnp-db-cleaner - no pnp-postgres-ping data`
   - `api-pnp-db-cleaner - no pnp-haproxy-ping data`
   - `api-pnp-db-cleaner down`

   When getting any of these 3 alerts, please check the slack channel [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) if there is any upgrade going on.  

   The first two alerts indicates NewRelic is not receiving any metrics regarding pinging PostgreSQL or HAProxy, most likely api-pnp-db-cleaner pod is down or got an error somewhere.

1. Check api-pnp-db-cleaner pod is running in `us-east`
  - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-db-cleaner%2522%257D%255D)
  - In the `Deployment Status` table at the bottom, check that 1 pod is running in `us-east` region
  - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows.
    - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.
    - Execute `kubectl oss pod get -napi -lapp=api-pnp-db-cleaner`
    - You should see 1 pod with the status `Running`, if status is different, execute `kubectl describe -napi po <pod name>` to see why it is not running properly.
  - If pod is running as expected there may be a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes, Postgresql database, or the underlying infrastructure, then [Contact TF squad]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).

2. Pod not in running state
   - If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state (see step 4) and also see collect error messages shown by running `kubectl describe po -napi <pod_name>`.
   - If there are panic errors in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.
   - You can attempt `kubectl oss pod delete <pod_name> -n api `, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or may be with the docker image for that pod (which can be found out using the kubectl describe command).
   - After the pod is recreated, wait for another half hour to see the incident is self-resolved. If all pods in all 3 regions are restarted and the incident is still not resolved, reassign the incident to tip-api-platform level 2.

3. Check NR APM metrics
  - Access [NR APM]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/applications/167237636)
  - This is the APM metrics for the production instance, if you want to know for `stage` change to the corresponding app name such as `api-pnp-db-cleaner-stage`  

4. Check logs in logDNA
  - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
  - The logs should give some indication on what the problem is.
  - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
  - In each region, in a cluster, execute  
    `kubectl logs  -n api -lapp=api-pnp-db-cleaner -c api-pnp-db-cleaner --tail=50`
    (The `--tail=50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)


### Errors occurred in PnP DB Cleaner

   - `api-pnp-db-cleaner failed to clean danglings`
   - `api-pnp-db-cleaner cleaning of database failed`

1. Check logs in logDNA or Kubernetes  
  - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
  - The logs should give some indication on what the problem is.
  - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
  - In each region, in a cluster, execute  
    `kubectl logs  -n api -lapp=api-pnp-db-cleaner -c api-pnp-db-cleaner --tail=50`
    (The `--tail=50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)
  - If the errors are related to PostgreSQL availability, then [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).
  - If the errors are api-pnp-db-cleaner coding issues, then reassign the PagerDuty incident to `tip-api-platform level 2`.

### Failed to reinit watch map in api-pnp-subscription-consumer

   - `api-pnp-db-cleaner reinit of watch maps failed`

1. Wait for half an hour to see if the incident is self-resolved. If not, do the following:
  - Check the logs in logDNA or Kubernetes as described in the above step for **api-pnp-subscription-consumer** of all 3 regions `us-east`, `us-south` and `eu-de`, see if there are any errors regarding `WMINIT`.
  - You might have to restart **api-pnp-subscription-consumer** pod by deleting the current pod, `kubectl oss pod delete -l app=api-pnp-subscription-consumer -n api`, then a new pod will be auto created.
  - After the pod is recreated, wait for another half hour to see the incident is self-resolved. If all pods in all 3 regions are restarted and the incident is still not resolved, reassign the incident to `tip-api-platform level 2`.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.api-platform-prd.name}}]({{site.data[site.target].oss-slack.channels.api-platform-prd.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-stg.name}}]({{site.data[site.target].oss-slack.channels.api-platform-stg.link}})  
* [{{site.data[site.target].oss-slack.channels.api-platform-dev.name}}]({{site.data[site.target].oss-slack.channels.api-platform-dev.link}})  

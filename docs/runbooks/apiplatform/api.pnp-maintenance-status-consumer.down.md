---
layout: default
title: "API Platform - PnP Maintenance Status Consumer is down"
type: Alert
runbook-name: "api.pnp-maintenance-status-consumer.down"
description: "This alert will be triggered when all instances of the PnP Maintenance Status Consumer went down"
service: tip-api-platform
tags: api-pnp-maintenance-status-consumer, maintenance
link: /apiplatform/api.pnp-maintenance-status-consumer.down.html
---

## Purpose

This alert is triggered when PnP Maintenance Status Consumer is not responding and/or NewRelic is not receiving metrics.

## Technical Details

PnP Maintenance Status Consumer is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. Every 5 minutes, it will run a job that will make a call to the PnP database and process those records. If it determines that a maintenance record needs a change in the state value, it will insert a MaintenanceInsert record into the RabbitMQ queue for nq2ds to process the update.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-status%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.

## User Impact

PnP Maintenance records will not be able to reflect their state value accurately as according to their `plannedStart` and `plannedEnd` times.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### `api-pnp-maintenance-status-consumer database failure`  

- Verify that Postgres is up and running and check if there are any current Postgres related alerts (https://github.ibm.com/cloud-sre/runbooks/blob/master/docs/runbooks/apiplatform/api.postgres.down.md)  
- Check the SQL statements from the log and ensure that the table exists in Postgres DB.  
- Check that the configuration for Postgres is correct. Check the beginning of the log to see if there were any startup errors in connection.
- Further investigation into the logs may be needed as duplicate key error, violating foreign key constraint could be one of the causes of the alert.   

### `api-pnp-maintenance-status-consumer is unresponsive`  

- Follow steps for `api-pnp-maintenance-status-consumer_down`. Restart the application if necessary.  

### `api-pnp-maintenance-status-consumer down`

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Verify if PnP Maintenance Status Consumer has been running regularly
    - Access [NewRelic Insights]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/query?hello=overview&query=SELECT%20%60pnp-RecordsSent%60,%20%60pnp-db-failed%60%20from%20Transaction%20WHERE%20appName%3D%27api-pnp-maintenance-status-consumer%27%20%20since%201%20day%20ago). Change the `appName` value in the query to `api-pnp-maintenance-status-consumer-stage` to see results for staging environment.  
    - Verify that there is a transaction record every 5 minutes. If not move onto the next step.
    - Verify that `pnp-db-failed` value is not true. If it is, check if there is an alert for PnP database. Otherwise move onto step 3.

3. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-status%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time. If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  
        - Execute `kubectl oss pod get -n api -l app=api-pnp-maintenance-status-consumer`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes, Postgresql database, or the underlying infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

4. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api `, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

5. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -n api -l app=api-pnp-maintenance-status-consumer -c api-pnp-maintenance-status-consumer --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.  


## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

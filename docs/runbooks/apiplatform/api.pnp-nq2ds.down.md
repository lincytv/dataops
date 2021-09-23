---
layout: default
title: "API Platform - PnP NQ2DS is down"
type: Alert
runbook-name: "api.pnp-nq2ds.down"
description: "This alert will be triggered when all instances of the PnP NQ2DS went down"
service: tip-api-platform
tags: api-pnp-nq2ds, nq2ds
link: /apiplatform/api.pnp-nq2ds.down.html
---

## Purpose
This alert is triggered when PnP NQ2DS is not responding and/or NewRelic is not receiving metrics.

## Technical Details
PnP NQ2DS (Any Queue to Data Store) is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. The PnP NQ2DS listens for messages on several queues which includes Incident, Maintenance, Status, Notification and Resource records. For each record it processes, it can insert, update or delete records in the PnP Postgres Database.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-status%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
PnP data will not be able to be stored properly in the data store.  


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### PnP NQ2DS process data database failure
- `api-pnp-nq2ds process case database failure`
- `api-pnp-nq2ds process incident database failure`
- `api-pnp-nq2ds process maintenance database failure`
- `api-pnp-nq2ds process status database failure`
- `api-pnp-nq2ds sendNoteToDB database failure`
- `api-pnp-nq2ds insertUpdateResource database failure`
- `api-pnp-nq2ds prd-db-reconnection-failed`

- If you get prd-db-reconnection-failed means the service lost the connection and it cannot be reestablished.
  * Check the logs
    - `kubectl oss pod get -l app=api-pnp-nq2ds -napi`
    ```
    kubectl oss pod get -l app=api-pnp-nq2ds  -napi
NAME                             READY   STATUS    RESTARTS   AGE
api-pnp-nq2ds-6b54478b8b-kdfjj   2/2     Running   0          103m
    ```
    - `kubectl -napi logs api-pnp-nq2ds-<podid> -c api-pnp-nq2ds`
    ```
    kubectl -napi logs api-pnp-nq2ds-6b54478b8b-kdfjj -c api-pnp-nq2ds
    ```
  * If see an error like the follow:
    ```
    Oct 12 10:33:54api-pnp-nq2ds-6b54478b8b-kdfjjapi-pnp-nq2dsError2020/10/12 14:33:54.271831 insert.go:369: Error in starting insert transaction:  sql: database is closed
Oct 12 10:33:54api-pnp-nq2ds-6b54478b8b-kdfjjapi-pnp-nq2ds2020/10/12 14:33:54.271915 utils.go:566: [pnp-abstraction@v1.0.24/db/utils.go->Delay:566] Transaction failed. Going to retry after 1 seconds.
Oct 12 10:33:56api-pnp-nq2ds-6b54478b8b-kdfjjapi-pnp-nq2dsError2020/10/12 14:33:56.272608 insert.go:369: Error in starting insert transaction:  sql: database is closed
Oct 12 10:33:56api-pnp-nq2ds-6b54478b8b-kdfjjapi-pnp-nq2ds2020/10/12 14:33:56.272689 utils.go:566: [pnp-abstraction@v1.0.24/db/utils.go->Delay:566] Transaction failed. Going to retry after 1 seconds.
Oct 12 10:33:57api-pnp-nq2ds-6b54478b8b-kdfjjgrapi-pnp-nq2dsError2020/10/12 14:33:57.273035 insert.go:369: Error in starting insert transaction:  sql: database is closed
Oct 12 10:33:57api-pnp-nq2ds-6b54478b8b-kdfjjrapi-pnp-nq2ds2020/10/12 14:33:57.273120 utils.go:566: [pnp-abstraction@v1.0.24/db/utils.go->Delay:566] Transaction failed. Going to retry after 1 seconds.s
    ```
    - Restart the service `kubectl oss pod delete -l app=api-pnp-nq2ds -napi`
    ```
    kubectl oss pod delete -l app=api-pnp-nq2ds -napi
    ```
  * Check the logs again, if the connection recovers, create a bug incident to report the problem. Otherwise continue the next steps.   
- If there are more than one active related alert, this could mean that the PnP Postgres database is down or not functional.
- Verify that Postgres is up and running and check if there are any current Postgres related alerts. See [Postgres runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.postgres.down.html).  
- Check the SQL statements from the log and ensure that the table exists in Postgres DB.  
- Check that the configuration for Postgres is correct. Check the beginning of the log to see if there were any startup errors in connection.  
- Further investigation into the logs may be needed as duplicate key error, violating foreign key constraint could be one of the causes of the alert.  

### PnP NQ2DS process data decryption error
- `api-pnp-nq2ds process case decryption error`
- `api-pnp-nq2ds process incident decryption error`
- `api-pnp-nq2ds  process status decryption error`
- `api-pnp-nq2ds  decodeAndMap-maintenance decryption error`
- `api-pnp-nq2ds  process notification decryption error`
- `api-pnp-nq2ds  process resource decryption error`  


- If there are more than one active related alert, this could mean that messages being posted to RabbitMQ queue are not encrypted correctly or at all. Contact 'tip-api-platform' Level 2 support team.  
- If there is only one of this type of alert active, then check the log for the specific message that was trying to be decrypted and where it came from.

### PnP NQ2DS post data encryption error
- `api-pnp-nq2ds  post case encryption error`
- `api-pnp-nq2ds post incident encryption error`
- `api-pnp-nq2ds post maintenance encryption error`
- `api-pnp-nq2ds post resource encryption error`  


- If there are more than one active related alert, this could mean that the encryption package used to encrypt messages before it gets put onto the RabbitMQ queue is not functioning correctly. Contact 'tip-api-platform' Level 2 support team.
- If there is only one of this type of alert active, then check the log for the specific message that was trying to be encrypted and where it came from.

### api-pnp-nq2ds down

1. Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  

2. Verify if PnP NQ2DS has been running regularly
    - Access [NewRelic Insights]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/query?hello=overview&query=SELECT%20%60pnp-mq-failed%60,%20%60pnp-db-failed%60%20from%20Transaction%20WHERE%20appName%3D%27api-pnp-nq2ds%27%20%20since%201%20day%20ago). Change the `appName` value in the query to `api-pnp-nq2ds-stage` to see results for staging environment.    

3. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-nq2ds%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time.   
        - Execute `kubectl oss pod get -l app=api-pnp-nq2ds  -n api`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with Kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Also, you can check if other PnP components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

4. If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod (which can be found out using the `kubectl describe command`).  

5. Check logs in logDNA
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.  
    - In each region, in a cluster, execute  
    `kubectl logs -n api -l app=api-pnp-nq2ds -c api-pnp-nq2ds --tail 50`
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.


**If there are panic errors or any other coding specific issue in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.**


## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

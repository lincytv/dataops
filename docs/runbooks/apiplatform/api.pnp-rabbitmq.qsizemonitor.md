---
layout: default
title: "API Platform - PnP RabbitMQ queues size exceeds threshold "
type: Alert
runbook-name: "api.pnp-rabbitmq.qsizemonitor"
description: "This alert will be triggered when specific queues in PnP RabbitMQ is encountering a problem"
service: tip-api-platform
tags: rabbitmq, apis, pnp, queue
link: /apiplatform/api.pnp-rabbitmq.qsizemonitor.html
---

## Purpose

This alert is triggered when specific queues in PnP RabbitMQ is encountering a problem (eg. long backlog of messages)
and/or NewRelic is not receiving metrics.

## Technical Details

PnP RabbitMQ is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. See
the [list of all RabbitMQ URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/RabbitMQ_for_OSS.html) per region and
cluster.

It might be an indication that we have a postgreSQL DB connection problem, when the connection can't be recovered after it has been lost, PnP consumers stopped working accumulating messages in the queues and process need to be restarted to connect to the DB.
We had experienced this problem mainly with `pnp_nq2ds` and `pnp_subscritpion_consumer`


## User Impact

If some queues in PnP RabbitMQ is not reachable, then the entire PnP flow is stopped or slowed down considerably. This
impact may be specific to a region, as we have RabbitMQ servers in each region/cluster.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. These monitors use NewRelic to get the number of elements in each queue, and each monitor run at specific NewRelic location, 
   sometimes the monitor fails becuase there an error in NewRelic, before to follow any of the next steps check the monitor in NewRelic and
   make sure it is not a NewRelic issue. 
   The PD alert has a URL like the follow:
   `https://synthetics.newrelic.com/accounts/1926897/monitors/97ab2d10-6f64-4818-98aa-599a5b14b2f3/results/717e2a4b-348e-4f1f-bf24-23858107c9bb`
   that points to the Synthetics monitor. 
   * Click Synthetics URL,it will open NewRelic at the monitor. 
   * Click on the **Re-Check** button first.
   * If **Passed** you are done, the alert will be resolved soon.
   * If not, click on **Failures** and make sure it is not a NewRelic failure, otherwise continue the runbook
   
2. Go to the corresponding RabbitMQ of the alert and verify that the queue backlog is not over 50 messages. Access
   the [RabbitMQ management UI]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/RabbitMQ_for_OSS.html) with
   the [RabbitMQ credentials]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html) and check under
   Queues tab. Ignore the message count for queue `pnp.deadletter.msgs`.

   **NOTE:**
   On RabbitMQ `Queues` page, under `Message rates` columns, as long as column `ack` value is `>=` column `incoming`
   value, then total messages value should be decreasing over time.
   

3. If there is a backlog, here are some commands you can run depending on the specific queue:

   | Queue Name                | Component                                 | Command                                                                                                                                      |
   | :------------------       | :----------------------------------       | :---------------------------------------------------------------------------------------------------------------------------- |
   | incident.nq2ds            | api-pnp-nq2ds                             | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code>                                                                      |
   | maintenance.nq2ds         | api-pnp-nq2ds<br>api-pnp-change-adapter   | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code><br><code>kubectl oss pod delete -l app=api-pnp-change-adapter -n api</code> |
   | notification.nq2ds        | api-pnp-nq2ds                             | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code>                                                                      |
   | resource.nq2ds            | api-pnp-nq2ds<br>api-pnp-resource-adapter | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code><br><code>kubectl oss pod delete -l app=api-pnp-resource-adapter -n api</code>|
   | status.nq2ds              | api-pnp-nq2ds                             | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code>                                                                       |
   | incident.subscription     | api-pnp-nq2ds                             | <code>kubectl oss pod delete -l app=api-pnp-nq2ds -n api</code>                                                                       |
   | maintenance.subscription  | api-pnp-maintenance-status-consumer       | <code>kubectl oss pod delete -l app=api-pnp-maintenance-status-consumer -n api</code>                                                 |
   | notification.subscription | api-pnp-notifications-consumer            | <code>kubectl oss pod delete -l app=api-pnp-subscription-consumer -n api</code>                                                     |
   | status.subscription       | api-pnp-status-consumer                   | <code>kubectl oss pod delete -l app=api-pnp-status-consumer -n api</code>                                                             |

   <br><br>
   The commands in the table above performs a `kubectl oss pod delete -l app=<deployment> -n <nameSpace>` for all pods of the affected component. 
   This effectively triggers the Kubernetes scheduler to spin up new pods to replace the ones have been deleted.

4. As long as the total message value is decreasing over time, there is nothing more to do but to wait it out.

If there is a problem with RabbitMQ,
then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

{% include_relative _{{site.target}}-includes/edb-ingestor-redirect.md %}

## OSS Links

[RabbitMQ down runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html)

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

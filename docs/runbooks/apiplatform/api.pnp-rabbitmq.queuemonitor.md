---
layout: default
title: "API Platform - EDB RabbitMQ queues is encountering a problem"
type: Alert
runbook-name: "api.pnp-rabbitmq.queuemonitor"
description: "This alert will be triggered when specific queues in EDB RabbitMQ is encountering a problem"
service: tip-api-platform
tags: rabbitmq, apis, edb, queue
link: /apiplatform/api.pnp-rabbitmq.queuemonitor.html
---

## Purpose

This alert is triggered when specific queues in PnP RabbitMQ is encountering a problem (eg. long backlog of messages)
and/or NewRelic is not receiving metrics.

## Technical Details

PnP RabbitMQ is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. See
the [list of all RabbitMQ URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/RabbitMQ_for_OSS.html) per region and
cluster.

## User Impact

If some queues in PnP RabbitMQ is not reachable, then the entire EDB flow is stopped or slowed down considerably. This
impact may be specific to a region, as we have RabbitMQ servers in each region/cluster.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Go to the corresponding RabbitMQ of the alert and verify that the queue backlog is not over 1000 messages. Access
   the [RabbitMQ management UI]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/RabbitMQ_for_OSS.html) with
   the [RabbitMQ credentials]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html) and check under
   Queues tab. Ignore the message count for queue `edb.deadletter.msgs`.
   
   To quickly check if the alert is a false positive without going to RabbitMQ, follow these instructions:
      1. Using https://ibm.pagerduty.com/incidents/PGUZNSG as an example of false positive, go to the first URL in the PD alert details: https://alerts.newrelic.com/accounts/1926897/incidents/253020634
      2. Click on the link to the right of Results
      ![image](..images/edb_pagerduty_incident_example.png){:width="700px"}
      3. If the error is something like -102 connect ECONNREFUSED, it means that during the execution of the test script it was not able to query/connect to the RabbitMQ API successfully. You can also view the Script log tab and see the same error `GET https://045ebf9b-1bad-4ba1-b3f0-fb6e6372a052.bkvfv1ld0bj2bdbncbeg.databases.appdomain.cloud:32206/api/queues/%2F/edb.synthetic.provision false
       rabbitmq queue size request failed with error : Error: connect ECONNREFUSED 169.61.60.36:32206 true`
      4. If the alert was real, the end of the Script log should display something like `The queue size for edb.synthetic.provision is 1751 and could signify a potential processing issue.`

   **NOTE:**
   On RabbitMQ `Queues` page, under `Message rates` columns, as long as column `ack` value is `>=` column `incoming`
   value, then total messages value should be decreasing over time.

2. If there is a backlog, here are some commands you can run depending on the specific queue:

   | Queue Name      | Component                           | Command                                                                                                                                      |
   | :--------------------------- | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
   | edb.mapping.raw.events                                      | api-edb-mapping-consumer            | <code>kubectl get pods -n api --no-headers=true | awk '/edb-mapping-consumer/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.hyperwarp.events                                        | api-edb-hooks-consumer              | <code>kubectl get pods -n api --no-headers=true | awk '/edb-hooks-consumer/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.synthetic.provision                                     | api-edb-adapter-synthetic-provision | <code>kubectl get pods -n api --no-headers=true | awk '/edb-adapter-synthetic-provision/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.status.sent.msgs                                        | api-edb-processing-status           | <code>kubectl get pods -n api --no-headers=true | awk '/edb-processing-status/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.adapter.metrics                                         | api-edb-adapter-metrics             | <code>kubectl get pods -n api --no-headers=true | awk '/edb-adapter-metrics/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.adapter.sysdig.{ausyd/default/eude/<br/>eugb/useast/ussouth} | api-edb-adapter-sysdig         | <code>kubectl get pods -n api --no-headers=true | awk '/edb-adapter-sysdig/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.adapter.tip                                             | api-edb-adapter-tip                 | <code>kubectl get pods -n api --no-headers=true | awk '/edb-adapter-tip/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.adapter.dryrun                                          | api-edb-adapter-dry-run             | <code>kubectl get pods -n api --no-headers=true | awk '/edb-adapter-dry-run/{print $1}' | xargs  kubectl delete -n api pod</code>|
   | edb.audit                                          | api-edb-audit             | <code>kubectl get pods -n api --no-headers=true | awk '/edb-audit/{print $1}' | xargs  kubectl delete -n api pod</code>|

   For New OSS Account, if you don't have enough access to execute `kubectl delete pod`, you can run following commands with kubectl oss plugin instead, or ask service admin help to execute commands in above table.

   | Queue Name      | Component                           | Kubectl oss command                                                                                                                                      |
   | :--------------------------- | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
   | edb.mapping.raw.events                                      | api-edb-mapping-consumer            | <code>kubectl oss edb delete api-edb-mapping-consumer</code>|
   | edb.hyperwarp.events                                        | api-edb-hooks-consumer              | <code>kubectl oss edb delete api-edb-hooks-consumer</code>|
   | edb.synthetic.provision                                     | api-edb-adapter-synthetic-provision | <code>kubectl oss edb delete api-edb-adapter-synthetic-provision</code>|
   | edb.status.sent.msgs                                        | api-edb-processing-status           | <code>kubectl oss edb delete api-edb-processing-status</code>|
   | edb.adapter.metrics                                         | api-edb-adapter-metrics             | <code>kubectl oss edb delete api-edb-adapter-metrics</code>|
   | edb.adapter.sysdig.{ausyd/default/eude/<br/>eugb/useast/ussouth} | api-edb-adapter-sysdig         | <code>kubectl oss edb delete api-edb-adapter-sysdig</code>|
   | edb.adapter.tip                                             | api-edb-adapter-tip                 | <code>kubectl oss edb delete api-edb-adapter-tip</code>|
   | edb.adapter.dryrun                                          | api-edb-adapter-dry-run             | <code>kubectl oss edb delete api-edb-adapter-dry-run</code>|
   | edb.audit                                          | api-edb-audit             | <code>kubectl oss edb delete api-edb-audit</code>|


   The commands in the table above performs a `kubectl delete pod` for all pods of the affected component. This effectively triggers the Kubernetes scheduler to spin up new pods to replace the ones have been deleted.

   If deleting the pods does not help to bring the queue count down (ie. the column `ack` value is **not** `>=` column `incoming` value) you can try to increase the replicas count:

   | Queue Name              | Directory in oss-charts             | Instructions                                                                                                                                         |
   | :------------------------ | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | edb.mapping.raw.events  | api-edb-mapping-consumer            | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-mapping-consumer`<br/>`kdep <region>-production-values.yaml`            |
   | edb.hyperwarp.events    | api-edb-hooks-consumer              | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-hooks-consumer`<br/>`kdep <region>-production-values.yaml`              |
   | edb.synthetic.provision | api-edb-adapter-synthetic-provision | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-adapter-synthetic-provision`<br/>`kdep <region>-production-values.yaml` |
   | edb.status.sent.msgs    | api-edb-processing-status           | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-processing-status`<br/>`kdep <region>-production-values.yaml`           |
   | edb.adapter.metrics     | api-edb-adapter-metrics             | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-adapter-metrics`<br/>`kdep <region>-production-values.yaml`             |
   | edb.audit     | api-edb-audit             | Increase `replicaCount` value in `values.yaml`<br/>`helm del --purge api-edb-audit`<br/>`kdep <region>-production-values.yaml`             |

   For New OSS Account, if you don't have enough access to execute `helm del --purge`, you can run following commands with kubectl oss plugin instead.
   
    | Queue Name              | Directory in oss-charts             | Instructions                                                                                                                                         |
   | :------------------------ | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | edb.mapping.raw.events  | api-edb-mapping-consumer            | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-mapping-consumer -n api`<br/>`kdep <region>-production-values.yaml`            |
   | edb.hyperwarp.events    | api-edb-hooks-consumer              | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-hooks-consumer -n api`<br/>`kdep <region>-production-values.yaml`              |
   | edb.synthetic.provision | api-edb-adapter-synthetic-provision | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-adapter-synthetic-provision -n api`<br/>`kdep <region>-production-values.yaml` |
   | edb.status.sent.msgs    | api-edb-processing-status           | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-processing-status -n api`<br/>`kdep <region>-production-values.yaml`           |
   | edb.adapter.metrics     | api-edb-adapter-metrics             | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-adapter-metrics -n api`<br/>`kdep <region>-production-values.yaml`             |
   | edb.audit     | api-edb-audit             | Increase `replicaCount` value in `values.yaml`<br/>`kubectl oss helm uninstall api-edb-audit -n api`<br/>`kdep <region>-production-values.yaml`             |

   
   For New OSS Account, you can also execute following commands with kubectl oss plugin instead, please replace $INCREASE_NUMBER.

   | Queue Name              | Directory in oss-charts             | Kubectl oss command                                                                                                                                         |
   | :------------------------ | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
   | edb.mapping.raw.events  | api-edb-mapping-consumer            | <code>kubectl oss pod scale api-edb-mapping-consumer --increase=$INCREASE_NUMBER -n api</code> |
   | edb.hyperwarp.events    | api-edb-hooks-consumer              | <code>kubectl oss pod scale api-edb-hooks-consumer --increase=$INCREASE_NUMBER -n api</code> |
   | edb.synthetic.provision | api-edb-adapter-synthetic-provision | <code>kubectl oss pod scale api-edb-adapter-synthetic-provision --increase=$INCREASE_NUMBER -n api</code> |
   | edb.status.sent.msgs    | api-edb-processing-status           | <code>kubectl oss pod scale api-edb-processing-status --increase=$INCREASE_NUMBER -n api</code> |
   | edb.adapter.metrics     | api-edb-adapter-metrics             | <code>kubectl oss pod scale api-edb-adapter-metrics --increase=$INCREASE_NUMBER -n api</code> |
   | edb.audit     | api-edb-audit             | <code>kubectl oss pod scale api-edb-audit --increase=$INCREASE_NUMBER -n api</code> |


   A good rule of thumb when increasing the replicas count is to first increase by 3, up to a max of double the original value. E.g. For edb-mapping-consumer, it originally had 6 replicas, I would first increase it to 9 and observe the queue message count. Usually this should be enough for it to start decreasing.

    **NOTE:**
    If queue count is not decreasing after increasing the replicas count, check the [health](https://cloud.ibm.com/kubernetes/clusters) of the worker nodes of the cluster. If the status is `Critical`, try to reload the worker node and announce that your are doing so in [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}). If you do not have permission to reload the worker node, ask for assistance in [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}).

3. As long as the total message value is decreasing over time, there is nothing more to do but to wait it out.

If there is a problem with RabbitMQ,
then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

{% include_relative _{{site.target}}-includes/edb-ingestor-redirect.md %}

## OSS Links

[RabbitMQ down runbook]({{site.baseurl}}/docs/runbooks/apiplatform/api.pnp-rabbitmq.down.html)

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

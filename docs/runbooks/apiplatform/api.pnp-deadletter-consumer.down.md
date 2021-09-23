---
layout: default
title: "API Platform - PnP/EDB Deadletter Consumer is down"
type: Alert
runbook-name: "api.pnp-deadletter-consumer.down"
description: "This alert will be triggered when all instances of the PnP/EDB Deadletter Consumer service went down"
service: tip-api-platform
tags: api-pnp-deadletter-consumer, api-edb-deadletter-consumer, rabbitmq, consumer, pnp, edb
link: /apiplatform/api.pnp-deadletter-consumer.down.html
---

## Purpose

This alert is triggered when PnP/EDB Deadletter Consumer is not responding and/or NewRelic is not receiving metrics.  

## Technical Details

PnP/EDB Deadletter Consumer is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.  

This component is a RabbitMQ consumer, all it does is read and log messages off of `pnp.deadletter.msgs` and `pnp.unrouted.msgs` queues for PnP Deadletter Consumer and `edb.deadletter.msgs` for EDB Deadletter Consumer.  

The NewRelic dashboard [API Platform Services Dashboard(PNP Deadletter Consumer)]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-deadletter-consumer%2522%257D%255D) or [API Platform Services Dashboard(EDB Deadletter Consumer)]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-edb-deadletter-consumer%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.  

## User Impact

If PnP/EDB Deadletter Consumer is not running, there is no user impact. The PnP/EDB flow does not depend on this component to work. It is a nice to have, not high priority.  

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check pods are running in all 3 regions
    - Access [API Platform Services Dashboard(PNP Deadletter Consumer)]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-deadletter-consumer%2522%257D%255D) or [API Platform Services Dashboard(EDB Deadletter Consumer)]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-edb-deadletter-consumer%2522%257D%255D)
    - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
    - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
        - Execute `kubectl oss pod get -napi -l app=api-pnp-deadletter-consumer` or `kubectl oss pod get -l app=api-edb-deadletter-consumer -n api`
        - You should see 1 pod with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_PnP_Healthz_Paths.html) have similar issue. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes, or the underlying infrastructure, [Contacting TF squad]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).  
    If the problem is with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

2. Check NR APM metrics
    - Access [NR APM]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/applications/167237692)  
    - This is the APM metrics for the production instance, if you want to know for `stage` or `dev` change to the corresponding app name such as `api-pnp-deadletter-consumer-stage` or `api-edb-deadletter-consumer-stage`.  

3. Check logs in logDNA or in Kubernetes  
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs should give some indication on what the problem is.
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
    - In each region, in a cluster, execute  
    `kubectl logs -napi -lapp=api-pnp-deadletter-consumer -c api-pnp-deadletter-consumer --tail 50` or `kubectl logs -napi -lapp=api-edb-deadletter-consumer -c api-edb-deadletter-consumer --tail 50`
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

If the pod is in a non-Running state you can try, first, collect logs from the pods in bad state and also see collect error messages shown by running `kubectl describe po -napi <pod_name>`.  
You can attempt `kubectl oss pod delete <pod_name> -napi`, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod(which can be found out using the kubectl describe command).

If there are panic errors in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

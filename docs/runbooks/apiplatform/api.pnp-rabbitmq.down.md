---
layout: default
title: "API Platform - PnP RabbitMQ is down"
type: Alert
runbook-name: "api.pnp-rabbitmq.down"
description: "This alert will be triggered when RabbitMQ is down or not working properly"
service: tip-api-platform
tags: rabbitmq, apis
link: /apiplatform/api.pnp-rabbitmq.down.html
---

## Purpose

This alert is triggered when PnP RabbitMQ is not responding and/or NewRelic is not receiving metrics.

## Technical Details

PnP RabbitMQ is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is 1 instance running. See the [list of all RabbitMQ URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/RabbitMQ_for_OSS.html) per region and cluster.

The rabbitmq library handles disconnections from the RabbitMQ server, and also attempts re-connection to either one of the 2 RabbitMQ URLs for the cluster at a time, if it can't connect to one of the URLs then it tries the other one, doing this indefinitely. When rabbitmq lib detects that the connectivity to RabbitMQ is unhealthy, it stops all producers from sending msgs, it ensures that no message are lost. As long as the connectivity to RabbitMQ is unhealthy, the producer will be in a stuck state as long as the connectivity gets back to normal.  

## User Impact

If PnP RabbitMQ is not reachable, then all consumers and producers will not be able to connect to RabbitMQ. This impacts the whole flow. This impact may be specific to a region, as we have RabbitMQ servers in each region/cluster.  

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

> The follow steps were provided by Shane as first steps to try
1. In the PagerDuty alert, click the Failure_Link to open the failure in NewRelic
2. For the latest failed result, client on 'View result'
3. Under Settings -> General, copy the Monitor URL
4. Run a curl command to see if you can reach the Monitor URL:
curl -v <Monitor_URL>
5. If the curl command fails, open a Case against the RabbitMQ team stating that the endpoint is not reachable

From the alert you should be able to see what environment and region it refers to. Check the alert in Newrelic, the small graph showing the threshold and the current value.  

- Check logs in logDNA or in Kubernetes  
  - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
  - The logs should give some indication on what the problem is.
  - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
  - In each region, in a cluster, execute for the specific component in the correct cluster/region  
    `kubectl logs -napi -lapp=<component_label> --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

The issue may be many things including network problems, Kubernetes cluster problems, or the pod is unable to send metrics to NewRelic which then it thinks there is something wrong but it's actually all good, check the [NewRelic status page]({{site.data[site.target].oss-apiplatform.links.new-relic-status.link}}) to see if there is any issue in the NewRelic side. Need to check other pods on the same region/cluster for the same problem, if one pod on the the same cluster have problems connecting to RabbitMQ then other pods that uses RabbitMQ should have the same problem, if not it is a pod-specifc problem which is most likely solvable with a kubectl delete.

You can access the [RabbitMQ management UI]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/pnp-rabbitmq-URLs.html) and check under Connections tab if the state of the connections are running. Also in this same tab you can see the Network column in the table showing From client/To client that activity is happening. These are indications that rabbitMQ is working. Need to make sure you connect to the correct RabbitMQ instance, there are many of them so need to be sure to cnnect to the right one.

If there is a problem with RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).

{% include_relative _{{site.target}}-includes/edb-ingestor-redirect.md %}

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

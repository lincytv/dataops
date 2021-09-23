---
layout: default
title: "PnP - Performance is slow"
type: Alert
runbook-name: "api.pnp-slow-performance"
description: "This alert is triggered when slow transactions are detected by NewRelic"
service: tip-api-platform
tags: pnp, apis, performance, slowness
link: /apiplatform/api.pnp-slow-performance.html
---

## Purpose

This alert is triggered when slow transactions are detected by NewRelic.  

## Technical Details

PNP APIs are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.  

The NewRelic dashboard [API Platform - PnP Performance]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/745595?duration=1800000) provides you with details of the performance of all API-PnP components, staging and production environments.  

## User Impact

If the performance is very degraded, it will directly impact custumers using the PnP APIs, as updates will take longer than expected to be available for them.  

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Check NewRelic  
    - Open [API Platform - PnP Performance]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/745595?duration=1800000) with your browser. This dashboard may not give you the answer to the slowdown, but gives an idea of how all components are performing.  
    - Open [NewRelic APM]({{site.data[site.target].oss-apiplatform.links.new-relic.link}}/accounts/1926897/applications)  
    - Find and open the component the alert claims to be the problem  
    - Under `Transactions`, in the left-side menu, you can see the transactions that are most time-consuming. Make sure you check both Web and Non-web transactions.  
    - If the problem can't be narrowed down, it's a good idea to check other components to see if they have similar performance problems, which may allow you find what the problem is.  
    - It's worth checking [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) slack channel for any changes or issues going on with Kubernetes.

2. Check logs in logDNA or Kubernetes
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
    - The logs may give some indication on what the problem is. e.g. a lot of requests(flooding), or a lot of errors, or maybe nothing is going on, or calls to the database is clearly taking a lot of time to complete.  
    - If you are unable to see logs in logDNA, you can see it using `kubectl` command.  
    - In each region, in a cluster, execute (change `<component_name>` with the actual name of the service. e.g. `api-pnp-status`)  
    `kubectl logs -napi -lapp=<component_name> -c <container-name> --tail 50`  
    The `--tail 50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed.

When you have identified where the slowness is, for example if the database is slow, we need to check if the same problem is occuring with other components that use the database. If the other components are having similar problem, we know that the database or networking is most likely the problem, not the application component. If the source of the slowness is not managed by us, then you need to contact the component owner, for Kubernetes and Postgresql database is the Technical Foundation squad, [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html), for RabbitMQ, then [contact RabbitMQ support team]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html).  

What we can try is to restart the pods running the app, to see if the issue disapears.  
`kubectl oos pod delete <pod_name> -napi `  

If there are panic errors or any other coding specific issue in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

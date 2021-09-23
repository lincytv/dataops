---
layout: default
title: "PnP Change Adapter is down"
type: Alert
runbook-name: "api.pnp-change-adapter.down"
description: "This alert will be triggered when all instances of the PnP Change Adapter service went down"
service: tip-api-platform
tags: api-pnp-change-adpater
link: /apiplatform/api.pnp-change-adapter.down.html
---

## Purpose
This alert is triggered when all instances of the PnP Change Adapter service went down.

## Technical Details
PnP Change Adapter is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there is at least 1 instance running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-change-adapter%2522%252C%2522like%2522%253Atrue%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
The pnp change adapter service will be unreachable and can not handle the maintenance records from Doctor or ServiceNow.

## Instructions to Fix

   {% include {{site.target}}/oss_bastion_guide.html %}

   When getting this alert, please check the slack channel [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) if there is any upgrade going on.  

1. Check pods are running in all 3 regions
   - Access [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-pnp-change-adapter%2522%252C%2522like%2522%253Atrue%257D%255D)
   - In the `Deployment Status` table at the bottom, check that all pods are running in all 3 regions
   - If unable to check the NewRelic dashboard, manually check with the `kubectl` command as follows
       - Configure kubectl to connect to a specific region and to the affected cluster, one at a time
       - Execute `kubectl oss pod get -n api -l app=api-pnp-change-adpater`
       - You should see 1 pod with the status `Running`, if status is different,execute `kubectl describe -n api po <podname>` to see why it is not running properly.
   - If all pods are running as expected there may have a networking problem or some issue with kubernetes. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underline infrastructure [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)


2. If the pod is in a non-Running state, you can collect logs from the pods in bad state(Follow step 3) and then attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one. If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)  

3. Check logs in logDNA
  - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html)
  - The logs should give some indication on what the problem is.
  - If you are unable to see logs in logDNA, you can see it using `kubectl` command.
  - In each region, in a cluster, execute  
    `kubectl logs  -n api -l app=api-pnp-change-adpater -c api-pnp-change-adpater --tail=50`

    The `--tail=50` option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed


  After the pod is recreated, wait for another half hour to see the incident is self-resolved. If all pods in all 3 regions are restarted and the incident is still not resolved, reassign the incident to tip-api-platform level 2.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

---
layout: default
title: "API Platform - PnP Heartbeat failed"
type: Alert
runbook-name: "api.pnp-heartbeat.failed"
description: "This alert will be triggered when PnP Heartbeat failed"
service: tip-api-platform
tags: heartbeat, apis
link: /apiplatform/api.pnp-heartbeat.failed.html
---

## Purpose

This alert is triggered when PnP Heartbeat failed.

## Technical Details

PnP Heartbeat is a synthetic monitor in NewRelic. The monitor queries the /incidents PnP Status API and ensures that at least one incident is returned.

There are 3 NR synthetic monitors per environment (stage, prod), one for each `us-south`, `us-east` and `eu-de`. You can find the monitors in [NewRelic Synthetics]({{site.data[site.target].oss-apiplatform.links.new-relic-synthetics.link}}), search for "PnP Heartbeat".  

If PnP Heartbeat has fired an alert, it means there maybe something wrong in the PnP Status API or in the connectivity with ServiceNow.

## User Impact

Can affect the ability for notifications such as BSPNs and Change records to be posted to the external status page via PnP.  This is high priority and must be resolved.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

Steps:

1. When this issue occurs, one of the first things to do is please post message to Slack channel #toc-avm and tag @tocavms to indicate there may be an issue posting CIEs and BSPNs.  This is necessary to give the AVMs a heads-up to this problem. Please post this message:
   ```
   @tocavms PnP has identified an issue that may limit the ability to post notifications such as CIEs and associated BSPNs to the external status page. The PnP team is currently working to resolve the issue as quickly as possible.
   ```
   Once this issue is resolved, please update the channel to let the AVMs know.

2. Check NewRelic to find out what error message the synthetic monitor is reporting
   - Click the NewRelic incident link in the PagerDuty incident
   - Within the NewRelic incident, click the `View result` links for the failure(s)
   - Click the `Script log` tab to get the details of the failure
   - Click the `Re-check` button to ensure that the problem still exists
3. Check PnP Status logs in LogDNA or in Kubernetes
    - From the alert you should be able to see what environment and region it refers to
    - See [logDNA links for each service]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/PNP_logDNA_links.html#pnp-status). Open logs for `PnP Status`.
    - If you are unable to see logs in LogDNA, you can see it using `kubectl` command:
        - In each region, in a cluster, execute for the specific component in the correct cluster/region:
           ```  
           kubectl logs -napi -lapp=api-pnp-status -c api-pnp-status --tail 100
           ```
        - Note that the `--tail 100` option indicates that it will get the last 100 lines of log entries of the pod, it can be changed or removed.
    - Some helpful text to search the pnp-status logs for:
        ```
        - Failed to query snow CIEs Error:
        - ERROR: failed to find CIEs due to bad status
        - Failed to filter snow CIEs Error:
        - conversion fail
        ```
4. If you see errors in the logs and you believe that restarting the pod could fix it, you can do so by executing the following to force a recreation of the pnp-status pods:
    ```
    kubectl oss pod delete -l app=api-pnp-status -napi 
    ```
5. If you feel that the incident is a false positive, check the [NewRelic status page]({{site.data[site.target].oss-apiplatform.links.new-relic-status.link}}) to see if there are any NewRelic outages
6. If you are sure that this is a NewRelic problem, open an issue with [NewRelic Support]({{site.data[site.target].oss-apiplatform.links.new-relic-support.link}}) to investigate

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

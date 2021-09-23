---
layout: default
title: "Scorecard / Global Catalog OSSRecord API Healthz Failures"
type: Alert
runbook-name: "api.scorecard-pod-down-in-k8s"
description: "This alert will be triggered when pinging or calling Scorecard or Global Catalog OSSRecord APIs' healthz failed"
service: tip-api-platform
tags: api-scorecard-backend, api-gcor-api
link: /apiplatform/api.scorecard-pod-down-in-k8s.html
---

## Purpose
Alerts will be triggered if one or more pods of an API Platform Scorecard backend component or Global Catalog OSSRecord API component is down.
Or, when NewRelic PING or API synthetic monitors for an Scorecard backend api or Global Catalog OSSRecord API component have failed.
In each region, there are 3 pod instances running depending on the component.


## Technical Details
Scorecard backend component or Global Catalog OSSRecord API component are deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 pod instances running.

PING and API synthetic monitors have been set up in New Relic to monitor the healthz url of API Platform components in each region (i.e. the URL tested is the regional URL for the API component so we know the test is calling the correct region).

NRQL monitors have also been set up to monitor pods for each Scorecard backend component in each region..

New Relic alerts policies that are monitoring Kube pods using NR API scripts globally (sev 1):
1. [oss_scorecard_k8s_global_prd]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/442094)
2. [oss_scorecard_k8s_global_stg]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/443431)

New Relic alerts policies that are monitoring Kube pods using NRQL conditions by region (sev 2):
1. [oss_scorecard_k8s_prd]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/442073)
2. [oss_scorecard_k8s_stg]({{site.data[site.target].oss-apiplatform.links.new-relic-alert.link}}/accounts/1926897/policies/443439)


## User Impact
The API component may not be reachable or functioning correctly so this alert is critical to resolve.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Scorecard Backend / Global Catalog OSSRecord API Healthz Failed or Pods down

1. Verify if API component is responding

    - Find out from the PagerDuty incident, which API component is failing, and production or staging environment, and whether it is failed globally or in a particular region.
    - Find for the proper URL based on the component and region from [Scorecard API Healthz URLs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Scorecard_Healthz_Paths.html), and click on the link or do **curl** command on it.
    - The response should be something like  
      ```
      {"href":"{{site.data[site.target].oss-apiplatform.links.scorecard-backend-api-prod.link}}","code":0,"description":"The API is available and operational."}
      ```
    - If the reply was as above with code:0, then we know that we have at least 1 region is up.
    - Continue to step 2 regardless of the reply, even if the reply is the same as the above, some problem may exist so we need check.


2. Check pods are running in all 3 regions

    - Check [{{site.data[site.target].oss-slack.channels.technical-foundation.name}}]({{site.data[site.target].oss-slack.channels.technical-foundation.link}}) to see if there are any upgrades currently going on with the affected environment.  
    - Manually check if pods are running is the affected regions with the `kubectl` command as follows
        - Configure kubectl to connect to a specific region and to the affected cluster, one at a time. If you don't know how to configure `kubectl` for each regions, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)
        - Execute `kubectl oss pod get -n api | grep scorecard` or `kubectl oss pod get  -n api | grep gcor` depends on the healthz api that is failing
        - You should see 3 pods with the status `Running`, if status is different continue to the next step
    - If all pods are running as expected there may have a networking problem or some issue with kubernetes. You can [check if other APIs]({{site.baseurl}}/docs/runbooks/apiplatform/How_To/APIs_Scorecard_Healthz_Paths.html) have similar issue. Also, you can check if other API Platform components in the same region are having issues or active alerts. Need to contact Technical Foundation squad if you believe there is problem with Kubernetes or the underlying infrastructure [Contact TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html).
    - If there are pods in non-Running state, you can first see the logs from the pods in bad state (see **Check logs** section below) and also see error messages shown by running `kubectl describe po -n api <pod_name>`.  
    - You can attempt `kubectl oss pod delete <pod_name> -n api`, this will delete the current pod and deploy a new one.  
    - If that does not work it could be some problem with Kubernetes or may be with the docker image of that pod, which can be found out using the `kubectl describe command`.  


3. Check logs in Kubernetes

      - In each region, in a cluster, execute
    `kubectl logs  -n api -l app=api-scorecard-backend -c api-scorecard-backend --tail=50` or `kubectl logs  -n api -l app=api-gcor-api -c api-gcor-api--tail=50`(The --tail 50 option indicates that it will get the last 50 lines of log entries of the pod, it can be changed or removed)
    - If the pod is in a non-Running state you can first check logs from the pods in bad state and also see error messages shown by running `kubectl describe po -napi <pod_name>`. Then you can attempt `kubectl oss pod delete <pod_name> -napi `, this will delete the current pod and deploy a new one. If that does not work it could be some problem with Kubernetes or maybe with the docker image for that pod(which can be found out using the kubectl describe command).
    - If there are panic errors or any other coding specific issue in the logs which are preventing the container to be in a Running state, reassign the PagerDuty alert to 'tip-api-platform' level 2.


If the problem continues then reassign the PagerDuty incident to tip-api-platform level 2.

## Contacts
**tip-api-platform level 2**
* [{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}).

**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.cto-sre-dashboard.name}}]({{site.data[site.target].oss-slack.channels.cto-sre-dashboard.link}})

---
layout: default
description: Runbook Selfhealing Scheduler Service Down
title: Runbook Selfhealing Scheduler Service Down
service: selfhealing-scheduler
runbook-name: Runbook Selfhealing Scheduler Service Down
tags: oss, selfhealing, scheduler
link: /doctor/Runbook_Selfhealing_Scheduler_Service_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This alert will be triggered if the OSS Selfhealing Scheduler service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The pod where the service is located has problem.
  3. Network problem.

## User Impact

Users who are using Selfhealing Scheduler functionality provided by this service will be affected.

## Instructions to Fix

1. Double check the URL status:

   ```
   curl https://us-east.pte.cf.w3.cloud.ibm.com/selfhealing/api/v1/healthz\?service=scheduler
   ```
   If it return is not `ok` about scheduler, please go to next step.

2. Re-create Selfhealing Scheduler service.(Selfhealing Scheduler service is **single instance** and deployed on **us-east** region by default)
   - Login to IKS us-east production cluster:
     ```
     ibmcloud login -a cloud.ibm.com -r us-east -g default --sso
     select account: OSSPTE (75959dfd03574da79e1c3d29fa29e83f) <-> 2073240
     ibmcloud ks cluster config --cluster bulp6evw0senqe743cc0
     ```
   - Check the pod status of Selfhealing Scheduler:
     ```
     get po -n pte|grep scheduler|grep -v logs
     ```
     * If the pod status is not **Running**,re-create pod by following command:
     ```
     kubectl delete pod <<pod_name>> -n pte
     ```
   - Check the pod log of Selfhealing Scheduler:
     ```
     kubectl logs -f <<pod_name>> -n pte
     ```
     * If the log contains **Listening on 0.0.0.0:4587, CTRL+C to stop**,that means the pod is up and running.
     * If the pod status not running and can't re-create due to some reason,we need re-deploy it to other IKS cluster,please go to step 3

3. Re-deploy Selfhealing Scheduler service to new IKS cluster.
   - Clone oss-chart git repository:
   ```
   git clone git@github.ibm.com:cloud-sre/oss-charts.git
   git branch <<your branch name>>
   git checkout <<your branch name>>
   vi oss-charts/pte-selfhealing-scheduler/useast-production-values.yaml
   #set the enabled value to false
   ```
   - If you want to re-deploy on us-south region:
   ```
   vi oss-charts/pte-selfhealing-scheduler/ussouth-production-values.yaml
   #set the enabled value to true
   ```
   - If you want to re-deploy on eu-de region:
   ```
   vi oss-charts/pte-selfhealing-scheduler/eude-production-values.yaml
   #set the enabled value to true
   ```
   - Submit pull request on https://github.ibm.com/cloud-sre/oss-charts,the CD pipeline will be triggered automatically once the PR merged.
   - Repeat step 2 with new cluster which deployed selfhealing scheduler service and verify the pod running status.
   - If the pod status still not running on new IKS cluster, please contact **csschen@cn.ibm.com** for help.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: Apply Kube Network Policy
title: Apply Kube Network Policy
service: schematics
runbook-name: 002 Apply Kube Network Policy
tags: oss, terraform, schematics, kube, Calico
link: /schematics/Runbook_apply_kube_network_policy.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}


## Purpose
This runbook is used for apply Calico network policy.

## Technical Details
Calico Network Policy is managed by IBM Schematics service. Any updates should be using Schematics service.

## Change Policy
1. [Here](https://github.ibm.com/cloud-sre/oss-terraform-prod/tree/master/iks/network-policy/policy) are the policies code

## Apply Policy Changes
1. Go to [IBM Cloud Console](https://cloud.ibm.com/schematics/overview), then switch to account #2117538
2. Go to [Schematics](https://cloud.ibm.com/schematics/overview) page
3. Find the Schematics workspace(workspace name is <kube cluster>+'-network-policy'), then click it got details page
4. Click `Actions->Pull latest` button on top-right of details page, then wait for the pull to complete.
5. Click `Generate Plan` button on the top-right
6. Carefully check the result of Plan, make sure only the version will be updated. No any resources will be `destroyed`
7. Click `Apply Plan` button on the top-right. After applied, check the policy by `calicoctl get GlobalNetworkPolicy`.


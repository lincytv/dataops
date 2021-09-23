---
layout: default
description: Upgrade Kube cluster
title: Upgrade Kube cluster
service: schematics
runbook-name: 001 Upgrade Kube cluster
tags: oss, terraform, schematics, kube
link: /schematics/Runbook_upgrade_kube.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}


## Purpose
This runbook is used for upgrade IKS cluster.

## Technical Details
IKS cluster is managed by IBM Schematics service. Any updates should be using Schematics service.


## Instructions to Fix
1. Go to [IBM Cloud Console](https://cloud.ibm.com/schematics/overview), then switch to account #2117538
2. Go to [Schematics](https://cloud.ibm.com/schematics/overview) page
3. Find the Schematics workspace(workspace name is same with kube cluster), then click it got details page
4. Click `Settings` tab on details page
5. Find and update `kube_version` variables to the target version
6. Click `Generate Plan` button on the top-right
7. Carefully check the result of Plan, make sure only the version will be updated. No any resources will be `destroyed`
8. Click `Apply Plan` button on the top-right. After applied, check the kube version again.

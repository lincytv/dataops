---
layout: default
title: "API Platform - Catalog service memory utilization high"
type: Alert
runbook-name: "api.api-catalog.memory-high"
description: "This alert will be triggered when an API Catalog pod is using more than 80% or 90% of allocated memory"
service: tip-api-platform
tags: catalog, apis
link: /apiplatform/api.api-catalog.memory-high.html
---

## Purpose
This alert is triggered when an API Catalog pod is using more than 80% or 90% of allocated memory

## Technical Details
Catalog API is deployed in 3 regions in Armada `us-south`, `us-east` and `eu-de`. In each region, there are 3 instances running.

The NewRelic dashboard [API Platform Services Dashboard]({{site.data[site.target].oss-apiplatform.links.new-relic-insight.link}}/accounts/1926897/dashboards/572530?filters=%255B%257B%2522key%2522%253A%2522deploymentName%2522%252C%2522value%2522%253A%2522api-api-catalog%2522%257D%255D) you can see all the details of all pods running in all regions and identify possible problems with the pods.


## User Impact
Many users and applications rely on this service to access the rest of our APIs. These services and users may be unable to get to another API if Catalog is not working.
It is very important for this service to be up and running at all times.


## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. Restart the api-api-catalog pods in the affected region/environment
    - Run the following command to delete/force restart all `api-api-catalog` pods in the cluster:
      `kubectl oss pod delete -l app=api-api-catalog -n api`
    - Wait approximately 10 minutes and the NR alert should clear automatically.

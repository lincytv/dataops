---
layout: default
description: CELL Resource Usage Data
title:  CELL Resource Usage Data
service: doctor
runbook-name: Runbook DEA Cell Resource Usage Data
tags: doctor, dea, usage
link: /doctor/Runbook_DEA_Cell_Resource_Usage_Data.html
type: Informational
---

## Where the CELL usage data is used

1. The resource usage graphs in each environment's cloud page
2. OpsConsole > Administration > Resource usage page
3. The Report > Utilization report in the Doctor Manager View
4. The memory/disk load percentage data in Monitor generated logs

## Calculation method

1. The physical usage data, including total data and used data, are accumulated by all CELLs.
2. The app reserved (or called "allocated") data are collected from all IBM and customer app data in CCDB. Taking the current YP_DALLAS memory load 80.73% as an example, we can calculate this percentage value in the following way:

   1. Get the numerator (reserved memory) from CCDB:
`SELECT sum(apps.disk_quota * apps.instances) as disk_sum, sum(apps.memory * apps.instances) as mem_sum FROM apps where apps.state='STARTED' and diego=true and (apps.package_state='STAGED' or apps.package_state='PENDING')`
Then the reserved memory is: mem_sum/1024 = 62068G.
   
   2. Get the denominator (max memory capacity) from BOSH:
Fetch all CELLs of the environment by looping all deployments and triggering  _<bosh_url>/deployments/<deployment>/vms?format=full_ for each one. Among them, 961 instances with job name "cell" have VM details. For each CELL VM, get its max over-commit capacity _properties.diego.executor.memory_capacity_mb_ from its deployment yml, and add them together. In YP_DALLAS' case, all Diego deployments' _properties.diego.executor.memory_capacity_mb_ is 81920, making the total max reserving capacity: 81920*961/1024=76880G.

   3. Use the max reserving capacity to divide the reserved memory, and get the memory load percentage:
62068/76880=80.73%.

## About Over Commit

With Over Commit, customers can deploy memory/disk * overcommit-factor from the memory/disk they purchase.

For example, D_MUFG purchased 64GB memory and with *2 overcommit-factor, the total memory that can be used with the charge in dedicated environments is 64GB x 2 = 128GB at no cost.

In the Diego YML, the defined max capacity is already multiplied by overcommit-factor, and thus we could use the value directly. E.g., in D_CIO, each CELL's physical memory is 32G, and its overcommited max capacity is 80G.

When the all_app_reserved_resource/max_reserving_capacity_from_bosh > 100% (the DISK/MEMORY RESERVED graph in Doctor), even though the physical usage might be far from 100%, CF will refuse any more app pushes and alert the "insufficient resource" error.

## About IBM app v.s. customer app

The app distribution between customer and IBM were not restricted, i.e., a cell is just randomly found to stage your app. Thus, there's no way to decouple IBM and customer app from cell perspective. 

From the app perspective, we can decide whether an app is from IBM or customer by checking whether its org is an internal org.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

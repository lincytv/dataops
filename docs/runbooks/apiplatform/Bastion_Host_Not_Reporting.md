---
layout: default
title: "API Platform - Bastion Host is not reporting"
type: Alert
runbook-name: Bastion_Host_Not_Reporting
description: "This alert will be triggered when a bastion host is not reporting"
service: tip-api-platform
tags: bastion
link: /apiplatform/Bastion_Host_Not_Reporting.html
---

## Purpose
To monitor bastion hosts are healthy. When bastion endpoint is not reporting, newrelic monitors the status of bastion hosts and reports when not responsive.

## Technical Details
Bastion hosts are deployed in the 9 IKS clusters. As an essential service of managing the OSS environments access, it is critical to monitor the health status of Bastion hosts and trigger alert if any Bastion host is not healthy.
If Newrelic detects this condition it issues an alert for the violation period.

## Instructions to Fix
Notify oss bastion admin at Slack channel #oss-account-migration-bastion.
Also you can contact yujunjie@cn.ibm.com and bjdqian@cn.ibm.com.

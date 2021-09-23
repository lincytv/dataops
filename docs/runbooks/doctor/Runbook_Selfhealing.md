---
layout: default
description: An overview of Self-healing functions
title: What is Self-healing
service: backend
runbook-name: Self-healing
tags: doctor,backend
link: /doctor/Runbook_selfhealing.html
type: Alert
---

## Purpose

Self-healing is to improve efficiency of Site Reliability Engineering (SRE) daily work by helping SRE handle some repeatable jobs automatically. It consists of the following two parts:

## Rule Management  

SRE can define some rules against PagerDuty Service. Once a PagerDuty incident matches the rule issued it will trigger the the action defined in the rule, such as execute a fix script, open an RTC work item, send notifications, etc.

## Scheduler Jobs  

SRE can add some scheduler jobs that will run with a specified interval like daily or hourly. For example, adding a scheduler job that is to check the status of the root password for all Virtual Machines (VM's) and reset it if the password will be expired.

## How does it works?  

### Rule Management  

When Self-healing receives a PagerDuty incident it will parse the incident to extract some required information for the trigger action, like environment information, and persist into database first, then match the incident with all pre-defined rules. If matched rules are found, it will trigger.  


### Scheduler Jobs  

There is a scheduler job management service to trigger all defined scheduler jobs. For now, scheduler jobs only support triggering the script on Doctor agent or management virtual machine in each cloud environment.


## Assumption and on-boarding process

### If the services are applications or servers

  1. [Configure Self-healing]({{site.baseurl}}/docs/runbooks/doctor/Runbook_configure_selfhealing.html)

### If the service are isolated server

  1. [Deploy Doctor Agent]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Deploy_Doctor_Agent_In_Dedicated_SL_Account.html)

  2. [Configure Self-healing]({{site.baseurl}}/docs/runbooks/doctor/Runbook_configure_selfhealing.html)

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

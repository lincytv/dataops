---
layout: default
description: RETIRED - This incident is created after Prometheus monitor detects a stopped Postgres database server.
title: RETIRED - Prometheus monitor detects a stopped Postgres database server
service: doctor
runbook-name: RETIRED - Runbook Postgres Server Down
tags: oss, prometheus, doctor, postgres, postgresql
link: /doctor/Runbook-Postgres-Server-Down.html
type: Alert
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}


# [FIRING:1] PostgresAlert ...

## Purpose

The incident is created after Prometheus monitor detects a stopped Postgres database server.

## Technical Details

A [{{repos-postgres-exporter-name}}]({{repos-postgres-exporter-link}}) for [{{prometheus-name}}]({{prometheus-io-link}}) is used to collect metrics describing the state of the Postgres database server.

When certain metrics meet certain criteria as described in **metric_relabel_configs** in **prometheus.yml**, see [{{wukong-portal-name}}]({{wukong-portal-link}}) -> Echometer-> Prometheus Configuration Files.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/prometheus_yml.png){:width="640px"}
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/metric_relabel_configs.png){:width="640px"}
An alert is created, see **prometheus.rules** in the same admin portal page.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/prometheus_rules.png){:width="640px"}

The alert is picked up by the [Alert Manager for Prometheus]({{prometheus-io-link}}/docs/alerting/alertmanager/), and the Pager Duty incident is created as described in **alertmanager.yml** under [{{wukong-portal-name}}]({{wukong-portal-link}}) -> Echometer->Other Services Configuration Files.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/alertmanager_yml.png){:width="640px"}
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/alertmanager_yml_content.png){:width="640px"}

## User Impact
A Postgres database is down. If it were the Slave, it needs to be restarted to continually serve as a replication to the Master. If it were the Master, a fail-over might have occurred and the Slave server might have become the new Master. Nevertheless, the down server needs to be restarted.

## Instructions to Fix
The IP of the down server is included in the title of the PD incident.
Access to the Postgres servers are restricted. Find one of the following to log into the server and issue a `service postgresql restart` command.
- {% include contact.html slack=sre-platform-chief-architect-slack name=sre-platform-chief-architect-name userid=sre-platform-chief-architect-userid notesid=sre-platform-chief-architect-notesid %}
- {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}
- {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}
- {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

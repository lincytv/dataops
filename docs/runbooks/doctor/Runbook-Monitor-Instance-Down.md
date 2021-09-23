---
layout: default
description: RETIRED - Alert triggered when Prometheus fails to get monitor metrics. Job X has been down for X minutes.
title: RETIRED - Prometheus failed to get monitoring metrics (Monitor-Instance-Down)
service: doctor
runbook-name: RETIRED - Monitor Instance Down
tags: oss, prometheus, doctor
link: /doctor/Runbook-Monitor-Instance-Down.html
type: Alert
---



{% include {{site.target}}/load_oss_doctor_constants.md %}

## Job X has been down for X minutes.

## Purpose
This alert is issued when Prometheus fails to get monitor metrics.

## Technical Details
This is an internal error: the monitor isn't working. Either the Prometheus monitor itself is down, or the monitor cannot get any metrics for the monitored target.

## User Impact
The state of the monitored target is unknown since monitoring had stopped.

## Instructions to Fix
1. Find the IP and port of the monitoring instance from the Title of the {{doctor-alert-system-name}} instance, for example: from incident title _9.37.201.34:5101 of job postgres has been down for more than 5 minutes_. The **IP** is _9.37.201.34_ and **port** is _5101_.
2. For 9.37.201.34:5101, you can check the status on the web page [{{prometheus-name}} echometer status ]({{site.data[site.target].oss-doctor.links.prometheus.link}}/?g0.range_input=1h&g0.expr=http_status_code_echometer&g0.tab=0).
![]({{site.baseurl}}/docs/runbooks/doctor/images/prometheus/echometer _status.png)
3. If the value of the vertical coordinates in the above chart is 0.
  - Resolve this alert.
  - Send out a mail to qushiming@cn.ibm.com who will find out the root cause of triggering this alert.
4. If the value of vertical coordinates is 1.
  - Checking the status of container `doctor_echometer` on server 9.37.201.34.
    - If the container in bad status.
      - Restart this container with the command `docker restart doctor_echometer`.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

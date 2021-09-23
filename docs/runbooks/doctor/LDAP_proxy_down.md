---
layout: default
description: LDAP proxy down
title: LDAP proxy down
service: doctor
runbook-name: LDAP proxy down
tags: oss
link: /doctor/LDAP_proxy_down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}


## Instructions to Fix

1. In most cases, the alert will auto resolve within 30 minutes, since it's caused by intermittent network problem. Please click [this link](https://insights.newrelic.com/accounts/1926897/dashboards/725632?filters=%255B%257B%2522key%2522%253A%2522hostname%2522%252C%2522value%2522%253A%2522ldap-proxy-monitor-2-584f44bb45-t6hhs%2522%257D%255D&query=SELECT%20uniqueCount(status)%20FROM%20%60unixMonitor:Vmstat%60%20WHERE%20status%20LIKE%20%27%25numEntries%25%27%20AND%20hostname%20LIKE%20%27%25ldap-proxy-monitor-2%25%27%20TIMESERIES%2050%20second%20SINCE%20180%20minutes%20ago%20UNTIL%201%20minutes%20ago) to check the New Relic chart, if it says zigzag or blank, that means there would be a problem there.

2. If it's still open after 30 minutes, contact {% include contact.html slack=doctor-backend-7-slack name=doctor-backend-7-name userid=doctor-backend-7-userid notesid=doctor-backend-7-notesid %} and/or {% include contact.html slack=tip-api-platform-5-slack name=tip-api-platform-5-name userid=tip-api-platform-5-userid notesid=tip-api-platform-5-notesid %} and/or {% include contact.html slack=kong-support-slack name=kong-support-name userid=kong-support-userid notesid=kong-support-notesid %}.

3. This alert probably implies TIP ELK is impacted which will put ELK into a sev 1.

---
layout: default
description: Blink Access Logs.
title: Query Blink Access Logs
service: doctor
runbook-name: Query Blink Access Logs
tags: doctor, cloud, blink
link: /doctor/Runbook_Query_Blink_Access_Logs.html
type: Informational
---

## Blink Servers

There are 4 servers. Please login each server.

|hostname|IP|IP|IP|region|
|:----|:-----|:-----|:-----|:-----|
|ossbus1|169.60.135.236|10.186.184.154|9.66.242.220|Dallas|
|ossbus2|169.60.99.20|10.188.27.188|9.66.242.217|WDC|
|doctormbus3|169.44.75.235|10.154.56.42|9.66.246.4|Dallas|
|doctormbus4|158.85.7.124|10.109.1.21|9.66.246.5|WDC|


## 1. Cat Logs

Blink creates a log file each day.

![Blink Servers]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_cat_log.png){:width="640px"}

```
cat /var/log/haproxy.log | grep keyword
```

or  

```
cat /var/log/haproxy.log.1 | grep keyword
```

or untar the tar file , then run cat command.

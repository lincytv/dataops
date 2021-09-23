---
layout: default
description: Restart and Verify InfluxDB Service on Target VM.
title: Restart InfluxDB Service on Target VM
service: doctor
runbook-name: "Runbook InfluxDB is down"
tags: oss, influxdb, doctor
link: /doctor/Runbook-InfluxDB-is-down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## Purpose

## Technical Details

## User Impact

## Instructions to Fix

1. Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
2. Select **Doctor Keeper**
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/WukongDoctorKeeper.png){:width="640px"}
3. Search for `DOCTOR_BUS` node.
4. Press **SSH**
5. `su` `<YOUR_SSO_ID>`.
6. When prompted for your password, use your SSO Password.
7. `sudo -i` to change to root.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/WukongDoctorKeeper2.png){:width="640px"}
8. Run `ps -ef | grep influx`.
  * if following process is listed  
    >eg. `root    $PID    1 16 Dec25 ?        01:37:13 influxd -config /etc/influxdb/influxdb.generated.conf`

    -  if yes kill it with command `kill -9 $PID`
9. Backup log.
  * `cp /flash/influx/output.log /flash/influx/output.log.<timestamp>`   
    >eg. `cp /flash/influx/output.log /flash/influx/output.log.2018-02-01-07-40.15`

10. Go to /home/doctor/.
  * `cd /home/doctor`
  * Run `./start_influxdb.sh` to start influxdb again
  >**Don't use `service influxdb restart` to restart influxdb**.

11. Run command `docker restart doctor_receiver` to restart receiver service.  
12. Run `ps -ef | grep influx` again to see whether service is restarted.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

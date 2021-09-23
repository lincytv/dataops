---
layout: default
description: This alert indicates a self-healing heartbeat error.
title: TipSelfHealing Down
service: tipselfhealing
runbook-name: TipSelfHealing Down
tags: doctor,tipselfhealing
link: /doctor/Runbook_TipSelfHealing_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose
This alert will be triggered if the self-healing heartbeat detect that tipselfhealing service is outage.

## User Impact

Netcool will bypass the self-healing for all events in tip work flow if this alerts lasts 10 minutes.

We have Netcool impact servers. One is deployed in us-south and another one is deployed in us-east. As the primary server is deployed in us-south, the self-healing down alert from us-east does not impact current tip flow.



## How does self-healing heartbeat work?
- test interval: 1 minute
- self-healing API: test the global API only
- test pass criteria: self-healing API call gets response in 5 seconds (allow retry once), self-healing result is received in 30 seconds
- selfhealing_down alerting criteria: 2 failures in last 5 minutes

- self-healing heartbeat is deployed in netcool impact server.

## Instructions to Fix

1. Login to [{{wukong-portal-name}}]({{wukong-portal-link}})

2. Click 'CI & CD' in the navigation menu.

3. Use the 'Continuous Deployment' input to filter the service "doctor_datahub or doctor_tipselfhealing" and  record the Environment.

4. Click the 'Remote Command' in the navigation menu and input the Environment in the filter.

5. Check doctor_datahub and doctor_tipselfhealing status:

      For doctor_datahub:

        curl -i http://localhost:4777/datahub/healthz

      For doctor_tipselfhealing:

        curl -i http://localhost:4917/tipselfhealing/tip/events/environment

      if the curl command returns 200,the doctor-datahub and doctor-tipselfhealing status is online. Go to next step.

      if the curl command returns is not 200,execute the following command to get logs:

      For doctor_datahub:

        docker logs --tail=500 doctor_datahub

      For doctor_tipselfhealing:

        docker logs --tail=500 doctor_tipselfhealing

      If there are some errors in the log, please copy related logs in a file and contact csschen@cn.ibm.com for help.

6. Check doctor_datahub and doctor_tipselfhealing container status:

      For doctor_datahub:

        a. docker ps -a --filter status='running'|grep datahub

        b. echo $?

      if the result is not 0,restart the docker container by executing the following command:

        docker restart doctor_datahub

      For doctor_tipselfhealing:

        a. docker ps -a --filter status='running'|grep tipselfhealing

        b. echo $?

      if the result is not 0,restart the docker container by executing the following command:

        docker restart doctor_tipselfhealing

7. Check the network from doctor_tipselfhealing to Tip Webhook:

        curl https://tip-oss-flow.cloud.ibm.com/hooks/healthcheck

    If it returns "{"status":200,"message":"tip up"}", the network is OK. Otherwise contact Technical Foundation squad to verify whether this is a network issue. [Contacting TF]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)


8. Usually the PD will be resolved automatically within 30 minutes. If not, snooze the alert for 12 hours and send email to  {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} with related logs.
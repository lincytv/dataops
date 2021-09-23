---
layout: default
description: Runbook Registry Service URL Down
title: RETIRED Runbook Registry Service URL Down
service: doctor_registry
runbook-name: Runbook Registry Service URL Down
tags: oss, bluemix, doctor, doctor_registry
link: /doctor/Runbook_Registry_Service_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

__

## Purpose

This alert will be triggered if the Doctor registry service monitored by New Relic cannot be reached.

## Technical Details

The reason for this alert could be one of the following:
  1. The service is down or restarting.
  2. The container where the service is located is down.
  3. Network problem.

## User Impact

Users who are using the functionality provided by this service will be affected.

## Instructions to Fix


1. Double check the URL status:
   ```
   curl -k https://<bus_ip>:4568/registry/mbus -i -v
   ```
   If the status is `200` and the output is like the following sample, then you can resolve the alert. If not, please go to next step.
   ```
   {"public_ip":"169.44.75.235","private_ip":"10.154.56.42","port":6479,"auth":"xxxx","auth_vault":"xxxx}
   ```

   > **Notes:**
    * Replace the `<bus_ip>` with the IP address reported in the alert. For example, `https://9.66.246.2:4568/registry/mbus`, the IP address is `9.66.246.2`.


3. Restart the Service.
   - Login to [{{wukong-portal-name}}]({{wukong-portal-link}})
   - Select **Remote Command**.
   - Find the environment reported in the alert.
     > Registry service runs on Baremetals if the PD alerts show something like `registry_service_healthcheck_failed:doctorbus1. Details:` the problem is related to **doctor_mbus1** search for a partial name such as _doctor_ or _mbus_

   - Restart the service container reported in the alert, for example,:

      ``docker restart doctor_registry ``

   - To check the logs and the logs output like below is active not hung :

      ``docker logs doctor_registry --tail=20``

      ```
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0012
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0649
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "GET /registry/mbus HTTP/1.0" 200 176 0.0006
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "GET /registry/mbus HTTP/1.0" 200 176 0.0006
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0680
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0648
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "GET /registry/mbus HTTP/1.0" 200 176 0.0006
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0700
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "POST /registry/node/refresh HTTP/1.0" 200 31 0.0658
       127.0.0.1 - - [13/Nov/2018:09:49:10 +0000] "GET /registry/mbus HTTP/1.0" 200 176 0.0006
      ```

   - Run the curl command in step 1 again.
     * If it return `200` and the expected the output, resolve the alert.
   - If it still can not be fixed,  Escalate the alert in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}).

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

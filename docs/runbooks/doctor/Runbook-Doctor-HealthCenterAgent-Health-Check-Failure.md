---
layout: default
description: This incident indicates the doctor agent can't process requests correctly any more.
title: Doctor HealthCenter - Agent Health Check Failure
service: doctor
runbook-name: Doctor HealthCenter - Agent Health Check Failure
tags: oss, bluemix, doctor, healthcenter
link: /doctor/Runbook-Doctor-HealthCenterAgent-Health-Check-Failure.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

This incident indicates the doctor agent can't process requests correctly any more.

## Technical Details

## User Impact

## Instructions to Fix

### Resolve the incident immediately in the following cases

1. Agent upgrade is ongoing.
2. Agent is restarting for a known reason.
3. Log in to the [{{doctor-portal-name}}].
  * Select the environment reported in incident body.
  * In the instance list select any BOSH VM.
  * Click the SSH icon. If this works properly, resolve the incident.

### Otherwise, resolve the incident using the following steps

1. Find the environment name from the incident body.  
    {% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
2. Run the command `docker logs --tail=2000 doctor_backend > /tmp/agent_log` to save latest agent log for investigation later.
   Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
   if you cannot find the **doctor_backend** container.
3. Run the command `docker restart doctor_backend` to restart doctor backend.  
4. Verify using `curl -X GET http://127.0.0.1:4569/cloud/hello`.

{% include_relative _{{site.target}}-includes/tip_ssh.md %}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

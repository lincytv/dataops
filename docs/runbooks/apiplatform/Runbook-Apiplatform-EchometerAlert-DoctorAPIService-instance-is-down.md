---
layout: default
title: "RETIRED API Platform - Echometer alert: Doctor API service instance is down"
type: Alert
runbook-name: "Runbook-Apiplatform-EchometerAlert-DoctorAPIService-instance-is-down"
description: "This alert will be triggered if the api_doctor_api service does not work properly."
service: tip-api-platform
tags: api_doctor_api, apis
link: /apiplatform/Runbook-Apiplatform-EchometerAlert-DoctorAPIService-instance-is-down.html
---
{% capture tip-api-platform-1-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.slack }}{% endcapture %}
{% capture tip-api-platform-1-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.name }}{% endcapture %}
{% capture tip-api-platform-1-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.userid }}{% endcapture %}
{% capture tip-api-platform-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.notesid }}{% endcapture %}

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

## Purpose
This alert will be triggered if the api_doctor_api service does not work properly.

## Technical Details
If any instance of the API Platform's Doctor API service is down, we need to:
1. Ensure the failing instance is removed from the API gateway's ring balancer. (If self-healing succeeds, the failing instance should be auto removed.)
2. Try to recover the failing instance.
3. Add the recovered instance back into the ring balancer.

## User Impact
- If any of the Doctor API service's instance is down and is not removed from the API gateway's ring balancer, user requests routed to that instance might return an error.
- If the failing instance is removed from the API gateway's ring balancer, but is not recovered and added back, the load balancing for handling user requests might be impacted.

## Instructions to Fix
1. Verify if the reported instance is indeed down.
    1. In the PagerDuty details, there is `Service: api_doctor_api in env: is down, url is http://<IP>:8081/api/doctor/healthz`. Copy the IP and go to Wukong.
    2. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
    3. Go to the `CI & CD` panel, search `api_doctor_api` in  _Continuous Deployment_. You will see the lists of available instances.
    4. Find the impacted environment name which matches the IP in the previous step, and navigate to `Doctor Keeper` on the left-hand side bar, search for the impacted environment, and click SSH. A console window will open for the environment's Doctor VM.
    5. Login with your SSO ID. Use `su <YOUR_SSO_ID>`.
    6. Call `curl http://localhost:8081/api/doctor/healthz`, If the output contains 'The API is available and operational', this means the instance is still up and running, so you could skip the following steps and resolve the PagerDuty alert. Otherwise, go through the following steps for recovery.
2. If the service instance is indeed down, ensure it is removed from the ring balancer.
    1. Go to `API Management` on the left side and switch to the `API` tab.
    2. Click the `Manage virtual hosts` button and click the `Targets` button of `api_doctor_service` to verify that the IP address has already been removed by self-healing. If it's still there, then remove it manually and record `manually removed target` in the PagerDuty alert's note.
3. (Optional) If the repetitive PagerDuty incidents keeps alerting, you could mute the alerts for a certain period of time:
    1. Go to `Echometer` of Wukong.
    2. Search `api_doctor_api`, find the failing instance whose status is 1, click the Mute button and input how long you want to mute the alerts.
4. Find out the reason why the service instance stops and try to recover it.
    1. Check the log to try to find out the reason.
        * If you have [logmet]({{site.data[site.target].oss-doctor.links.logmet.link}}) access, log in and search `instance_id:DoctorServiceApi`.
        * If you do not have logmet access, access the instance VM as in Step 1, using `sudo docker logs api_doctor_api` to check the log.
    2. Try to find out the reason, and recover the instance.
        * [TODO] If any dependency error is found, such as a cipher service error, re-assign this PagerDuty alert to the appropriate person.
        * If no special error is found, use `sudo docker restart api_doctor_api` to restart the service instance.
5. Once a recovery alert about the service instance is received, add the recovered instance back to the ring balancer.
    1. In the service instance's vm (the same one as in Step 1), call `curl http://localhost:8081/api/doctor/healthz`, if the output contains 'The API is available and operational', it means the instance is recovered successfully.
    2. If the service instance is recovered, add it back to the ring balancer:
        1. Go to `API Management` on the left side and switch to `API` tab.
        2. Click the `Manage virtual hosts` button and then click the `Targets` button of `api_doctor_service`. In the new tab click the `Add a target` button , fill in the instance `<IP>:8081`, and then click Save.
6. After completing all the instructions, if the service instance still does not work, escalate the PagerDuty alert to the level 2 contancts of the tip-api-platform policy: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}.

## Notes and Special Considerations

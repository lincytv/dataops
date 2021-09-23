---
layout: default
title: "RETIRED API Platform - Echometer alert: Catalog service instance is down"
type: Alert
runbook-name: "Runbook-Apiplatform-EchometerAlert-CatalogService-instance-is-down"
description: "This alert will be triggered if doctor_apicatalog does not work properly."
service: tip-api-platform
tags: doctor_apicatalog, catalog, apis
link: /apiplatform/Runbook-Apiplatform-EchometerAlert-CatalogService-instance-is-down.html
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
This alert will be triggered if the doctor_apicatalog service does not work properly.

## Technical Details
If any of the API catalog service's instances are down, we need to:
1. Ensure the failing instance is removed from the API gateway's ring balancer. (If self-healing succeeds, the failing instance should be auto removed.)
2. Try to recover the failing instance.
3. Add the recovered instance back into the balancer.

## User Impact
- If any of the API catalog service's instances are down and are not removed from the API gateway's ring balancer, user requests routed to that instance might return an error.
- If the failing instance is removed from the API gateway's ring balancer, but is not recovered and added back, the load balancing for handling user requests might be impacted.

## Instructions to Fix
1. Verify if the API catalog service instance is indeed down.
    1. In the PagerDuty details, there is `Service: api_catalog_service in env: is down, url is http://<IP>:7001/api/catalog/healthz`. Copy the IP and go to Wukong.
    2. Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
    3. Go to the `CI & CD` panel, search `apicatalog` in  _Continuous Deployment_. You will see the lists of available instances. Find the impacted environment that matches the IP in the previous step, and click its name to SSH to the VM. A console window will open.
    4. Call `curl http://localhost:7001/catalog/api/catalog/healthz`, If the output contains 'The API is available and operational', this means the instance is still up and running, so you could skip the following steps and resolve the PagerDuty alert. Otherwise, go through the following steps for recovery.
2. If the service instance is indeed down, ensure it is removed from the ring balancer.
    1. Go to `API Management` on the left side and switch to the `API` tab.
    2. Click `Manage virtual hosts` button and click the `Targets` button of `api_catalog_service` to verify that the IP address has already been removed by self-healing. If it's still there, then remove it manually and record `manually removed target` in the PagerDuty alert's note.
3. (Optional) If the repetitive PagerDuty incidents keeps alerting, you could mute the alerts for a certain period of time:
    1. Go to `Echometer` of Wukong.
    2. Search `api_catalog_service`, find the failing instance whose status is 1, click the Mute button and input how long you want to mute the alerts.
4. Find out the reason why the service instance stops and try to recover it.
    1. Check the log to try to find out the reason.
        * If you have [logmet]({{site.data[site.target].oss-doctor.links.logmet.link}}) access, log in and search `instance_id:ApiCatalog`.
        * If you do not have logmet access, access the instance VM as in Step 1, using `sudo docker logs doctor_apicatalog` to check the log.
    2. Try to find out the reason, and recover the instance.
        * If any DB connection error is found, leave a note in the PagerDuty incident, and re-assign it to the level 2 contact of the tip-api-platform policy: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}.
        * [TODO] If any dependency error is found, such as cipher service error or client implementation error, re-assign this PagerDuty alert to the appropriate person.
        * If no special error is found, use `su <YOUR_SSO_ID>` and then `sudo docker restart doctor_apicatalog` to restart the service instance.
5. Once a recovery alert about the service instance is received, add the recovered instance back to the ring balancer.
    1. In the service instance's vm (the same one as in Step 1), call `curl http://localhost:7001/catalog/api/catalog/healthz`. If the output contains 'The API is available and operational', it means the instance has recovered successfully.
    2. If the service instance is recovered, add it back to the ring balancer:
        1. Go to `API Management` on the left side and switch to `API` tab.  Click Save.
           The following enties should be present in the list:
            * IP: 10.109.1.51  PORT: 7001  WEIGHT: 100
            * IP: 10.109.1.21  PORT: 7001  WEIGHT: 100
6. After completing all the instructions, if the service instance still does not work, escalate the PagerDuty alert to the level 2 contacts of the tip-api-platform policy: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}

## Notes and Special Considerations

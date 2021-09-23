---
layout: default
title: "RETIRED API Platform - Echometer alert: Key service instance is down"
type: Alert
runbook-name: "Runbook-Apiplatform-EchometerAlert-Keyservice-instance-is-down"
description: "This alert will be triggered if the api_key_service does not work properly."
service: tip-api-platform
tags: api_key_service, apis
link: /apiplatform/Runbook-Apiplatform-EchometerAlert-Keyservice-instance-is-down.html
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
This alert will be triggered if the api_key_service does not work properly.

## Technical Details
Api_key_service has enabled self-healing, if one of the instances is down, self-healing will auto remove it from ring-balancer. If self-healing failed to remove it, we need to remove it manually.

## User Impact
- If api_key_service cannot get config from cipher service, self monitoring will not work.
- If self-healing runs successfully, key service will not have any impact to the end user.

## Instructions to Fix
1. Verify if the api_key_service has been affected due to this instance down.
    * Click the Alert URL, to see its detail contents. If there is something similar to `Service: apiplatform_key_service in env: is down, url is http://X.X.X.X:8888/api/auth/healthz`, remember the IP address and navigate to Wukong.
    * Login to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
    * Go to `CI&CD` panel, search `api_key_service` in the _Continuous Deployment_. You will see the lists of the api_key_service available.
    * Copy the Environment name which matches the IP in the last step and Navigate to the `Doctor Keeper` on the left-hand side bar, Search for the impacted envirtonment, and click SSH. A console window will open for the environment's Doctor VM.
    * Login with your SSO ID: use `su <YOUR_SSO_ID>`, and switch to root: `sudo -i`.
    * Call `curl http://localhost:8888/api/auth/healthz`. If the output doesn't contain 'The API is available and operational', this implies that the key_service has stopped.
2. If the service is indeed down, remove it from ring-balancer.
    * Go to `API Management` on the left side and switch to `API` tab.
    * Click `Manage virtual hosts` button and click the `Targets` button of api_key_service to verify that the IP address has already removed(Self-healing will remove it automatically). If the IP has been removed from the target, self-healing will have a record in the PagerDuty alert's note. If self-healing failed to remove it , then remove it manually and record `manually removed target` in the PagerDuty alert's note.
3. Find out the reason why api_key_service exit and try to recover it.
    * Login into the [logmet]({{site.data[site.target].oss-doctor.links.logmet.link}}) and search with `instance_id:KeyServiceApi`, find out the reason and move to the next step.
    * If you have no access to logmet. Login the instance as Step 1.
    * Use `docker logs api_key_service` to find out the reason why api_key_service exit. [TODO]If any dependency errors found, such as cipher error or IAM error, please assigned this PagerDuty alert to the appropriate person.
    no special error , try to restart.
    * If no special error found, use `docker restart api_key_service` to restart the service and wait for several minitues.
    * Call `curl http://localhost:8888/api/auth/healthz`, If the output contains 'The API is available and operational.' , api_key_service recovered.
4. Once a recovery alert about the service instance is received, add the service to ring-balancer back if recovered.
    - In the service instance's vm (the same one as in Step 1), call `curl http://localhost:8888/api/auth/healthz` again to check whether output contains 'The API is available and operational.' or not.
    - If the api_key_service were recovered. Add it back to ring-balancer. follow the steps:
        * Go to `API Management` on the left side and switch to `API` tab.
        * Click `Manage virtual hosts` button and click the `Targets` button of api_key_service. In the new tab click the `Add a target` button , fill in the instance `<IP:PORT>`. The PORT of api_key_service is 8888. After that, click save button.
5. After all the operations, if api_key_service still does not work well, use `docker logs api_key_service` to see the logs then escalate the PagerDuty alert to level 2 of the tip-api-platform policy contacts: {% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}.

## Notes and Special Considerations

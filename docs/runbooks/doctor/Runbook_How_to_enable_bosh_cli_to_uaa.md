---
layout: default
description: This alert is triggred when Cloud release loading failed.
title: How to enable BOSH_CLI to User Account and Authentication (UAA)
service: doctor_backend, doctor_cloud,bosh_cli
runbook-name: How to enable BOSH_CLI to UAA
tags: oss, bluemix, doctor, doctor_backend
link: /doctor/Runbook_How_to_enable_bosh_cli_to_uaa.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

Show the steps to set an environment to use Account and Authentication (UAA) Cloud Foundry


## Technical Details

Make sure you have access to the [Doctor configuration]({{doctor-config-repo-link}}) repo, if you don't, request access to  {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %}. You will update bosh_cli to use Account and Authentication (UAA) Cloud Foundry method and you will need to update the configuration file for the environment.

## User Impact
If **UAA** and **CredHub** is deployed already in the environment, user will have issues to connect to BOSH_CLI, they will get errors like the follow reported:
```
Metrics are missing  for the environment 

Shuan Shuan Chen [5:53 AM]
@dcarriero Cann't get bosh token on D_DYS1.
```curl -X POST https://159.122.240.180:8443/oauth/token?client_id=bosh_cli&client_secret=&grant_type=password&username=boshuser&password=boshpassword&response_type=token 'content-type:application/x-www-form-urlencoded' -H 'accept:application/json'```
execute this command returns 404
Could you help to check?

Donatello Carriero [6:06 AM]
@csschen please use the director private ip 10.164.0.45.....when @Wang Hui added the Bosh UAA enabled mark for DYS1 we used the public ip,,but since yesterday UAA is enabled on the private ip (edited)

Shuan Shuan Chen [6:58 AM]
@dcarriero Changed the director ip to private and it worked.
metrics in D_DYS1 recovered.
```
The environment need to use the private IP and Bearer as authentication method.

## Instructions to Fix

1.  Check if **UAA** and **CredHub** is deployed as below:
  - There is a planned _CR_ to deploy _UAA_ and _CredHub_, once the corresponding _DR_ is done, the owner should post a message in [{{oss-doctor-name}}]({{oss-doctor-link}}) to notify Doctor team. But if we did not get the notification or something went wrong, we need to check if _UAA_ and _Credhub_ is deployed manually.
    * Check **doctor_backend** or **doctor_cloud** service logs, there should be an error like `authentication failed` when fetching bosh deployment information, [Doctor Backend Service more info]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
    * Check environment JML file
        - From [{{doctor-portal-name}}]({{doctor-portal-link}}#datacenter).
        - Find the environment.
        - Click on the JML icon.
        - Search for **is_credhub_enabled** for the CredHub status, `is_credhub_enabled: true`
    * Check [CR 874307](https://jazzop27.rtp.raleigh.ibm.com:9443/ccm/web/projects/CloudOE#action=com.ibm.team.workitem.viewWorkItem&id=874307), check if the corresponding DR is completed.
    - If above condition is met:
    - Open Doctor yml file e.g. taishan_dedicated_aa2.yml (make sure you have fetched the latest code)
    - Add a line in section of cloud -> bosh  `auth_method: Bearer`
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/auth_method_bearer.png){:width="640px"}
    - Restart ``docker restart doctor_backend`` or ``docker restart doctor_cloud`` service.
    - Optional: restart bosh_cli_ssh service from supervisorctl
        * Connect to BOSH_CLI for the environment
        * `sudo -i`
        * `supervisorctl restart bosh_cli_ssh`
    - Any issue about _CredHub_, pleases contact the DR owner or gubin@cn.ibm.com as CR owner
    - Verify if all information in Doctor cloud page is available


2. If the issue still can not be fixed,  escalate the alert or ask help in slack channel [{{oss-doctor-name}}]({{oss-doctor-link}})


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: EU Emergency Process Revoke User Privilege Failure.
title: "EU Emergency Process Revoke User Privilege Failure"
service: cicd
runbook-name: EU Emergency Process Revoke User Privilege Failure
tags: oss, bluemix, doctor,eu access
link: /doctor/Runbook_EU_Emergency_Process_Revoke_User_Privilege_Failure.html
type: Alert
---


{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
{% include {{site.target}}/load_ghe_constants.md %}
__

1. As EUaccess service depend on {{usam-short}} system, so check if {{usam-short}} system down by accessing [{{usam-name }}]({{usam-link}}), if you can access and login it should be OK and go to step 2, otherwise go to slack channel [{{eu-emerg-approvers-name}}]({{eu-emerg-approvers-link}}) and post a message about {{usam-name}} down, **and snooze the incident and resolve it after {{usam-short}} is covered**   

> **Note:** You can check {{usam-short}} outages [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_Oncall_Tips_and_Techniques.html#outages).

2. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
3. Select **CI & CD** from the left side menu.
4. Search out service `doctor_euaccess`, hese instances should be run on **{{doctor-service1-name}}** and **{{doctor-service2-name}}**.
5. Restart listed environments one by one, please, by clicking on the icon under the *Action* column.
6. If still got alert, check VaaS down or not, [VaaS](https://ibm-cloudplatform.slack.com/messages/C3VAABL4S)
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_euaccess.png)
7. If the alert persist after you restart the service, check the logs before to try to restart again.
  - `docker logs doctor_euaccess --tail 200`
  - If you see errors in the USAM API such as:
      ```
      EuaccessManager-check_access_expiration:Start to check user USAM access expiration
      [2018-12-28 17:35:56 +0000] INFO: EuaccessManager-check_access_expiration:User khayden@us.ibm.com’s access to usam group OPS_EU_EMERG expired
      ```
8. If a rejected request is still pending at the user queue or access is still open after two hours of being approved, remove the access from Doctor.
  - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Keeper** from the left side menu.
  - SSH one of VM's that runs `doctor_euaccess` service, If you cannot SSH use **Remote Command** instead.
  - Check the user in this group.
    ```
     curl -k -v -i -X GET http://127.0.0.1:8080/EUExceptionApprovalProcess/eu/process/usam/group/users?system=<USAMSystem>\&group=OPS_EU_EMERG\&code=<USAMCode>
    ```
     *Where:*<br>
       **USAMSystem:** From the  ID - USAM system map table<br>
       **USAMCode:**   Use the ID from USAMSystem and find match the ID at the ID - Code map table to get the Code<br>
       If you are using **Remote Command** call the *curl* command without **-v -i**<br>
     *Example:*
      ```
       curl -k -v -i -X GET http://127.0.0.1:8080/EUExceptionApprovalProcess/eu/process/usam/group/users?system=IBM%20Cloud%20Databases\&group=OPS_EU_EMERG\&code=br2KgQxiF
      ```
  - Revoke the user.
      ```
      curl -k -v -i -X POST 'http://127.0.0.1:8080/EUExceptionApprovalProcess/eu/process/privilege/revoke?system=<USAMSystem>&code=<USAMCode>&deletesystem=no' -d '{"user_id":"","groupName":"OPS_EU_EMERG","comment":""}' \
--header 'content-type: application/json'
      ```
       *Where:*<br>
         **USAMSystem:** From the  ID - USAM system map table<br>
         **USAMCode:**   Use the ID from USAMSystem and find match the ID at the ID - Code map table to get the Code<br>
         **user_id:**  w3ID<br>
         **comment:**  Your comments of the operation<br>
         If you are using **Remote Command** call the *curl* command without **-v -i**<br>
       *Example:*
         ```
           curl -k -v -i -X POST 'http://127.0.0.1:8080/EUExceptionApprovalProcess/eu/process/privilege/revoke?system=IBM%20Cloud%20Databases&code=br2KgQxiF&deletesystem=no' -d '{"user_id":"nierui@cn.ibm.com","groupName":"OPS_EU_EMERG","comment":"Revoke by Doctor"}' \
--header 'content-type: application/json'
          ```
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/revoke_USAM_request.png){:width="640px"}
### ID - USAM system map

|ID|USAM system|
|:----|:-----|
|1952|USAM-PIM1-BMX|
 |2256|USAM-DYS0-BMX|
 |2513|API Connect|
 |3746|Cloud-IMF-Prod|
 |3746|MobileServices-Prod-EU|
 |3953|Cloud-IDS-GHE|
 |4018|SOS-IDMgt|
 |4946|USAM-YPFRANKFURT-CloudantDemo|
 |5001|USAM-YPFRANKFURT-GHEDemo|
 |5103|Compose_internal_SSH_eu_emerg|
 |5152|WIoTP-SL-Prod|
 |5225|Cloud-SecurityServices-Prod|
 |5225|Cloud-SecurityServices-Prod-EU|
 |5349|Compose-WatsonEU-UI|
 |5369|USAM-KMS-EU|
 |5441|Armada-IdMgmt|
 |5453|MobileServices-Prod-RestrictedRegions-EU|
 |5664|IBM Cloud Databases|
 |5800|Armada-EU-IdMgmt|
 |5895|IBM Cloud Certificate Manager EU|
 |5978|Compose_internal_SSH|
 |5978|compose_ops|
 |830|Hybrid MPPv1 EU Production[1626233]|

### ID - Code map

  This table was moved to [Box Code Map - EU Emergency Process Revoke User Privilege Failure](https://ibm.ent.box.com/notes/633799063392), if you don't access please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}


- Check these runbook:
  - [EU Emergency Process Stop Polling Pending USAM Request]({{site.baseurl}}/docs/runbooks/doctor/Runbook_EU_Emergency_Process_Stop_Polling_Pending_USAM_Request.html)
  - [EU Emergency Process USAM API Invoke Failure]({{site.baseurl}}/docs/runbooks/doctor/Runbook_EU_Emergency_Process_USAM_API_Invoke_Failure.html)
  - [Failed to call USAM rest client to list pending access request of eu emerg access]({{site.baseurl}}/docs/runbooks/doctor/Runbook-Failed-to-call-USAM-rest-client-to-list-pending-access-request-of-eu-emerg-access.html)
  - Last resource is contact {{usam-short}} team.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

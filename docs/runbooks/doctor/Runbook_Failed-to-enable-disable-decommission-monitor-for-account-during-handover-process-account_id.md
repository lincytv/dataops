---
layout: default
description: Failed to enable, disable or decommission monitor for account during handover process.
title: Doctor Failed to Enable/Disable/Decommission Monitor
service: doctor
runbook-name: "Doctor Failed to Enable/Disable/Decommission Monitor"
tags: oss, bluemix, doctor, SSH
link: /doctor/Runbook_Failed-to-enable-disable-decommission-monitor-for-account-during-handover-process-account_id.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

Runbook for enable/disable/decommission monitoring failure during handover process.

## Technical Details

The APIs of Monitoring system are down, or the monitor's name mapping is empty.

## User Impact

The Monitoring system may still work for decommissioned environments, however, it may not work for environments that were handed over.

## Instructions to Fix

Open a Terminal and execute the following:
* `curl -X GET {{doctor-rest-apis-link}}/dlt/accounts/handover/history?account_id=xxx` to obtain tenant name and user name.  
  -  Where **account_id** is from the {{doctor-alert-system-name}} alert e.g. _Failed to enable monitor for account during handover process: account_id = **xxx**_

  - If the {{doctor-alert-system-name}} for:
    - If _enable monitor failure_ e.g. _Failed to enable monitor for account during handover process: account_id = 329_.
      * Get the user name in a handover history record where:
        - `handover_stage="handover_SRE"`.
        - `handover_stage_status="confirmed"`.
    - If _disable monitor failure_ e.g. _Failed to disable monitor for account during handover process: account_id = 329_
      * Get the user name in a handover history record where:
        - `handover_stage="return_to_deploy"`.
        - `handover_stage_status = "confirmed"`.
    - If _decommission monitor failure_ e.g. _Failed to deccommission monitor for account during handover process: account_id = 329_
      * Get the user name in handover history record where:
        - `handover_stage="deactive"`.
        - `handover_stage_status="confirmed"`.

  >**Note:** If you are connected using VPN, you may get the follow error message when running the curl command: **curl: (7) Failed to connect to 169.54.192.207 port 4574: Operation timed out**<br> You can connect to Jumpbox (_{{bosh-cli-link}}_) and run the curl command from there. More info about Jumpbox at [Doctor SSH Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html)

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/handover_history.png){:width="640px"}

* Manually try to enable/disable/decommission monitor by invoking API as follows:
    - If _enable monitor failure_.
      * ```
      curl -H "Content-Type: application/json" -X POST http://{{doctor-service1-ip|strip}}:4588/monitor/enableEnvironment -d '{"tenant": "xxx", "user": "xxx@xx.ibm.com", "account_id":xxx}
      ```
    - If _disable monitor failure_.
      * ```
      curl -H "Content-Type: application/json" -X POST http://{{doctor-service1-ip|strip}}:4588/monitor/disableEnvironment -d '{"tenant": "xxx", "user": "xxx@xx.ibm.com", "account_id":xxx}'
      ```
    - If _decommission monitor failure_.
      * ```
      curl -H "Content-Type: application/json" -X POST http://{{doctor-service1-ip|strip}}:4588/monitor/deccommissionEnvironment -d '{"tenant": "xxx", "user": "xxx@xx.ibm.com", "account_id":xxx}'
      ```



* The API should return with success immediately. The monitoring of the enabling/disabling/decommissioning is ongoing in a separate thread, check the monitor log to see if there are any errors in the log.

```
 ssh doctor@9.37.249.242    (PWD:  Doctor4....)
 sudo -i
 docker logs doctor_monitor
 (find the right docker img by issuing a cmd: docker ps -a)
 ```

 > **NOTE:** Alternatively, if you don't have the password for "doctor@{{doctor-service1-ip}}", do the following:<br>
 (a) Got to [{{wukong-portal-name}}]({{wukong-portal-link}}).<br>
 (b) Select **Doctor Kepper**.<br>
 (c) Search the webpage for IP _{{doctor-service1-ip}}_. <br>
 (d) Get the server name found on (c), such as _{{doctor-service1-name}}_. <br>
 (e) Go to **RemoteCommand**, filter on the server name found (d). <br>
 (f) Run the command `docker logs --tail 200 doctor_monitor` <br>
 (g) The log will be too big to show in the result box. Adjust the tail number of lines as necessary.


If any errors get returned by the monitor team's API, contact {% include contact.html slack=monitoring-apis-slack name=monitoring-apis-name userid=monitoring-apis-userid notesid=monitoring-apis-notesid %}.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

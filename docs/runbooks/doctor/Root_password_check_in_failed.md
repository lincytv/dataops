---
layout: default
description: Fix issues when root password is failed to check-in.
title: Root password check in failed
service: admin
runbook-name: Root password check in failed
tags: root, password, failed
link: /doctor/Root_password_check_in_failed.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

# Purpose

Fix issues when root password is failed to check-in

# Technical Details
When root password is enabled with root check-in/out function in Doctor, the password of root will be managed by Doctor, instead of Softlayer.

![Root password status]({{site.baseurl}}/docs/runbooks/doctor/images/root_pwd/Root_check_in_icon.png)

> **Note**:

   > 1. All bosh VM (listed in instances tab of Doctors'cloud page) should be enabled root password check-in/out automatically. If any failure, please refer to this runbook
   > 2. For non-bosh VM (not listed in instances tab of Doctor's cloud page ,but in Iaas tab) , not all VMs are enabled (white eye), if it's not enabled , need to confirm with VM owner if can enable root checkin.
   > 3. If you got alert with one VM but it shows "white eye", please skip and report to lupxg@cn.ibm.com
   > 4. If confirmed that a VM should enable root check-in, please follow [another runbook]({{site.baseurl}}/docs/runbooks/doctor/Enable_root_password_check_in_out_function.html)  

# User Impact
Cannot login system using root id.

# Instructions to Fix

Access to WATSON environments are strictly controlled and only available to a few personel.
If this incident is raised for a WATSON environment *during the CDL on-duty time*, then resolve this alert without any action and send the failed env/ip to
{% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%}.

If this incident is raised for a WATSON environment *during the North American on-duty time*, then reassign the incident to
the secondary on-call person ({% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid%}
or {% include contact.html slack=doctor-backend-6-slack name=doctor-backend-6-name userid=doctor-backend-6-userid notesid=doctor-backend-6-notesid%}).
Access to the Watson Health environments (Watson-Health-Hippa and Watson-Health-LSC-Sandbox) are even more restricted and Crystal or Alex need to engage
{% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} to resolve it.

## Prerequisites
Before continuing, make sure you comply with the following prerequisites, otherwise look for help at [{{oss-doctor-name}}]({{oss-doctor-link}})

- Verify that your _SSO_ can login the host(s) and has `sudo` privilege on it.
- Verify If public IP is accessible from Doctor agent.
- Verify SSO access is not slow.  
- Verify `sudo -i` is not slow.


## 1. Before fixing the issue, verify if the alert is a real failure.
  1. Login [{{doctor-portal-name}}]({{doctor-portal-link}}).
  2. Enter the page of environment.
  3. In **Detail** tab, click tab of **Iaas**
  4. For each failed ip, input ip in "Filter" box and check the color of eye icon.
  5. If all are green, resolve the alert and skip the following steps.

## 2. Verify if Cert is correctly deployed and function id can access the host
  * **Option1:**
     1. Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
     2. Select **Privilege ID Management** from the left side menu.
     3. Select an environment from dropdown list box.
     4. Select host(s).
     5. Click button **Check/Fix Cert**.

     > **Note:** The {{doctor-alert-system.name}} alert will show in the details section something like the follow:<br><br>
     Validating root on some VMs failed. _Env: D_MHI2_ Failed IPs: _["169.56.0.201", "169.56.0.106"]_<br>
     Where:<br>
           Environment is: _D_MHI2_<br>
           Host(s): _169.56.0.201_ and _169.56.0.106_

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/check_fix_cert.png)

  * **Option2:**
    1. Run API: (replace variables needed)
        ```
        curl -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/cert/check  -d '{"ips":["host_ip1","host_ip2",...,"host_ipN"],"email":"{{usam-id-example}}"}' -H 'MODERATE-TENANT:env_name'  -H 'Authorization:your_api_key'  -H 'Content-Type: application/json'
        ```

    > **Note**: The _env_name_, is the environment name showing on Doctor with capital e.g. _D_MHI2_,  API key is created in Doctor, your _Account_ page, please be noticed it's no Doctor API key.
      _ips_ parameter can be an array of IPs which you want to check. e.g _"ips": ["10.28.100.13", "10.28.100.16", "10.28.100.62"]_


    ![]({{site.baseurl}}/docs/runbooks/doctor/images/api/api_key.png)

  * Check email after 5~15 mintues (it actually depends on the environment and VM numbers in the list), for cert deployment result.
  > **Note:** If you do not receive any email within 15 minutes, please try to run step 1 again, if there is still no email received, please resolve the incident with comments 'Failed to check the certs for the IPs, and contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid%} for assistance.'. also send an email to {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} with the pagerduty incident ID for further assistance.

## 3. If Cert verification failed in _Step 2_, then need to create or correct function ID (including deploy cert)

  * **Important:** Verify if your SSO ID can login to the host that you are working on and, has `sudo` privilege.

  * **Option1:**
    1. Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
    2. Select **Privilege ID Management** from the left side menu.
    3. Select an environment from dropdown list box.
    4. Select host(s).
    5. Click button **Create ID**.
      > Use your SSO ID , if you SSO id does not work use a firecall ID. If neither of them work check **User Root User**
      still does not work go [6. Still showing red eye](#6-still-showing-red-eye)


    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/create_id.png)
  * **Option2:**
    1. Run API: (replace variables needed)

    ```
    curl -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/function_id/create   -d '{"ips":["host_ip1","host_ip2",...,"host_ipN"],"ssouser":"your_sso_id","ssopassword":"your_sso_password","executor":"{{usam-id-example}}"}'  -H 'MODERATE-TENANT: env_name'  -H 'Authorization: your_api_key' -H 'Content-Type: application/json'
    ```

  * Check mail, you will receive three mails for result of _creating id_, _deploying cert_ and _adding key_, make sure all steps are successful.
  * If any of the steps fail, please verify the following:  
      - If public ip is accessible from Doctor agent (if ping is ok).
      - If SSO login is slow  (From [{{doctor-portal-name}}]({{doctor-portal-link}}) agent ,run SSH _your_sso_id_@_host_ip_ or SSH from [{{doctor-portal-name}}]({{doctor-portal-link}}) portal)
      - If sudo -i is slow

  * If no above issue, but cert deployment is failed, contact {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid%}  
  * if no above issue but create function id failed, contact {% include contact.html slack=datapower-config-slack name=datapower-config--name userid=datapower-config-userid notesid=datapower-config-notesid%}


## 4. Force Checkin

  * **Option1:**
  1. Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
  2. Select **Privilege ID Management** from the left side menu.
  3. Select an environment from dropdown list box.
  4. Select host(s).
  5. Click button **Checkin**.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/checkin.png)

  * **Option2:**  
  1. Login into doctor agent (SSH) and run the API or use remote command: (replace variables as needed)

    ```
    curl -k -X POST http://127.0.0.1:4693/security/firecall/root/checkin -d '{"requestor":"your_intranet_id","instances":["host_ip1","host_ip2",...,"host_ipN"]}'
    ```

## 5. Refresh IaaS
  1. Login [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
  2. Find environment.
  3. Click on the emvironment.
  4. Under the **Details** section.
  5. Click on **IaaS** link.
  6. Click on the refresh icon.
  7. Find the host(s) using the **Filter** field.
  8. Check if there is showing green eye ![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_green.png)in root column for corresponding VM.

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/details_iaas_root.png)
  >**Note:** After applying Step 3, please wait about 5 minutes if you don't see a green eye in Step 4. and try again 4.

## 6. Still showing red eye

* If you could not resolve it, snooze the incident and contact {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} for more assistance.


## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

Just like for any of the privileged shared IDs discussed in this document, the usage of such IDs is discouraged and monitored for abuse. Only exceptional cases justify the usage of root credentials to access a Bluemix system, and the following list shows the allowed escalation path in case an urgent need of accessing a system arises:

  - access must be done using personal SSO ids
  - if the Active Directory is not reachable for any reason, and SSO ids cannot be used, operators should leverage the firecall IDs to access the OS
  - if for any reason the firecall IDs do not work, or is not defined on the target system, operators can use the root account to access the system. This case is managed as an exception and is monitored and tracked by our alerting mechanisms based on QRadar rules.
  - If Doctor tool goes down, a "Break the Glass" mechanism is in place so that a defined number of security focal point, who have access to credentials vault, are contacted by operators for root password. The Doctor tool will be in charge for changing root password when it rises.

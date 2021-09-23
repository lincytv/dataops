---
layout: default
description: Enable root check-in/out function in Doctor.
title: Enable root password check in out function
service: admin
runbook-name: Enable root password check in out function
tags: root, password, failed,checkin
link: /doctor/Enable_root_password_check_in_out_function.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}



# Purpose
 Enable root check-in/out function in Doctor.

# Technical Details
When root password is enabled with root check-in/out function in Doctor, the password of root will be managed by Doctor, instead of Softlayer. this function will work as follow:
  1. User need to provide incident id when check out password.
  2. Once root password is checkout then checkin, the password will be changed.
  2. Any check-out can hold password only 2 hours, will automatically check-in and change password when expire.
  3. Schedule job is running to change password when it's going to expire.   
  4. Schedule job is running to retry any check-in failure.
  5. Schedule job is running to check new VM (BOSH) then enable root.

![Root password status]({{site.baseurl}}/docs/runbooks/doctor/images/root_pwd/Root_check_in_icon.png)


> **Note:**
1. All BOSH VM (listed in _Instances_ tab under the _Details_ section of an environment of _Doctors'_ cloud page) should be enabled root password check-in/out automatically. If any failure, please refer to [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Root_password_check_in_failed.html)
2. For non-BOSH VM (not listed in _Instances_ tab of _Doctor's_ cloud page ,but in _IaaS_ tab) , not all VMs are enabled (white eye), if it's not enabled , need to confirm with VM owner if can enable root checkin

# User Impact
Need to get root password following root check-out process.

# Instructions to Fix

>**Note:** If the failure happens in any **WATSON** environment, please resolve this alert without any action and send the failed env/ip to any of the follow: {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%}, {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid%}, {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid%} by mail or slack dm.  <br><br>
For **WATSON_HEALTH** resolve this alert without any action and send send the failed env/ip to {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} <br><br>
Currently doctor on-call agents are not allowed to operate **WATSON** environments.

## Prerequisites

Before continuing, make sure you comply with the following prerequisites, otherwise look for help at [{{oss-doctor-name}}]({{oss-doctor-link}})

- Verify that your _SSO_ can login the host(s) and has `sudo` privilege on it.
- Verify If public IP is accessible from Doctor agent.
- Verify SSO access is not slow.  
- Verify `sudo -i` is not slow.

## 1. Create or correct function ID (including deploy Cert)

 * **Option1:**
   1. Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
   2. Select **Privilege ID Management** from the left side menu.
   3. Select an environment from dropdown list box.
   4. Select host(s).
   5. Click button **Create ID**.
   6. Provide your SSO ID and password.
   7. Click OK.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/create_id.png)
 * **Option2:**
   1. Run API: (replace variables needed)
       ```
       curl -X POST https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/function_id/create   -d '{"ips":"_host public ip_","ssouser":"_your sso id_","ssopassword":"_your sso password_","executor":"{{site.data[site.target].oss-doctor.links.usam.id-example}}"}'  -H 'MODERATE-TENANT: env name'  -H 'Authorization: your api key' -H 'Content-Type: application/json'

       After 12-December-2018 use:

       curl -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/function_id/create   -d '{"ips":"_host public ip_","ssouser":"_your sso id_","ssopassword":"_your sso password_","executor":"{{site.data[site.target].oss-doctor.links.usam.id-example}}"}'  -H 'MODERATE-TENANT: env name'  -H 'Authorization: your api key' -H 'Content-Type: application/json'

       ```
       > **Note**: The _env_name_, is the environment name showing on Doctor with capital e.g. _D_MHI2_,  API key is created in Doctor, your _Account_ page, please be noticed it's no Doctor API key.
         _ips_ parameter can be an array of IPs which you want to check. e.g _"ips": ["10.28.100.13", "10.28.100.16", "10.28.100.62"]_

      ![]({{site.baseurl}}/docs/runbooks/doctor/images/api/api_key.png)
  * Check mail, you will receive three mails for result of _creating id_, _deploying cert_ and _adding key_, make sure all steps are successful.
  * If all prerequisites are OK, but Cert deployment is failed, contact {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid%}  
  * if all prerequisites are OK, but create function id is failed, contact {% include contact.html slack=datapower-config-slack name=datapower-config-name userid=datapower-config-userid notesid=datapower-config-notesid%}

## 2. Only required for NON-BOSH VM Add the host to enabled list.

  * **Option1:**

      1. Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
      2. Select **Privilege ID Management** from the left side menu.
      3. Select an environment from dropdown list box.
      4. Select host(s).
      5. Click button **Add to cover list**.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/add _to_cover_list.png)


  * **Option2:**

      1. Run API: (replace variables needed)
          ```
          curl -X POST https://pnp-api-oss.cloud.ibm.com/doctorapi/api/doctor/checkout/enablement -d  '{"ips":["host_public_ip1","host_public_ip2"..."host_public_ipN"],"environment":"env_name"}'   -H 'Authorization:your api key'  -H 'Content-Type: application/json'

          After 12-December-2018 use:

          curl -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/checkout/enablement -d  '{"ips":["host_public_ip1","host_public_ip2"..."host_public_ipN"],"environment":"env_name"}'   -H 'Authorization:your api key'  -H 'Content-Type: application/json'
          ```

## 3. Force Checkin

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

## 4. Refresh IaaS

  * Login [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
  * Find environment.
  * Click on the emvironment.
  * Under the **Details** section, click on **IaaS** tab.
  * Click on the refresh icon.
  * Find the host(s) using the **Filter** field.
  * Check if the host is showing a green eye ![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_green.png) in root column for corresponding VM.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/details_iaas_root.png)

  >**Note:** After applying Step 3, please wait about 5 minutes if you don't see a green eye in Step 4. and try again 4.

## 5. Still showing red eye

  If Step 1 is successful or Step 2 completed without any issue but still showing a red eye ![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_red.png), contact {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid%} for more assistance.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}
![root usage notice]({{site.baseurl}}/docs/runbooks/doctor/images/root_pwd/Root_usage_notice.jpg)

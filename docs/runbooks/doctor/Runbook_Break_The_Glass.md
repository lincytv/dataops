---
layout: default
description: The purpose of this runbook is so the on-duty operator will have another way to fetch the root password in case Doctor cannot work
title: Break the Glass on-duty operator
service: doctor
runbook-name: Runbook Break the Glass
tags: oss, bluemix, bbo, BBO_Ops
link: /doctor/Runbook_Break_the_Glass.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_sosat_constants.md%}

## Purpose

Doctor Vault manages the root password for all the environments and Softlayer network device (Vyatta).

The purpose of this runbook is so the **Break the Glass** on-duty operator will have another way to fetch the **root** password in case {{doctor-portal-name}} can not work.

If you are a Primary Doctor on-call operator and do not have access to do the following steps in this runbook, assign the PD incident to a Secondary on-call.

## Technical Details

### 1. Vault architectural diagram

{% if site.target == 'ibm'%}
![Vault topology]({{site.baseurl}}/docs/runbooks/doctor/images/vault/vault-topology.png)

Currently we have 5 servers cross WDC01 and WDC04 to deploy Consul cluster and Vault.

* doctorvault1.bluemix.net 169.45.232.29/10.149.35.210
* doctorvault2.bluemix.net 169.45.232.30/10.149.35.218
* doctorvault3.bluemix.net 158.85.30.158/10.109.1.86
* doctorvault4.bluemix.net 158.85.30.150/10.109.1.79
* doctorvault5.bluemix.net 158.85.5.244/10.109.1.90

Consul cluster is running on these 5 servers and Vault is just running doctorvault3/4/5. All of these servers are running in Softlayer service zone.

All the EU requests will be routed to VaaS.

Consul cluster is running in these 5 servers, and vault is just running doctorvault3/4/5.
All of these servers are running in Softlayer service zone.

{% endif %}

### 2. How to use the check-in/check-out feature on Doctor portal

  1. Open the page of [{{doctor-portal-name}} ->datacenter]({{doctor-portal-link}}/#/datacenter).

  2. Search for environment using the _Search keyword_ field.

  3. Click on the environment hiperlink.
  ![]({{sire.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/open_cloud_by_env.png){:width="600px"}

  4. A colored eye icon on the left of the row indicates the current state of this instance.

  5. Click the icon to operate check-in/check-out.

     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/root_checkout_1.png){:width="700px"}

     - If the color is green![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_green.png), indicates an available state.

        - A user can click the icon, then input a valid PD or RTC number to check the password out.

      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/root_checkout_3.png){:width="700px"}

     - If the color is blue![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_blue.png), indicates that the current user has checked out this password already. Users could click the icon to view the password with expiration time in a dialog box with the following actions:  

          - a. extend the checkout for 2 more hours

          - b. check in the password (any existing session with root will be terminated)

          - c. cancel
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/root_checkout_5.png){:width="600px"}

     - If the color is yellow-green![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_yellow_green.png), indicates the password is being used by another user. Users may click the icon, then input a valid PD or RTC number to check the password out.

     - If the color is red![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_red.png), indicates an invalid state. A user won't be able to check out a root for this instance and need to contact [{{oss-doctor-name}}]({{oss-doctor-link}}), Slack channel for assistace.

     - If the color is white ![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/root_checkout_white.png), indicates that the check in/checkout function is not enabled for this instance.

       There is a demo in this [{{box-name}}]({{box-link}}/s/ig9yy1xhgcp5tb0b9869lk8zewkc0f8w).

### 3. When to invoke the "Break the Glass" process

In the following cases:

  1. Unable to login into [{{doctor-portal-name}}]({{doctor-portal-link}})
  2. Doctor function ID in the target server, does not work.
  3. Doctor **cipher** service is down.

We have enabled the monitoring for **cipher** service and will send the alert to the new PD service _doctor-break-the-glass_.


### 4. Which PD service must be used to open a ticket in case the check-in/check-out process doesn't work

We create a new PD service **doctor-break-the-glass**.

### 5. Who are the members (worldwide) involved "on-duty" for the "Break the Glass" process

Need security team to give us the on-call list.

We have created a draft on-call scheduler [here]({{doctor-critical-alerts-link}}/schedules#PRH4TIK).

### 6. Where is the daily check for all Vyatta passwords stored on the vault system tracked? Who will get informed if an issue arises from the cross check?

Doctor has a daily script to cross check the Vyatta password. Notify the network team when an issue should be raised.

### 7. How to use the "break_the_glass" token to get the root password

**root password break the glass**

  1. Apply the [{{usam-name}}]({{usam-link}}) for **bluemix-cred-vault-break-glass**       [here]({{site.data[site.target].oss-doctor.links.ibm-wiki.link}}/home?lang=en#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/Request%20Access%20to%20Cred%20Vault).

  2. Apply the vault **bluemix-cred-vault-break-glass** token from vault admin once your {{usam-short}} request is approved.



     Vault admin: {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=sre-platform-chief-architect-slack name=sre-platform-chief-architect-name userid=sre-platform-chief-architect-userid notesid=sre-platform-chief-architect-notesid %}, ...

     And then you will get a wrapping_token token generated by vault xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx



  3. As the on-call operator, you need to unwrap the token by yourself.

     You can use the vault client and HTTP API to do it. e.g. using HTTP API

       ```
       curl -k --header "X-Vault-Token: wrapping_token" --request POST
       http://vault_server:8200/v1/sys/wrapping/unwrap
       ```

     The vault_server includes 10.109.1.86, 10.109.1.79, 10.109.1.90. You can use any of them.

     You need send this request from any server from Softlayer _Service Zone_.

  4. When to invoke **bluemix-cred-vault-break-glass**

     First, you can list the vault directory e.g.

      ```
      curl -H "X-Vault-Token: client_token" -X GET
      http://vault_server:8200/v1/generic/crn/v1/yp_dallas/public/oss/-/-/rootpassword/doctor/?list=true
      ```

     to get all IP addresses which are managed by Vault.

     You can continue to go to the next folder level by

  5. Getting the password.

     When you get the full path, run:

      ```
      curl -H "X-Vault-Token: client_token" -X GET http://vault_server:8200/v1/generic/crn/v1/yp_dallas/public/oss/-/-/rootpassword/doctor/75_126_118_5
      ```

### 8. How to get data and list key from vault

**Vyatta break the glass**

  1. Apply the [{{usam-name}}]({{usam-link}}) for **bluemix-cred-vault-break-glass** [here]({{site.data[site.target].oss-doctor.links.ibm-wiki.link}}/home?lang=en#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/Request%20Access%20to%20Cred%20Vault).

  2. Apply the vault "Vyatta break the glass" token from vault admin once your USAM request is approved.


     Vault admin: {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}, {% include contact.html slack=sre-platform-chief-architect-slack name=sre-platform-chief-architect-name userid=sre-platform-chief-architect-userid notesid=sre-platform-chief-architect-notesid %}, ...

     And then you will get a wrapping_token token generated by vault
     xxxxxxxx-xxxx-xxxx-xxxxxxxxxxxx


  3. As the on-call operator, you need unwrap the token by yourself.

     You can use vault client and HTTP API to do it.

     e.g. using HTTP API

     ```
     curl -k --header "X-Vault-Token: wrapping_token" --request POST http://vault_server:8200/v1/sys/wrapping/unwrap
     ```

     vault_server includes 10.109.1.86, 10.109.1.79, 10.109.1.90. You can use any of them.

     You need send this request from any server from Softlayer "Service Zone".

  4. When invoke **Vyatta break the glass**

     First, you can list the vault directory
     e.g.

     ```
     curl -H "X-Vault-Token: client_token" -X GET http://vault_server:8200/v1/generic/crn/v1/softlayer_278444/?list=true
     ```

     and you may get

     ```json
     {"request_id":"d260ab78-dfa7-f76e-b00e-ff23c3010127","lease_id":"","renewable":false,"lease_duration":0,"data":{"keys":["-/"]},"wrap_info":null,"warnings":null,"auth":null}
     ```

     and you can continue to go to the next folder level by

     ```
     curl -H "X-Vault-Token: client_token" -X GET http://vault_server:8200/v1/generic/crn/v1/softlayer_278444/-/?list=true
     ```

  5. Get the password
     When you get the full path

     e.g.

     ```
     generic/crn/v1/softlayer_278444/-/oss/-/-/vyattapassword/network/10_107_50_136
     ```

     You can get the password by the following API

     ```
     curl -H "X-Vault-Token: client_token" -X GET http://vault_server:8200/v1/generic/$vault_key
     ```

     e.g.

     ```
     curl -H "X-Vault-Token: client_token" -X GET http://vault_server:8200/v1/generic/crn/v1/softlayer_278444/-/oss/-/-/vyattapassword/network/10_107_50_136
     ```

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

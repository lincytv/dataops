---
layout: default
description: CF Account/Password is Out of Date or Invalid
title: CF Account/Password is Out of Date or Invalid
service: doctor
runbook-name: Runbook CF account password out of date
tags: oss, vm
link: /doctor/Runbook_CF_account_password_out_of_date.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Technical Details

This might not mean that the account/password is out-of-date. Please log in to the environment and find the reason.

A {{doctor-alert-system.name}} alert like the following will be created:

    Title

    Cf account/password out-of-date for L_BNSF_002

    Description

    Please check whether the cf account/password provided by doctor is valid, if invalid please update and synchronize the password to make it take effect. Runbook:https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_CF_account_password_out_of_date.html.
    cf login failed with the msg :
    ```
    CF_COLOR=false CF_HOME=tcfhome1521015369653645725 cf login --skip-ssl-validation -a https://api. -u NA -p NA -o OE_Runtimes_Scaling -s RT_Scaling
    API endpoint: https://api.
    FAILED
    Error performing request: Get https://api./v2/info: dial tcp: lookup api. on 139.51.62.166:53: no such host
    TIP: If you are behind a firewall and require an HTTP proxy, verify the https_proxy environment variable is correctly set. Else, check your network connection.
    ```

## Instructions to Fix
1. Go to [{{wukong-name}}]({{wukong-link}}).
2. Click on **Remote Command** from the navigation menu.
3. Search the environment provided by the alert.
> **TIP** from the alert message: "Cf account/password out-of-date for D_YS0", D_YS0 is the environment.

4. Check the inception(s).
5. Get the port number for that particular environment from a taishan [local/public/dedicated] [env].yml file under [Doctor Configuration]({{repos-bluemix-fabric-link}}/doctor-configuration/tree/master/config).
  - Look for "port: " key/value pair in the yml file.For instance, **D_YS0** will be the one in the image below:
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/doctor_conf_taishan_env_get_port.png){:width="640px"}
6. Run the command for:
    * Dedicated and Local environments:
       * ``curl http://localhost:port#/ope/ansible/runtime/variables``
    * Public environments:
        * ``curl http://localhost:port#/scriptengine/runtime/variables``

    e.g. ``curl http://localhost:4569/ope/ansible/runtime/variables`` for D_YS0 environment.

   ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/CF_Account_Password_Invaild_variables.png){:width="640px"}
7. Check whether $CF_ADMIN_USER and $CF_ADMIN_PWD exist.
8. Check "$CF_TARGET_API". It should be **https://api._#env_domain_name#_**, ``e.g. https://api.dys0.bluemix.net``.
9. If steps 7 and 8 returned the expected variables, then the incident can be resolved. Otherwise, run the followed command to sync the environment:
    * Dedicated and Local environments:
       * ``curl -X POST http://localhost:port#/ope/ansible/runtime/variables``
    * Public environments:
        * ``curl -X POST http://localhost:port#/scriptengine/runtime/variables``

    e.g. ``curl -X POST http://localhost:4569/ope/ansible/runtime/variables`` for D_YS0 environment.
    Then apply 6 again to make sure the environment is in synch now.

## Notes and Special Considerations

1. If this incident was triggered by TOC or other team, more details of failure can be found at the original incident.
2. The script log can be found at [{{wukong-portal-name}}]({{wukong-portal-link}}) -> **Script Execution Audit**.
3. If you need more help or the issue is not resolved, please contact {% include contact.html slack=auto-scaling-slack name=auto-scaling-name userid=auto-scaling-userid notesid=auto-scaling-notesid %}.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

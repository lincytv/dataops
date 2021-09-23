---
layout: default
description: Bluemix Alert SEV3
title: Bluemix Alert SEV3 Ops admin console doctor check failed
service: doctor
runbook-name: Runbook st_admcnsl_doctorChk Ops admin console doctor check failed
tags: doctor
link: /doctor/Runbook_St_Admcnsl_doctorChk_Ops_admin_console_doctor_check_failed.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__
## Notes
This Alert was migrated from Marmot to Newrelic and the alert message will be changed.

## Purpose
Verify doctor admin console is up and running for a specific environment.

## Alert will come with a message like the following:

    You will receive some new alerts like:

    INC0753260:PDE1105071:st_admcnsl_doctorChk:D_YS0:d-ys0:dedicated::us-south

    This alert covered all the Metrics and if one of the metrics is false and the alert will be triggered:   
       ${org_name}.${env_name}.fabric.admcnsl_chk.bmdocTxCounts;
       ${org_name}.${env_name}.fabric.admcnsl_chk.bmdocBandWidth;
       ${org_name}.${env_name}.fabric.admcnsl_chk.bmdocRespTimes;
       ${org_name}.${env_name}.fabric.admcnsl_chk.bmdocDea

    This check runs on the doctor api. The settings come from the JML file. It probably can't connect.
    Check the logs

    Can try restarting.

    Check to see if the doctor ip and port have been changed recently using git log.
    Maybe need to revert changes.

        bluemix_doctor_agent_public_ip: < ip >
        bluemix_doctor_agent_public_port: < port >



## User Impact
User is not able to open Bluemix Admin Console.

## Instructions to Fix

* Log into the [{{doctor-portal-name}}]({{doctor-portal-link}}) agent of the environment mentioned in the alert.
    > **TIP**
    > - Find the environment by viewing the incident in Doctor.
    >   - From the left side menu:
    >   - Incident -> PagerDuty Incident -> Use the search options to find the ticket.

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
__

* Run these APIs on Doctor Agent in the previous step.

```
  curl -X GET http://127.0.0.1:4569/cloud/app/dea_usage
  curl -X GET http://127.0.0.1:4569/cloud/app/cell_usage
  curl -X GET http://127.0.0.1:4569/cloud/monitor/network/usage/hourly
```
  > **Note:** The first curl command returns the DEA (Droplet Execution Agent) usage.<br> This only applies to environments that have not been migrated to Diego.<br> For environments that have been migrated, you can expect a result of `{"result":"failed","detail":null}`; consider that a valid result.

   {% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
    {{ note_backend_port  | markdownify }}

* If the curl commands return JSON objects.
  - Go to [{{doctor-portal-name}} ->Blink]({{doctor-portal-link}}/#/proxy_blink).
  - Find the environment in previous step.
  - Click on the ACE(IBM) link under the ACE Console column.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/Doctor_Blink_ACE_IBM.png){:width="640px"}
  - If no results.
    * Run the following:
    ```
      docker restart doctor_backend
    ```
    * Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html) if you cannot find the **doctor_backend** container.
    * Wait ten minutes.
    * Run the curl commands again.

* Verify previous step opens successfully.
> **Note:** Make sure that the `proxy.pac` file from [dset-pac]({{repos-bluemix-fabric-link}}/dset-pac) has a line for the environment, if you are using `proxy.pac`, ff it is not listed in the `proxy.pac` file, make a pull request to include it.<br><br>While waiting for your pull request to be merged, you can set your Firefox browser to use the Blink proxy server directly by:<br><tab>* Opening Preferences -> Advanced -> Network -> Settings… -> enabling ‘Manual proxy configuration’.<br><tab>* Set ‘HTTP Proxy’ to `{{doctor-blink-proxy-link|strip}}`.<br><tab>* Set the port to `{{doctor-blink-proxy-port|strip}}`.

  - Add the check option to the URL e.g. _https://console.gcc.ca-east.bluemix.net/check_.
  - Check the result in this new page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/Doctor_Blink_ACE_IBM_Check.png){:width="640px"}
  - Note especially the Doctor checks:
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/DoctorChecksInAdminConsole.png){:width="600px"}
  - If all checks return successful, **the alert will be resolved automatically**.

## Notes and Special Considerations
Sometimes the alert is caused by memory full or disk full. If you have other problems, please contact {% include contact.html slack=admin-console-slack name=admin-console-name userid=admin-console-userid notesid=admin-console-notesid %}

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: This runbook is for PagerDuty alerts for monitoring the following APIs for environments that are handed over to SRE/customers.
title: Doctor Cloud Resource Usage APIs
service: doctor
runbook-name: Doctor Cloud Resource Usage APIs
tags: oss, bluemix, doctor, vm , api, APIs
link: /doctor/Runbook_cloud_resource_usage_APIs.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose
This runbook is for PagerDuty alerts for monitoring the following APIs for environments that are handed over to SRE/customers.

## Technical Details
These APIs are used by [{{doctor-portal-name}}]({{doctor-portal-link}}) and OpsConsole to display resource usage data.

1.  /cloud/app/dea_usage
2.  /cloud/app/cell_usage
3.  /cloud/instance/v1?filter=dea
4.  /cloud/instance/v1?filter=cell
5.  /cloud/monitor/network/usage/hourly?count=1
6.  /cloud/monitor/network/responsetimes
7.  /cloud/monitor/network/transactions

### How to visit these APIs

* In [{{doctor-portal-name}}]({{doctor-portal-link}}):

![usage runbook]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/usage_runbook_1.png)

* In OpsConsole:

![ops console]({{site.baseurl}}/docs/runbooks/doctor/images/opsconsole.png){:width="504px" height="258px"}

* From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Doctor Keeper**
  * Find an environment using _Enter to filer environment_
  * Click on **SSH**

    Example: `curl http://localhost:4569/cloud/monitor/network/responsetimes`.

    {% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
    {{ note_backend_port  | markdownify }}

{% if site.target =='ibm' %}
* From OpsCenter APIs (only when you're using IBM network):

  Example:
  -  In browser, visit

    ```
    https://api.opscenter.bluemix.net/cloud/monitor/network/responsetimes?user_name=xxx@xx.ibm.com&api_key=xxx&env_name=D_YS0
    ```
  -  In terminal, visit

    ```
    curl -k -X GET -d "user_name=xxx@xx.ibm.com&api_key=xxx&env_name=D_YS0"  {{site.data[site.target].oss-doctor.links.opscenter-api.link}}/cloud/monitor/network/responsetimes
    ```
{% endif %}
### Alert format

In the Details section of the alert, there are one or more rows for each affected environment, in the following format:
*[Env name] API: [API path] Error: [error message]*.

Example:
*YS1_LONDON API: /cloud/app/dea_usage Error: returned data include invalid values*

## User Impact

## Instructions to Fix

### Notes

* Known issues


  > Note that some of the steps below ask you to curl endpoints under http://localhost:4569. For some environments, port 4569 is not correct and you will receive a *curl: (7) Failed to connect to localhost port 4569: Connection refused* error. If this happens, look up the correct *cloud* port. See **To check the port** section above, and retry the curl command with the correct port.

  {% if site.target == "ibm" %}

  - For worldwide on-duty persons, if you encounter blocking issues, please describe in the alert note, and snooze the alert to CDL on-duty time.
  {% endif %}

  Fix the problem one environment at a time. Based on the [error message], take one of the following actions:

- *Env doctor agent is down*

  - Handle the 'Doctor backend agent down' issue first if necessary, and the API issue will probably recover after the env agent is up again.

- *returned data are: {"result"=>"failed", "detail"=>"mbus timeout"}*

  - If all the 7 APIs have this error, there are probably problems with the Doctor backend agent itself. A restart might be needed.
     1. Check whether the env is green on [{{doctor-status-name}}]({{doctor-status-link}}).
     2. If the status in step 1 is ok, check whether its connection status exists and looks normal in Wukong > Register.
     3. If the status in step 2 is ok, check whether the alerted APIs still work. If they all work, it might be a transient timeout issue and can be ignored.

  -  For the API */cloud/app/dea_usage*, */cloud/app/cell_usage*, or */cloud/monitor/network/usage/hourly?count=1*, you could check them from the Doctor UI. Click into the env's detail page to see if there's data flowing (refer to the screenshot in the previous section). If nothing is wrong, then it is a false alarm of mbus's routing timeout and can be ignored.

  -  For other APIs whose data is not displayed in the Doctor UI, you can visit them via Wukong > Keeper SSH backend (e.g., `curl http://localhost:4569/cloud/monitor/network/responsetimes` in the backend). If there is data being returned, then it's a false alarm of mbus's routing timeout and can be ignored.

  - If */cloud/monitor/network/usage/hourly?count=1* reports error *returned data are: {"result"=>"failed", "detail"=>"mbus timeout"}*, the possible causes might be:

    - Doctor backend agent fails to connect to shared mongo service. This will impact the */cloud/monitor/network/usage/hourly?count=1* API, and when you execute `curl -X POST http://localhost:4569/cloud/monitor/network/datapower/status`, there'll be *Failed to record datapower network throughput data for tenant xxx, error msg is mbus timeout* in the output log. It's probably a network issue in the connection between the shared mongo service and the environment's Doctor backend agent.

    - Contact {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}.

  - *include invalid values*

  - If */cloud/app/dea_usage* & */cloud/app/cell_usage* both have this error, there's probably a ccdb connection issue. When this issue happens, the cloud page of the env will look like this:

![]({{site.baseurl}}/docs/runbooks/doctor/images/network_issue.png){:width="632px" height="284px"}
  * Sometimes it's transient and data can be recovered by executing: `curl -X POST http://localhost:4569/cloud/app/app` in the environment's Doctor backend agent.

  * Check whether the DNS settings in */etc/resolv.conf* has the env's BOSH director IP as the first name server. If not, contact {% include contact.html slack=bosh-director-slack name=bosh-director-name userid=bosh-director-userid notesid=bosh-director-notesid %}.

  * If the DNS settings are good, check with SRE whether the ccdb of the env is down.

  * If it's not a ccdb connection issue：
     - For */cloud/app/cell_usage* or */cloud/app/dea_usage*, if the percentage is over 100%, execute `curl -X POST http://localhost:4569/cloud/app/app` to trigger a refresh, and check whether it's a transient status and can be cleared. If not, it might be an issue where our customer is encountering insufficient resources, and SRE will handle it.

![]({{site.baseurl}}/docs/runbooks/doctor/images/over_100.jpg){:width="561px" height="244px"}

  * For other invalid values of */cloud/app/cell_usage* or */cloud/app/dea_usage*, execute `curl -X POST http://localhost:4569/cloud/app/app` and analyze the log for causes, or contact {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid %} for a fix.

- *include null/empty data value*
  - For network APIs (_/cloud/monitor/network/*_)
      - If only one network API is impacted:
         - Check the API by curl from the environment's Doctor backend. If it returns valid data that is not null/0, then it might be a transient error and can be ignored. Otherwise, if it returns null/0 for all fields, then it's invalid. Execute `curl -X POST http://localhost:4569/cloud/monitor/network/datapower/status` to trigger a refresh, and then see whether there's valid data returned.

      - If more than one network API is impacted:
         - Check the [environment's Datapower dashboard]({{site.data.ibm.oss-doctor.links.doctor-portal.link}}/#/datapower_dashboard). If there's no data, contact {% include contact.html slack=datapower-config-slack name=datapower-config-name userid=datapower-config-userid notesid=datapower-config-notesid %}.

         - If all data fields of these APIs are null/0, check the *cloud.datapower.dpaddress* field of the environment's config yml file (located in the [{{site.data.ibm.oss-doctor.links.doctor-config-repo.name}}]({{site.data.ibm.oss-doctor.links.doctor-config-repo.link}}) GitHub repository). If there's no info there, contact {% include contact.html slack=bosh-director-slack name=bosh-director-name userid=bosh-director-userid notesid=bosh-director-notesid %}.

         - If there is a datapower config in yml, it's probably some other datapower config issue. Execute `curl -X POST http://localhost:4569/cloud/monitor/network/datapower/status` and check the log.

         - **Possible causes**:
             - Missing domain name in the url as the following screenshot shows. Contact {% include contact.html slack=datapower-config-slack name=datapower-config-name userid=datapower-config-userid notesid=datapower-config-notesid %}.
              ![]({{site.baseurl}}/docs/runbooks/doctor/images/missing_domain_name.jpg){:width="556px" height="159px"}

             - Missing datapower config in JML as the following screenshot shows. Contact {% include contact.html slack=datapower-config-slack name=datapower-config-name userid=datapower-config-userid notesid=datapower-config-notesid %}.
              ![]({{site.baseurl}}/docs/runbooks/doctor/images/jml_datapower_config.jpg){:width="694px" height="99px"}

             - Data returned is empty as the following screenshot shows. Contact {% include contact.html slack=datapower-config-slack name=datapower-config-name userid=datapower-config-userid notesid=datapower-config-notesid %}.
              ![]({{site.baseurl}}/docs/runbooks/doctor/images/network_empty.jpg){:width="598px" height="69px"}



* *returned data are: {"result"=>"failed", "detail"=>nil}*

   - For *dea_usage* or *cell_usage* APIs, check the 4 usage circle graphs for the env. If there's no data there it might be env failing to fetch ccdb config from BOSH yml. A restart of the doctor agent might fix this.
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/empty_graphs.jpg){:width="586px" height="260px"}


* *update time longer than 6 hours*

    - For */cloud/instance* API, execute `curl -X POST http://localhost:4569/cloud`.

    - For */cloud/app/dea_usage* or */cloud/app/cell_usage* API, execute `curl -X POST http://localhost:4569/cloud/app/app`.

* *Failed to get the list of all current environments*

  In most cases it's a false alarm. If a normal alert of "Failed to get valid resource usage data for x env" follows in a few minutes, then it is a false alarm and can be safely ignored. Otherwise, Stop and then Start the *monitor_cloud_usage_data* job in Wukong > Scheduler Task to re-trigger the checking.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

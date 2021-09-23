---
layout: default
description: Once an environment is decommissioned we need do some clean work for Doctor agent
title: DECOMMISSIONED - Clean decommissioned environment from Doctor
service: doctor
runbook-name: "Runbook - Clean decommissioned environment"
tags: Decommission, Clean, Runbook,Doctor
link: /doctor/Runbook_Clean_Decommissioned_Environment.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

# Decommissioned

## Purpose
Once an environment is decommissioned we need do some clean work for Doctor agent, so this environment will not be displayed on Doctor portal anymore

## Technical Details
1. Remove all Doctor services and compose configuration on agent VM
2. Remove supervisor task and configuration on agent VM
3. Delete keeper from Wukong portal
4. Delete environment from environment type list on user page of wukong portal


## User Impact
NA

## Instructions to Fix

### Make sure the environment has been decommissioned.

  * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  * Select **Governance**
  * Select **Handover Management**
  * User the search box, to find the environment name.
  * Check the environment.
  * If the environment has been decommissioned continue, otherwise stop here.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/decommissioned_env.png){:width="640px"}

### Remove alerts from NewRelic

- Go to [{{new-relic-portal-name}} Alert polices]({{new-relic-portal-link-polices}}).
- Select a police for the list below, and click on it.
   > **Note:** The listed polices are the active ones at time when this runbook was updated, polices can be added or removed depending of the business needs. Please update this runbook if you see any differences and/or contact {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %} for assistance or via slack channel: <a href="{{oss-doctor-link}}">{{oss-doctor-name}} for help.

| Police Name    |
| ------------- |
| [access_service_health_check](https://alerts.newrelic.com/accounts/1926897/policies/282485)  |
| [access_service_health_check_watson](https://alerts.newrelic.com/accounts/1926897/policies/357798)  |
| [backend_service_health_check_watson](https://alerts.newrelic.com/accounts/1926897/policies/503209) |
| [BBOAlertPolicy](https://alerts.newrelic.com/accounts/1926897/policies/317004) |
| [Blink policy](https://alerts.newrelic.com/accounts/1926897/policies/429944) |
| [Blink Watson policy](https://alerts.newrelic.com/accounts/1926897/policies/434107) |
| [Cloud metrics policy](https://alerts.newrelic.com/accounts/1926897/policies/437899) |
| [cloud_release_check_policy](https://alerts.newrelic.com/accounts/1926897/policies/367099) |
| [Doctor Agent Policy](https://alerts.newrelic.com/accounts/1926897/policies/223233) |
| [doctor_server_system_usage](https://alerts.newrelic.com/accounts/1926897/policies/276909) |
| [Firecallmgr checkin policy](https://alerts.newrelic.com/accounts/1926897/policies/282439) |
| [security_service_health_check_watson](https://alerts.newrelic.com/accounts/1926897/policies/503152) |
| [security_service_health_policy](https://alerts.newrelic.com/accounts/1926897/policies/440552) |
| [SSHTunnel policy](https://alerts.newrelic.com/accounts/1926897/policies/427729)|

- Search for the decommissioned environment, using the *Search conditions* filter.
 - If you find the decommissioned environment in the police, switch it off or removed it.
 ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/polices/turn_police_off.png){:width="640px"}
   - You will get the following message: __Are you sure you want to disable this condition? All related open incidents will close as a result.__
   - Click **OK**
- Repeat the process for the all policies listed.


### Remove doctor containers and configuration

>**Note:** Sometimes the environment mentioned in the PD has been partially decommissioned already, and the Doctor agent is  not longer running. If that is the case, you won't be able to SSH or run remote command, in that case, skip this step.

  {% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}

  * Run `docker ps` or {% raw %} `docker ps --format '{{.Names}}'` {% endraw %} to list all present containers.

  * Run `docker rm -f <container_name>` to remove them.
    - e.g. `docker rm -f bbo_agent`

  * Delete /opt/doctor-keeper/config/docker-compose.yml file.
    - `rm /opt/doctor-keeper/config/docker-compose.yml`

  * Go to /etc/supervisor/conf.d
    - `cd /etc/supervisor/conf.d`

  * Remove all configuration file under this path.
    - `rm *.*`  or `rm -rf /etc/supervisor/conf.d`

  * Run `supervisorctl status` to list all supervisor task.

  * Run `supervisorctl stop <task_name>` to stop it.
    > **WARNIGN Make sure doctor_keeper is the last task to be removed**
    - e.g. `supervisorctl stop doctor_keeper`


### Remove the /healthz check for the environment from Echometer.
  - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Click **Echometer**.
  - Search for the environment.
  - Click the **Delete** button.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/healthz.png)

### Remove environment from Doctor Keeper

  - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Doctor Keeper** page.
  - Search environment name and delete keeper.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/remove_env.png){:width="640px"}

### Remove environment from Environment Type

  - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **User** page.
  - Click **Environment Type** tab.
  - Search environment name and delete it.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/env_types_delete.png){:width="640px"}

### Refresh ETCD database
  - Selet **Doctor Kepeer**.
  - From the top right hand side click on **Sync**
  - Wait until it completes
  - Click on **Refresh**


## Notes and Special Considerations

After completed all the steps the environment might still displayed at Doctor datacenter, the environment will be removed from datacenter until Doctor server side gets refreshed and it may take a couple hours to do so.

{% include {{site.target}}/tips_and_techniques.html %}

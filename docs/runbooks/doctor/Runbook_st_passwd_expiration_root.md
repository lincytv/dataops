---
layout: default
description: How to solve an alert for root password expire on local env
title: How to solve an alert for root password expire on local/dedicated environment
service: doctor
runbook-name: root password expire  
tags: oss, bluemix, doctor, gre
link: /doctor/Runbook_st_passwd_expiration_root.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md  %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Technical Detail
Doctor is helping to extend root password on local environments. There are scheduled jobs defined and running in self-healing page. When there is an alert reported that the root password is going to expire, that means Doctor did not extend it successfully. Currently, the system ips that are managed by Doctor's job are defined in **envips.csv** file.

# Local Environment

## Step 1. Confirm the system is in envips.csv
  * Login bosh cli using your sso  (for local env, there are 2 cli, need to check one by one because there might only be one cli that has envips.csv)
  * Go to /root/bin or /var/releases/bin  
  * Run command: cat envips.csv   
  * If the IP is not in the list, create a git issue to GRE https://github.ibm.com/cto-gre/common/issues, go to step 3
  * If the IP is already in the list, go to next step

## Step 2. check job log
  * Login [{{doctor-portal-name}}]({{doctor-portal-link}})
  * Select **Diagnose**.
  * Click on **Self-healing**.
  * Select **Schedule Jobs** on the top drop down.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_jobs.png){:width="640px"}
  * Find the corresponding jobs  ( you can select show 100 items in each page,  using browser's find function with key words  "extend root")
     * There are several jobs for different type of systems , find the one according the system type
        * 'Extend root password for local BNPP director',
        * 'Extend root password for local bosh director'
        * 'Extend root password for local bosh cli'
        * 'Extend Root Password For Local Env'
  * Click the action button at the right of the job ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/three_dots.png){:width="40px"}. (3 dots)
  * Select environment name
  * In the popup window, click the log to see the detail, if it report job failure, re-run the job by clicking
       **Run One-time** buttton on the popup window
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/selfhealing/schedule_jobs_logs.png){:width="640px"}
  *  If the job succeed, but error vms reported, contact {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid %} then go to step 3

## Step 3. Extend root password manually
   > If there are too many systems, please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} to get help)

   * login the systems that was reported with root password expire in the incident
   * run comand: sudo -i
   * run command : `chage -d yyyy-mm-dd root`  (yyyy-mm-dd is the date of today)
   * run command : `chage -l root`, to make sure password expire date is extended， then you can resolve the incident


# Dedicate Environment

## Step 1

On Doctor agent shell, run command below replacing the port number for each environment,  
 1. `curl -k -X POST http://127.0.0.1:<port>/cloud/refresh/iaas_servers`  
 2. `curl -k -X POST http://127.0.0.1:<port>/security/firecall/check_root_expiration`

>For 1 get the port number from [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}/tree/master/config) file taishan_dedicate_<envname>.yml

![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/doctor_conf_taishan_env_get_port.png){:width="640px"}

>For second command get the port from the compose YML file at **doctor_security**. Use  `cat /opt/doctor-keeper/config/docker-compose.yml`

![]({{site.baseurl}}/docs/runbooks/doctor/images/root_pwd/docker_security_port.png){:width="640px"}

## Step 2

* In [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select  **Scheduler Task**.
* Select an environment from left-top corner.  
* Find the task call api by searching URL `/cloud/refresh/iaas_servers` and Name: `refresh_iaas_servers` ,see figure, click **Stop** button then click **Start** button.  
* Find the task call api by searching URL`/security/firecall/check_root_expiration` and Name: `root password - reset password for expiration` ,see figure, click **Stop** button then click **Start** button.    
 ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/scheduler_task_check_root_expiration.png){:width="640px"}


## Notes and Special Considerations
   {% include {{site.target}}/tips_and_techniques.html %}

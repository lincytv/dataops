---
layout: default
description: This alert indicates a heartbeat loss for the BBO agent.
title: DECOMMISSIONED - Doctor BBO Agent Down
service: bbo
runbook-name: Doctor BBO Agent Down
tags: oss, bluemix, bbo, BBO_Agent_Down
link: /doctor/Runbook_BBO_Agent_Down.html
type: Alert
---

{% capture docker-compose-yml %} {{site.data[site.target].oss-docker.links.compose-yml.link}} {% endcapture %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This runbook is intended for use by a Doctor user.  GRE users should use [this]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Exec_Fail_GRE.html) runbook because they will not generally have access to all the
functions described below.

This alert indicates a heartbeat loss for the BBO agent.
<div class="alert alert-danger" role="alert">
<strong>Do <u>not</u> resolve the PagerDuty incident yourself!</strong> Monitoring will detect that the problem is fixed and automatically resolve the incident.
If the problem is not fixed, the BBO services will remain down in the environment but a new PagerDuty incident will <u>not be opened</u>.
</div>

## Technical Details
BBO Agent is hosted on Doctor Agent VM. It relies on BOSH CLI connectivity.

A Hello-World task is sent to the BBO agent to see if it executes, if an output is generated, and if the output is as expected.

### Possible errors (Check this one first before to continue, you may find the solution here)

Sometimes the output.logs contains errors as follows
Check [Most common BBO errors]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down_Common_Output_Log_Errors.html)


### BBO Agent in docker compose file
The configuration for BBO agent is in the file ``{{docker-compose-yml}}`` on the Doctor Agent.
When necessary edit this file:

* From [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select **Doctor Keeper**
* Search for the environment.
* Start a **SSH** session
* Use an editor, such as vi, and edit ``{{docker-compose-yml}}``
> **Note:** Use [Jump Box]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html) as alternative to get on the instance VM.

{% include_relative _{{site.target}}-includes/tip_ssh.md %}
__

* In the file, there is a section similar to:
  ```  
    bbo_agent:
      command: 4569 taishan_local_fpl https://172.24.18.132:4568
      container_name: bbo_agent   
      environment:
      - GROUP_KEY=377b924d4468ca49814ab141f314fa4c
      image: doctormbus1.bluemix.net:5000/bbo_v3/backend:3.58
      mem_limit: 1500000000   
      network_mode: host   
      restart: always   
      stdin_open: true   
      tty: true   
      volumes:   
      - /opt/bbo/data:/opt/bbo/data
  ```
  Where:
    * The number after _command_ is the port number.Look for _port:_ for each particular environment.{% capture note_backend_port %}{% include_relative _ibm-includes/get_backend_port.md %}{% endcapture %}
    {{ note_backend_port  | markdownify }}
  * The last two parameters in the command line (`taishan_local_fpl https://172.24.18.132:4568`
    in this example) may not exist, as in:
    ![docker-compse.yml]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/docker-compose1.png){:width="500px"}
    <br>They are used by more current versions of the BBO agent. You should try to add them. They are:
      - Parameter 2 (e.g. taishan_local_fpl) is the name of the configuration file.  It is the base name of the file in [this](https://github.ibm.com/BlueMix-Fabric/doctor-configuration/tree/master/config) GHE project.
      - Parameter 3 (e.g. https://172.24.18.132:4568) is the IP and port for accessing the registry that makes this configuration file available.  The IP and port can be copied from the
        doctor_backend portion of the docker-compose.yml file:
        ![docker-compse.yml]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/docker-compose2.png){:width="600px"}
         You can check if the configuration file can be downloaded when you restart the bbo_agent.  When you restart the container, you should
        not see the error `Failed to load BBO config from doctor config file`. If you see this error then look
        [here]({{site.baseurl}}/docs/runbooks/doctor/Runbook_missing_route_to_mbus_on_inception_vm.html) for some hints
        as to what IP and port to use.
  * GROUP_KEY is used to download configuration file. At this time, it should be `377b924d4468ca49814ab141f314fa4c`.
  * The version number of BBO agent is at the end of "image".
      You can find the available version number as shown:
      ![BBO version]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_image_ver.png)
  * Image registry, refer to the doctor_backend section in ``{{docker-compose-yml}}`` file.
      This address is usually _doctormbus1.bluemix.net:5000_ or _doctormbus3.bluemix.net:5000_.

* After editing this file.
* Run `curl -k https://127.0.0.1:5999/compose/up` to restart the BBO agent.
  >**Note:** if this command hangs, you need to pull the image manually first, by running the command ` docker pull 10.250.9.68:5000/bbo_v3/backend:3.16 ` (substitute 3.16 with the actual version number).

There are many causes for a BBO agent being down, or a BBO task to fail.
For example:
- The BBO agent may run out of memory after running for some time.
- The disk of the Doctor Agent VM may become full causing the BBO Agent container to stop.
- The disk of the BOSH CLI VM may become full causing the BBO Agent container to stop.
- The function id (doctor or Taishan) on BOSH CLI VM may be expired.
- The function id (doctor or Taishan) may be locked due to excessive incorrect password attempts (potentially by some unknown scripts).
- Network connectivity issue.
- BBO version is too old.
- BBO job is not correctly synchronized.
- or even: BBO job bugs.
- etc.

## User Impact
BBO job and task cannot be executed.

### Before you start (It may save you much effort)

<div class="alert alert-danger" role="alert">
If you receive <strong>a large number of</strong> BBO Down Alerts or BBO script execution failure for many environments,  <a href="https://doctor.cloud.ibm.com/best_operator/agents.html">Check the BBO agents active chart</a>, <strong>if you see several lines in red, it is an indication that BBO MBUS is down or problem with the BBO server</strong>, for example, the inode usage is full on the BBO Server.

When a problem on BBO server is suspected, <strong>contact</strong> {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} or {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}in slack channel: <a href="{{oss-doctor-link}}">{{oss-doctor-name}}</a> <strong>as soon as possible</strong> or try to follow <a href="{{site.baseurl}}/docs/runbooks/doctor/ibm-only/Doctor_how_to_restart_BBO_agents.html">How to restart BBO agents</a>.
</div>

If the alert reports the follow problem:
```
  /home/doctor/dcf2aed5fd.run.remote.script.sh: line 55: ./bbo.test.for.doctor.sh: No such file or directory
  BBO SCRIPT EXEC WITH ERROR CODE
```
Then please follow the instructions in [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html) and snooze the Pager Duty incident for 24 hours.
Otherwise proceed with the next step.

## Ensure the bbo_agent is Running
1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
2. Click **BBO CI & CD** in the navigation menu
3. Find the environment in one of the BBO Agent lists.
4. If the environment is listed at the bottom of the page in the pink table for `BBO Agent List (Down or not deployed)`.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_agent_list_down_or_not_deployed.png)
5. Press the `restart` button beside the environment name.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_restart.png){:width="160px"}
  - Wait for ~5-10 minutes and refresh the page.
  - The environment should move up to the white table for `BBO Agent List (Running)`.  If this does not happen within a reasonable amount of time you can restart the bbo_agent container as described [here](#restarting-the-bbo-agent) or by changing the version of the bbo_agent as described [here](#3-versions-of-bbo-agent-and-job).

## Check Status in Wukong
On the _BBO CI & CD_ page the number of jobs in the working, pending, and failed and processed state are shown:

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_working_pending_processed.png){:width="640px"}

If you are experiencing Pager Duty incidents for failures running BBO script, the problem may be that there is a backlog of BBO jobs for that particular environment.
* The _Working_ column contains the number of jobs currently running in an environment.
* The _Pending_ column contains the number of jobs waiting in the queue to run.
* The _Completed_ columns contains the number of jobs that have run since the bbo_agent was first created.

* The _Failed_ column contains the number of Jobs that failed.  It is an indication of whether the Jobs are written properly and are not relevant to the health of the bbo_agent itself.

Press the `Refresh` button at the top of the page to show the latest values for these columns.  If you refresh too frequently you may not see any change in values - wait a minute or two before successive refreshes.

If there is a large or growing value in the _Pending_ column, you may experience problems running your own BBO job as described in [Confirm BBO Agent is Working](#confirm-bbo-agent-is-working), or you may not get the output.logs file when you successfully submit your own BBO job.
* It may be that there are too many scheduled jobs being started for this environment and this is beyond your control.  You may just have to wait until the scheduled jobs run their course and complete.
* It may be that the BOSH CLI is very slow in running the jobs and a backlog is building up. You may check this by logging in to the BOSH CLI and running the `top` command as root to see the load on the system.

In general, check the health of the BOSH CLI.

You can reset all these columns back to zero (0) by changing the bbo version number as described in [Versions of BBO Agent and Job](#3-versions-of-bbo-agent-and-job), or by following the instructions at [Restarting the BBO Agent](#restarting-the-bbo-agent)

The value in the _Working_ column should not be zero if there jobs waiting in the _Pending_ column.

The value in the _Completed_ column should continually be increasing, especially if you see jobs in the _Working_ and _Pending_ columns.

In general, the BBO agent is healthy if there are up to 8 jobs in the _Working_ column, less than 30 jobs in the _Pending_ column, and a continuously increasing number in the _Completed_ column. If this is the case, then the incident may automatically resolve soon. It may have been caused by a spike in the number of jobs running in the past or a recent burden on the Bosh CLI.

## Running the Health Check Yourself

The health check for the BBO agent is run every 10 minutes. It takes some time to run the checks and then work those results through the systems to create Pager Duty incidents (for failed results) or to automatically resolve Pager Duty incidents (when BBO agents are repaired and working properly). If you want to resolve a Pager Duty incident more quickly you can run a health check yourself. Click on the *Run Health Check* button located on the BBO CI & CD page next to the environment name:
![Run Health Check]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_run_health_check.png){:width="180px"}  
This runs the health check for an individual environment and can automatically resolve an incident more quickly.

## Confirm BBO Agent is working:

1. Go to [{{doctor-portal-name}}]({{doctor-portal-link}}/#/bbo).
2. Select the environment from environment list.

      Select the environment name in the {{doctor-alert-system-name}} incident under the Details tab,
      like the follow:

        BBO Agent Down:

        Name:au-syd(YP_SYDNEY)

        Where YP_SYDNEY is the environment.


3. Click on **Say Hello** button or input the following BBO command:

    > **Note:**  Please do _NOT_ replace `$DOCTOR_USER` with your id.  $DOCTOR_PWD does not need to be specified anymore

    ```
      run boshcli script: bbo.test.for.doctor.sh $DOCTOR_USER $DOCTOR_USER
    ```
4. Click the **Analyze** button , the above command eventually generates a file named `output.logs`.
5. The BBO agent is working properly, if the content of `output.logs` is like the following and contains the words _Hello World_:

    ```
    =================================================
    192.168.227.108 (hello-world.sh)
    =================================================
    Hello World
    ```
    The IP address (192.168.227.108) may be different in your output.  If your output satisfies these conditions, you are finished! **Do not** resolve the incident - it will automatically resolve once NewRelic determines that there isn't a problem anymore.  Also note that a script is typically run on several VMs with different IP addresses - you may see several of them return _Hello World_ in the _output.logs_ file.

![BBO Agent is working]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/bbo_agent_is_working_confirmation.png){:width="639px" height="422px"}

## Instructions to Fix

If you get an error like this:

```
 Could not open a connection to your authentication agent.

 ERROR: No key file loaded for SSH key authentication and no password provided.

 Usage: ./run.sh [OPTIONS]...[ARGS]

   -s|--script
```

login to boshcli, check the /tmp permissions:

`sudo ls -al / | grep tmp`

if the /tmp permissions is not 777, change it to 777

`sudo chmod 777 /tmp`

and try to run BBO again, from [{{doctor-portal-name}}]({{doctor-portal-link}}/#/bbo).

Each of the following sections fixes or eliminates one cause of failure.
Try one section at a time, and [verify if the problem is fixed](#confirm-bbo-agent-is-working)

### 1. One and only one BBO agent per environment   
For an environment with more than one instance VMs, there must be one and only one BBO agent running among all instance VMs.

1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}); use **Remote Command**.
2. Enter environment name in the _Filter Environment Name_ field.
3. Select all inceptions for the environment.
4. Enter `docker ps | grep bbo_agent` in the _shell command_ box.
5. Press the _Run_ button.
6. There should be exact one instance with a running "bbo_agent".

![One bbo_agent]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/bbo_agent_one_and_only_one_per_environment.png){:width="639px" height="422px"}

If you find an extra bbo_agent running,
comment out the [bbo_agent section from the docker-compose file, and curl](#bbo-agent-in-docker-compose-file) to restart the agent.  To change a line into a comment simply add a hash/pound sign (#) to the line, typically in column 1.

If there is no bbo_agent running,
add a [bbo_agent section to the docker-compose file, and curl](#bbo-agent-in-docker-compose-file) to restart the agent.

### 2. Confirm Bosh CLI is working
BBO Agent will run scripts on Bosh CLI. You need to confirm that BoshCLI is working properly.
If not, contact a Bluemix Fabric SRE, via [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}), to fix it.

* You need to test the login to the BoshCLI via w3 BoshCLI (aka SSH through [Jumpbox](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html)).

>**Note:**<br>
[Request access to Jumpbox](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html#assumption-and-onboarding-process) <br>
[Problems logging into Jumpbox](https://pages.github.ibm.com/cloud-sre/runbook/docs/runbooks/doctor/Runbook_problems_logging_into_SSH_jumpbox.html)

```
$ ssh [your intranet id]@bosh-cli-bluemix-new.rtp.raleigh.ibm.com  (example intranet id: ibmuser@us.ibm.com)
$ cd /var/releases/bin
$ ./boshcli_[env].sh
```

* If you get the following message:
```
ssh: connect to host 9.39.221.144 port [port number]: Connection refused
```
Please contact a Bluemix Fabric SRE to check BoshCLI via [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.

* You also need to test login via web SSH and perform some system checks.
* Go to [Doctor Datacenter]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}/#/datacenter)
* Click SSH icon _(NOT CLI icon)_ of `[env]` to login to BoshCLI using your SSO ID and password.
![ssh icon]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_ssh_icon.png){:width="639px"}

* Make sure you can login to BoshCLI without errors.
![How to determine if you have logged in successfully?]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_How_to_determine_if_you_have_logged_in_successfully.png){:width="639px"}

* If you get a message **No passwd entry for user 'SSO ID'**  or **su: Authentication failure** and you are sure you typed your correct SSO ID password, send an email to {%include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid %} to check your access for the environment selected. As an alternative, use **Remote Command** form [{{wukong-portal-name}}]({{wukong-portal-link}}) to continue with the next steps.

* Make sure BoshCLI is not out-of-disk by run `df -h` command. Follow [Disk Usage Is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html#step-5-if-disk-usage-is-still-too-high) if you need to remove some files to make more space available.
* Make sure BoshCLI is not out-of-memory by run `top` command.
* To find the [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) who is oncall via @cybot in Slack, post `@cybot whois oncall GRE` in the channel.

#### What if the Inception VM is Too Busy?
In a local environment, the BOSH CLI and the Doctor Agent services run on the same machine (the Inception machine - IVM).

{% include_relative _{{site.target}}-includes/tip_busy_vm_1.md %}

A low user Cpu usage might indicate that BBO jobs are being interrupted and not
running smoothly. The backlog of jobs could increase showing up as a growing number in the _Pending_ column.

### 3. Versions of BBO agent and job
* Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
* Click **BBO CI & CD** in the navigation menu.
* Find the environment in one of the BBO Agent lists.
* If the environment is listed in the pink table for `BBO Agent List (Down or not deployed)`.
  - Press the `restart` button in the same table cell as the environment name.
  - Wait for ~5-10 minutes and refresh the page.
  - See the environment moved to the white table for `BBO Agent List (Running)`.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_agent_list_down_or_not_deployed.png)
* If the environment is in the `BBO Agent List (Running)` list, select the `[env_name]` by selecting the checkbox.
* Verify the BBO version of `[env_name]`.
* Choose a different version (always choose one of the latest two versions) by selecting 'Select BBO Image Version' from the drop-down list.   
> **Note:** If version change can't be done on **BBO CI & CD** page, you can go to **CI & CD** page to do version upgrade.     

* Click the 'Update' button.
* Wait ~5-10 minutes before refreshing the page to confirm the version was successfully changed.
![bbo_version_update]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_update_version.png){:width="640px"}  

> **Note:** Changing the **CI & CD** version changes the **Job Version** column to blank.
It's important to first select the environment, click the silver **Refresh** button, then click the **Restart** button next to environment name. This will restart the BBO Agent.

> **Important:** Make sure **Job Version** column is not **0**, if yes, select this environment and click **Sync Job** button to sync BBO job to latest version.

> **Note:** If BBO agent version can't be changed from portal **Wukong > BBO CI&CD**, try to do it on Doctor agent VM, modify the version number in the ``{{docker-compose-yml}}`` file, then `curl` to restart BBO agent at the new version.



If there is an extra bbo_agent running,
comment out the [bbo_agent section from the docker-compose file, and curl](#bbo-agent-in-docker-compose-file) to restart the agent.  To change a line into a comment simply add a hash/pound sign (#) to the line, typically in column 1.

If there is no bbo_agent running,
add a [bbo_agent section to the docker-compose file, and curl](#bbo-agent-in-docker-compose-file) to restart the agent.

#### _You should follow all the steps in each section._

#### Each environment can run only one BBO agent instance.

Otherwise, you may get the context of output.logs like this:

    SL_USER is null
    SL_API_KEY is null
    LOGIN TARGET VMS via doctor certificate!

If there are two Doctor Agent VMs and both are running the bbo_agent,
stop one instance and comment out the bbo_agent part in the file ``{{docker-compose-yml}}`` on one node.

Alternatively, this could indicate a problem accessing the environment's doctor-configuration file
[here](https://github.ibm.com/BlueMix-Fabric/doctor-configuration/tree/master/config), or in the contents of that file.
Please contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}).


* If the content of _output.logs_ is 'Hello World', this indicates that the BBO Agent is working properly. **Do not** resolve the incident - it will auto-resolve shortly.

* If the content of _output.logs_ contains: _./bbo.test.for.doctor.sh: No such file or directory_ or _./run.sh: No such file or directory_, then notify the on-call [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) to sync BBO scripts for this environment. Use `@cybot whos oncall GRE` to locate the on-call [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}). Once the files are made available, the incident will automatically resolve (BBO script is located at BoshCli's folder /root/bin. You can check if the script exists on the BoshCli vm which is defined in the Doctor yml file).

* If you got an error like _/home/doctor/bbo_7cfa71b246run.remote.script.secure.sh: line 55: ./: Is a directory_, try another command: `run boshcli script: analyze.ccdb.sh --help`. The output should contain:
    ```
    Displays basic organization, application, and services statistics in CCDB.

    Usage: ./analyze.ccdb.sh [OPTIONS]...[ARGS]
    ...(more)
    ```

    If the content of output.logs contains: _./analyze.ccdb.sh: No such file or directory_, then notify the on-call [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) as above and wait for the incident to automatically resolve.

* If you get the _output.log_ generated, and the following message in output:

    ```
    spawn rm -f /opt/bbo/tasks/2b41024e09/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55/bbo_para_string_2b41024e09.txt
    spawn ssh -A doctor@10.144.27.234
    You are required to change your password immediately (password aged)
    ```

    It means the password of the function id (Doctor or Taishan) on BoshCli VM has expired. You need to follow the steps to refresh the password:

      1. Remember the function id in the output `{function id}@xx.xxx.xxx.xx message`.
      2. Login to the BoshCli VM using your SSO id.
      3. Run command `sudo su` to switch to root.
      4. Run command `passwd {function id}` for example: `passwd doctor`.

    Then input the original password of the function id to refresh it.
    > **Note:** you CAN NOT change the password text freely. The password should be fixed to make sure the Doctor function works well. You should get the password of function id from the Doctor supervisor. Any question regarding the function id password, please contact {% include contact.html slack=oss-developer-slack name=oss-developer-name userid=oss-developer-userid notesid=oss-developer-notesid %}.

* If the output log contains:
    ```
    ERROR: Unable to establish a connection to [xxx.xxx.xxx.xxx] with the user name and password provided.
           Verify that the user name and password specified are correct.
    ```
    please do:
    1. login the IP which is shown in the error message. You could try login to agent first, then ssh IP.
    2. check with `chage -l doctor`, make sure the user is not expired. If expired, extend the expiration date.
    3. goto **Wukong -> Privilege ID Management -> select ENV -> find the IP above -> click "Create ID" button**.
    4. wait for the email response. If success, try running the helloworld again. Otherwise, report to {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid%} or {% include contact.html slack=oss-developer-slack name=oss-developer-name userid=oss-developer-userid notesid=oss-developer-notesid%}.

* If the output log does not generate a link, make sure the BBO command was entered correctly, and then go to the next section.
    ![bbo_example]({{site.baseurl}}/docs/runbooks/doctor/images/bbo_example.png){:width="639px" height="422px"}

* If the script continues running without _output.log_, please follow these steps:

    [Restarting the BBO Agent](#restarting-the-bbo-agent)and see if the restart fixes it (via the hello world command).
    1. Logon on to BoshCli of this environment using your SSO ID and password.
    2. Run `sudo –i`.
    3. Add function id into sudo without password.
      ```
      echo "doctor ALL=(ALL:ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)
      echo "taishan ALL=(ALL:ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)
      ```
    4. Unlock function ID.
      ```
      faillog -u doctor -r
      faillog -u taishan -r
      ```
    5. Restart the SSH service.
       `service ssh restart`
    6. Run the BBO command on [{{doctor-portal-name}}]({{doctor-portal-link}}/#/bbo). If the content of _output.logs_ is 'Hello World', your work is done.  **Do not** resolve this incident - it will automatically resolve once NewRelic determines that the problem is fixed. If the script is still keep running without _output.log_, you need to continue with the next steps.
    7. Go to [{{site.data[site.target].ghe.repos.bluemix-fabric.name}} doctor-configuration]({{site.data[site.target].ghe.repos.bluemix-fabric.link}}/doctor-configuration/tree/master/config) and find the .yml of the environment e.g. _taishan_dedicated_bnsf.yml_. Open the yml, find **boshcli_user** and **bosh_cli**.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/cloud_boshcli_user_bosh_cli.png)
    8. Logon to [{{wukong-portal-name}}]({{wukong-portal-link}}), find the environment, click SSH of a _doctor_agent_ VM, use your SSO ID, run `sudo -i`, run `docker ps` (if there is no bbo_agent, please SSH the other VM on the Wukong page) and follow this steps: [Missing authorized keys](http://localhost:4000/docs/runbooks/doctor/Runbook_BBO_Agent_Down_Common_Output_Log_Errors.html#case-3-missing-authorized_keys)
    9. Open a bash shell into the bbo_agent container, and try to SSH to BoshCli:


### Restarting the BBO Agent

To restart the BBO Agent you need to sign onto the Doctor Agent machine from _Doctor Keeper_ as described [here](#1-one-and-only-one-bbo-agent-per-environment) and run these commands:

```
sudo -i
docker rm -f bbo_agent
curl -k https://127.0.0.1:5999/compose/up
```

`sudo -i` is needed since you will need to run the other commands as root.

If you experience problems with the _docker_ command you can run the following to see if the docker service is healthy:

```
# docker rm -f bbo_agent
# Error response from daemon: driver "devicemapper" failed to remove root filesystem for a5ead706a991e94607c0c684b61c8
```

  or

```
# docker logs --tail 10 bbo_agent
# Error response from daemon: can not get logs from container which is dead or marked for removal
```

If you get an error returned from the docker daemon such as these, you need to restart it, and then restart the doctor services as follows:

```
# service docker restart
# curl -k https://127.0.0.1:5999/compose/up

```
#### Check BBO logs:
* Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
* Click **BBO CI & CD** in the navigation menu.

  ![BBO logs]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_open_ssh.png){:height="150px"}
* Click the `[env_name]` to open the Doctor agent or inception VM where the BBO agent is running. Refer to this command in the screenshot to view logs.
    ![BBO logs]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_logs.png){:width="593px" height="307px"}

## Handling a flood of BB0 Agent Down alerts

In the past there were a few times when this alert was raise for many or all IBM Cloud environments.  The root cause was not known but it could have resulted from some loss of a network connection.  The root cause was resolved quickly but it left 60 or more Pager Duty alerts open.  Instead of testing each and every environment manually, wait for NewRelic to determine that the problem no longer exists and resolves the incidents automatically.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

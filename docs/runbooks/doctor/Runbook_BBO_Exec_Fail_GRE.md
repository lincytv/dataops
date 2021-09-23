---
layout: default
description: This alert indicates a BOSHCLI Script can not be executed using BBO.
title: RETIRED Doctor BBO script could not be executed correctly - runbook for GRE
service: bbo
runbook-name: "Doctor BBO script could not be executed correctly - runbook for GRE"
tags: oss, bluemix, bbo, BBO_Agent_Down, st_bbo_exec_fail, gre
link: /doctor/Runbook_BBO_Exec_Fail_GRE.html
type: Alert
---

{% capture docker-compose-yml %} {{site.data[site.target].oss-docker.links.compose-yml.link}} {% endcapture %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This alert indicates a BOSHCLI Script can not be executed using BBO.
<div class="alert alert-danger" role="alert">
<strong>Do <u>not</u> resolve the PagerDuty incident yourself!</strong> Monitoring will detect that the problem is fixed and automatically resolve the incident.
If the problem is not fixed, the BBO services will remain down in the environment but a new PagerDuty incident will <u>not be opened</u>.
</div>

## Technical Details
BBO Agent is hosted on Doctor Agent VM. It relies on BOSH CLI connectivity.

A task to run _bbo.test.for.doctor.sh_ is sent to the BBO agent to see if the BBO agent can run the script on the BOSH CLI. The output is examined for the words `Hello world`. If the output is not generated or if it is but does not contain this string then the incident is raised.

There are many causes for a BBO agent being down, or a BBO task to fail.
For example:
- The BBO agent may run out of memory after running for some time.
- The disk of the Doctor Agent VM may become full causing the BBO Agent container to stop.
- The function id (doctor or taishan) on BOSH CLI VM may be expired.
- The function id (doctor or taishan) may be locked due to excessive incorrect password attempts (potentially by some unknown scripts).
- Network connectivity issue.
- BBO version is too old.
- BBO job is not correctly synchronized.
- or even: BBO job bugs.
- etc.

Some of these causes are addressed by this runbook.  If you have followed all the steps in this runbook and the problem persists, you can reach out for help as described in [How to Reach Out for Help](#how-to-reach-out-for-help).

GRE team members can apply for access to {{wukong-portal-name}} as described [here]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Request_the_operator_bbo_role.html).

## User Impact
BBO job and task cannot be executed.


### Special instructions if you have a large number of st_bbo_exec_fail incidents

If you receive **a large number of** st_bbo_exec_fail incidents or failures to run a BBO script for many environments, pick one environment and see if the problem can be fixed by following this runbook. If not, there might be a problem with the BBO Server, for example, the inode usage is full on the BBO Server.

When a problem on BBO server is suspected, contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} in slack channel: [{{oss-doctor-name}}]({{oss-doctor-link}}) as soon as possible.

## Ensure the bbo_agent is Running
1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
2. Click **BBO CI & CD** in the navigation menu.
3. Find the environment in one of the BBO Agent lists.
4. If the environment is listed at the bottom of the page in the pink table for `BBO Agent List (Down or not deployed)`.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_agent_list_down_or_not_deployed.png)
5. Press the `restart` button beside the environment name.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_restart.png){:width="160px"}
  - Wait for ~5-10 minutes and refresh the page.
  - The environment should move up to the white table for `BBO Agent List (Running)`.  If this does not happen within a reasonable amount of time you can restart the bbo_agent container as described [here](#4-restarting-the-bbo-agent) or by changing the version of the bbo_agent as described [here](#3-versions-of-bbo-agent-and-job).

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

You can reset all these columns back to zero (0) by changing the bbo version number as described in [Versions of BBO Agent and Job](#3-versions-of-bbo-agent-and-job), or by following the instructions at [Restarting the BBO Agent](#4-restarting-the-bbo-agent)

The value in the _Working_ column should not be zero if there jobs waiting in the _Pending_ column.

The value in the _Completed_ column should continually be increasing, especially if you see jobs in the _Working_ and _Pending_ columns.

In general, the BBO agent is healthy if there are up to 8 jobs in the _Working_ column, less than 30 jobs in the _Pending_ column, and a continuously increasing number in the _Completed_ column. If this is the case, then the incident may automatically resolve soon. It may have been caused by a spike in the number of jobs running in the past or a recent burden on the Bosh CLI.

## Running the Health Check Yourself

The health check for the BBO agent is run every 10 minutes. It takes some time to run the checks and then work those results through the systems to create Pager Duty incidents (for failed results) or to automatically resolve Pager Duty incidents (when BBO agents are repaired and working properly). If you want to resolve a Pager Duty incident more quickly you can run a health check yourself. Click on the *Run Health Check* button located on the BBO CI & CD page next to the environment name:
![Run Health Check]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_run_health_check.png){:width="180px"}  
This runs the health check for an individual environment and can automatically resolve an incident more quickly.


## Additional instructions

Each of the following sections fixes or eliminates one cause of failure.
Try one section at a time, and [verify if the problem is fixed](#confirm-bbo-agent-is-working)

### 1. One and only one BBO agent per environment   
Some environments have more than one Doctor Agent.  In public and dedicated environments, the Doctor Agent is a separate VM.  In local environments, the services of Doctor Agent and the Bosh CLI run together on the Inception machine(s).  In the _Doctor Keeper_ page of [{{wukong-portal-name}}]({{wukong-portal-link}}) the Doctor Agent machines (or inception machines for local environments) are shown - one or more per environment.  The BBO agent should only be running on one machine for each environment.  If there is only one Doctor Agent for the environment, continue with the [next step](#2-confirm-the-bosh-cli-is-working).

Here are instructions to ensure that only one BBO agent is running in each environment:

1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}); click on _Doctor Keeper_.
2. Enter environment name in the _Enter to filter environment_ field; press _Enter_.
3. For each machine, click on SSH,
   - type `su <SSO-ID>` substituting your SSO ID for `<SSO-ID>`,
   - when promoted, enter your password, and
   - then run `sudo -i` to become root.
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/WukongDoctorKeeper2.png){:width="500px"}
4. Run the command `docker ps | grep bbo_agent`.
5. You should see the BBO agent listed. If the bbo is not listed try running `docker ps -a | grep bbo_agent` (the *-a* parameter shows all containers, running or not). If the status of the bbo_agent is exited (like `Exited (137) 22 minutes ago`) you need to restart it as described [here](#4-restarting-the-bbo-agent).

**Note** You can also log onto these machines from [{{doctor-portal-name}}]({{doctor-portal-link}}).

If you find an extra bbo_agent running, choose one of the Doctor Agent machines and remote it by running `docker rm -f bbo_agent` to remove the bbo_agent container from that machine.  You should mention that there were two bbo_agents running in the environment [here](#how-to-reach-out-for-help).

If there is no bbo_agent running on either machine you need to reach out for help [here](#how-to-reach-out-for-help).

### 2. Confirm the Bosh CLI is working
BBO Agent will run scripts on Bosh CLI. You need to confirm that BoshCLI is working properly.
If not, you may need to restart it.

* You need to test the login to the w3 BoshCLI using bosh-cli-bluemix-new.rtp.raleigh.ibm.com (also known as SSH through [Jumpbox](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html)). To log on to the Jumpbox, follow [these instrutions](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html#assumption-and-onboarding-process).  If you have problems with the JumpBox, follow
[these instructions](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Runbook_problems_logging_into_SSH_jumpbox.html).
```
$ ssh [your intranet id]@bosh-cli-bluemix-new.rtp.raleigh.ibm.com  (example intranet id: ibmuser@us.ibm.com)
$ cd /var/releases/bin
$ ./boshcli_[env].sh
```

* If you get the following message
```
ssh: connect to host 9.39.221.144 port [port number]: Connection refused
```
you must try to login from Doctor.
  - Go to [Doctor Datacenter]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}/#/datacenter)
  - Click SSH icon _(NOT CLI icon)_ of `[env]` to login to BoshCLI using your SSO ID and password.
![ssh icon]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_ssh_icon.png){:width="500px"}
  - Make sure you can login to BoshCLI without errors.
![How to determine if you have logged in successfully?]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_How_to_determine_if_you_have_logged_in_successfully.png){:width="639px"}

  -  If you get a message **No passwd entry for user 'SSO ID'**  or **su: Authentication failure** and you are sure you typed your correct SSO ID password, send an email to {%include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid %} to check your access for the environment selected.

* Make sure BoshCLI is not out-of-disk by run `df -h` command. Follow [Disk Usage Is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html), especially
[step 2]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html#step-2-remove-a-container-and-re-created-it)
to remove the bbo_agent container if you need to free up some disk space.
* Make sure BoshCLI is not out-of-memory by run `top` or the `free -mh` command.

#### What if the Inception VM is Too Busy?
In a local environment, the BOSH CLI and the Doctor Agent services run on the same machine (the Inception machine - IVM).

{% include_relative _{{site.target}}-includes/tip_busy_vm_1.md %}

A low user Cpu usage might indicate that BBO jobs are being interrupted and not
running smoothly. The backlog of jobs could increase showing up as a growing number in the _Pending_ column.

### 3. Versions of BBO Agent and Job
To change the version of the BBO Agent running in an environment, go to [{{wukong-portal-name}}]({{wukong-portal-link}})

1. Click **BBO CI & CD** in the navigation menu.
![bbo_version_update]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_update_version.png){:width="640px"}
2. Find the environment in one of the BBO Agent lists.
   If the environment is listed at the bottom of the page in the pink table for `BBO Agent List (Down or not deployed)` follow the instructions [above](#ensure-the-bbo_agent-is-running)
   If the environment is in the `BBO Agent List (Running)` list, select the `[env_name]` by selecting the checkbox beside the BBO entry in column 1 of the table.
3. Take note of the BBO version of `[env_name]`.
4. Choose a different version (always choose one of the latest two versions) by selecting 'Select BBO Image Version' from the drop-down list.    
5. Click the *Update* button.
6. Wait ~5-10 minutes before refreshing the page to confirm the version was successfully changed.

> **Important:** Changing the BBO version changes the _Job Version_ column to zero (0).  This is an **invalid state**.
If the _Job Version_ column is **0**, select this environment and click the **Refresh Jobs** button, wait 2 minutes, and then click **Sync Jobs** button to sync the BBO job to latest version.

> **Note:** If BBO agent version can't be changed from portal **Wukong > BBO CI&CD** then reach out as described [here](#how-to-reach-out-for-help).

### 4. Restarting the BBO Agent
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

### 5. Check the BBO Agent logs:
* Go to [{{wukong-portal-name}}]({{wukong-portal-link}})
* Click **BBO CI & CD** in the navigation menu.

  ![BBO logs]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_open_ssh.png){:height="150px"}

* Click the `[env_name]` to open the Doctor agent or inception VM where the BBO agent is running. Refer to this command in the screenshot to view the logs of the bbo_agent.
    ![BBO logs]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_logs.png){:width="593px" height="307px"}

## Confirm BBO Agent is working

You can test if the BBO Agent is working properly by submitting your own job. If you get the desired output, you confirmed that the BBO is working properly - the Pager Duty incident will automatically be resolved soon.

![BBO Agent is working]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/bbo_agent_is_working_confirmation.png){:width="639px" height="422px"}

1. Go to [{{doctor-portal-name}}]({{doctor-portal-link}}/#/bbo).  Go to Diagnose->BBO.
2. Select the environment from environment list.

      Select the environment name in the {{doctor-alert-system-name}} incident under the Details tab,
      like the follow:

        Description: Violated New Relic condition: st_bbo_exec_fail:YP_SYDNEY:yp_sydney:public:au-syd.  

        Where YP_SYDNEY is the environment.


3. Click on **Say Hello** button or input the following BBO command:

    > **Note:**  Please do _NOT_ replace `$DOCTOR_USER` with your id.

    ```
      run boshcli script: bbo.test.for.doctor.sh $DOCTOR_USER
    ```
4. Click the **Analyze** button , this eventually generates a file named `output.logs`.
5. The BBO agent is working properly, if the content of `output.logs` is like the following and contains the words _Hello World_:

    ```
    =================================================
    192.168.227.108 (hello-world.sh)
    =================================================
    Hello World
    ```
    The IP address (192.168.227.108) may be different in your output.  The test is typically run on several VMs with different IP addresses - if one of them returns _Hello World_ then the BBO agent is working properly.

    If your output satisfies these conditions, the problem is fixed and you can stop following these instructions.  **The incident will be resolved automatically shortly**.


### Possible errors

Sometimes the output.logs contains errors as follows:


#### a) Null values in the request

You may get the context of output.logs like this:

    SL_USER is null
    SL_API_KEY is null
    LOGIN TARGET VMS via doctor certificate!

For this situation, you will need to follow the instructions [here](#1-one-and-only-one-bbo-agent-per-environment) to ensure there is only one instance of the bbo_agent running for the environment.

#### b) Script bbo.test.for.doctor.sh is not found

If the alert reports the follow problem:
```
  /home/doctor/dcf2aed5fd.run.remote.script.sh: line 55: ./bbo.test.for.doctor.sh: No such file or directory
  BBO SCRIPT EXEC WITH ERROR CODE
```
Then please follow the instructions in [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html) and snooze the Pager Duty incident for 24 hours.
Otherwise proceed with the next step.

#### c) ./ is a directory

If you got an error like:
```
/home/doctor/bbo_7cfa71b246run.remote.script.secure.sh: line 55: ./: Is a directory
```
try another command: `run boshcli script: analyze.ccdb.sh --help`. The output should contain:
```
 Displays basic organization, application, and services statistics in CCDB.

Usage: ./analyze.ccdb.sh [OPTIONS]...[ARGS]
...(more)
```

If the content of output.logs contains: _./analyze.ccdb.sh: No such file or directory_, then please follow the instructions in [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html) and snooze the Pager Duty incident for 24 hours.
Otherwise proceed with the next step.

#### d) File output.logs is not generated

If the output log does not generate a link, make sure the BBO command was entered correctly:
![bbo_example]({{site.baseurl}}/docs/runbooks/doctor/images/bbo_example.png){:width="639px" height="422px"}

If the script continues running without _output.log_, please follow these steps:

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
6. Restart the BBO agent in [{{wukong-portal-name}}]({{wukong-portal-link}}) on the _BBO CI & CD_ page
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/bbo_cicd/bbo_restart.png){:width="160px"}
7. Run the _bbo.test.for.doctor.sh_ command on [{{doctor-portal-name}}]({{doctor-portal-link}}/#/bbo).

If the content of _output.logs_ is 'Hello World', the problem is fixed and the incident will resolve automatically soon. If the script is still keep running without _output.log_, you will need to reach out for help as described [here](#how-to-reach-out-for-help) and ask the Doctor on-call person to investigate further.

#### e) Exceptions for D_ANZ environments

The BBO agent is not stable on these environments. You still need to follow the instructions in all the previous sections, then wait 10 minutes before trying to run the _bbo.test.for.doctor.sh_ BBO command. You may need to attempt to run _bbo.test.for.doctor.sh_ 4 or 5 times.

## How to Reach Out for Help

If you are unable to fix this problem you can ask for help from the [oss-doctor]() slack channel.  The doctor on-call person can
follow instructions at [Doctor BBO Agent Down]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html) and
[Doctor BBO script could not be executed correctly]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Exec_Fail.html) to fix the problem.  You can find out the doctor on-call person with `@cybot whois oncall doctor`.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

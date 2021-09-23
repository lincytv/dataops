---
layout: default
description: This alert indicates a BOSHCLI Script can not be executed.
title: Doctor BBO script could not be executed correctly
service: doctor
runbook-name: "Doctor BBO script could not be executed correctly"
tags: oss, bluemix, bbo, st_bbo_exec_fail
link: /doctor/Runbook_BBO_Exec_Fail.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This runbook is intended for use by a Doctor user.  GRE users should use [this]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Exec_Fail_GRE.html) runbook because they will not generally have access to all the
functions described below.

This alert indicates a BOSHCLI Script can not be executed via BBO.
<div class="alert alert-danger" role="alert">
<strong>Do <u>not</u> resolve the PagerDuty incident yourself!</strong> Monitoring will detect that the problem is fixed and automatically resolve the incident.
If the problem is not fixed, the BBO services will remain down in the environment but a new PagerDuty incident will <u>not be opened</u>.
</div>

## Technical Details
BBO Agent is hosted on Doctor Agent VM. It relies on BOSH CLI connectivity.

A Hello-World task is sent to the BBO agent to see if it executes, if an output is generated, and if the output is as expected.


## User Impact
BBO job and task cannot be executed.

## Instructions to Fix
Each of the following sections fixes or eliminates one cause of failure.
Try one section at a time, and [verify if the problem is fixed]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#confirm-bbo-agent-is-working)

### 1. One and only one BBO agent per environment   
For an environment with more than one instance VMs, there must be one and only one BBO agent running among all instance VMs.

1. Go to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}), use **Remote Command**.
2. Enter environment name in the _Filter Environment Name_ field.
3. Select all instances for the environment.
4. Enter `docker ps | grep bbo_agent` in the _shell command_ box.
5. Press the _Run_ button.
6. There should be exact one instance with a running "bbo_agent".

![One bbo_agent]({{site.baseurl}}/docs/runbooks/doctor/images/bbo/bbo_agent_one_and_only_one_per_environment.png){:width="639px" height="422px"}

### 2. Confirm Bosh CLI is working
BBO Agent will run scripts on Bosh CLI. You need to confirm that BoshCLI is working properly.
If not, contact a Bluemix Fabric SRE to fix it.

* You need to test the login to the BoshCLI via w3 BoshCLI (aka ssh through [Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html)).

>[Request access to Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html#assumption-and-onboarding-process)
 [Problems logging into Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Runbook_problems_logging_into_SSH_jumpbox.html)

```
$ ssh [your intranet id]@bosh-cli-bluemix-new.rtp.raleigh.ibm.com  (example intranet id: ibmuser@us.ibm.com)
$ cd /var/releases/bin
$ ./boshcli_[env].sh
```

* If you get the following message, please contact a Bluemix Fabric SRE to check BoshCLI via the sre-platform-onshift Slack channel.
```
ssh: connect to host 9.39.221.144 port [port number]: Connection refused
```

* You also need to test login via web SSH and perform some system checks.
* Go to [Doctor Datacenter]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}/#/datacenter)
* Click SSH icon _(NOT CLI icon)_ of `[env]` to login to BoshCLI using your SSO ID and password.
![ssh icon]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_ssh_icon.png){:width="593px"}

* Make sure you can login to BoshCLI without errors.
![How to determine if you have logged in successfully?]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_How_to_determine_if_you_have_logged_in_successfully.png){:width="593px"}

* If you get a message **No passwd entry for user 'SSO ID'**  or **su: Authentication failure** and you are sure you typed your correct SSO ID password, send an email to **Bluemix Admin/Germany/IBM** to check your access for the environment selected. As an alternative Go to [{{wukong-portal-name}}]({{doctor-portal-link}}), use **Remote Command** to continue with the next steps.

* Make sure BoshCLI is not out-of-disk by run `df -h` command. Follow [Disk Usage Is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html) if you need to remove some files to make more space available.
* Make sure BoshCLI is not out-of-memory by run `top` command.
* To find the [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) who is oncall via @cybot in Slack, post `@cybot whois oncall GRE` in the channel.


If there is an extra bbo_agent running,
comment out the [bbo_agent section from the docker-compose file, and curl]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#bbo-agent-in-docker-compose-file) to restart the agent.  To change a line into a comment simply add a hash/pound sign (#) to the line, typically in column 1.

If there is no bbo_agent running,
add a [bbo_agent section to the docker-compose file, and curl]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#bbo-agent-in-docker-compose-file) to restart the agent.

#### _You should follow all the steps in each section._

#### Each environment can run only one BBO agent instance.

Otherwise, you may get the context of output.logs like this:

    SL_USER is null
    SL_API_KEY is null
    LOGIN TARGET VMS via doctor certificate!

For this situation, stop one instance and comment out the bbo_agent part in the file `{{doctor-compose-path}}` on one node.



* If the content of output.logs is 'Hello World', this indicates that the BBO Agent is working properly. **Do not** resolve this PagerDuty incident - NewRelic will resolve it when it determines that the problem is fixed.  Note that the hello-world.sh script is typically run on several VMs with different IP addresses - if one of them returns _Hello World_ then **wait for NewRelic** to resolve the incident.

* If the content of output.logs contains: _./hello-world.sh: No such file or directory_ or _./run.sh: No such file or directory_, then please follow the instructions in [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html). Snooze the PagerDuty incident for 24 hours.

* If you got an error like _/home/doctor/bbo_7cfa71b246run.remote.script.secure.sh: line 55: ./: Is a directory_, try another command: `run boshcli script: analyze.ccdb.sh --help`. The output should contain:
    ```
    Displays basic organization, application, and services statistics in CCDB.

    Usage: ./analyze.ccdb.sh [OPTIONS]...[ARGS]
    ...(more)
    ```

    If the content of output.logs contains: _./analyze.ccdb.sh: No such file or directory_, then follow the instructions in [this runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html) and snoose the PagerDuty incident for 24 hours..

* If you get the output.log generated, and the following message in output:

``spawn rm -f /opt/bbo/tasks/2b41024e09/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55/bbo_para_string_2b41024e09.txt
spawn ssh -A doctor@10.144.27.234
You are required to change your password immediately (password aged)``

It means the password of the function id (Doctor or Taishan) on BoshCli VM has expired. You need to follow the steps to refresh the password:

  1. Remember the function id in the output `{function id}@xx.xxx.xxx.xx message`.
  2. Login to the BoshCli VM using your SSO id and run command `sudo su` to switch to root.
  3. Run command `passwd {function id}` for example: `passwd doctor`.

Then input the original password of the function id to refresh it. NOTE you CAN NOT change the password text freely. The password should be fixed to make sure the Doctor function works well. You should get the password of function id from the Doctor supervisor. Any question regarding the function id password, please contact {% include contact.html slack=oss-developer-slack name=oss-developer-name userid=oss-developer-userid notesid=oss-developer-notesid %}.

* If the output log does not generate a link, make sure the BBO command was entered correctly, and then go to the next section.
    ![bbo_example]({{site.baseurl}}/docs/runbooks/doctor/images/bbo_example.png){:width="639px" height="422px"}

If the script continues running without output.log, please follow these steps:

 1. Logon on to BoshCli of this environment using your SSO ID and password.

 2. Run `sudo –i`.

 3. Add function id into sudo without password.

    ``echo "doctor ALL=(ALL:ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)
    echo "taishan ALL=(ALL:ALL) NOPASSWD: ALL" | (EDITOR="tee -a" visudo)``

 4. Unlock function id.

    ``faillog -u doctor -r
    faillog -u taishan -r``

  5. Restart the ssh service.

     `service ssh restart`

  6. Run the BBO command on [{{site.data[site.target].oss-doctor.links.doctor-portal.name}}]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}#/bbo). If the content of output.logs is 'Hello World', **do not** resolve this incident - NewRelic with resolve the incident automatically when it determines the problem is fixed. If the script is still keep running without output.log, you need to follow the below steps:

  7. Go to [{{site.data[site.target].ghe.repos.bluemix-fabric.name}}]({{site.data[site.target].ghe.repos.bluemix-fabric.link}}/doctor-configuration/tree/master/config) and find the .yml of this environment. Open the yml, find boshcli_user and bosh_cli.

  8. Logon to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}), find the environment, click ssh of a doctor_agent vm, logon with your sso id, run `sudo -i`, run `docker ps` (if there is no bbo_agent, please ssh the other vm on the wukong page).

  9. In bbo_agent container, try to ssh to BoshCli.

     ``docker exec -it bbo_agent bash
     ssh -i /opt/bbo/data/<user>_key -i /opt/bbo/data/<user>_key-cert.pub <user>@<boshcli>``

  (replace \<user> with boshcli_user and \<boshcli> with bosh_cli values obtained from step 7)

  If you can not ssh to BoshCli, there maybe something wrong with the certificate. You need to sign the ssh key of function id.

#### If the BBO Agent is not working properly, first check if there is only one BBO agent instance running in that environment

There were two agent VMs in the public production environment and two inception VMs in most of the local environments. If there is a 'bbo_agent' container running in both of two agent VMs, you need go to one agent VM and remove one with `docker rm -f bbo_agent`. Also remember to remove the bbo section from _/opt/doctor-keeper/config/docker-compose.yml_.

### 3.Make sure bbo.test.for.doctor.sh exists in BOSHCLI VM(s)
  * Check /root/bin folder of each BOSHCLI VM
  * Verify that bbo.test.for.doctor.sh exists. If it not exist, create it manually. [refer to]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html) and snoose the Pager Duty incident for 24 hours.
  * Make sure the script is executed correctly: ./bbo.test.for.doctor.sh <SSO ID> -p <SSO Password>.

## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

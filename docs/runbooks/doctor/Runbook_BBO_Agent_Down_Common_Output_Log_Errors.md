---
layout: default
description: This informational runbook show the most common errors form the output.log.
title: Doctor BBO Agent Down Common Output Log Errors
service: bbo
runbook-name: Doctor BBO Agent Down Common Output Log Errors
tags: oss, bluemix, bbo, BBO_Agent_Down
link: /doctor/Runbook_BBO_Agent_Down_Common_Output_Log_Errors.html
type: Information
---

{% capture docker-compose-yml %} {{site.data[site.target].oss-docker.links.compose-yml.link}} {% endcapture %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
This informational runbook is intended use by a Doctor agents only. Listed the most common errors shown at the output.log
form the [{{doctor-portal-name}}->Diagnose->BBO]({{doctor-portal-link}}/#/bbo)

## Technical Details
BBO Agent is hosted on Doctor Agent VM. It relies on BOSH CLI connectivity.

A Hello-World task is sent to the BBO agent to see if it executes, if an output is generated, and if the output is as expected.

## User Impact
BBO job and task cannot be executed.


### Case 1 Null values in the request

You may get the context of output.logs like this:

    SL_USER is null
    SL_API_KEY is null
    LOGIN TARGET VMS via doctor certificate!

For this situation, you will need to follow the instructions [here]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#1-one-and-only-one-bbo-agent-per-environment) to ensure there is only one instance of the bbo_agent running for the environment.

### Case 2 Script bbo.test.for.doctor.sh is not found

If the alert reports the follow problem:
```
  /home/doctor/dcf2aed5fd.run.remote.script.sh: line 55: ./bbo.test.for.doctor.sh: No such file or directory
  BBO SCRIPT EXEC WITH ERROR CODE
```
Then please follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}

### Case 3 ./ is a directory

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

If the content of output.logs contains: _./analyze.ccdb.sh: No such file or directory_, then please follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}

### Case 4 File output.logs is not generated

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

If the content of _output.logs_ is 'Hello World', the problem is fixed and the incident will resolve automatically soon.

### Case 5
```
LOGIN TARGET VMS via doctor certificate!

================================================================================
10.143.123.161 (/opt/bbo/jobs/common/run.remote.script.sh)
===============================================================================
```

It is most likely a disk usage space issue in the BOSH_CLI VM follow this [Follow [Disk Usage Is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html#step-5-if-disk-usage-is-still-too-high)

### Case 6
```
LOGIN TARGET VMS via doctor certificate!

================================================================================
192.168.150.4 (/opt/bbo/jobs/common/run.remote.script.sh)
================================================================================
sudo: unable to resolve host (none)
```

Please follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#1-the-bbo-agent-is-trying-to-run-scripts-on-the-wrong-machine), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}

### Case 7
```
ERROR: Unable to establish a connection to [xxx.xxx.xxx.xxx] with the user name and password provided.
       Verify that the user name and password specified are correct.
```

Please do:
1. login the IP which is shown in the error message. You could try login to agent first, then ssh IP.
2. check with `chage -l doctor`, make sure the user is not expired. If expired, extend the expiration date.
3. goto **Wukong -> Privilege ID Management -> select ENV -> find the IP above -> click "Create ID" button**.
4. wait for the email response. If success, try running the helloworld again. Otherwise, report to {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid%} or {% include contact.html slack=oss-developer-slack name=oss-developer-name userid=oss-developer-userid notesid=oss-developer-notesid%}.

### Case 8
```
./bbo.test.for.doctor.sh: No such file or directory
BBO SCRIPT EXEC WITH ERROR CODE
```

Follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}.


### Case 9
```
LOGIN TARGET VMS via doctor certificate!

================================================================================
192.168.62.4 (/opt/bbo/jobs/common/run.remote.script.sh)
================================================================================

@@ Error connecting to server using SSH keys: 192.168.62.4
```
Follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}.


### Case 10
```
UAA_SECRET is null
LOGIN TARGET VMS via doctor certificate!
================================================================================
192.168.105.4 (/opt/bbo/jobs/common/run.remote.script.sh)
================================================================================

ssh: connect to host 192.168.105.4 port 22: Connection refused
```
Follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}.

### Case 11
```
SL_USER is null
SL_API_KEY is null


10.10.211.11 (/opt/bbo/jobs/common/run.remote.script.secure.sh)


doctor@10.10.211.11's password: 
Permission denied, please try again.
```
Follow the instructions in [bbo.test.for.doctor.sh not found]({{site.baseurl}}/docs/runbooks/doctor/Runbook_bbo_test_for_doctor_sh_not_found.html#2-there-is-a-failure-in-downloading-the-script), snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %}.

### Case 12
```
ERROR: Unable to establish a connection to [192.168.105.155] with the user name and password provided.
       Verify that the user name and password specified are correct.
ERROR: Unable to establish a connection to [192.168.105.174] with the user name and password provided.
       Verify that the user name and password specified are correct.
ERROR: Unable to establish a connection to [192.168.105.2] with the user name and password provided.
       Verify that the user name and password specified are correct.
```

This issue is not common and mostly happend in local environments.The problem is most likely connectivity to the local/customer VM's.
BBO is trying to SSH to the listed IP's using doctor functional id. contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} for help.

### Case 13
If Doctor Diagnose->BBO returns the expected result
```
================================================================================
XXX.XX.XXX.XXX (hello-world.sh)
================================================================================
Hello World
```

But WuKong -> BBO CI & CD returns something like the follow:

```
{"dsl"=>"#!/bluemix/dsl w3ibm-cio \nrun boshcli script: bbo.test.for.doctor.sh $DOCTOR_USER", "title"=>"BBO Test", "tenant"=>"D_CIO", "engine"=>"BBO", "job_id"=>"ac5a5e07-8fd6-4514-98b1-42db6b1f7e55", "task_id"=>"79e5d8b75c", "log"=>"Execution time of BBO task 79e5d8b75c exceeded 20 minutes, please go to 'Doctor > Diagnose > BBO' to check result of BBO Task.", "status"=>"failed"}
```

Notice the part **exceeded 20 minutes**. It could be a symptom of backlog transactions in the bosh cli VM,snooze the Pager Duty incident for 24 hours and contact {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} for help. Or try to cleanup `/home/doctor`, `/home/doctor/tmp`, `/home/taishan` and `/home/taishan/tmp`.

## Common Issues not reported on the output log

### Case 1

If `docker logs bbo_agent` returns something like the follow:

```
["#<NoMethodError: undefined method `connection_completed' for nil:NilClass>", "/usr/local/lib/ruby/gems/2.1.0/gems/em-http-request-1.1.2/lib/em-http/http_connection.rb:27:in `connection_completed'"]
["#<EventMachine::ConnectionNotBound: unknown connection: 379013>", "/usr/local/lib/ruby/gems/2.1.0/gems/eventmachine-1.2.0/lib/eventmachine.rb:194:in `run_machine'"]
["#<EventMachine::ConnectionNotBound: unknown connection: 1754059>", "/usr/local/lib/ruby/gems/2.1.0/gems/eventmachine-1.2.0/lib/eventmachine.rb:194:in `run_machine'"]
["#<EventMachine::ConnectionNotBound: unknown connection: 1922013>", "/usr/local/lib/ruby/gems/2.1.0/gems/eventmachine-1.2.0/lib/eventmachine.rb:194:in `run_machine'"]
["#<EventMachine::ConnectionNotBound: unknown connection: 2217357>", "/usr/local/lib/ruby/gems/2.1.0/gems/eventmachine-1.2.0/lib/eventmachine.rb:194:in `run_machine'"]
["#<EventMachine::ConnectionNotBound: unknown connection: 2385710>", "/usr/local/lib/ruby/gems/2.1.0/gems/eventmachine-1.2.0/lib/eventmachine.rb:194:in `run_machine'"]
```

Apply the steps at [Restarting the BBO Agent]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#restarting-the-bbo-agent)

### Case 2
If disk usage space is recurrent, check the {{docker-compose-yml}} check the **bbo_agent** section

```
services:
  bbo_agent:
    command: 4569 taishan_public_fra_yp https://169.44.75.235:4568
    container_name: bbo_agent
    image: doctormbus3.bluemix.net:5000/bbo_v3/backend:5.20190902030131
    mem_limit: 2500000000
    network_mode: host
    restart: always
    stdin_open: true
    tty: true
    volumes:
    - /opt/bbo/logs:/opt/bbo/bluemix_best_operator/logs  <===
    - /opt/bbo/data:/opt/bbo/data
```

If you see the follow `- /opt/bbo/logs:/opt/bbo/bluemix_best_operator/logs` under **volumes**.
1. Create a backup of the {{docker-compose-yml}} file.
2. Open the file.
3. Remove the line `- /opt/bbo/logs:/opt/bbo/bluemix_best_operator/logs` under **volumes**.
4. Save the file.
5. Goto the BOSH_CLI VM and clean data under **/opt/bbo/logs**
6. Apply the steps at [Restarting the BBO Agent]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html#restarting-the-bbo-agent)

### Case 3 missing `authorized_keys`

1. Login Doctor Agent VM using my SSO ID and then get into the BBO Agent: `docker exec -it bbo_agent bash`
2. List all processes and checking the BBO tasks: `ps -ef | cat | grep /opt/bbo/tasks`

    ```
    root     16985 16867  0 01:44 ?        00:00:00 sh -c timeout -k 10 900 bash -c 'source /opt/bbo/tasks/739dcf2bf0/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55/confi
    g_dedhfapx.sh; cd /opt/bbo/tasks/739dcf2bf0/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55; /opt/bbo/jobs/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55/analyze > /opt/bbo/tasks/739dcf2bf0/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55/analyze.std 2>&1 '
    ```

    Then we can see the ongoing tasks.

3. Then open browser to check the task logs, since we now know the task id: [https://doctor.cloud.ibm.com/#/bbo?task_id=739dcf2bf0](https://doctor.cloud.ibm.com/#/bbo?task_id=739dcf2bf0)
see something like this:

    ```
    ++ '[' -z /opt/bbo/tasks/739dcf2bf0/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55 ']'
    ++ echo /opt/bbo/tasks/739dcf2bf0/ac5a5e07-8fd6-4514-98b1-42db6b1f7e55
    + /opt/bbo/jobs/common/run.boshcli.script.sh --para_wrap 5726
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed

      0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
    100    14  100    14    0     0   2384      0 --:--:-- --:--:-- --:--:--  2800
      % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                     Dload  Upload   Total   Spent    Left  Speed
    ```

4. It looks something wrong with the login. So go back to **bbo_agent** to try login by doctor using key:

    ```
    root@doctor-london-yp:/opt/doctor-keeper/config# docker exec -it bbo_agent bash
    root@doctor-london-yp:/# ssh -i /opt/bbo/data/doctor_key -i /opt/bbo/data/doctor_key-cert.pub doctor@10.112.178.141
    Account locked due to 1631 failed logins
    Password:
    ```
5. Tried to reset fail log on BOSH CLI `root@boshcli:~# faillog -u doctor -r` (using firecall ID) (It does not resolve the issue)

6. Then checked the authorized_keys in doctor, looks it has been changed:

    ```
      doctor@boshcli:~/.ssh$ ls
      authorized_keys.bak  id_rsa  id_rsa.pub  known_hosts  mykey  mykey.pub
    ```
7. Change it back: `doctor@boshcli:~/.ssh$ mv authorized_keys.bak authorized_keys`  

8. Try to login from bbo_agent again and it works:
```
root@doctor-london-yp:/# ssh -i /opt/bbo/data/doctor_key -i /opt/bbo/data/doctor_key-cert.pub doctor@10.112.178.141
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-108-generic x86_64)
IBM's internal systems must only be used for conducting IBM's business or for purposes authorized by IBM management
 * Documentation:  https://help.ubuntu.com/
 ```

9. It does not work either try the follow:
  - From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Privileged ID Management** from the left side menu.
  - Find the instance of doctor agent, check it on and then click button **Check/Fix Cert**.This will fix the cert for the function ids on doctor agent.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/chwck_fix_certs.png){:width="640px"}
  - Select **Bosh Client** and click on **Correct Public Key**.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/correct_public_key.png){:width="640px"}
  - Input your SSO ID and password to submit
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/submit_correct_key.png){:width="640px"}
9. Restart the bbo_agent, and looks the BBO agent now working well.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

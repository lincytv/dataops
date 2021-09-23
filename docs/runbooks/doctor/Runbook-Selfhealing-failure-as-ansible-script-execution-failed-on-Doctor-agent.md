---
layout: default
description: Self-healing failure when Ansible script execution failed on Doctor agent
title: Self-healing failure as Ansible script execution failed on Doctor agent
service: doctor
runbook-name: Self-healing failure as Ansible script execution failed on Doctor agent
tags: oss, bluemix, doctor, blink, Ansible
link: /doctor/Runbook-Selfhealing-failure-as-ansible-script-execution-failed-on-Doctor-agent.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}

## Purpose

This Runbook is used to resolve alerts around failed Ansible tasks that were triggered by self-healing.

## Technical Details

By nature, Ansible tasks rely on a native SSH connection to the target VM for remote script execution. Therefore this kind of alert is usually caused by the inability of the Doctor functional ID to SSH to the target VM. This is usually caused by an incorrect credential or SSH key.

## User Impact

The script defined in the self-healing rule cannot be executed on the target VM successfully.

## Instructions to Fix
When got Auto-Scaling PD alert from TOC or forwarded here with likr the example log below,
```
Log:

PLAY [10.143.123.161] **********************************************************
TASK [file] ********************************************************************
fatal: [10.143.123.161]: UNREACHABLE! => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": false}
to retry, use: --limit @/opt/ansible/playbooks/playbook_b6f485049e6f.retry
PLAY RECAP *********************************************************************
10.143.123.161 : ok=0 changed=0 unreachable=1 failed=0
```
Follow this steps:
  1. Find the environment including the ip which is 10.143.123.161 in example log.
      - **Option 1** If the IP is not in present in the PD details try the service now link form the PD **View in ServiceNow**, you may see something like the follow in this example the IP is `192.168.150.41`:
      ```
      {
      "crn": {},
      "incident_id": "INC0698103",
      "incident_ui_url": "https://watson.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=INC0698103",
      "journal": [
      "[Note from Doctor]\n\nOutput of task https://doctor.cloud.ibm.com/#/script_execution/c8265c34e75a"
      "on tenant L_BNPP:\n\nPLAY [192.168.150.4] ***********************************************************\n\nTASK [file] ********************************************************************
      \nfatal: [192.168.150.4]: UNREACHABLE! =\u003e {\"censored\": \"the output has been hidden due to the fact that 'no_log: true' was specified for this result\", \"changed\": false}\n\tto retry, use: --limit @/opt/ansible/playbooks/playbook_c8265c34e75a.retry\n\nPLAY RECAP *********************************************************************\n192.168.150.4 : ok=0 changed=0 unreachable=1 failed=0 \n\n\n"
      ],
      "tip_msg_type": "update.request"
      }
      ```
      - **Option 2** by searching the IP in the [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}/tree/master/config) Use the primary BOSH_CLI IP address.
  2. Login to the doctor agent in the right environment.
  3. Make sure **doctor_scriptengine** is running by `docker ps |grep doctor_scriptengine`
  4. Get inside the container `docker exec -it doctor_scriptengine bash`
  5. Once inside change to `cd /opt/ansible/playbooks`
  6. Find the playbook_********.yml, which is playbook_b6f485049e6f in example log.
      - Use an editor open it and changed `no_log: False`
      - Save the file and exit the container.
  7. Check for any space issue in the doctor VM, if you see space issues follow this [Disk Usage is High]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html).
  8. `cd /opt/ansible/playbooks`
  7. Rerun the playbook `ansible-playbook playbook_********.yml` , and you will get the result output.

    root@(none):/opt/ansible/playbooks# ansible-playbook playbook_233769846eee.yml
    [WARNING]: Found both group and host with same name: 10.250.9.68
    PLAY [192.168.150.4] ********************************************************************************************************************
    TASK [file] *****************************************************************************************************************************
    changed: [192.168.150.4]
    TASK [copy] *****************************************************************************************************************************
    changed: [192.168.150.4]
    TASK [shell] ****************************************************************************************************************************
    changed: [192.168.150.4]
    TASK [fetch] ****************************************************************************************************************************
    changed: [192.168.150.4]
    TASK [file] *****************************************************************************************************************************
    changed: [192.168.150.4]
    TASK [Check script execution result] ****************************************************************************************************
    skipping: [192.168.150.4]
    PLAY RECAP ******************************************************************************************************************************
    192.168.150.4              : ok=5    changed=5    unreachable=0    failed=0

### Error case 1

If the error contains:

  ```

  "UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: ssh: connect to host xxx.xxx.xxx.xxx (usually bosh cli VM IP) port 22: Connection timed out\r\n", "unreachable": true}

  ```

or

  ```

  "UNREACHABLE! => {"changed": false, "msg": "Failed to connect to the host via ssh: Permission denied (publickey,password,keyboard-interactive).\r\n", "unreachable": true}

  ```

In this second case you need to find out the BOSH command line VM IP from the environment's **IaaS** VM list.

  1. Log in to the target environment Doctor agent VM.
      * Go to  [{{wukong-portal-name}}]({{wukong-portal-link}}).
      * Select **Doctor Keeper**.
      * Search for target environment.
      * Click on **SSH**.
      * su `<YOUR_SSO_ID>`.
      * Then `sudo -i` to change to root.
      * When prompted for your password, use your SSO password.
        - If SSH does not open in a different tab, try to use a different browser, like Firefox.
        - Just login to bosh cli VM which is contained in alert error message if local environment.

  2. Check the key `<<user>>` and `<<ssh_key>>` of **ope** section in the doctor _yml_ config files:

      - `taishan_public_<<bluemix_customer_name>>.yml`  if public environment. e.g. _taishan_public_fra_yp.yml_
      - `taishan_dedicated_<<bluemix_customer_name>>.yml`  if dedicated environment. e.g. _taishan_dedicated_cisco_1.yml_
      - `taishan_local_<<bluemix_customer_name>>.yml`  if local environment.

      The bluemix_customer_name is in the environment.yml of the target environment. The bluemix_customer_name can be found by clicking on the YML icon which is to the right of the JML icon on the doctor home page.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/jml_bluemix_customer_name.png)

      The doctor yml config file is stored in the [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}/tree/master/config).
      Please request access rights if you are unable to open it at [{{oss-doctor-name}}]({{oss-doctor-link}})..
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/config_ope_ansible_user_ssh_key.png)

  3. Execute the command: `docker ps -a` to list all the docker containers, execute `docker exec -it doctor_backend bash` if the doctor_backend container is listed. Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.

  4. Execute `ssh -i <<ssh_key>> <<user>>@xxx.xxx.xxx.xxx`, where `<<ssh_key>>` and `<<user>>` are in the config file mentioned in step 2. The target IP is the bosh cli VM IP which is contained in the alert error message. If prompted for a password, then that means the `<<user>>` public SSH key was wrong in the target host VM.
  > **Note:** If the bosh cli VM IP is 'bosh_cli_ip' or something else that is not an IP address, check the configuration file for this environment in the [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}/tree/master/config).
  The attribute to check is "ope > ansible > script_repo > ip". Correct it to be same value of the attribute "cloud > bosh > bosh_li", then commit to the git repository and restart 'doctor_backend' agent on Wukong > CI & CD page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_backend_restart.png)

  5. SSH to the target host VM (contained in alert message) using your `<<YOUR_SSO_ID>>`. Check whether the directory `/home/<<user>>` exists, using `<<user>>` mentioned in step 2.
      - Contact {% include contact.html slack=ansible-self-healing-slack name=ansible-self-healing-name userid=ansible-self-healing-userid notesid=ansible-self-healing-notesid %} if the directory does not exist.
      - Check the `/home/<<user>>/.ssh/authorized_keys` file to see if it contains the public key of `<<user>>`.
      - If the `<<user>>` public key was not set in the authorized_keys file, add it to the authorized_keys file.
      - If the `<<user>>` public key was already set in the authorized_keys file, execute `ls -l /home/<<user>>/.ssh/authorized_keys`
        - Check the owner which must be the `<<user>>`
        - Check the rights which must be 600
      - Repeat steps 1-4. The alert can be resolved if you can execute: `ssh -i <<ssh_key>> <<user>>@xxx.xxx.xxx.xxx` successfully without a password.


      How to find the public key of `<<user>>`:

        - Login to any one of the other environments and repeat steps 1-4, if executing `ssh -i <<ssh_key>> <<user>>@xxx.xxx.xxx.xxx` successfully runs without a password that means the `<<user>>` public key in the `/home/<<user>>/authorized_keys` file in this environment is correct.
        - The `<<user>>` public key ends with "bosh-cli-bluemix".

### Error case 2

If the error contains

```

"UNREACHABLE! => {"changed": false, "msg": ""Unable to find '/opt/ansible/scripts/xxx/xxx' in expected paths.", "unreachable": true}"

```

1. Login to the target environment doctor agent VM.
  * Goto [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Doctor Keeper**.
  * Search for target environment.
  * Click on **SSH**.
  * su `<YOUR_SSO_ID>`.
  * Then `sudo -i` to change to root.
  * When prompted for your password, use your SSO password.
    - If SSH does not open in a different tab, try to use a different browser, like Firefox.
    - Just login to bosh cli VM which is contained in alert error message if local environment.
2. Run the command `docker exec -it doctor_backend bash` to allow us to run commands in the running **doctor_backend** container.
Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.
3. Find the apikey in [Config repo](https://github.ibm.com/BlueMix-Fabric/doctor-configuration/tree/master/config), find the `apikey` in registry_mbus1.yml, the apikey is used in next step.
4. Run the following command inside the `doctor_scriptengine` container to sync the script repository manually:

   ```shell
   ansible-playbook /opt/ansible/scripts/doctor_scripts/http_download_file.yml --extra-vars "REMOTE_HOST=localhost DEST_HOST=localhost DEST_PATH=/opt/ansible/scripts/ DEST_FILE_NAME=doctor_scripts.tar.gz
   REGISTRY_ENDPOINT=<REGISTRY_ENDPOINT_VALUE> REGISTRY_APIKEY=<apikey>"
   ```

  >**Note:** You can find the REGISTRY_ENDPOINT_VALUE by running command `ps -ef | grep ruby | grep cloud`, and then the value for "-r" parameter is the registry endpoint, where the value is similar to https://x.x.x.x:4568.

### Error case 3

If the error contains
```

"FAILED! => {"failed": true, "msg": "Incorrect sudo password"}"

```
1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
2. Select **Remote Command**.
3. Find the VM's IP in the list, check its box, update the doctor account's password, and then unlock the account.
   1. Fetch the correct doctor password. -- procedure TBD
   2. Run the command `usermod --password $(echo xxxxxx | openssl passwd -1 -stdin) doctor`, where xxxxxx represents the correct doctor password of this environment.
   3. Run the command `faillog -u doctor -r`.
4. Normally this incident is caused from auto-scaling. Re-assign the incident back to the auto-scaling on call person for a manual re-run of the Ansible task.

### Error case 4

If the error contains

```

"Failed to run anisble task 2d0a02232cee, stdout_log: stderr_log:Failed to exec cmd ansible-playbook /opt/ansible/playbooks/playbook_2d0a02232cee.yml, error:Cannot allocate memory - fork(2), has notified Doctor developer about this problem."

```
1. Check the available memory on the BOSH CLI VM by logging onto the BOSH CLI VM and running the `free -m` command.
2. If the memory is low (for example, 8 MB) and the environment is a dedicated environment:
   * Verify that there is no _Deployment Records_ running.
       - [{{doctor-portal-name}}]({{doctor-portal-link}}).
       - Select **Analytics**.
       - Select **Gravity Wave**.
       - Select **Environment** from the dropdown list.
       - Check the **Deployment Records** section.
       - If not deployment continue.
    * Verify that no {{ucd-portal-short}} processes running.
       - [{{ucd-portal-name}}]({{ucd-portal-link}}).
       - Select **Applications**.
       - Select **Bluemix-End2End**.
       - Searching for the environment.
       - Click on the environment.
       - Click on the **History** tab.
       - If not deployment continue.
    * Verify that the environment is not being worked by the SRE team.
        - Search the environment at [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) Slack channel.
        - If not activity continue.
    * Try running a _Hard Restart Server_ for the BOSH CLI VM (via {{doctor-portal-name}}).
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/vm_hard_restart.png)
3. Restart the **doctor_backend** container.
  * Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Remote Command**
  * Select the environment
  * Run `docker restart doctor_backend`.
  * Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
    if you cannot find the **doctor_backend** container.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/remote_cmd_1.png)

### Error case 5

Script execution fails and no log information can be obtained. When the 'eye' icon under the _Logs_ column is selected a blank _Script Execution Log_ dialog opens.

1. Restart the **doctor_backend** container.
* Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
* Select **Remote Command**
* Select the environment
* Run `docker restart doctor_backend`. Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.

### Error case 6

Script execution fails, there is no task ID showing in Doctor, and the environment in Doctor is showing up as _unknown_.

1. Restart the **doctor_backend** container.
  * Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Remote Command**
  * Select the environment
  * Run `docker restart doctor_backend`. Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.
2. Wait for the restart to take effect.

### Error Case 7

If the error contains
```

The environment parameter AUTOSCALING_*** and **** passed from doctor when execute self-healing scripts is empty

```

  1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  2. Select **Remote Command**.
  3. Find the environment's IP in the list by doctor environment name (e.g. D_YS0), check its box.
  4. Run the command:
      * For dedicated and local environment:
        `curl http://localhost:4569/ope/ansible/runtime/variables`
      * For public environment:
        `curl http://localhost:4600/scriptengine/runtime/variables`
      * Check the output of the command and whether the parameter mentioned in the alert is empty.
      * If it is empty or incomplete go to step 5. If not, resolve the alert.
  5. If the parameter is empty, run the command:
      * For dedicated and local environment:
        `curl http://localhost:4569/ope/ansible/runtime/variables`
      * For public environment:
        `curl -X POST http://localhost:4600/scriptengine/runtime/variables`

### Error Case 8

```angular2html
fatal: [192.168.100.4]: FAILED! => {"changed": false, "failed": true, "invocation":
 {"module_name": "setup"}, "module_stderr": "", "module_stdout": "sudo: unable to resolve
 host inception02\r\nsudo: a password is required\r\n", "msg": "MODULE FAILURE", "parsed": false}
```

  1. login into the target VM shows in ansible log. for example `192.168.100.4` in the env.
  2. run
  ```angular2html
    docker exec -it doctor_scriptengine bash
    cd /opt/ansible/
```
  3. run `ssh -i doctor_key doctor@192.168.100.4 or ssh -i taishan_key taishan@192.168.100.4`.
  4. run `sudo ls` test sudo.
  5. if sudo is asking for a password, add the user with sudo privilege.

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

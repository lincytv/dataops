---
layout: default
description: This runbook will guide Doctor operator how to reload Doctor agent.
title: How to reload Doctor agent
service: admin
runbook-name: How to reload Doctor agent
tags: oss, bluemix, reload, doctor, agent
link: /doctor/Runbook_how_to_reload_Doctor_agent.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}


## Purpose
 This runbook will guide Doctor operator how to reload Doctor agent.

## Technical Details
To reload a Doctor agent ,we need to backup configurations on existing agent, then
reload Doctor agent based on template in Softlayer portal, then restore the configuration


## User Impact
Doctor user will have no access of Doctor agent, GREs cannot access VMs on this environment using web ssh , BBO will not work

## Instructions to Fix

**Pre:**

Notify GRE and Doctor oncall in slack channel , clarify user impact

**Step**:
In Doctor home page, in message board, update with below message :
"Doctor agent on _#{env_name}_ is going to upgrade and  unavailable for an hour, please use w3 bosh cli to access all VMs."

**Step1 : Backup current configuration files on Doctor agent**

Backup or Copy the content for below files,
- /opt/doctor-keeper/config/keeper.yml
- /opt/doctor-keeper/config/docker-compose.yml  
- /etc/hosts
- /etc/rsyslog.d/60-bmx-qradar.conf  ( or /etc/rsyslog.d/60-bmx-qradar-0.conf)
- /etc/rsyslog.d/30-doctor.conf
- /etc/resolv.conf
- /var/opt/BESClient/besclient.config
- /etc/sssd/sssd.conf
- /etc/krb5.conf
- /etc/nsswitch.conf
- /opt/ansible/doctor_key
- /opt/ansible/doctor_key-cert.pub
- /opt/ansible/taishan_key
- /opt/ansible/taishan_key-cert.pub

**Step2 : Reload the system in Softlayer portal**

1. Login IBM Cloud https://cloud.ibm.com, using ibm id doctorbm@cn.ibm.com. (Please make sure there is no ibm id cookie saved in your browser)
2. Switch to account that need to be rebuilt .  
3. Select Doctor agent device . In the top menu list, click devices->device list,  then filtered by device name "doctor", find doctor agent VM
4. Check device type. Click doctor agent VM , in device detail page, navigate to storage,  scroll down to other storage, check the device type is Local 25G Local or SAN 25G or Local 100G or SAN 100G
5. On the right corder, select action->load from image.
6. In load from Image page,  select "public"  to view , filtered by template name "doctor",  then
  - select "Doctor_Dedicated_Local25G_with_security_patch" if storage is Local 25G ,
  - select "Doctor_Dedicated_Local100G_with_security_patch" if storage is Local 100G. 
  - select "OSS-Doctor-Agent-Ubuntu-16.04-Dedicated-SAN-20180809", if SAN 100G.
7. Click "Load Selected Image"
8. Confirm the selection, then you should get "load initiate" popup
9. Wait for the loading is completed (Refresh the list to check if there is an icon besides the device name).

**Step3 : Restore configurations**

1. Once the reloading is completed, login the Doctor agent using your sso id , From w3 boshcli-> env boshcli->Doctor agent. (Find the IP in Iaas list or Doctor keeper with name #ENV_NAME).
  - Tips: the system's root password can be found in SL portal
2. Important:  Please make sure you are in Doctor agent , **stop BESclient**  using command `service besclient stop`   (the update of config file can only be available during stop_  
3. Restore all files backuped in step 1 . 
4. Restart keeper by killing keeper porcess. run "ps -ef |grep keeper", then run "kill -9 xxx"
5. Start all docker services : curl -k https://localhost:5999/compose/up, verify all services are started and registered (Wukong ->register)

5.1 Run following commands to restore doctor key files for doctor_security container.
 - Exec into doctor_security container. 
 
 `docker exec -it doctor_security bash`
 
 - Remove following files in doctor_security container.
 
`cd  /opt/ansible`

`rm  doctor_key doctor_key-cert.pub taishan_key taishan_key-cert.pub`

 - Restart doctor_security container.
 
`exit`

`docker restart doctor_security`

5.2 Run following commands to restore doctor key files for bbo_agent container.
 - Exec into bbo_agent container. 
 
 `docker exec -it bbo_agent bash`
 
 - Remove following files in doctor_security container.
 
`cd  /opt/bbo/data`

`rm doctor_key doctor_key-cert.pub taishan_key taishan_key-cert.pub`

 - Restart bbo_agent container.
 
`exit`

`docker restart bbo_agent`

6. Change local user doctor's password to the value in agent yml file.  run `passwd doctor`
7. Verify if local user 'taishan' exist (run `passwd taishan`). if yes, change the password , otherwise, create local user taishan with password in agent yml file, use below script:

        user=`cat /etc/passwd | grep "\/home\/$1"`
        if [ -z $user ]; then
        echo "$1 not exist, create the user"
        groupadd $1
        useradd -g $1 -d /home/$1 -m -s /bin/bash -K PASS_MAX_DAYS=90 $1
        usermod -a -G adm,dialout,cdrom,floppy,audio,dip,video,plugdev,admin $1
        usermod --password $(echo $2 | openssl passwd -1 -stdin) $1
        [[ `grep $1 /etc/sudoers` ]] || echo "$1 ALL=(ALL:ALL) ALL" >> /etc/sudoers
        else
        echo "user $1 already exist"
        fi

   step :
     *  create a file ,copy above script, then save.
     *  run command bash _#your_file_ taishan _#password_

8. Start BESClient using command `service besclient start` ,  Verify it is running with command  `ps -ef |grep BESClient`
9. Restart rsyslog, command: `service rsyslog restart`
9.1 Restart sssd . command: `service sssd restart`

10. Verify blink is working ，check estado page is visible

11. Verify NewRelic agent is installed and running,run `ps -ef |grep newrelic-infra` , if yes, skip this step, otherwise, Install NewRelic agent, run the following command in **Remote Command Line**:

  * For Dedicate and Local enviroments, run below command to download install script and install newRelic,
   ```
   scp -o StrictHostKeyChecking=no -i /opt/doctor-keeper/scripts/sshhub_key sshhub@10.125.89.62:/tmp/install-newrelic-infra.sh /tmp && cd /tmp  && chmod +777 install-newrelic-infra.sh && ./install-newrelic-infra.sh
   ```

  * For Public environments, copy the `install-newrelic-infra.sh` from Doctor Mbus4,

   ```
   scp -o StrictHostKeyChecking=no -i /opt/doctor-keeper/scripts/sshhub_key sshhub@158.85.7.124:/tmp/install-newrelic-infra.sh /tmp && cd /tmp  && chmod +777 install-newrelic-infra.sh && ./install-newrelic-infra.sh
   ```
12. Verify NewRelic agent is started,

    ```
    ps -ef |grep newrelic-infra
    ```
    if the output like below, the Newrelic agent is running.
    ```
    root     15048     1  3 07:42 ?        00:00:06 /usr/bin/newrelic-infra
    ```

13. Check user sshhub if password expired (`chage -l sshhub`). if yes, run command `chage -d $current-date sshhub`（replace $current-date with today's date , like 2018-11-15)

14. Check if falcon sensor is installed by "ps -ef |grep  falcon-sensor". if not, run command
```scp -o StrictHostKeyChecking=no -i /opt/doctor-keeper/scripts/sshhub_key sshhub@10.154.56.42:/tmp/falcon-sensor-5607.deb /tmp && cd /tmp  && dpkg -i   /tmp/falcon-sensor-5607.deb && /opt/CrowdStrike/falconctl -s --cid=20709802E00E4B4C9442CE5F8CA3E69D-9C && service falcon-sensor start```
15. Verify falcon sensor is started by "ps -ef | grep falcon-sensor"
16. Post a message to notify GRE that Doctor agent is available


## Notes and Special Considerations
- If sso id is not working , need to rerun  UCD process A3020 , refer : https://w3-connections.ibm.com/wikis/home?lang=en-us#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/A3020%20-%20Deploy%20security-release%20hardening%20(Public%2C%20Dedicated%2C%20Local)

If any issue, please contact Shuan Shuan or Wang Hui

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
description: How to solve an alert for high run disk usage.
title: Disk Usage is High
service: doctor
runbook-name: Disk Usage is High
tags: oss, bluemix, doctor
link: /doctor/Runbook_Disk_Usage_is_High.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Step 1. Confirm the disk usage is high
  * Login [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Remote Command**.
  * Find the environment reported in the alert using the _Filter Environment Name_.
  * Check the environment.
  * Input the follow commands in the _shell commnad_ text box:
    - `df -h ` to confirm that the disk usage is really higher than 90 percents.  
    - `df -i ` to confirm that the disk inode usage is really higher than 90 percents.
  * Click **Run** to execute the above commands.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/remote_cmd_1.png)

  * If  **Remote Command** and WuKong keeper doesn't work, try WebSSH from Taishan or W3 BoshCli, then SSH to doctor agent.
  * Click `SSH` button, login using your sso ID and password.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/web_ssh/web-ssh-button.png){:width="639px"}
  * SSH to doctor agent .
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/web_ssh/web-ssh-boshcli.png){:width="639px" height="422px"}
  * Then try to restart the doctor-keeper process , after the keeper restated, go to next step to clear disk usage:
  `sudo supervisorctl restart doctor_keeper`

## Step 2. If the problem is with a BOSH CLI VM then check the follow before to continue with the next steps

<div class="alert-warning">
  Issue fixed by GRE <a href="https://github.ibm.com/BlueMix-Fabric/cf-sre/issues/293#issuecomment-15024176">Issue</a>. You may skip this step. If you get contacted by GRE, refer them to the git issue.
</div>
<br>
 When a new version of boshcli is installed in the VM's a `.bosk.bk` is created and sometimes it did not get removed.
 GRE contact the doctor on call team ,because after running this command from root:
   - `du -sh * 2>/dev/null | sort -h | tail -n 10` you will something like the follow:
      ```
       root@doctor-agent:/# du -sh * 2>/dev/null | sort -h | tail -n 10
       11M     sbin
       133M    opt
       138M    boot
       299M    root
       300M    mnt
       809M    home
       846M    lib
       1.1G    usr
       1.7G    etc
       23G     var
      ```
   - Then you can the next command, focussing in the largest directories such as, in this example, `/etc/`; `find /etc/ -type d -exec du {} -k --max-depth=0 \; | sort -n | tail -n 10` from their [runbook](https://github.ibm.com/BlueMix-Fabric/GRE-runbooks/blob/master/Bosh/st_bosh_disk_high.md#bosh-cli-root-disk-usage-high) it returns a disk space problem either at `/home/doctor` or `/home/taishan/`.

  * Run  `ls -la` at the reported location if you see a file `/home/doctor/.bosk.bk` or `/home/taishan/.bosk.bk`.
  * Request to a GRE on call to run [clean.boshcli.disk.sh](https://github.ibm.com/BlueMix-Fabric/ops-infra-tools/blob/master/boshcli/clean.boshcli.disk.sh) for the environment.
  * If the script does not removed `.bosk.bk` then manually remove it.
  > **Note:** You could manually removed them without running the GRE script, however the GRE cleanup script will cleanup other  areas that need to be cleanup.

  * Check the disk space again. it should be good at this point, otherwise continue with the next steps.

## Step 3. Remove a container and re-created it  

<div class="alert-warning">
For shared service environments (starting with <strong>DOCTOR_*</strong>), If there is no doctor container to delete. please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %}  and {% include contact.html slack=kong-support-slack name=kong-support-name userid=kong-support-userid notesid=kong-support-notesid %} to free some useless larger files.
</div>
<br>

  * For doctor agent{% if site.target == 'ibm' %}(**except L_RBCSCC and L_RBCGCC**){% endif %}:

    - Run {% raw %} `docker ps --format '{{.Names}}'` {% endraw %} to list all present containers.
    - If `bbo_agent` is listed
      - Run `docker rm -f bbo_agent` to remove the bbo agent container.
    - Otherwise, try `docker rm -f <container_name>` where container_name can be `doctor_security` or `doctor_access` or any other container from the listed above.
    - `curl -k https://127.0.0.1:5999/compose/up` to re-create the removed container.


      {% if site.target == 'ibm' %}
       **Warning:** _It is not used for L_RBCSCC and L_RBCGCC environments._

       **If the alert is for environments (L_RBCSCC and L_RBCGCC), you will need to delete the containers and create new containers one by one. You can run the following command in Remote Command to remove and create new containers.**

      `/opt/restart_allCon.sh`
       _If the script does not exist, please contact level 2 for assistance._  This script restarts all the docker containers and
       [this]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Runbook_For_L_RBCSCC_Manual_Command_For_Starting_Doctor_Agent_Service.html) runbook describes that process in more detail.
      {% endif %}


    * If removing a container doesn't result in significant disk usage reduction, consider to do the same to other containers. After running the `curl` command above, you should see in console something like
    ```
    {"detail":{"bbo_agent":"up","blink_agent":"up","doctor_access":"up","doctor_backend":"up","doctor_blink_ace":"up","doctor_mongodb":"up","doctor_scriptengine":"up","doctor_security":"up"},"result":"success"}
    ```
    Replace `bbo_agent` in the `docker rm -f ...` command with other containers in this list, such as `doctor_backend`, and then `curl` again.

    * Use the `df` command in Step 1 to check disk usage. If you are happy with the reduction, then you can skip Step 3.

## Step 4. Remove deprecated docker images.

<div class="alert-warning">
For shared service environments (starting with <strong>DOCTOR_*</strong>), If there is no images to delete. please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %}  and {% include contact.html slack=kong-support-slack name=kong-support-name userid=kong-support-userid notesid=kong-support-notesid %} to free some useless larger files.
</div>

  * Remove unused docker image
    - `docker rmi $(docker images -q)`
  * Run the follow command in **Remote Command**.
    - ` docker rmi $(docker images |grep -v doctor-cli |awk '{print $1":"$2}')` to remove unused images.
  * If there are images with "none" tag, you need to run the command:
    - `docker rmi $(docker images |grep none | awk '{print $3}')`

  * Run
    - `df -h`
    - `df -i`
    - To check if the disk or inode is still high( >90%).
  * The `docker rmi` commands above removes unused docker images one by one, and does not stop when one image cannot be removed due to a running container using the image. If you get "Execute shell command error" when running a `docker rmi`, just move on to the next step. In order to confirm the actural reason for "Execute shell command error", you would need to remove the docker images one by one using an ssh session.


## Step 5. Confirm the disk and inode usage.
  * From **Remote Command** run the follow:
    - `df -h ` to check the disk usage.  
    - `df -i ` to check the disk inode usage.
    - As the last resource if the space is not released try `service docker restart`. It will restart all docker containers.

>**If the usage is lower than 90 percent, the alert will be auto-resolved.**

## Step 6. If Disk Usage is Still Too High

  1. Check the bbo_agent service at `/opt/doctor-keeper/config/docker-compose.yml` file.
      - Under the volumes section if you see something like the follow:
        - `- /opt/bbo/logs:/opt/bbo/bluemix_best_operator/logs` and it is the only entry replace it by `- /opt/bbo/data:/opt/bbo/data`
      - If you see both `- /opt/bbo/data:/opt/bbo/data` and `- /opt/bbo/logs:/opt/bbo/bluemix_best_operator/logs` remove the second one and leave the first one as it is.
      - bbo_agent should look like the follow:
        ```
          bbo_agent:
            command: 4569 taishan_dedicated_hrb2 https://10.109.1.21:4568
            container_name: bbo_agent
            image: doctormbus1.bluemix.net:5000/bbo_v3/backend:5.20190902030131
            mem_limit: 1500000000
            network_mode: host
            restart: always
            stdin_open: true
            tty: true
            volumes:
            - /opt/bbo/data:/opt/bbo/data
          ```
      - If you make any changes to the *docker-compose.yml* follow Step 2 again.
      - Clean the logs at `/opt/bbo/logs` to release space.

  2. If the disk usage is still too high try the follow:

      - `du -sh * 2>/dev/null | sort -h | tail -n 10` you will something like the follow:
       ```
        root@doctor-agent:/# du -sh * 2>/dev/null | sort -h | tail -n 10
        11M     sbin
        133M    opt
        138M    boot
        299M    root
        300M    mnt
        809M    home
        846M    lib
        1.1G    usr
        1.7G    etc
        23G     var
       ```

      - Then you can the next command, focussing in the largest directories such as, in this example, `/etc/`; `find /etc/ -type d -exec du {} -k --max-depth=0 \; | sort -n | tail -n 10`, you can also, check the runbook which the GRE team uses to resolve this problem on the BOSH CLI in an environment [here](https://github.ibm.com/BlueMix-Fabric/GRE-runbooks/blob/master/Bosh/st_bosh_disk_high.md#bosh-cli-root-disk-usage-high).  It has some procedures which you might find helpful.

  3. Check **/home/doctor**, **/home/taishan** and  **/opt/bbo/logs**  on the BOSH_CLI VM if they have many files listed like `*.run.remote.script.sh` and/or `bbo_para_string_*` apply the command below to released space and to avoid overloading BBO agents:

      - Run the below command:
      ```
      find "/home/doctor/" -name "[0-9|a-z|A-Z]*.run.remote.script.sh" -type f -mtime +1 -exec rm -r {} \;
      find "/home/doctor/" -name "bbo_para_string_[0-9|a-z|A-Z]*.txt" -type f -mtime +1 -exec rm -r {} \;
      ```

  4. Remove logs form **/var/log/** , **/opt/ansible/logs/** located in the  Doctor IVM

      - Use a command like the below to cleanup space:
      ```
      find "/opt/ansible/logs/" -name "check_root_password_expiration_*.*" -type f -mtime +15 -exec rm -r {} \;
      ```

## Notes and Special Considerations
The above steps can normally be done from **Remote Command** for the environment, or in an ssh session.
In case neither Remote Command nor ssh from WuKong -> Doctor Keeper works, [Doctor Tips and Techniques](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/Doctor_Oncall_Tips_and_Techniques.html) includes other ways to get the ssh session from Doctor.

{% include {{site.target}}/tips_and_techniques.html %}

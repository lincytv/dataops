---
layout: default
description: Instructions to copy files between a VM in an environment and your local machine
title: Copy Files Between VM and Local Machine
service: jumpbox
runbook-name: "Copy Files Between VM and Local Machine"
tags: jumpbox scp
link: /doctor/Runbook_Copy_File_Using_JumpBox.html
type: Instructions
---

{% capture docker-compose-yml %} {{site.data[site.target].oss-docker.links.compose-yml.link}} {% endcapture %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Purpose
These instructions describe how to copy a file from a VM in an environment to your local machine, or from your local machine to a VM in an environment using JumpBox.

## Instructions
Follow [How to Copy Files To/From a VM in an Environment]({{site.baseurl}}/docs/runbooks/doctor/Doctor_Oncall_Tips_and_Techniques.html#how-to-copy-files-tofrom-a-vm-in-an-environment)
instructions to use **Web Sftp/SSH Tunnel** to copy file(s) to/from a VM from your laptop. The instructions below are to be used in JumpBox.

>**Nota:** Refer to this runbook [Doctor SSH Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html) if you are new to JumpBox.


1. You need to ensure the file exists on the BOSH CLI for the environment.  If it exists there, continue to step 2.  If not, copy the file there
   with the instructions below:
   - Sign on to the BOSH CLI using your SSO
   - Change to your home directory with `cd ~`.
   - Copy the file from the VM in question to the BOSH CLI using the following command substituting the IP of the VM and the fullly qualified file name in the following:
      ```
      scp <SSO_ID>@<IP_of_VM>:<Fully_Qualified_File_Name> .

          e.g.

      scp vanbroek@10.106.192.93:/home/SSO/vanbroek/test.txt .
      vanbroek@10.106.192.93's password:
      ```
      Provide your SSO password when prompted.
2. Download the file from the BOSH CLI to your home directory on the JumpBox:
   - Sign on to the JumpBox as described [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html).
   - Run the sftp command for your environment:
     ```
     cd /var/releases/bin
     ./sftp_ys0_dallas.sh
     Please input username (vanbroek):
     ```
     Provide your SSO ID when prompted.
   - Change your home directory on the JumpBox which is where your file will be downloaded:
     ```
     lcd /home/vanbroek@ca.ibm.com
     ```
   - Download the file from your home directory on the BOSH CLI to your home directory on the JumpBox:
     ```
     get test.txt
     ```
     Copy as many files as you like.
   - Quit the sftp session and go to your home directory on the JumpBox:
     ```
     quit
     cd ~
     ```
3. Copy the file from your home directory on the JumpBox to your local machine using your intranet ID:
   ```
   scp vanbroek@ca.ibm.com@bosh-cli-bluemix-new.rtp.raleigh.ibm.com:/home/vanbroek@ca.ibm.com/test.txt .
   Password:
   Verification code: 542384
   ```  
   Provide your intranet password and the 2fa code for your JumpBox when prompted.    

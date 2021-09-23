---
layout: default
description: What is SSH Jumpbox? A SSH Jumpbox was built here in order to allow SRE easily access every environment.
title: Doctor SSH Jumpbox
service: doctor
runbook-name: "Doctor SSH Jumpbox"
tags: oss, ssh, Jumpbox
link: /doctor/Doctor_SSH_Jumpbox.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}


# What is SSH Jumpbox
Cloud Public/Dedicated/Local were deployed at different Softlayer account or at customer data center for Local, Every environment was isolated and stand at different vLan. A direct inbound connection to every VMs is definitely not allowed. Typically a different VPN need to be setup in order to access different environment, thus need to switch back and forth with different VPN ID in order to switch to different environment. Further more, the management VM list will keep increasing when new environments were added, it hard to find the right management VM to the right Bluemix environment.
A SSH Jumpbox was built here in order to allow SRE easily access every environment.

# How it work

Here is a high level architecture on how it was implemented.
![SSH Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/images/jumpbox/SSHJumpbox.png){:width="639px" height="422px"}
A reversed SSH connection was established from each BOSH CLI VM to SSH Jumpbox, that was monitored by a supervisor daemon. A unique port was allocated for each connection, the port information is at
[SSH Port]({{site.data[site.target].oss-doctor.links.doctor-ops-infra-tools-repo.ssh-ports}}). For each Cloud environment, there a script was created for wrapping up the port and the SSH Jumpbox, the script was deployed to bosh-cli-bluemix-new.rtp.raleigh.ibm.com using a Jenkins job, thus, the SSH was initiated from this host. The script are like boshcli_xxx.sh, just simply issue the one you want. Another set of script like sftp_xxx.sh are for file transfer. For Agent deployment, it was managed by UCD process A0215.
![SSH]({{site.baseurl}}/docs/runbooks/doctor/images/jumpbox/SSH.png){:width="639px" height="422px"}

# Assumption and onboarding process

## If the service are applications or servers

1. [Request CLI Access]({{site.baseurl}}/docs/runbooks/doctor/Request_CLI_access.html)

2. [Request SSO ID]({{site.baseurl}}/docs/runbooks/doctor/Request_SSO_ID.html)

## If the services are Isolated Servers
1. [Request access to SSH Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Request_Access_to_SSH_Jumpbox.html)

2. [Request CLI Access]({{site.baseurl}}/docs/runbooks/doctor/Request_CLI_access.html)

3. [Request SSO ID]({{site.baseurl}}/docs/runbooks/doctor/Request_SSO_ID.html)


# How to use

1. In a terminal on your local machine.
  - Run the `ssh <YOUR_INTRANET_ID>@{{bosh-cli-link}}` command (example intranet id: _{{usam-id-example}}_).

2. If this is the first time you are logging in.
  - You should supply your intranet password at the prompt and capture the 2FA authenticator information that is displayed in the terminal output. **Please note that this is different to the 2FA information used to connect to the Doctor UI**.
  - For example:

    ```
    Your new secret key is: XXXXXXXXXXXXXXXX
    Your verification code is XXXXX
    Your emergency scratch codes are:
      XXXXXXXX
      XXXXXXXX
      XXXXXXXX
      XXXXXXXX
      XXXXXXXX

    ...done.
    {{site.data[site.target].oss-doctor.links.usam.id-example}}@{{site.data[site.target].oss-doctor.links.bosh-cli.link}}:~$
    ```

    > **Note:** If you lost your verification code,  contact {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} to reset your boshcli 2FA

    - On subsequent connections you will be prompted for **intranet password** followed by authenticator 2FA verification code.

    - If you enter the wrong verification code a few times, you'd be locked out from JumpBox. To clear the lock, send an email to {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} to reset the failure count.

3. Change to script location.
  - `cd /var/releases/bin`

4. Run the boshcli_*.sh or sftp_* script for the environment to which you want to connect.
  - For example `./boshcli_yf_london.sh`
  > **Note:** If your password is not accepted when logging into BOSH CLI VMs. There may be problems with your SSO ID attributes (attributes don't match required filters when validating identity). Please contact {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} for assistance.

5. Login using your **SSO ID and password** when prompted.
![]({{site.baseurl}}/docs/runbooks/doctor/images/jumpbox/connect_to_vm.png){:width="640px"}

# Runbook
[Bluemix Alert SEV2 - ibm.allenvs.infra.sshTunnel st_Doctor_SSHTunnel]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Bosh_Cli_SSH_Metrics_ibm_allenvs_infra_sshTunnel.html)

---
layout: default
description: BBO Job fails - file envadminui.csv not found
title: BBO Job fails - file envadminui.csv not found
service: doctor
runbook-name: Runbook Envadminui CSV File Not Found
tags: oss, bluemix, doctor
link: /doctor/Runbook_Envadminui_CSV_File_Not_Found.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## Purpose
This runbook addresses how to resolve a BBO failure due to a missing file (_envadminui.csv_) required to run the health check.

## Technical Details
BBO is intended to run commands on any of the Virtual Machines in an environment. It uses the Bosh Cli as a gateway to access those Virtual Machines.  The BBO health check runs this command:

```
run boshcli script: run.sh -i envadminui.csv -s hello-world.sh -u $DOCTOR_USER
```

This runs command `run.sh -i envadminui.csv -s hello-world.sh -u $DOCTOR_USER` on the Bosh Cli and that command runs `hello-world.sh` on the Virtual Machines specified in the file _envadminui.csv_. This is like a double hop, from the requestor of BBO through the Bosh Cli to a target Virtual Machine (or a list of Virtual Machines) in the environment.  This is typical since a GRE uses BBO to run a script on one of the Virtual Machines in the environment to heal a specific problem on that Virtual Machine.

In some cases, the file _envadminui.csv_ is not present on the BOSH CLI and the command fails with:

```
Task output:ERROR: File with IP addresses does not exist [envXXXXXui.csv]
BBO SCRIPT EXEC WITH ERROR CODE
```

The incident will keep triggering until the situation is fixed.  This runbook tells you how to fix the situation by creating this file.

## Steps to Create the Missing File

We are trying to sort out why this file is missing, but a temporary solution is to create it manually.  

Follow these steps:

1. Go to [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
2. Open the environment in a new window.
3. On the **Instances** tab under **Details**.
4. Type `admin` in the filter and take note of the IP address - you will need that address below.
    ![Doctor Blink Buttons]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/envadminui_csv_ip_address.png)
5. Sign on to the Bosh CLI (for dedicated and public) or the inception machine (for local) with your SSO.  If there are two inception machines for a local environment, you may need to create the file on each of them to successfully resolve the problem.
6. Run the following, replacing **130.198.71.86** with the IP address from step 4:

  * For dedicated and public environments:

    ```
    $ ssh john@us.ibm.com@bosh-cli-bluemix-new.rtp.raleigh.ibm.com
    Password: <Your W3 password>
    Verification code: XXXXXX  (Your 2FA, it is not the one used to login to doctor)
    $ cd cd /var/releases/bin
    /var/releases/bin$ ./boshcli_<environment>.sh
    Please input username (john):
    john
    Password:<Your SSO password>
    john@boshcli-1:~$
    john@boshcli-1:~$ sudo -i
    john@boshcli-1:~$ cd /var/releases/bin
    john@boshcli-1:~$ echo 130.198.71.86 > envadminui.csv
    ```

  * For local environments:

    {% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
  * `cd /var/releases/bin`
  * `echo 130.198.71.86 > envadminui.csv`

**You have created the file! Now you are ready to rerun the BBO command to see if it works.**

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

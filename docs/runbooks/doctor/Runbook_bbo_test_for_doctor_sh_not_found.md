---
layout: default
description: Discribes the actions When a large number of BBO alerts are triggered.
title: bbo.test.for.doctor.sh not found
service: bbo
runbook-name: bbo.test.for.doctor.sh not found
tags: oss, bluemix, bbo, BBO_Agent_Down
link: /doctor/Runbook_bbo_test_for_doctor_sh_not_found.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
__

The shell script _bbo.test.for.doctor.sh_ is used to test whether the BBO agent is functioning properly.  This script is run
on the BOSH CLI and may not exist there for a few reasons:

## 1. The BBO agent is Trying to Run Scripts on the Wrong Machine

This case may apply if there are **two** BOSH CLI machines, a primary and a backup. The BBO agent should run this script
on the primary BOSH CLI, but it may be configured to run on the backup which may not have the script installed.

The configuration is stored in a GHE project [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}).
This project has restricted access and you may not be able to examine the configuration directly.
However, it is possible for you to see which BOSH CLI is configured as the primary by going to
[{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter) and selecting the environment.
Take note of the **IP addresses** for both Bosh Client icons at the top of the environments details page:

  ![BBO logs]({{site.baseurl}}/docs/runbooks/doctor/images/bosh_cli_IP.png){:height="150px"}

If the primary BOSH CLI is incorrect, you will need to swap the bosh_cli IP addresses.

<div class="alert alert-danger" role="alert">
The  follow steps only applies for local environments that have a backup bosh_cli VM
</div>

1. Goto the [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}).
2. Search the local environment, if the environment is _L_FPL_ then the configuration file will be `taishan_local_fpl.yml`.
3. Open the configuration file and look for the **cloud:** tag:
  ```
  cloud:
        bosh:
           bosh_cli: 192.168.150.4          <====
           bosh_cli_backup: 192.168.150.3   <====
           bosh_url: https://192.168.150.2:25555/
           bosh_user: admin
           bosh_pwd: {{cipher}}1dd650af1504086757_ZG9jdG9y_e1bb
           boshcli_user: doctor
           boshcli_pwd: {{cipher}}c9b714671520483111_ZG9jdG9y_c9e8{{secret}}
           deployments: bnpp
  ```
 4. Swap the **bosh_cli** IP's, for this example should look as the follow:
  ```
  cloud:
        bosh:
           bosh_cli: 192.168.150.3          <====   
           bosh_cli_backup: 192.168.150.4   <====
           bosh_url: https://192.168.150.2:25555/
           bosh_user: admin
           bosh_pwd: {{cipher}}1dd650af1504086757_ZG9jdG9y_e1bb
           boshcli_user: doctor
           boshcli_pwd: {{cipher}}c9b714671520483111_ZG9jdG9y_c9e8{{secret}}
           deployments: bnpp
  ```
 5. Now look for the cloud tag **script_repo:** under **ope:**
  ```
  script_repo:
        ip: 192.168.150.4
        location: /root/bin
        zip: /home/doctor/scripts.tar.gz
        user: doctor
        password: {{cipher}}23f41d431505790644_ZG9jdG9y_cf08
        ssh_key: /opt/ansible/doctor_key
  ```
  6. Set **ip:** value the new primary IP in this example will be `192.168.150.3` the new IP.
  7. Add the appropriated notes and save the configuration file.
  8. Restart **bbo_agent** at the Doctor VM.
  9. Wait a couple minutes and run Diagnose again.

> Note: Please reach out for help as described [here]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Exec_Fail_GRE.html#how-to-reach-out-for-help)
if you need help to fix this situation or the Diagnose still does not return "Hello world" after these steps.

## 2. There is a Failure in Downloading the Script

The script _bbo.test.for.doctor.sh_ is downloaded from [this](https://github.ibm.com/BlueMix-Fabric/ops-infra-tools) GHE project by UCD process A7500 and A7504.  It's possible that this download is failing.  You can verify this by logging onto
UCD and checking the history of the processes run for the environment.

If you cannot find the scripts on the BOSH CLU,
please reach {% include contact.html slack=gre-ucd-a7500-tester-slack name=gre-ucd-a7500-tester-name userid=gre-ucd-a7500-tester-userid notesid=gre-ucd-a7500-tester-notesid %} or [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) to fix it.

While UCD gets fixed you can follow the this workaround:

1. Check **/root/bin** folder exit of each BOSHCLI VM.
  * If does not exist create it by `ln -s /var/releases/bin /root/bin`
2. Verify that **bbo.test.for.doctor.sh** exists under **/root/bin**. If it not exist, create it manually.
3. Make sure the script is executed correctly: `./bbo.test.for.doctor.sh -p` .


## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

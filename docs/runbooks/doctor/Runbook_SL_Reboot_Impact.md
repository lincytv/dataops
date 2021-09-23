---
layout: default
description: Describes how to proceed when Web SSH does not work after reboot for SL Reboot Impact
title: Runbook SL Reboot Impact
service: softlayer
runbook-name: SL Reboot Impact
tags: oss, bluemix, doctor, softlayer
link: /doctor/Runbook_SL_Reboot_Impact.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}

## Web SSH does not work after reboot.

SRE can't access BoshCli from the {{doctor-portal-name}} page of specified environment.

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
{% include_relative _{{site.target}}-includes/tip_ssh.md %}

* Restart doctor_access service
  - RUN `docker restart doctor_access`.

## Estado status

Estado status on the [{{doctor-portal-name}}]({{doctor-portal-link}}) page shows NaN or Estado report isn't shown on [{{doctor-portal-name}} > Diagnose > Estado]({{doctor-portal-link}}/#/selfhealing/estado) for specified environment.

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}

* Restart doctor_backend service
  - RUN `docker restart doctor_backend`.
* After doctor_backend re-started
  > **TIP:** Run `curl -X GET http://127.0.0.1:4569/cloud/hello` and verify a return of  _{"result":"success"}_.
  - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Scheduler Task** from the menu.
  - From the dropdown list, select the environment.
  - Search scheduler task **refresh_estado_status** and restart it.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/scheduler_task/restart_task.png)

### Blink does not work after Softlayer reboot

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}

* Check the /etc/resolv.conf as the sudo user.
* You should see at least three entries.
  - The first one should be the "powerdns" (e.g. "nameserver 169.47.197.120" in D_KP3DAL).
    - If the first one is missing, we need to add it manually.
      - From [{{doctor-portal-name}}]({{doctor-portal-link}}).
      - Find a environment by using the Filer.
      - Click on **SSH** icon.
      ![]({{sire.base
        }}/docs/runbooks/doctor/images/doctor/datacenter/bbo_ssh_icon.png){:width="600px"}
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/bbo_How_to_determine_if_you_have_logged_in_successfully.png){:width="600px"}
      - Get the powerDNS in the BoshCli VM.
        * Find it on the `/etc/resolv.conf` file.
      - restart container **blink_agent** & **doctor_blink_ace**.
        * `docker restart blink_agent`
        * `docker restart doctor_blink_ace`  
  - The second and third ones should be "nameserver 10.0.80.11" and "nameserver 10.0.80.12".
* If "blink_agent" container is not in "running" status
  - Run `docker rm -f blink_agent`.
  - Run `curl -k https://127.0.0.1:5999/compose/up`.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

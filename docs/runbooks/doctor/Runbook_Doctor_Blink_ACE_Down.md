---
layout: default
description: This Runbook is for PagerDuty alerts when the doctor blink ace service is down.
title: Doctor Blink ACE Service is Down
service: doctor_blink_ace
runbook-name: "Doctor Blink Ace Service is Down"
tags: oss, bluemix, doctor, blink, blink_agent, docker
link: /doctor/Runbook_Doctor_Blink_ACE_Down.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose
This alert happens when doctor_blink_ace service is down.

## User Impact
This alert indicates that marmot ACE monitoring will not be able to monitor this environment's console any more.

## Instructions to Fix

### Step 1 Verify if blink ace is recovered
   - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}}) , select **Remote Command**
   - Search and select this server `DOCTOR_PROXY	10.124.116.122`.
   - Copy following command to the command box.

   ```curl -I -x {hub}:{port} http://estado.{domain name}```

   - **TIP:** To find the hub and port:
     - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}}) , select **Remote Command**
     - Run `cat /opt/doctor-keeper/config/docker-compose.yml`.
     - Search `doctor_blink_ace`.
     - Find the `--hub` parameter in `command` of `doctor_blink_ace`. **For lacaixa environments, please use this IP 10.112.157.236 as hub.**
     - Find the `--port` parameter in `command` of `doctor_blink_ace`.
     - You will see something like the follow:

            doctor_blink_ace:
                command: doctor-blink --hub 10.124.116.122 --port 45001 --auth false --user blink-ace
   - **TIP:** To find the domain name:
     - Find the Environment, by viewing the incident in [{{doctor-portal-name}} -> Incident -> PagerDuty Incident]({{doctor-portal-link}}/#/eventmanager/pd_incidents).
      - Use the search options to find a ticket.
      - Then using the Environment, find the domain name.
      - [{{doctor-portal-name}} -> Access -> Blink]({{doctor-portal-link}}/#/proxy_blink)
      - Use the search list to find the Environment found previously.
      - Get the domain name from the search results.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_agent_3.png)

If the return http code is `HTTP/1.1 200 OK` , then you can resolve this incident.

If not, maybe estado is down, another test to see if blink ace is healthy is to curl ace console link.

```curl -I -x {hub}:{port} https://console.{domain name}```

**Note:** the links to access the Console are not available for the public staging and production environment (YS_* and YP_*).

### Step 2 Restart the blink ace
Login into the doctor agent VM.
- Restart blink ace.
  - Run `docker restart doctor_blink_ace` as root on the VM.
  - If you receive a __Error response from daemon: No such container: doctor_blink_ace__ error, make sure you are on the correct VM. In [{{wukong-portal-name}}]({{wukong-portal-link}}), some environments have more than one VM listed (for example, a SH CLI VM and a Doctor VM).
  - If you receive a __Cannot connect to the Docker daemon. Is the docker daemon running on this host?__ error, run `service docker restart` and then retry step 5 above.
  - If you receive a __Error response from daemon: Cannot restart container doctor_blink_ace: Container 5ed44baca9bfe645f08b2d18bab437510846cd977a1f26152c1a1e206b359e75 is already active__ error (or `docker ps -a` shows the doctor_blink_ace container in `Exited (1) x hours ago` state), run `docker ps -a` to list the container, `docker rm <CONTAINER_ID>` to remove the container, and then `curl -k https://127.0.0.1:5999/compose/up` to restart the container.

- Verify blink ace has started.
  - Run ```docker ps```, you should see doctor_blink_ace listed in the output and the status column should reflect the time in which you restarted it (i.e. Up About a minute).
- Verify if blink ace is recovered as Step 1.

### Step 3 Change the version of blink ace
- Verify the version of doctor_blink_ace
  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}}) , select **Remote Command**
  - Run ```docker ps |grep doctor_blink_ace```, you will see the current image, like this:

           eadfcccba3b7 doctormbus3.bluemix.net:5000/doctor_go/blink_ace:latest "doctor-blink --proxy"
  - If the image is ```doctor_go/blink_ace``` and the version is ```latest```, the version is correct.
- Change the version of ```doctor_blink_ace```.
  - Go to [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
  - Select **CI & CD**
  - Enter ```doctor_blink_ace``` in the **Continuous Deployment** prompt.
  - Press Enter or click on the refresh icon.
  - Select the Environment.
  - Select `doctor_go/blink_ace`
  - Select the `latest` version.
  - Click **Upgrade**.
- Verify blink ace has started.
  - Select **Remote Command**
  - Search for the Environment
  - Run ```docker ps```, you should see doctor_blink_ace listed in the output, the version of image is `latest` and the status column should reflect the time in which you restarted it (i.e. Up About a minute).
- Verify if blink ace is recovered as Step 1.

## Notes and Special Considerations

 If any questions, please contact {% include contact.html slack=cloud-software-dev-slack name=ccloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} or {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid %}.

 {% include {{site.target}}/tips_and_techniques.html %}

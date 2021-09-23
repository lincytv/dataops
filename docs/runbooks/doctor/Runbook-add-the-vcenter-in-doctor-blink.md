---
layout: default
description: Add Vcenter in Doctor Blink
title: Add Vcenter in Doctor Blink
service: doctor
runbook-name: Add Vcenter in Doctor Blink
tags: oss, bluemix, doctor, credentials, blink
link: /doctor/Runbook-add-the-vcenter-in-doctor-blink.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}

## Purpose

Add Vcenter in Doctor Blink.

## Technical Details

Add the Vcenter IP address and domain name in the inception VM1 and VM2 where the _blink_agent_ service is located.

## User Impact

User cannot access the **Vcenter** via the domain name in the browser.

## Instructions to Fix  

### 1. Get the Vcenter IP address.

You can get if from the deployment yaml or ask the local team for it.

  * From [{{doctor-portal-name}}]({{doctor-portal-link}})
  * Search for the environment.
  * Under the **YML** column.
  * Click on the **YML** icon _bosh deployment yml_
  * Find the _host_ and _domain_ entries.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/yml_domain.png){:width="640px"}
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/yml_domain.png){:width="640px"}

### 2. Edit the `/etc/hosts`

In the inception VM1 and VM2. Add the following line: `$vcenter_ip vcenter.$domain`

  {% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}
  {% include_relative _{{site.target}}-includes/tip_ssh.md %}


* e.g. for bnsf002 environment add  `169.1.14.150 vcenter.bmx002.bnsf.bluemix.net` to the /etc/host by using an editor of your choice, such as vim.

### 3. Restart the Doctor blink agent

  * By running the command `docker restart blink_agent`, in the inception VM1 and VM2.

### 4. Test Vcenter

  * Enable blink proxy in your browser.
    - See [{{doctor-dset-pac-name}}]({{doctor-dset-pac-link}}) for how to setup and use the {{doctor-blink-proxy-name}}.
  * Access the Vcenter at `https://vcenter.$domain`

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

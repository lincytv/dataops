---
layout: default
description: An overview and onboarding of the SSH Web Console
title: SSH Web Console
service: doctor
runbook-name: Runbook SSH Web Console
tags: oss, bluemix, doctor,ssh,ssh_web
link: /doctor/Runbook_SSH_Web_Console.html
type: Information
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## What is Doctor SSH Web Console
Doctor SSH web console is a tty (terminal) web simulator running in Bluemix Doctor. Doctor users can use this simulator to SSH all servers in Bluemix environments without any VPN.

Doctor SSH web console has a security audit and access control. But it don't save any passwords or keys for target server. The Doctor user has to use their own SSH key or password to access the target server via Doctor SSH web console.

## How it works

Here is a high level architecture on how it was implemented.
![Doctor Web SSH Console]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/SSH_web_console_arch.png){:width="700px"}

The Doctor web SSH console can support user/password or SSH key to access your target server in public/dedicated/local environments. When a _connect server_ command comes, Doctor agent will spin a SSH connection from the target server to the SSH hub cluster. The SSH Web server will use this connection to connect to the target server. This connection will be closed if the session is closed.

## How to onboarding
### Using Doctor Web SSH Console

1. Doctor web SSH console agent is running in the Doctor agent. It will auto-deploy by {{ucd-portal-short}} ({{ucd-portal-name}}) when a new environment is created.
2. There are **SSH** buttons/icons in {{doctor-portal-name}} portal associated with each device. Typically, there are two main entrances:
  * **Option 1**
  * From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/cloud).
  * Search an environment.
  * Click on the environment.
  * Go down to the **Details** section.
  * Select **IaaS** tab.
  * Find a VM using the search filter.
  * Click on **SSH** icon under the _Actions_ column.
  ![Doctor Web SSH Console Device list]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-iaas.png){:width="640px"}
  * **Option 2**
  * From [{{doctor-portal-name}}->Access->Device List]({{doctor-portal-link}}#/vm_action)
  * Select an environment from the dropdown list.
  * Click on **SSH** icon under the _Actions_ column.
  ![Doctor Web SSH Console Iaas]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-device-list.png){:width="640px"}
  * In both cases a new tty terminal in a new browser tab will open.
  ![Doctor Web SSH Console Iaas]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-tty.png){:width="640px"}
3. It gets the **IaaS** list by _IaaS API_ key from the Bluemix deploy configuration file (JML file). Which it needs to install a Doctor agent [How]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Operation_Score_Card.html) in the target environment, if the servers are not contained in the Bluemix Platform _IaaS_ list.
4. _Doctor_ also supports the _SSH_ to the target server by _SSH_ key, and it needs to upload the SSH Private key first in the preference page. Here are the steps:
    * From [{{doctor-portal-name}}]({{doctor-portal-link}}).
    * Click your ID to open the preference page.
    ![Doctor Web SSH Console Key 1]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-1.png){:width="640px"}
    * Click the account button.
    ![Doctor Web SSH Console Key 2]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-2.png){:width="640px"}
    * Click the SSH key button.
    ![Doctor Web SSH Console Key 3]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-3.png){:width="640px"}
    * Add, Delete, Update your key.
    ![Doctor Web SSH Console Key]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-key-4.png){:width="640px"}
5. For some servers which have special configurations, e.g. ssh service in the GitHub server bind port 122 not default 22, the *8Port Forward** function can forward SSH requests to target endpoints using specific ports.
    * Open the port forward page.
    ![Doctor Web SSH Console port forward 1]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-port-forward-1.png){:width="640px"}
    * Input the port number.
    ![Doctor Web SSH Console port forward 2]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/Web-ssh-port-forward-2.png){:width="640px"}

## Assumption and onboarding process

### If the services are applications or servers

1. [Request SSO ID]({{site.baseurl}}/docs/runbooks/doctor/Request_SSO_ID.html)

### If the services are Isolated Servers

1. [Request SSO ID]({{site.baseurl}}/docs/runbooks/doctor/Request_SSO_ID.html)

2. [Deploy Doctor Agent]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Runbook_Deploy_Doctor_Agent.html)

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

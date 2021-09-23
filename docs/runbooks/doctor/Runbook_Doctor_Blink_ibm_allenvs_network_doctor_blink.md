---
layout: default
description: This Runbook is for PagerDuty alerts when the doctor blink service is down.
title: Doctor Blink Service ibm.allenvs.network.doctor.blink is Down
service: blink_agent
runbook-name: Doctor Blink Service is Down
tags: oss, bluemix, doctor, blink, blink_agent, docker
link: /doctor/Runbook_Doctor_Blink_ibm_allenvs_network_doctor_blink.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}
__

## Purpose

This alert happens when doctor_blink service is down.

## Technical Details

There are two deployments of the Blink agent at Doctor agent VM. One for Operators can be used via the Doctor portal; it checks Estado (**https://estado.xxx.bluemix.net** e.g. **https://estado.rbc.ca-east.bluemix.net**) response time in each Bluemix account (the threshold is 60s). The other deployment is for monitoring the test Bluemix console.

Grafana shows the status of the doctor blink for all environments at [{{grafana-dashboard-name}}]({{grafana-dashboard-link}}). Select the specific environment to isolate it's status and filter out all other environments.


## User Impact
If blink service is down, user can not access to the web service or web portal of this environment with blink proxy.

## Instructions to Fix

### If you receive a PagerDuty alert containing one the follow

`st_ace_homepage_proxy_local` or `st_ace_homepage_proxy_dedicated`.

For example: _Bluemix Alert SEV2 - DEDICATED:mizuho.env1.ace.homepage : **st_ace_homepage_proxy_dedicate** (ACE homepage is unavailable due to proxy error)_

  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
  - Select **Remote Command**
  - Search for the Environment.
  - Input ```docker restart doctor_blink_ace```.
  - Click **Run**.

### If you receive a PagerDuty alert like

`Bluemix Alert SEV2 - ibm.allenvs.network.doctor.blink.ENV.st blink (Doctor Blink is down)`

#### Step 1 Verify that the environment is complete and handled over to SREs

  - From [{{doctor-portal-name}} Governance -> Handover Management]({{doctor-portal-link}}/#/handover).
  - User the search box, to find the alert environment.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/handover/hand_over_to_customer.png){:width="640px"}
  - **If the environment is not `Hand Over to Customer` resolve the PD and stop here**.
  - if the alert keeps triggering, please contact {% include contact.html slack=cloud-software-dev-slack name=ccloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} or {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid %}.

#### Step 2 Check if the Estado page for the environment is available

   - Try to access `https://estado.{domain name}` by {{doctor-blink-proxy-name}} at `{{doctor-blink-proxy-link|strip}}:{{doctor-blink-proxy-port|strip}}`
   {% if site.target == 'ibm'%}
     (For L_DEV the proxy configuration should be set according the environment : <br>
L_DEV02: `{{doctor-dev-env-proxy-ip|strip}}:{{doctor-dev-env-02-port|strip}}`,<br> L_DEV03: `{{doctor-dev-env-proxy-ip|strip}}:{{doctor-dev-env-03-port|strip}}`,<br> L_DEV04: `{{doctor-dev-env-proxy-ip|strip}}:{{doctor-dev-env-04-port|strip}}`, <br> L_DEV05: `{{doctor-dev-env-proxy-ip|strip}}:{{doctor-dev-env-05-port|strip}}`,<br> L_DEV06: `{{doctor-dev-env-proxy-ip|strip}}:{{doctor-dev-env-06-port|strip}}`). <br>
For more information of [{{doctor-dev-env-portal-name}}]({{doctor-dev-env-portal-link}})
   {% endif %}

   - See [{{doctor-dset-pac-name}}]({{doctor-dset-pac-link}}) for how to setup and use the {{doctor-blink-proxy-name}}.

   - **TIP:** To find the domain name:
      - Find the Environment, by viewing the incident in [{{doctor-portal-name}} -> Incident -> PagerDuty Incident]({{doctor-portal-link}}/#/eventmanager/pd_incidents).
      - Use the search options to find a ticket.
      - Then using the Environment, find the domain name.
      - [{{doctor-portal-name}} -> Access -> Blink]({{doctor-portal-link}}/#/proxy_blink)
      - Use the search list to find the Environment found previously.
      - Get the domain name from the search results.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_agent_3.png)

   - If access to Estado fails, it does not necessarily mean that Blink is not healthy - Estado my be down. Another test to see if Blink is healthy is to Access the Console for the Environment (aka. ACE).  
       - [{{doctor-portal-name}} -> Access -> Blink]({{doctor-portal-link}}/#/proxy_blink).  
       - Find the environment and then click one of the ACE Console links.
       - If a page displays where you can **Log In** to the environment then you can resolve the incident.
       ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_agent_2.png)
       > **Note** that the links to access the Console are not available for the public staging and production environment (YS_* and YP_*).



#### Step 3 Login to the VM that has the doctor agent

  - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
  - Select **Doctor Keeper**
  - Search for target environment
  - Press **SSH**
  - `su` `<YOUR_SSO_ID>`.
  - `sudo -i` to change to root.
  - When prompted for your password, use your SSO Password.

  {% include_relative _{{site.target}}-includes/tip_ssh.md %}

#### Step 4 Check network status

  {% if site.target =='ibm' %}Skip this step if the environment is one of the Lacaixa or BNPP environments.{% endif %} For the rest of environments, on the VM, check network status

   - Run `nc <IP> 22 -w 3`.
   > **Note** You can find IP in docker-compose file.

   - Run `cat /opt/doctor-keeper/config/docker-compose.yml`.
   - Search `blink_agent`.
   - Find the `--hub` parameter in `command` of `blink_agent`.
   - You will see something like the follow:

            blink_agent:
              command: doctor-blink --hub {{doctor-ssh-ip-public|strip}} --port 45081 --user sshhub           

   - If there is no `--hub`, use default IP `10.124.116.109`.
   - Then run `echo $?`.
      - If the result is 0, continue to the next step.
      - If the result is anything other than 0, there is a network issue. Wait 5 minutes (in the event that the network issue is intermittent) and then run the `nc` command again. If the `nc` command still returns anything other than 0, contact the on-call network person via Slack. Once the network issue is resolved continue to the next step.

#### Step 5 Check if blink hub is correct

   - Navigating to [{{wukong-portal-name}}]({{wukong-portal-link}})
   - Select **Remote Command**
   - Search for the Environment.
   - Input ```cat /opt/doctor-keeper/config/docker-compose.yml```, click **Run**.
   - Search `blink_agent`.
   - Find the `--hub` parameter in `command` of `blink_agent`.
   - You will see something like the follow:

             blink_agent:
               command: doctor-blink --hub {{doctor-ssh-ip-public|strip}} --port 45081 --user sshhub  

   - Please check the hub IP, if there is no --hub, it indicates it use default IP `10.124.116.109`.

   |Environments|hub IP|
   |:-----|:-----|
   |public environments|169.44.75.235|
   |L_LACAIXA,LACAIXA_2,L_LACAIXA_3,L_LACAIXA_4,L_LACAIXA_5|10.126.152.74|
   |other environments|10.124.116.109, this hub ip is used by default|

   - If the hub ip is not correct, please logon the doctor agents and update it to correct one, then run `curl -k https://localhost:5999/compose/up`


#### Step 6 Restart the blink agent

  Once you receive a 0, {% if site.target =='ibm' %} or if the environment is Lacaixa or BNPP,{% endif %}, restart the blink agent by running `docker restart blink_agent` as root on the VM.

   - If you receive a __Error response from daemon: No such container: blink_agent__ error, make sure you are on the correct VM. In [{{wukong-portal-name}}]({{wukong-portal-link}}), some environments have more than one VM listed (for example, a SH CLI VM and a Doctor VM).
   - If you receive a __Cannot connect to the Docker daemon. Is the docker daemon running on this host?__ error when running the command in step 4 above, run `service docker restart` and then retry step 4 above.
   - If you receive a __Error response from daemon: Cannot restart container blink_agent: Container 5ed44baca9bfe645f08b2d18bab437510846cd977a1f26152c1a1e206b359e75 is already active__ error (or `docker ps -a` shows the blink_agent container in `Exited (1) x hours ago` state), run `docker ps -a` to list the container, `docker rm <CONTAINER_ID>` to remove the container, and then `curl -k https://127.0.0.1:5999/compose/up` to restart the container.


#### Step 7 To verify that the blink agent has started and working

  * **Step 7.1 Check the blink_agent is up and running:**
    - Run `docker ps` as root in the terminal.
    - You should see `blink_agent` listed in the output and the status column should reflect the time in which you restarted it (i.e. Up About a minute).
    - But if the blink_agent still not in "up" status, AND get the following error message after restart blink_agent,
    `Error response from daemon: Cannot restart container xxx:
    Container xxx is already active`
      - Please remove the blink_agent container by `docker rm -f blink_agent`.
      - Restart by `curl -k https://127.0.0.1:5999/compose/up`.

  * **Step 7.2 Once the blink_agent is up and running, verify the logs**
    >Note: Even the blink_agent container is up and running, it does not mean the blink agent is working, we should follow the steps to make sure the blink_agent is working

    - Check blink_agent logs by runing `docker logs -f --tail=10 blink_agent`
    - If you find this error from the log `start unbound error  exit status 1`, it means the `unbound` inside the blink_agent container does not start up well. This may caused by the `unbound` on Doctor VM is in `<defunct>` state. So you need to kill `unbound` on Doctor Agent VM and restart blink_agent.
      - On doctor agent VM, run `lsof -i:53`
      - Run `kill -9 <PID>`, PID is the PID of the unbound get from last command.
      - Run `docker restart blink_agent`
      - Run `docker logs -f --tail=10 blink_agent` , if you get the logs like this, then blink_agent is running successfully.

      ```
      2018/12/17 07:09:14 Blink: 5.2 Build time: 2018-03-22 18:30:00  Support long time response
      2018/12/17 07:09:14 Blink port:  45001
      2018/12/17 07:09:14 Using default blink hub
      2018/12/17 07:09:14 Blink agent using dns: 10.120.171.172,10.0.80.11,10.0.80.12
      2018/12/17 07:09:14 Primary DNS:  10.120.171.172  Secondary DNS:  10.0.80.11
      2018/12/17 07:09:14 Use username: sshhub
      2018/12/17 07:09:14 Blink authentication enabled

      ```
  * **Step 7.3 Make sure blink is using the correct port**
    - Run cat `/opt/doctor-keeper/config/docker-compose.yml`.
    - Search blink_agent.
    - You will see something like the follow:

             blink_agent:
               command: doctor-blink --port 48012 --auth true --user sshhub           
    - Now open [{{doctor-blink-ha-proxy-config-name}}]({{doctor-blink-ha-proxy-config-link}}).
    >**Note:** if you don't have access to the above link please contact  {% include contact.html slack=doctor-blink-slack name=doctor-blink-name userid=doctor-blink-userid notesid=doctor-blink-notesid%} to request access.

    - Look for the environment and get the backend of the environment.
      ```
      #L_RBCGCC
      acl acl_l_rbcgcc hdr_dom(host) -i gcc.ca-east.bluemix.net
      use_backend backend_l_rbcgcc if acl_l_rbcgcc
      acl acl_l_rbcgcc_customer hdr_dom(host) -i fg.rbc.com
      use_backend backend_l_rbcgcc if acl_l_rbcgcc_customer
     ```
    - Then search for **backend_l_rbcgcc**, for this example, in the document.
      ```
      backend backend_l_rbcgcc
              server server1 10.124.116.109:48012
      ```
    - Make sure port numbers match if does not, set the port number from {{doctor-blink-ha-proxy-config-name}} in the `/opt/doctor-keeper/config/docker-compose.yml`.
    - Check the port is not already use by another application.
      - Log into to the IVM is running *blink_agent* and run `netstat -pe | grep <<port_number>>` e.g. `netstat -pe | grep 45101`
      - if you get something like the follow:

      ```
      root@doctorssh2:~# netstat -pe | grep 45101
      tcp        0      0 10.124.116.109:45101    10.121.196.7:postgresql ESTABLISHED root       3599507163  1502/ruby   
      ```
      In this example port *45101* is already used by process *1502* try the follow to get the application using the port

      ```
      root@doctorssh2:~# ps -ef | grep 1502
      root      1502  1409  0 Sep10 pts/3    01:23:47 ruby launch.rb -c taishan_tipselfhealing -s tipselfhealing -r https://10.154.56.42:4568
      root     16879 14888  0 10:45 pts/5    00:00:00 grep --color=auto 1502
      ```

      In  this example the port is already occupied by *tipselfhealing*
    - If the port is already occupied stop the application using the *port* to let blink_agent to retake the port number need it.
      - Following our example you will something like the follow:
      ```
      root@doctorssh2:~# docker ps
        CONTAINER ID        IMAGE                                                              COMMAND                  CREATED             STATUS              PORT
        S               NAMES
        adacf29073aa        doctormbus3.bluemix.net:5000/taishan_v3/backend:5.20190910015924   "sh /opt/start.sh tai"   11 days ago         Up 11 days              
                doctor_tipselfhealing
      cbf65d4ed6b5        softinstigate/restheart                                            "./entrypoint.sh etc/"   3 years ago         Up 2 years              
      restheart
      ```
      - Stop the container, in this case, by `root@doctorssh2:~# docker docker stop doctor_tipselfhealing`
    - Once the port conflict is resolved restart blink_agent fisrt then the process used to occupied the blink port.
    - Check the logs and make sure blink is working.

#### Step 8 Check to see if Estado is running

  If Estado is running, continue to the next step. If Estado is still down, do the following:

   - Find your PagerDuty incident in Doctor under Incident -> PagerDuty Incident.
   - Click the three-dot icon in the Action column of the incident and then select Gravity Wave.
   - In the browser tab that opens, scroll down to Estado.
      - If Estado is running, continue to the next step.
      - If you see `Estado 0 services down`, the Estado status keep loading endlessly, and you click the + icon and no services are listed, then Estado is not running.
      - If Estado is not running, add a note to the PagerDuty incident that Estado is down and resolve the incident.

#### Step 9 If you had verified that Estado is running in step 7

But the request for Estado times out in your browser, make sure that the `proxy.pac` file from [{{doctor-dset-pac-name}}]({{doctor-dset-pac-link}}) has a line for the environment if you are using `proxy.pac`. If it is not listed in the `proxy.pac` file, make a pull request to include it. While waiting for your pull request to be merged, you can set your Firefox browser to use the Blink proxy server directly by:
  * Opening Preferences.
  * Seledct Advanced.
  * Select Network.
  * Select Settings…
  * Enabling ‘Manual proxy configuration’.
  * Set ‘HTTP Proxy’ to `{{doctor-blink-proxy-link|strip}}`.
  * Set the port to `{{doctor-blink-proxy-port|strip}}`.

#### Step 10 Check the DNS configuration
  1. Find the bosh director ip in Doctor yml file in field **bosh_url**
    * To find bosh director IP
      - Go to [doctor-configuration](https://github.ibm.com/BlueMix-Fabric/doctor-configuration/tree/master/config) repository.
      - Find the yml file of the environment(e.g. taishan_dedicated_aa1.yml).
      - Find bosh director ip in field **bosh_url**.
      ![Get bosh url]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/GetBoshURLDoctor_Blink_Item8.png){:width="640px"}
  2. Login into the blink agent VM, see [Step 3](#step-3-login-to-the-vm-that-has-the-doctor-agent) for instructions how to log into.
  3. Once completed previous step, `cat /etc/resolv.conf`. You will see something like the follow:

          root@bmx-doctor-agent-aa1:~# cat /etc/resolv.conf
          nameserver 169.47.131.89
          nameserver 10.0.80.11
          nameserver 10.0.80.12

  4. Check if the bosh director IP address from 1 does exist.
    **If does not:**
      - For public and dedicated environments, add bosh director ip to the first line of /etc/resolv.conf file.
      - For local environments, __DO NOT make any change, you need to confirm with SRE if the configuration is ok in slack channel #sre-platform-onshift__.

  5. Restart blink_agent as [Step 5](#step-5-restart-the-blink-agent) explains.

## Notes and Special Considerations

 If any questions, please contact {% include contact.html slack=cloud-software-dev-slack name=ccloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %} or {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid %}.

 {% include {{site.target}}/tips_and_techniques.html %}

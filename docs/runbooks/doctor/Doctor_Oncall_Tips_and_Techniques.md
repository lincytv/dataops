---
layout: default
description: A list of tips and techniques useful for Doctor on-call duties
title: Doctor tips and techniques
service: doctor
runbook-name: Doctor tips and techniques
tags: oss, bluemix, runbook, oncall, ssh, Jumpbox
link: /doctor/Doctor_Oncall_Tips_and_Techniques.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Purpose

To give some helpful tips and techniques useful for users while they are on call for Doctor Pager Duty.

## Disaster recovery

## Alerts

### Cf account/password out-of-date for {<<env_name>}

- Reassign it to SRE([{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}})) operator, these type of alerts are not the responsibility of the doctor team on-call.

### Echometer URL Down Failure: Service: cloud in env: <<env_name> is down.

- From [{{doctor-portal-name}} Governance -> Handover Management]({{doctor-portal-link}}/#/handover).
- If no decommission info for the ENV and the Server is in Yellow status.
- Double check at [{{oss-doctor-name}}]({{oss-doctor-link}}).
- It could be a test environment.
  - If it is a test environment, remove it from Echometer, use [Doctor_Echometer_Guide]({{site.baseurl}}/docs/runbooks/doctor/Doctor_Echometer_Guide.html) runbook.

### Alerts definition documentation

- [Doctor alerts & alerts handled by Doctor Ops](https://ibm.ent.box.com/notes/290166794378)
- [Alerts identified during doctor's runbooks migration](https://ibm.ent.box.com/notes/307491423896)

## How to's

### How to access a VM, when SSH from Wukong and Doctor Home does not work.

- For dedicate and public environments only.
- From [{{wukong-portal-name}}]({{wukong-portal-link}}/).
- Select **Doctor Keeper**.
- Get the alias or IP address of the VM to SSH.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/keeper/WukongDoctorKeeper.png){:width="640px"}
- From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/cloud) open a environment and select the IaaS tab.
- Search for the IP or alias name, IP address is recommend.
- Use the SSH console icon to connect.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/SSH_console.png){:width="640px"}

### How to check and operate Doctor-keeper

- check keeper status
  `supervisorctl status doctor_keeper`
- start keeper
  `supervisorctl start doctor_keeper`
- restart keeper
  `supervisorctl restart doctor_keeper`

> **Note:** restarting doctor_keeper terminates web-ssh session

### How to check Github status

- When GHE is down you can check the [status](https://status.whitewater.ibm.com/) or #whitewater-github on Slack

### How to check supervisorctl log errors

- supervisorctl tail -50 procn_ame stderr example `supervisorctl tail -50 bosh_cli_ssh stderr`

### How to check Doctor load balancers

- From [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
- Log into **OSS account**.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/switch_acct.png){:width="300px" height="288px"}
- From **Resource summary** click on **Services**.
- ![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/services/services.png){:width="600px"}
- From **Services**, select **CIS-Doctor**.
- Select **Reliability** from the left side menu.
- Then select **Global Load Balancers\***.
  > **Note** uk-south is currently turned off before to turned it on, please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %}, click [here](https://github.ibm.com/cloud-sre/ToolsPlatform/issues/7298) for more information.

### How to check the Health of a Machine

    {% include_relative _{{site.target}}-includes/tip_busy_vm_1.md %}

\_\_

### How to contact CDL and doctor team members

Refer to the follow [Emergency contact information](https://w3-connections.ibm.com/wikis/home?lang=en-us#!/wiki/W6a670ad9121a_43a8_a2c8_5f74c346e467/page/Emergency%20contact%20info/edit)

### How to Copy Files To/From a VM in an Environment

- Option 1:
  You can typically copy a file from a VM in an environment to your local machine or to the VM from your local machine. You simply:

  1. Navigate to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  2. Select the environment.
  3. Select the **IaaS** tab.
  4. Locate the VM
  5. Select option **Web Sftp**
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/web_sftp_1.png){:width="640px"}
  6. Enter your SSO user ID and password, and click Connect.
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/web_sftp_2.png){:width="480px"}

  If your file is larger than 100 MB the download is not allowed. As an alternative, you can follow
  [these]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Copy_File_Using_JumpBox.html) instructions to download the file.

- Option 2:
  Use the create SSH tunnel option
  1. Navigate to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  2. Select the environment.
  3. Select the **IaaS** tab.
  4. Locate the VM
  5. Select option **Create SSH Tunnel**
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/ssh_tunnel_1.png){:width="640px"}
  6. Select a port or leave port 22 as default and click **Next**.
  7. You will get a SSH command with a port number.
  8. Use the **Copy** button to copy the command to the clipboard then click on **Close**.
  9. Open a terminal and use the SSH command to connect to the VM
     ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/ssh_tunnel_2.png){:width="480px"}
  10. To copy files use `scp -P $port $user@$ip:$path` example `scp -P 43310 altorres@9.66.243.87:/home/SSO/altorres/test.txt .`
      for more [info]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Copy_File_Using_JumpBox.html)

### How to create a missing environment script for JumpBox

An environment is fully deployed but the Jumpbox script to SSH to an environment does not exist. The environment entry doest not exist at:
[{{doctor-ops-infra-tools-repo-name}} JumpBox Environments]({{doctor-ops-infra-tools-repo-ssh-ports}})

1. Clone the repository [{{doctor-ops-infra-tools-repo-name}}]({{doctor-ops-infra-tools-repo-link}}).
2. Create a new branch.
3. Get the port number of the environment from [{{doctor-blink-ports-config-name}}]({{doctor-blink-ports-config-link}}).
   - You will see a line like the follow: `ded_cfs2_1146961,60154,,45157` where:
     - ded = dedicated , loc = local , pub = public ...
     - cfs2 = environment name.
     - 1146961 is the Softlayer account number.
     - **60154** = doctor ssh tunnel port **This the port number you will use in the next steps**.
     - empty = doctor ssh_tunnel port2 normally unused.
     - 45157 = doctor blink port.
4. From your branch edit the file **JumpboxEnv.csv** under _/master/build/_
5. Add a new line at the button of the file like the follow (as the sample above):
   - `d_cfs2,9.66.243.81,60154,,` where:
     - d\_ dedicated env (l=local).
     - cfs2 environment name.
     - 9.66.243.81 Jumpbox IP address.
     - 60154 ssh port number from 3.
6. Save your changes and create a new pull request.
7. Request a review from the CDL team.
8. A CDL member will approve and merge your request or reject it providing comments.
9. If your PR is approved then a Jenkins job will start and generate the requested script for you at the Jumpox.
10. Check 30 min later to make sure the script exist and runs as expected.

> If you don't have access to the {{doctor-blink-ports-config-name}} request access to {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or {% include contact.html slack=doctor-blink-slack name=doctor-blink-name userid=doctor-blink-userid notesid=doctor-blink-notesid%} Still questions? look at this [issue](https://github.ibm.com/cloud-sre/ToolsPlatform/issues/6699) as example.

### How to create a temporary access for a user in doctor

This option can be use as workaround and/or an emergency situation and needs to be authorized by the requester manager and/or doctor admin.
The access is only temporary and will last at the most for 30 min. To obtain a regular access to doctor, please review [Request Doctor Access]({{site.baseurl}}/docs/runbooks/doctor/Request_Doctor_Access.html)

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **Users** from the left side menu.
- Click on **Add a new user**.
- You will get the follow:
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/add_new_user.png){:width="640px"}
- Enter the w3 email address or IBMid.
- Select the role(s) need for a user to perform his/her duties.
- Select then environment(s) required.
- Click on **Add and Close**.
  > If you don't know the roles/environments ask for user with a similar access as the user is requesting.

### How to determine the Primary Inception Machine

Local environments often have two Inception machines (a.k.a. IVM). One is a primary VM and the other a backup.
The primary VM is important since that is kept up-to-date and is used by UCD to deploy and update the environment.
The primary inception machine can be identified by running `ifconfig | grep ucarp` in Wukong->Remote Command.
If this returns something then that is considered the primary IVM.

This must be consistent with the **bosh_cli** value in the environment's configuration file found
[here](https://github.ibm.com/BlueMix-Fabric/doctor-configuration).
If they differ, then you should consult with the on-duty GRE and based on their confirmation, switch
the IPs between the **bosh_cli** and the **bosh_cli_backup**.
Use `@cybot whos on call GRE` to determine who the on-duty GRE is.

### How to find an environment domain

- From {{doctor-alert-system-name}} incident in [{{doctor-portal-name}} -> Incident -> PagerDuty Incident]({{doctor-portal-link}}/#/eventmanager/pd_incidents).
- Use the search options to find a ticket.
- Then using the Environment, find the domain name.
- [{{doctor-portal-name}} -> Access -> Blink]({{doctor-portal-link}}/#/proxy_blink)
- Use the search list to find the Environment found previously.
- Get the domain name from the search results.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink_agent_3.png)

### How to find audit (root/vyatta) login information

Sometimes a member from the security team will request information of who logged to a VM using root/vyatta user, a request like the follow may happened [Slack requet](https://ibm-cloudplatform.slack.com/archives/C84FD5R0W/p1549286886881900).

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **Privilege ID Management** from the left side menu.
- From the top menu, select **Action Audit**.
- Choose one or more filters you narrow down your search.

### How to find proxy configuration by environments

- [{{doctor-haproxy-conf-name}}]({{doctor-haproxy-conf-link}})
- [{{doctor-blink-ports-name}}]({{doctor-blink-ports-link}})

> **Note:** if you don't have access to the above link please contact {% include contact.html slack=doctor-blink-slack name=doctor-blink-name userid=doctor-blink-userid notesid=doctor-blink-notesid%} to request access.

### How to find UCD environment name in Doctor

- From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
- Use the search options to find an environment.
- Hover over the environment name.
- A popup window will display.
- Look for the **UCD_env_name:**
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/get_ucd_env_name.png){:width="600px"}

### How to fix when user is unable to access his own /homeSSO/SSOid home directory

Mostly SRE users connect to bosh_cli VMs to upload/download date either connecting via SSH or Web SSH or Web Sftp or SSH Tunnel.
Most of the time the problem are access rights to fix this problem follow the next steps.

> **This is not a doctor issue and needs to be resolved by SSOid team, before to start the following steps contact #sos-idmgt Slack channel if you or a user can't get help from SSOid team you may proceed with the steps belong**

- From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
- Use the search options to find an environment.
- Click on the environment name.
- You will move to environment details page or cloud page.
- Connect to the Bosh Client.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/bosh_client_icon.png){:width="600px"}
- Enter your SSO id or Firecall id.
- `sudo -i`
- `ls -l /home/SSO |grep <SSOid>`, example, `ls -l /home/SSO |grep altorres`
- if you see the follow:
  ```
  root@boshcli:/# ls -l /home/SSO |grep altorres
  drwx------  3 root           root                  4096 Apr 12  2018 altorres
  ```
- Change the ownership as `<SSOid>:BU018-BMX-GID-Filter`
  - `cd /home/SSO/<SSOid>`
  - `chown -R <SSOid>:BU018-BMX-GID-Filter <SSOid>`, example, `chown -R altorres:BU018-BMX-GID-Filter altorres`
  - Make sure changes were applied `ls -l /home/SSO |grep <SSOid>`, example `ls -l /home/SSO |grep altorres`
  - You should see:
    ```
    root@boshcli:/# ls -l /home/SSO |grep altorres
    drwx------  3 altorres           BU018-BMX-GID-Filter                  4096 Apr 12  2018 altorres
    ```
- After changing the ownership users should not have problem to access their `/home/SSO/<SSOid>` home location.

### How to get a "docker run" command from compose file

- Please refer to [Compose file version 2 reference](https://docs.docker.com/compose/compose-file/compose-file-v2/)
- Some examples:

```
doctor_backend
docker run -it --net=host --restart=always -d -v /opt/ansible:/opt/ansible -v /opt/sqllite/taishan_estado.db:/opt/taishan/taishan_estado.db -v /opt/sqllite/taishan_encrypt.db:/opt/taishan/taishan_encrypt.db --name doctor_backend doctormbus1.bluemix.net:5000/taishan_v3/backend:5.20180502055820  taishan_local_rbc-scc cloud,ope,estado,scheduler,servicemgr,encrypt,envscheduler https://10.125.89.62:4568

doctor_access
docker run -it --net=host --restart=always -d -v /var/log/doctor_access:/opt/logs --name doctor_access doctormbus1.bluemix.net:5000/taishan_v3/backend:5.20180507031752 taishan_local_rbc-scc access https://10.125.89.62:4568 4588

doctor_scriptengine
docker run -it --net=host --restart=always -d -v /opt/ansible:/opt/ansible -v /var/log/doctor_scriptengine:/opt/logs --name doctor_scriptengine doctormbus1.bluemix.net:5000/taishan_v3/backend:5.201803221048-staging  taishan_local_rbc-scc scriptengine https://10.125.89.62:4568 4600

doctor_security
docker run -it --net=host --restart=always -d -v /opt/ansible:/opt/ansible -v /opt/ansible:/opt/ansible --name doctor_security doctormbus1.bluemix.net:5000/taishan_v3/backend:5.20180526105701 taishan_local_rbc-scc security https://10.125.89.62:4568 4693
```

### How to get blink customer environment DNS IP address

- Option 1:
  - From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
  - Search the environment.
  - Click on **JML** icon.
  - A new window with the **JML** file contents will be displayed.
  - Search the word **dnssever** you will see a value pair like `apim_mgmt_pri_dnsserver: 10.112.225.110`
- Option 2:
  - From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Remote Command**.
  - Search and select the environment.
  - Run the command `docker logs -f --tail=10 blink_agent`
    - You will get something like the follow:
      ```
      2020/02/07 17:11:06 Blink agent using dns: 10.112.225.110,10.113.97.89,10.0.80.11,10.0.80.12  
      ```
    - Running `nslookup` on any device in the same host gave something like the following output:
      ```
        nslookup estado.lbg.eu-gb.bluemix.net  10.112.225.110
        Server:         10.112.225.110
        Address:        10.112.225.110#53
        Name:   estado.lbg.eu-gb.bluemix.net
        Address: 159.8.167.167
      ```

> **Note:** Blink traffic from user local laptop is the follow:
> `laptop -> HAProxy Server({{doctor-blink-proxy-domain}}) -> CustomerEnv Doctor Agent -> DNS resolution of the URL`

### How to get ibmadmin@us.ibm.com password for an environment

1. Get vault token:

```
curl -X POST -d '{"role_id":$vault_role_id,"secret_id":$vault_secret_id}' $vault_server_address:$vault_server_port/v1/auth/approle/login

e.g.: curl -X POST -d '{"role_id":"80cfc386-32b2-d6a9-9248-1d5b9e255d8f","secret_id":"d1fa4330-eaf1-a9b7-f09b-5e57b0e734a5"}' https://vserv-us.sos.ibm.com:8200/v1/auth/approle/login

or

curl -X POST -d '{"role_id":"80cfc386-32b2-d6a9-9248-1d5b9e255d8f","secret_id":"d1fa4330-eaf1-a9b7-f09b-5e57b0e734a5"}' https://vserv-us.sos.ibm.com:8200/v1/auth/approle/login |python -mjson.tool | grep client_token

or

curl -X POST -d '{"role_id":"80cfc386-32b2-d6a9-9248-1d5b9e255d8f","secret_id":"d1fa4330-eaf1-a9b7-f09b-5e57b0e734a5"}' https://vserv-us.sos.ibm.com:8200/v1/auth/approle/login | jq -r '.client_token'
```

2. Get password

```
curl $vault_server_address:vault_server_port/v1/$vault_path/secrets/password/v2 -H "X-Vault-Token:$client_token"

e.g.:

curl https://vserv-us.sos.ibm.com:8200/v1/auth/approle/login/v1/generic/crn/v1/448802/dedicated/bluemix-cloudfoundry/us-south/a-448802/lloyds/secrets/password/v2 -H "X-Vault-Token:d1fa4330-eaf1-a9b7-f09b-5e57b0e734a5"
```

> Note $vault_role_id, $vault_secret_id,$vault_server_address,$vault_server_port,\$vault_path can be found on JML file.
> from [{{doctor-portal-name}}->Datacenter]({{doctor-portal-link}}/#/datacenter)
> click the icon under JML for the environmet

> If /password/v2 does not exist get the /password/vX as follow:

- From [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter).
- Use the search options to find an environment.
- Click on the YML icon
- Once open the YML file search for `manifest_version`
  - If `manifest_version` is null or does not exist
    - Search for the value of "password" in the YML and/or JML files and use it.
  - If `manifest_version` is not null
    - From [{{wukong-portal-name}}]({{wukong-portal-link}}).
    - Select **CI & CD** from the left side menu.
    - Input **doctor_ucd** in the _Continues Deployment_ field.
    - Select any of the listed Environment(s)
    - Select **Remote Command** from the left side menu.
    - input the environment name and type the follow:
      `cat /opt/ucd/jml/<environmet>/jml/CloudFoundry/cfd-vars.yml|grep cf_admin_password`
      e.g.
      `cat /opt/ucd/jml/D_AA2/jml/CloudFoundry/cfd-vars.yml|grep cf_admin_password`
    - You will get something like the follow: `cf_admin_password: ((/secrets/password/v4))`
    - Use `password/v4` instead of `password/v2` for this example.

### How to get UAA admin password for a Bosh environment

Passwords are stored on credhub
Run the following command in boshcli to get its value :
`/var/releases/bin/check.credhub.sh -o get_credhub_value -s uaa_admin_client_secret`

      root@boshcli:~# /var/releases/bin/check.credhub.sh -o get_credhub_value -s uaa_admin_client_secret
      Warning: User to access credhub is not specified! Use default one: director_to_credhub!
      Warning: Password for credhub user is not specified! Get it from /opt/ops-infra-tools/20190711_101252/bin/jml_config_env_file_ops.conf!
      Warning: Credhub secert version is not specifiled! Use default version: 1
      {
        "data": [
          {
            "value": "XXXXXXXXXXX",
            "version_created_at": "2019-05-29T05:13:42Z",
            "type": "password",
            "name": "/secrets/uaa_admin_client_secret/v1",
            "id": "XXXXXXXXXXXXXXXXX"
          }
        ]
      }

### How to handle problems to access Doctor or Wukong

If you are having problems accessing Doctor or Wukong, you might be able to access it in the staging environmet:

- [Doctor staging]({{doctor-portal-staging-link}})
- [Doctor staging ldap]({{doctor-portal-staging-ldap-link}})
- [Wukong staging in UK]({{wukong-portal-staging-UK-link}})
- [Wukong staging in US south]({{wukong-portal-staging-US-south-link}})
- [Wukong staging in US east]({{wukong-portal-staging-US-east-link}})

> **Note:** if you don't have access contact {% include contact.html slack=doctor-blink-slack name=doctor-blink-name userid=doctor-blink-userid notesid=doctor-blink-notesid %}

### How to Hard Restart a VM

1. Navigate to [{{doctor-portal-name}}]({{doctor-portal-link}}).
2. User the Search field to find the environment.
3. Click on the selected environment.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/bosh-cli-ssh/no_route_to_host_1.png)
4. Under **Details**.
5. Move to **IaaS** tab.
6. Find the **BOSH CLI VM**.
7. Select the **three vertical dots** on the far right of the **BOSH CLI VM**
8. Click on **Hard Restart Server**. After the restart try logging in again.
   ![]({{site.baseurl}}/docs/runbooks/doctor/images/bosh-cli-ssh/no_route_to_host_2.png)

> **Note:** To restart a doctor VM search for the doctor IP addresses or search using `doctor` as keyword

### How to locate/find an environment when it is not present on the PD

- To find the environment associated with a Pager Duty incident like `INC0144869:ESC0747885:ibm.env5_lon.infra.dbbackup : st_dbbackup (DB backup is failed)`

  - Take the clue `ibm.env5_lon`
  - Enter it in the search field in the Doctor Home page (as in A):
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/search_for_environment.png){:width="640px"}

  * If a name like `ibm.env4` match multiple environments.
  * You can isolate the specific environment by clicking on each `Env` icon (B).
  * Searching for _monitor_env_name_ and _monitor_org_name_:
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/search_for_environment2.png)

- Find an environment by using PagerDuty ID number

  - From {{doctor-alert-system-name}} incident in [{{doctor-portal-name}} -> Incident -> PagerDuty Incident]({{doctor-portal-link}}/#/eventmanager/pd_incidents).
  - Use the search options to find a ticket.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/incident/pd/pd_environment.png){:width="640px"}

- Find an environment by IP
  - If you get a PD like the follow: `Bluemix Alert SEV2 - :.checkin.failure : failed (checkin root on instance 169.44.27.244)`
  - From [{{doctor-portal-name}} -> infrastructure -> IP Lockup]({{doctor-portal-link}}/#/ip_lookup).
  - Enter the IP address.
  - Click on Search.
  - Click on the SSH icon.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/infrastructure/ip_lookup/ip_loockup.png){:width="640px"}
  - A new tab will be open where you can get the environment name.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/infrastructure/ip_lookup/ip_lookup_ssh.png){:width="640px"}
  - In this example the environment name is `D_GTSXAAS`

### How to recover Blink Access (proxy_blink) List

If your a request like the follow:

```
David Middleton [10:23 AM]
@Jason Wang can you take a look at https://doctor.cloud.ibm.com/#/proxy_blink
I’m unable to load it incognito and in normal browser,
looks like the same issue that was happening yesterday
```

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **CI & CD** from the left side menu.
- From the **Continuous Deployment** filter out **doctor_blink**.
- Restart each of the listed environments one by one.

### How to recover data from Infrastructure->Network Management in Doctor

If you get a request like [this](https://ibm-cloudplatform.slack.com/archives/C84FD5R0W/p1544633866239200), `doctor_networkmgr` service
needs to be restarted.

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **CI&CD** from the left side menu.
- Search for **doctor_networkmgr**.
- Use the icon ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/refresh_btn.png){:width="20px"} to restart the service for all environments listed.
- Wait about 5 min to get the service fully back.
- Go to [{{doctor-portal-name}} Infrastructure->Network Management]({{doctor-portal-link}}/#/network_mgr).
- And make sure the data is recovered and notify it to the requestor.

### How to request access for eu_emerg

To access dev-ops functions for an EU Managed Environment, such as YP_FRANKFURT, you will need to request an eu_emerg access to the environment. For an example, when you attempt to SSH to YP_FRANKFURT, you will be prompted to request access.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_eu_permission_denied.jpg){:width="450px"}

The following [runbook]({{site.baseurl}}/docs/runbooks/doctor/Request_EU_Emergency_Access.html) explains the process and provides the required steps to request the appropriate access.

### How to resolve the Doctor agent running out of CPU/memory issue

When a Doctor agent encounters CPU/memory full (checking via commands like `top`, `free -m`), the blink_agent and/or bbo_agent might not work and triggers alerts. In this situation, we might need to reboot the Doctor agent VM.

For public/dedicated env, we can directly reboot or ask GRE to help reboot the Doctor agent VM that is under issue, since it's a dedicated VM that is only used for Doctor agent.

However, **for local env, we cannot reboot the Doctor agent VM, since it is a shared VM used by GRE/UCD team too**.

### How to restart auditd service

Rarely users are not able or have the rights to restart `auditd` service from a VM, and you may get a request on Slack like the follow:
[Slack request](https://ibm-cloudplatform.slack.com/archives/C84FD5R0W/p1549040823854700).

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **Doctor Keeper** from the left side menu.
- Filter the environment(s) requested.
- Use your SSO id.
- `sudo -i`.
- `service auditd restart`.
  > It is possible to use **Remote Command** as well instead of **Doctor Keeper**

### How to restart self-healing of an environment

See the [Slack request](https://ibm-cloudplatform.slack.com/archives/C84FD5R0W/p15803815780795) as reference.

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **Script Execution Audit** from the left side menu.
- Filter the environment(s) requested.
- Select the failed script.
- Click on **Run Again**

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/script_execution_audit/rerunScript.png){:width="600px"}

### How to restart BBO agents

This [how to restart BBO agents]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Doctor_how_to_restart_BBO_agents.html) runbook, shows how to diagnose BBO agents activity and how to restart them, if necessary.

### How to restart the doctor_backend manually

- Log into the VM using [JumpBox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html#how-to-use).

- Look for the **docker_backend** container.
  Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
  if you cannot find the **doctor_backend** container.
  - `docker ps -a`
- Removed the **docker_backend** container.

  - `docker rm -f docker_backend`
    > **Note:** If an environment has a slave script connect to both e.g. _boshcli_l_lufthansa.sh_ and _boshcli_l_lufthansa_slave.sh_ and remove the container where it exist. Use `docker ps -a` to find _docker_backend_ container

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/jumpbox/rmv_docker_backend.png){:width="700px"}

* Recreate the **doctor_backend** container without the `--network host`.

  - Look at `/opt/doctor-keeper/config/docker-compose.yml` file, and search for the `doctor_backend` section.

    - `cat /opt/doctor-keeper/config/docker-compose.yml`

    For example:

    ```
    doctor_backend:
      command: taishan_local_lufthansa cloud,ope,estado,scheduler,servicemgr,encrypt,envscheduler
        https://10.125.89.62:4568
      container_name: doctor_backend
      environment:
      - GROUP_KEY=377b924d4468ca49814ab141f314fa4c
      image: wcp-cto-oss-docker-local.artifactory.swg-devops.com/taishan_v3/backend:5.20180512141912
      network_mode: host
      restart: always
      volumes:
      - /opt/ansible:/opt/ansible
      - /opt/sqllite/taishan_estado.db:/opt/taishan/taishan_estado.db
      - /opt/sqllite/taishan_encrypt.db:/opt/taishan/taishan_encrypt.db
      - /var/log/doctor:/opt/logs
    ```

  - Replace the variables in _< >_ to construct the follow command:

  ```
  docker run -d -t -i --network host --name doctor_backend --restart always -e "GROUP_KEY=<GROUP_KEY>" -v /opt/ansible:/opt/ansible -v /opt/sqllite/taishan_estado.db:/opt/taishan/taishan_estado.db -v /opt/sqllite/taishan_encrypt.db:/opt/taishan/taishan_encrypt.db -v /var/log/doctor:/opt/logs doctormbus1.bluemix.net:5000/taishan_v3/backend:5.20180512141912 taishan_<environment> cloud,ope,estado,scheduler,servicemgr,encrypt,envscheduler https://<ip_address>:<port>
  ```

  Where:<br><br>
  **GROUP_KEY** = _377b924d4468ca49814ab141f314fa4_<br>
  **taishan\_\<environment>** = _taishan_local_lufthansa_<br>
  **https://\<ip_address>:\<port>** = _https://10.125.89.62:4568_ <br><br>

  After replacing the variables it will look like:

  ```
  docker run -d -t -i --network host --name doctor_backend --restart always -e "GROUP_KEY=377b924d4468ca49814ab141f314fa4" -v /opt/ansible:/opt/ansible -v /opt/sqllite/taishan_estado.db:/opt/taishan/taishan_estado.db -v /opt/sqllite/taishan_encrypt.db:/opt/taishan/taishan_encrypt.db -v /var/log/doctor:/opt/logs doctormbus1.bluemix.net:5000/taishan_v3/backend:5.20180512141912 taishan_local_lufthansa cloud,ope,estado,scheduler,servicemgr,encrypt,envscheduler https://10.125.89.62:4568
  ```

  > **Note:** If nothing is listening on https://127.0.0.1:5999/compose/up and the docker version is too old it does not support the `--network` option.<br>
  > remove GROUP_KEY as well.<br> > [Docker run reference guide](https://docs.docker.com/engine/reference/run/#operator-exclusive-options)

### How to restore data on ACE console when DEA Capacity shows an error occurred retrieving DEA capacity information...

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **CI&CD** from the left side menu.
- Search for **doctor_backend**.
  Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
  if you cannot find the **doctor_backend** container.
- Search for then environment.
- Use the icon ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/refresh_btn.png){:width="20px"} to restart the service.
- Wait about 2 min to get the service fully back.
- Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
- For Home Search for the environment.
- Click on the white eye under info.
- The **Cloud Environment Information** will be open.
- Click on **Sync**.
- Wait until the metadata get synchronized.
- Go back the console and refresh and make sure the error is gone.
- If data is not recovered review these additional runbooks:
  - [Metrics data is older than two hours]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Metrics_data_is_older_than_two_hours.html)
  - [Ops Admin Console Doctor Check Failed]({{site.baseurl}}/docs/runbooks/doctor/Runbook-Ops-admin-console-doctor-check-failed.html)

### How to recover Estado when Availiability shows NaN on doctor datacenter or Estado report isn't shown on Diagnose->Estado

- [Estado Status]({{site.baseurl}}/docs/runbooks/doctor/Runbook_SL_Reboot_Impact.html#estado-status)

### How to set up Github runbook pages in my local machine when github has a scheduled maintenance

- Clone the [{{repos-ibm-cloud-runbooks-name}}]({{repos-ibm-cloud-runbooks-link}}) repository.
  - \$ git clone https://github.ibm.com/cloud-sre/runbooks.git.
- If you don't have Ruby installed, install Ruby 2.1.0 or higher. We recommend using [RVM](https://rvm.io/).
- Install bundler.
  - \$ gem install bundler
- Install Jekyll and other dependencies from the GitHub Pages gem.
  - \$ bundle install
- Navigate to the root of the runbook repository.
- Run your Jekyll site locally.
  - \$ bundle exec jekyll serve
- Alternatively, if you have docker installed, from the root of the documentation repository, you can run the site by entering the following command:
  - docker run -v \$PWD:/srv/jekyll-p 4000:4000 -w /srv/jekylljekyll/jekylljekyllserve.
- The site can then be accessed at http://localhost:4000/ to run and visually test the pages.

### How to Soft Restart a VM

- **This action, does not work for Local environments**.
- In [{{doctor-portal-name}}]({{doctor-portal-link}}).
- Click on the hyperlink of the environment.
- Scroll down to the **Details** section.
- Click on **IaaS** tab.
- Search for the Domain Name **boshcli.[env].bluemix.net** e.g. _boshcli-1.dsvt0.us-ne.bluemix.net_
- In some environments, there is more than one VMs named **boshcli.\***.
  - You'd have to decide which one to work with it.
- Click on the three dots to the right, click on **Soft Restart Server**

![Soft Restart]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/SoftRestartServer.png){:width="640px"}

> **Note:** To restart a doctor VM search for the doctor IP addresses or search using `doctor` as keyword

### How to test and recover Doctor scorecard when page is blank

The log shows all API request through taishan_router/servicedb return 502.
Checks the logs from doctor_servicedb, if you see something like the follow:

```
2019/05/23 15:27:38 ^[[1;33m[W] Debug 1992897535618177560 router_request:HandleRequest() -- Router Get Response Timeout servicedb  ^[[0m
2019/05/23 15:27:38 ^[[1;33m[W] Delete cached endpoint, Bad endpoint: servicedb 9.32.164.226:4589 ^[[0m
2019/05/23 15:27:38 ^[[1;34m[I] Delete cached endpoint, Using endpoint for service  servicedb 9.32.164.226:4589 


2019/05/23 15:43:31 [E] Redis Dial Error: dial tcp 158.85.7.124:6479: getsockopt: connection timed out 
2019/05/23 15:43:31 [E] Service/Agent receiver subscribe error dial tcp 158.85.7.124:6479: getsockopt: connection timed out 
2019/05/23 15:43:31 [I] Is redis AUTH error false 
```

Means there is a network problem with one of the MBUS servers, then follow the next steps:

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **CI&CD** from the left side menu.
- Search for **doctor_servicedb**.
- For each VM listed

  1. Login to each doctor_servicedb VM.

     > if you can login with your SSO, use **Remote Command** instead.

  2. Open /opt/doctor-keeper/config/docker-compose.yml and find "doctor_servicedb" declaration

  ```
  doctor_servicedb:
  command: taishan_servicedb servicedb https://9.66.246.4:4568
  container_name: doctor_servicedb
  environment:
  - GROUP_KEY=377b924d4468ca49814ab141f314fa4c
  image: doctormbus3.bluemix.net:5000/taishan_v3/backend:5.20190505224709-scorecard
  logging:
    driver: json-file
    options:
      max-file: "10"
      max-size: 100m
  ```

  3. Update the IP in "command: taishan_servicedb servicedb https://9.66.246.5:4568",
     there are 2 IPs "9.66.246.4/doctormbus3" and "9.66.246.5/doctormbus4" that can switch and try
  4. curl -k https://localhost:5999/compose/up

- Check the logs again and make the connection is recovered
- Contact the network team and get assistance to recover the MBUS with a problem

### How to test and restart doctor-cli

If when trying to access **CLI** of an environment from the datacenter it does not return the login prompt or displays the follow error message:
_Can not connect to this server, please contact Doctor team!_
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/doctor-cli.png){:width="640px"}

- From [{{doctor-portal-name}}]({{doctor-portal-link}}).
- Select the environmet and click on the SSH icon.
- Use your SSO ID or firecall Id if you does not have access to the environment.
- Once logged into `sudo -i`
- Use this command `iptables -L` to check whether docker route info is missing.
  ![Missing Data]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/iptables_bad.png){:width="640px"}
- If data is missing restart docker by `service docker restart`.
- Wait about a minute or two and try **CLI** again
- If CLI is still not working contact doctor level 2 support.

> **Note:** Good return of `iptables -L` should look like the follow:
> ![Good Data]({{site.baseurl}}/docs/runbooks/doctor/images/web_ssh/iptables_good.png){:width="640px"}

### How to track down a {{doctor-alert-system-name}} incident generate in {{new-relic-portal-name}}

Track down incident creation: New Relic --> Kibana --> ServiceNow --> PagerDuty

- For a [{{new-relic-portal-name}} incident]({{new-relic-portal-link-alert|strip}}incidents/35272543/violations
  with {{new-relic-portal-name}}) account number nnnnnnn (1926897) and incident number iiiiiii (35272543)

- Log into [{{kibana-portal-name}}]({{kibana-portal-link}}) with IBM intranet w3 credentials.
- Click on **Add a filter** and create a filter using for alert_id with the {{new-relic-portal-name}} account number and incident number.
- Click on **Save**.
- Adjust the time range at the top right if needed.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/add_new_filter.png){:width="640px"}
- Click on the triangle on the left to see the details of the incident, or click the "INCnnnnn" link to go to ServiceNow.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/new_filter_result_set.png){:width="640px"}
- The ServiceNow incident URL can be seen after scrolling down.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/new_filter_full_results.png){:width="640px"}
- In ServiceNow, Look for the word "PagerDuty" to find the PD identifier
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/servicenow/activities.png){:width="640px"}
- In this case the [PD PWZEZPD will be](https://ibm.pagerduty.com/incidents/PWZEZPD)

### How to update environments current version

If the version of an environment is not shown at [{{doctor-portal-name}} Version Management]({{doctor-portal-link}}/#/versions), follow the next steps.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/governance/version_management.png){:width="640px"}

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **CI&CD** from the left side menu.
- Search for **doctor_backend**.
  Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
  if you cannot find the **doctor_backend** container.
- Search for then environment.
- Check if the doctor_backend version is not to old, if it is upgrade it to a newer version and skip the next step.
- Use the icon ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/refresh_btn.png){:width="20px"} to restart the service.
- Wait about 5 min to get the service fully back.
- Go to [{{doctor-portal-name}} Version Management]({{doctor-portal-link}}/#/versions).
- Select the environment and click on the **Refresh** button.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/governance/ver_management_refresh.png){:width="640px"}
- Once refresh completes the version should be displayed.

## List of Cybot commands

Background: Cybot went offline at the end of 2017, when it came back the help function was missing :(

Commands:

```
cybot [doctor] blink <environment name>
cybot [doctor] env/envs all
cybot [doctor] whereis|where is <environment name>
cybot [network] getsysinfo cpu|mem|all <IP Address>
cybot [network] iplookup <IP Address> [detail]
cybot [network] runcmd <IP Address> <command> ___ only ping,traceroute and mtr is supported
cybot [network] show account in <datacenter_name> [<pod_name>]
cybot [network] taglookup|tag lookup tag|ip|hostname <tag>|<IP>|<hostname>
cybot base64 encode|decode <query> - Base64 encode or decode <string>
cybot bbo app info [env] [org] [space] [app]
cybot bbo buildpack usage [env]
cybot bbo run command on [env] [ip] [command]
cybot bbo unresponsive vms [env]
cybot calendar - Display a calendar
cybot cie confirm <potential incident identifier> - resolves the Bluemix or CFS Potential CIE Incident and opens the Bluemix or CFS Confirmed CIE Incident
cybot cie list [CFS] [<number>d|w|m] - returns the list of Bluemix (or CFS) Potential and Confirmed CIE Incidents ongoing or resolved today (or resolved in the last <number> days|weeks|months)
cybot cie open [CFS] potential|confirmed public|staging|dedicated|local <environment_name> <summary> - opens Bluemix (or CFS) Potential or Confirmed CIE Incident
cybot cie resolve <incident identifier> - resolves Bluemix and CFS Potential and Confirmed CIE Incidents
cybot debug - write out the message object to the console where hubot is running
cybot estado <service> - get estado service status for all regions
cybot estado <service> <region> - get estado service status for specified region with more details
cybot grafana dashboard <component> <env> - Show ACE Mega dashboard, component are [bss, acems ,acecf], env are [env5, env5_lon, env5_syd]
cybot grafana vyatta traffic <ip_address> - show screen shot of traffic chart on grafana vyatta dashboard.
cybot help - Displays all of the help commands that Hubot knows about.
cybot help <query> - Displays all help commands that match <query>.
cybot pd incident <incident> - get the details of the incident.
cybot pd incidents - return the current incidents for the bluemix service
cybot pd me - get a list of all incidents owned by me.
cybot pd me ack! - acknowledge all incidents owned by me.
cybot pd me res! - resolve all incidents owned by me.
cybot pd note <incident> <content> - add a note to incident.
cybot pd notes <incident> - show notes for incident.
cybot pd res <incident1> <incident2> ... <incidentN> - resolve all specified incidents
cybot pd res <incident> - resolve incident.
cybot slack history <start_timestamp> <end_timestamp> - export all chat messages between the start and end time
cybot slticket help: show commands to CRUD softlayer tickets
cybot sop - returns help information for SOP commands
cybot ticket <ticket#>
cybot whos on call - return the 1st and 2nd responders of who's on call for each Bluemix service in pd
cybot whos on call <service> - return the 1st and 2nd responders of who's on call for a regex matching Bluemix service in pd
```

## Outages

- {{usam-short}} outages go to [{{onestatus-name}}]({{onestatus-link}}).

## Password expired

If a password has expired then you can reset the expiry date with:

```
chage -d `date +%Y-%m-%d` sshhub example TODAY=`date +%Y-%m-%d`; chage -d $TODAY <user>
```

Change the userid (in this case _sshhub_) as appropriate. You can run this command in remote command for a Doctor Agent. Note that this can be useful if the password is expired for sshhub which is used when running SSH from Wukong Doctor Keeper. For more information [How to solve an alert for root password expire on local env]({{site.baseurl}}/docs/runbooks/doctor/Runbook_st_passwd_expiration_root.html)

## SSH Scenarios

### If SSH does not open in a different tab.

Try to use a different browser, like Firefox.

### If SSH new tap opens, but your SSO user is not set up for the VM.

Use Remote Command from Wukong as an alternative.

- From [{{wukong-portal-name}}]({{wukong-portal-link}}).
- Select **Remote Command** from the left side menu.
- Search for the Environment.
  Using the text box, input a command.
- Click **Run**.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/remote_cmd_1.png)

### If you lost your verification code

Contact {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} to reset your boshcli 2FA

### If you are locked out from JumpBox

To clear the lock, send an email to {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} to reset the failure count.

### If the connection to a boshcli VM is too slow it can be an Active Directory (AD) problem

Plesaw contact {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%} to verify if there is an issue with AD.

### If datapower is unreachable

Check the affected VM `/etc/hosts` file and verify the datapower IP exist and it is pointing to the correct domain.
Reference: https://ibm-cloudplatform.slack.com/archives/C84FD5R0W/p1567107341011500

### Not able to SSH to inception VM from Wukong.

Sometimes we may not be able to login to the inception VM from wukong, before reporting a big issue or call emergency call, you can do further checking and see if we are able to reach it from different VMs (either another inception VM or boshcli).

1. SSH to another inception VM or BOSHCLI by using your SSO ID. Here you can either use WebSSH (from Wukong or Doctor portal), or W3 Jumpbox to login.
2. Get the IP of the target inception VM which is unreachable from wukong let's call it `<ip-of-unreachable-inception-vm>`
3. Ping the IP `<ip-of-unreachable-inception-vm>`, if there is response form the IP then we can try to ssh it.
4. SSH using command `ssh <your-sso-id>@<ip-of-unreachable-inception-vm>`
5. If you are able to login to the target inception VM now, try to restart the doctor-keeper process:
   `sudo supervisorctl restart doctor_keeper`

> **Note 1:** if you are not able to SSH using your SSO id, try to use function id. You may need to borrow it from someone from development team. <br> > **Note 2**: if the inception VM is not able to be reached from other VM, please ping GRE from slack to get further help. For example: is there any network issue, or try to reboot the inception VM etc.

For more information check [Missing route to mbus on inception VM]({{site.baseurl}}/docs/runbooks/doctor/Runbook_missing_route_to_mbus_on_inception_vm.html)

## Slack channels

| Channel                | Description                                                                                                                                                                                                                                             |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| #admin-requests        | Admin requests for the Cloud Platform Slack team                                                                                                                                                                                                        |
| #bluemix-local         | discuss bluemix local development                                                                                                                                                                                                                       |
| #bluemix-admin         | public channel for support cases and incident management with PaaS Admin Team                                                                                                                                                                           |
| #bluemix-xen7-migrate  | Discuss the move of Bluemix VMs to Xen7                                                                                                                                                                                                                 |
| #cto-oss-tip-internal  | For discussion between the internal OSS TIP team about design and development issues.                                                                                                                                                                   |
| #cto-sre-dashboard     | Questions related to the CTO STS Dashboard/Scorecard                                                                                                                                                                                                    |
| #cto-sre-product-ci    | Travis CI job status for CTO SRE Productization team                                                                                                                                                                                                    |
| #cto-sre-product-squad | Welcome to the Productization squad private channel! This is a great place to share information and ask questions.                                                                                                                                      |
| #dept_wh4a             | Items for discussion related to Department WH4A and intended for use in place of scheduled department meetings.                                                                                                                                         |
| #devit-usam            | USAM Admin teams discussion                                                                                                                                                                                                                             |
| #doctor-ic             | deprecated, replaced by #oss-doctor                                                                                                                                                                                                                     |
| #doctor-on-call-shift  | Slack channel dedicated for passing Bluemix Doctor on-call info/tips to the next shift. See also https://ibm.ent.box.com/folder/45327391663                                                                                                             |
| #doctor-setup-4-watson | Setting up Doctor fot Watson Environment - Test                                                                                                                                                                                                         |
| #eu-emerg-approvers    | channel with EU approvers for the purpose of collaborating on non-EU engineers requiring EU emergency access                                                                                                                                            |
| #local-builds-ic       | Deployment of Local Bluemix                                                                                                                                                                                                                             |
| #oss-doctor            | Doctor collaboration.                                                                                                                                                                                                                                   |
| #oss-kube-work         | This channel is for everything related to moving OSS Platform to Kubernetes. See wiki for more info: https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-on-Kubernetes                                                                              |
| #oss-tip-message-log   | Incidents from the TIP message flow                                                                                                                                                                                                                     |
| #sre-platform-onshift  | Bluemix private channel for the operations team, including primary and secondary members, geo leads, key participants from the network or management teams, etc. If specific issues need to be covered, don’t hesitate to fork out in another priv grp. |

## Bluemix Doctor Onboarding for Watson users

The [{{watson-env-onboarding-name}}]({{watson-env-onboarding-link}}) runbook is own by the Watson foundation services team and as doctor level two support you will need to request the access in this document.

- For section _1 Request Access to the Doctor Dashboard_ request root access instead of user access.
  - For instance instead to request `BMXDoctor-Operator-Watson-skprd-User` request `BMXDoctor-Operator-Watson-skprd-Root`
- For _AccessHub_ use the follow [document](https://pages.github.ibm.com/SOSTeam/SOS-Docs/idmgt/accesshub/Add-or-Remove-roles.html) along with the runbook above. If have questions about this runbook, please contact {% include contact.html slack=watson-foundation-slack name=watson-foundation-name userid=watson-foundation-userid notesid=watson-foundation-notesid %}

## Why's

### Why do I see C\_\* environments while other agents don't?

C*\* environment such as \_C_PROD-DAL09* are for CFS.
Environment type can be review from Wukong->Users->Environment Type
![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/env_types.jpeg){:width="640px" height="230px"}

If a user need access to CFS Environment types need to do the follow:

- 1 Apply for the follow {{usam-name}} access:
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/usam/BMXDoctor-operator-CFS.jpeg){:width="640px" height="230px"}
- 2 select the CFS\* environment type.
  - From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **Users**.
  - Search for a user and then click on **Edit**.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/search_user.png){:width="640px" height="230px"}
  - Select the Environment Type tab.
  - Select CFS types.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/Edit_EnvTypes.jpeg){:width="640px" height="230px"}

## Why remote command does not work for YP_FRANKFURT in Wukong

Use Wukong -> remote command on YP_FRNKFURT has potential security risk.The only way is to apply for EU exception request.Doctor agent runs on YP_FRNKFURT. It should be compliance policy. Check this [issue](https://github.ibm.com/cloud-sre/ToolsPlatform/issues/5145#event-55773647) for more information.

## Doctor schedulers

Currently you will see three schedulers from [{{wukong-portal-name}}]({{wukong-portal-link}}) CI & CD

- doctor_shared_scheduler
  - Use for doctor share services such as doctor_firecallmgr.
- doctor_schedulerhandler
  - Use [{{doctor-portal-name}}->Diagnose->Selfhealing]({{doctor-portal-link}}/#/selfhealing) for the Scheduled Jobs.
- bluecat-scheduler
  - Use [{{doctor-portal-name}}->Change->Bleucat]({{doctor-portal-link}}/#/bluecat) more info [here](https://doctor.cloud.ibm.com/partials/bluecat_docs/index.html).

## Another topic...

Add details for another topic here.

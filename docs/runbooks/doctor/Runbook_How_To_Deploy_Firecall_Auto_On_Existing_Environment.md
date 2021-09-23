---
layout: default
description: How to deploy firecall_auto on existing environment
title: How to deploy firecall_auto on existing environment
service: doctor
runbook-name: Runbook How To Deploy Firecall Auto On Existing Environment
tags: oss, bluemix, doctor, firecall
link: /doctor/Runbook_How_To_Deploy_Firecall_Auto_On_Existing_Environment.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}



## Steps to create firecall_auto id on new virtual machines
**TIP:** All the `curl` commands can be run on the terminal of your laptop.
### Requisite

#### 1. Request Access to API Platform.

* Log on [USAM](https://usam.svl.ibm.com:9443/AM/idman/MyUseridsCurrent).
* Verify if you already get access to this group `BMXDoctor-Operator-Apiplatform` under `USAM-PIM1-BMX` system.
* If yes, please go to next step.
* If no, you need to request this group on USAM.

  **system:** USAM-PIM1-BMX

  **groups:** BMXDoctor-Operator-Apiplatform

**TIP:** This request needs 3 level approvations, if it's on pending status for a long time, you can post a message to #oss-doctor slack channel to ask doctor team help to check.


#### 2. Install python on target IP.

 Python is needed on your virtual machine or bare metal, the version must be 2.6 or greater of 2.x, you can run following command to install python 2.7.

##### step 1 Install python

 ```
 apt-get install python2.7
 ```

##### step 2 Create soft link for python

 ```
 ln -s python2.7 /usr/bin/python
 ```

##### step 3 Verify python

 ```
 python -v
 ```

 If you can get version info about python, then you installed python successfully, you can execute `exit()` to exit from python command line and go to next step.

### Step 1 Get your API Key

  API key is used to call APIs, you can get your API key after you get this privilege `BMXDoctor-Operator-Apiplatform`. Please follow this guide to get your API key.

  [How to get your API key]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html)

### Step 2 Create the function id

#### 2.1 Run the following command

```shell
curl -k -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/function_id/create -d '{"executor":"xxx@cn.ibm.com", "ssouser":"workable user", "ssopassword":"workable password","ips":["xx.xx.xx.xx","xx.xx.xx.xx"]}' -H "Authorization:API Key" -H 'Content-type':'application/json' -H 'MODERATE-TENANT: YS0_DALLAS'
```

Where:

  * **executor**: your intranet id e.g. {{usam-id-example}}.
  * **ssouser** and **ssopassword**: provide a workable user and password (SSO or root).
  * **ips**: the IP list of new virtual machines.
  * **Authorization**: the [API key](#step-1-get-your-api-key)
  * **MODERATE-TENANT**: the environment name.

Function id is `doctor` or `taishan`, after this command is finished, you will receive 3 emails, and one of them indicates if function id is created successfully or not which subject is `Creation of doctor function id ...`, and from the subject of the email you can find what the function id is.

If function id was created successfully, email is like this:

![create function id successfully]({{site.baseurl}}/docs/runbooks/doctor/images/firecallauto-function-id-success.png){:width="640px"}

If function id was created failed, email is like this:

![create function id failed]({{site.baseurl}}/docs/runbooks/doctor/images/firecallauto-function-id-failed.png){:width="640px"}

#### 2.2 Verify the permission of function id
* Logon the vm or bare mental which you want to deploy firecall_auto to.
* Go to `/home` folder.
* Run `ls -al /home`
* Verify if function id folder is created. (From the email of last step, you can find the function id is `taishan` or `doctor`)
* Verify if the permissions of the function id folder is correct like this:

 ![function id]({{site.baseurl}}/docs/runbooks/doctor/images/firecallauto-function-id.png){:width="640px"}

* If not, run the following command:
```
chown -R doctor:doctor doctor
```
```
chown -R taishan:taishan taishan
```

### Step 3 Deploy cert

#### 3.1 Run the following command

```shell
curl -k -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/cert/check -d '{"email": "xx@cn.ibm.com", "ips": ["xx.xx.xx.xx","xx.xx.xx.xx"], "regenerateca": "true", "restartssh": "true"}' -H "Authorization:API Key" -H 'Content-type':'application/json' -H 'MODERATE-TENANT: YS0_DALLAS'
```

Where:

  * **email** with your intranet id e.g. {{usam-id-example}}.
  * **ips** with the ip list of new virtual machines.
  * **Authorization** with your [API key](#step-1-get-your-api-key).
  * **MODERATE-TENANT** with the environment name.
  
#### 3.2 Verify if cert is deployed successfully
* Logon the vm or bare mental which you want to deploy firecall_auto to.
* Go to `/etc/ssh` folder.
* Run `ls -al`
* Verify if cert files `ssh_host_rsa_key-cert.pub` and `ssh_user_ca.pub` are created.
* Verify if the file size are correct like this:

 ![function id]({{site.baseurl}}/docs/runbooks/doctor/images/firecallauto-deploy-cert.png){:width="640px"}


### Step 4 Add ips to cover list

```shell
 curl -k -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/checkout/enablement -d '{"environment":"YS0_DALLAS","ips":["xx.xx.xx.xx","xx.xx.xx.xx"]}' -H "Authorization:API Key" -H 'Content-type':'application/json'
 ```
Where:

  * **environment** with the environment name.
  * **ips** with the IP list of new virtual machines.
  * **Authorization** with your [API key](#step-1-get-your-api-key).

How to Verify:

You can verify the result from the response of this API, please check `detail` field of the result, if your IPs are in `success` field or your IPs in `failed` field but the message is `ip xx.xx.xx.xx had already added.` , it indicates this step is finished successfully.

e.g.

```
{"detail":{"success":{"xx.xx.xx.xx":"xx.xx.xx.xx"},"failed":{}},"result":"success"}
```


```
{"detail":{"success":{},"failed":{"xx.xx.xx.xx":"ip xx.xx.xx.xx had already added."}},"result":"success"}
```

### Step 5 Deploy firecall_auto
This step will checkout and checkin all the machines of the environment, so it may take more time, if there are more than one machine of one environment need firecall_auto, we suggest to finish above steps for all machines, then start this step.

#### 5.1 Check out firecall_auto

```shell
curl -k -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/ucd/pwd/checkout -d '{"type":"firecall_auto","requestor":"xx@cn.ibm.com","justification":"123456","pd_or_rtc":"rtc","environment":"YS0_DALLAS"}' -H "Authorization:API Key" -H 'Content-type':'application/json'
```

Where:

  * **requestor** with your intranet id e.g. {{usam-id-example}}.
  * **environment** with environment name.
  * **Authorization** with your [API key](#step-1-get-your-api-key).

How to Verify:

You can verify this step by the response of this API, if you can get password from `detail` field of the response, then it indicates this step is success.

e.g.


```
{"result":"success","detail":"xxxxxxxxxxxx"}
```

#### 5.2 Check in firecall_auto

```shell
curl -k -X POST {{doctor-rest-apis-link}}/doctorapi/api/doctor/ucd/pwd/checkin -d '{"type":"firecall_auto","requestor":"xx@cn.ibm.com","environment":"YS0_DALLAS"}' -H "Authorization:API Key" -H 'Content-type':'application/json'
```

Where:

  * **requestor** with your intranet id e.g. {{usam-id-example}}.
  * **environment** with environment name.
  * **Authorization** with your [API key](#step-1-get-your-api-key).

#### 5.3 Verify if checkin is finished
Checkin step may take more or less 2 hours, it depends on how many machines in this environment, please run the following command to check if checkin is finished.

```
curl -k -X GET {{doctor-rest-apis-link}}/doctorapi/api/doctor/ucd/pwd/checkstatus?environment=YS0_DALLAS\&id=firecall_auto -H 'Content-type':'application/json' -H "Authorization:API Key"
```

Where :

* **environment** with environment name.

You can verify the status of checkin. If `state` is `Check in` like following, it indicates checkin is triggered but not finished.
```
{"result":"success","detail":{"state":"Check in","requestor":"xx@cn.ibm.com","timestamp":1550571158,"ext":null}}
```

If `state` is `Available partially!` or `Available totally!`, it indicates checkin step is finished, please go to next step to verify firecall_auto.

```
{"result":"success","detail":{"requestor":"xx@cn.ibm.com","timestamp":1550702135,"state":"Available partially!","ext":{"failed_ips":["xx.xx.xx.xx","xx.xx.xx.xx"]}}}
```

If `state` is `Checkin failed`, there maybe something wrong with checkin step, please contract doctor team to check it.


#### 5.4 Verify firecall_auto

  * Logon the vm or bare mental which you want to deploy firecall_auto to.
  * Run this command `ls /home`, verify if firecall_auto folder exists.
  * If yes, firecall_auto has been deployed successfully.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

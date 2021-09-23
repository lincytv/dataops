---
layout: default
description: This Runbook is guidance of how to update Doctor when password of doctorbm@cn.ibm.com is changed.
title: Update Doctor when passworkd of doctorbm@cn.ibm.com is changed.
service: Doctor
runbook-name: doctorbm@cn.ibm.com password change
tags: oss, bluemix, doctor, doctorbm
link: /doctor/Runbook_Doctor_Update_of_Changing_doctorbm_Password.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

## Purpose

This action is required when doctorbm@cn.ibm.com password change

## Technical Details

doctorbm@cn.ibm.com ,function id used by Doctor  , should change it's password every 3 month. When the password is changed, we need to update Doctor configuration to make sure all services are using doctorbm@cn.ibm.com to get access still work

## User Impact
if password is expired or Docortor configuration is not update accordingly, some services cannot get access from 3rd party software and Doctor user cannot get service from Doctor

## Instructions to change Doctor password and Doctor configuration

1. Like normal IBM intranet ID, doctorbm@cn.ibm.com , need to change it's password every 90 days
2. There is a notification mail sent to doctorbm@cn.ibm.com before  7 days of  password expiry
3. Notify csschen@cn.ibm.com for Ruby code and bjdqian@cn.ibm.com for Go code to prepare for the password change
4. When they are ready, click the link in the mail to change the password
5. After the change is successful, let csschen@cn.ibm.com and bjdqian@cn.ibm.com knows
6. They will update the configuration file and restart corresponding services

### Here is the changes they made :
- Doctor Ruby 
 1. Change those config file on git@github.ibm.com:BlueMix-Fabric/doctor-configuration.git

```
config/taishan_dlt.yml
config/taishan_rtc.yml
config/taishan_servicedb.yml
config/taishan_ucd.yml
config/taishan_user_production.yml
config/taishan_pnp.yml
```

2. Restart doctor service
```
doctor_dlt   10.154.56.42,10.186.184.154
doctor_rtc   9.37.249.242
doctor_servicedb   9.32.164.22,9.37.249.242,9.32.164.226
doctor_ucd   9.37.249.242,9.32.164.226
doctor_user  9.37.249.243,9.32.164.226
doctor_pnp   9.37.249.243,9.32.164.226
```
- Doctor Go  
 1. change the two config files in: https://github.ibm.com/BlueMix-Fabric/doctor-go-select/tree/master/config
```
oss_certmanagement.yml
oss_usamutil.yml
```
 2. build a new doctor_go image from Wukong
 3. upgrade certmanagement and usamutil service from wukong, if the service can not be upgraded via wukong, ssh to the target machine, upgrade them manually


## Notes and Special Considerations

 {% include {{site.target}}/tips_and_techniques.html %}

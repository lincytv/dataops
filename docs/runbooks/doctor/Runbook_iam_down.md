---
layout: default
description: OSS IAM is down, user can not login doctor portal, wukong portal, grafana etc.
title: OSS IAM is down
service: doctor_iam, doctor_platformuser
runbook-name: Runbook oss iam is down
tags: oss, doctor, iam, platformuser
link: /doctor/Runbook_iam_down.html
type: Alert
---

{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose

Steps to recover OSS IAM when it is down


## User Impact

Unable to login doctor portal, Wukong portal, Grafana ...;

## Instructions to Fix

### Restart doctor_iam instances

  - Try to login Wukong staging, try any if the follow instances:  
    - [Doctor staging]({{doctor-portal-staging-link}})
    - [Doctor staging-ldap]({{doctor-portal-staging-ldap-link}})
    - [Wukong staging in UK south]({{wukong-portal-staging-UK-link}})
    - [Wukong staging in US south]({{wukong-portal-staging-US-south-link}})
    - [Wukong staging in US east]({{wukong-portal-staging-US-east-link}})
    
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/staging/Wukong staging.png){:width="640px"}
  
  - Goto **Remote Command**.
  - Input **DOCTOR_SSHHUB**.
  - Select **DOCTOR_SSHHUB	10.120.208.163**
  - Input this command `cat /etc/nginx/nginx.conf` then click Run button.
  - Search **upstream iam** from the output.
  - Get IAM instance IP from **upstream iam** part.
  
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/get_IAM_server.png){:width="640px"}
  
  - Search the IP address we get from last step, for example `10.154.56.42`.
  - Select this server on remote command page.
  - Input this command `docker restart doctor_iam` then click Run button.
  
  **If you failed to restart doctor_iam, you can start doctor_iam by following command:**
  ```
  docker run -i -t -p 9999:9999 --restart=always --net=host --name doctor_iam -v /opt/taishan_logs/iam:/opt/logs -e "PATH=/opt/ibm/wlp/bin:/opt/ibm/java/jre/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" -e "JAVA_VERSION=1.8.0_sr5fp15" -e "JAVA_HOME=/opt/ibm/java/jre" -e "LIBERTY_VERSION=18.0.0_01" -e "LOG_DIR=/logs" -e "WLP_OUTPUT_DIR=/opt/ibm/wlp/output" -d doctormbus3.bluemix.net:5000/taishan_v3/doctor_iam:5.20190523000000 server run defaultServer 
  ```

### How to check logs of doctor_iam

  - Logon the server which doctor_iam is running on, for example `10.154.56.42`.
  - Run `docker exec -it doctor_iam bash`.
  - Run `cd /logs/`.
  - Check `tokenservice.log`.
  
## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

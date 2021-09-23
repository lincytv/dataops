---
layout: default
description: User cannot use Access > App & User page on Doctor portal.
title: Function of Access > App & User page on Doctor portal not work.
service: cicd
runbook-name: Function of Access > App & User page on Doctor portal not work
tags: wukong, Wukong, doctor_cloud, doctor_backend
link: /doctor/Runbook_App_and_User_page_function_not_work.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose   
Fix issue that function of Access > App & User page on Doctor portal not work.

## Technical Details
If function of [Access > App & User page on Doctor]({{doctor-portal-link}}/#/app_user) portal not work, usually it was caused as there is something wrong with cloud service running on Doctor agent in container '**doctor_backend**'
> **Note:** In some environments it's in **doctor_cloud** container

## User Impact   
User cannot use function of Access > App & User page on Doctor portal   

## Instructions to Fix
1. Logon [{{wukong-portal-name}}]({{wukong-portal-link}}).   
2. Go to page **CI & CD**.
3. List all instance of **doctor_backend**.
Look [here]({{site.baseurl}}/docs/runbooks/doctor/Doctor_backend_container.html)
if you cannot find the **doctor_backend** container.
4. Find the environment where the issue is reported.
  - If you don't see the environment listed, try **doctor_cloud** instead of **doctor_backend** in step 3.
5. Check the checkbox of the environment.
6. Click on the icon under the *Actions* column of the environment select to restart it.
7. Wait about 2 minutes and continue with the next step.

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_backend_restart.png)

## How to check if data has been recovered
1. Logon [{{doctor-portal-name}}]({{doctor-portal-link}}/#/app_user).
2. Select the environment reported in the PD.
3. Select **User** from the down-drop list.
4. Use the user email who reported the incident or reported the problem from Slack.
5. Click on **Search**.
6. If data is displayed then, you can close the PD or report back to Slack.
7. Otherwise try restart **doctor_backend** again, if not data displayed contact level 2.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/access/app_and_user/app_user_displayed_data.png){:width="640px"}


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

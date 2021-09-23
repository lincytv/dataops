---
layout: default
description: Mute alerts when upgrading services guide
title: Mute Alerts Guide
service: backend
runbook-name: Mute Alerts Guide
tags: doctor,backend
link: /doctor/Runbook_Mute_Alerts_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

# Mute alerts when upgrading services guide


## 1. Mute all alerts

  *	Login in to [{{wukong-portal-name}}]({{wukong-portal-link}}).

  *	Select **Echometer** at the bottom of the left bar.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/menu_item.png){:width="60px"}

  * Click the **Mute All** button in the upper right corner of the page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/mute_all.png){:width="640px"}

  *	Enter the time in minutes that you want to mute the alerts. For example: _30_.

  *	Click the **Mute** button to create the mute rule.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/mute_all_duration.png){:width="640px"}


## 2. Mute alerts for specific environments/services

  *	Login in to [{{wukong-portal-name}}]({{wukong-portal-link}}).

  *	Select **Echometer** at the bottom of the left bar.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/menu_item.png){:width="80px"}

  * Find an environment/service in the Monitoring URL table, that you would like to mute all alerts. Using the **Filter Service/Env Name**  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/mute_by_env.png){:width="640px"}

  * Click the **Mute All** button in the upper right corner of the page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/mute_all.png){:width="640px"}

  *	Enter the time in minutes that you want to mute the alerts. For example: _30_.

  *	Click the **Mute** button to create the mute rule.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/mute_all_duration.png){:width="640px"}


## 3. Expire the mute

  *	Login in to [{{wukong-portal-name}}]({{wukong-portal-link}}).

  *	Select **Echometer** at the bottom of the left bar.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/menu_item.png){:width="80px"}

  *	Click the link **Alertmanager-link** beside the table _Other Services Configuration Files_.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/alertmanager_link.png){:width="640px"}

  * A new pop-up page will be displayed.

  * Click the **Silence** button at the top.

  * Filter out an alert/environment.

  * Click the **Expire** button for a mute/silence you want to drop.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/echometer/alertmanager_link_silence_expire.png){:width="640px"}

## Notes and Special Considerations
  {% include {{site.target}}/tips_and_techniques.html %}

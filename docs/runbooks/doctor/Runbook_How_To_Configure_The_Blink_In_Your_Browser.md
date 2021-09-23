---
layout: default
description: Configuring blink in your browser
title: How to Configure the Blink in Your Browser
service: doctor
runbook-name: Runbook how to configure the blink in your browser
tags: oss, bluemix, doctor, blink, browser
link: /doctor/Runbook_How_To_Configure_The_Blink_In_Your_Browser.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## 1. Add the blink in your firefox browser  
Add the blink proxy **{{doctor-blink-proxy-link|strip}}** and port **{{doctor-blink-proxy-port|strip}}**

  * 1.1 Select the preferences in the setting

  ![select the preferences in the setting]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/firefox_first.png)

  * 1.2 Setting the network in the advanced option  

  ![setting the network in the advance option]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/firefox_second.png){:width="600px"}

  * 1.3 Add the blink proxy in the connection setting  

  ![add the blink proxy in the connection setting]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/new_proxy.opscenter.bluemix.net.png){:width="600px"}

## 2. Add the blink in your chrome browser

  * 2.1 Click on the chrome menu in the browser toolbar  

  ![chrome menu]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/chrome-1.png)  

  * 2.2 Select Settings

  ![Select Setting]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/chrome-2.png)  

  * 2.3 Click Advanced

  ![Advanced]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/chrome-3.png)

  * 2.4 Under System, click Open Proxy Settings. This will open the Network Settings window.

  ![system]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/chrome-4.png)

  * 2.5 In the Proxies tab, under select a protocol to configure

  ![proxy setting]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/chrome-5.png){:width="600px"}

## 3. You also can use some proxy management software to manage the blink proxy.  

   Use your favorite browser proxy plugin, such as SwitchySharp.

   ![how to add the blink]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink.png){:width="600px"}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

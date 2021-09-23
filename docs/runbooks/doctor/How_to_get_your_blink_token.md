---
layout: default
description: Describes blink token set up and use.
title: How to get your Blink Token
service: admin
runbook-name: How to get your Blink Token
tags: root, password, failed
link: /doctor/How_to_get_your_blink_token.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}


## What is Blink?
Blink is a http proxy server.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/proxy_server.png){:width="640px"}


## What is Blink Token?
Blink Token is design for Blink proxy authentication. **Do not use blink token to login Doctor Portal**.

## Precondition
You are a user of Doctor and can log on to Doctor, and you are a user of Blink.

## How do I get my Blink Token?

  * Open [{{doctor-portal-name}}]({{doctor-portal-link}}) home page
  * Click your avatar.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/avatar.png){:width="200px"}
  * Click **Account** link.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/account.png){:width="200px"}
  * Find your **Blink Token** on **User profile** page.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/profile/info/get_blink_token.png){:width="640px"}

## How to use the token with curl command?

Just replace your w3 password with the token.
  * Create the follow variables:
    - myident
    - blinkToken
    - http_proxy
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/use_token_with_curl.png){:width="640px"}
  * Call a curl command:
    - `curl -X GET 'http://your_url_here'` e.g. `curl -X GET https://estado.skb-doj-dev01.bluemix.net/`

## How to use the token with Firefox browser?

  * [Configure your browser]({{site.baseurl}}/docs/runbooks/doctor/Runbook_How_To_Configure_The_Blink_In_Your_Browser.html)
  * Specify a URL target at the URL box
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/ulr_box.png){:width="640px"}
  * On the Authentication window, provide your W3Id and Blink Token as password.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/authentication_box.png){:width="640px"}

## How to use the token with browser plug-in?

[Foxyproxy](https://getfoxyproxy.org/) example:
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/FoxyProxy1.png){:width="640px"}
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/FoxyProxy1.png){:width="640px"}
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/FoxyProxy1.png){:width="640px"}


## How to verify ?

  * Please make sure that blink works fine with your W3Id/W3password.
  * Then make sure blink still works with your W3Id/BlinkToken.

## Will it expire ?
It will never expire.

## How to change it?
If your Blink Token is exposed, contact {% include contact.html slack=cloud-resource-api-slack name=cloud-resource-api-name userid=cloud-resource-api-userid notesid=cloud-resource-api-notesid%} and request to change it.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

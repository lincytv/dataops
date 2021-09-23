---
layout: default
description: Mail server connection refused
title: Mail Server Failure
service: doctor
runbook-name: Runbook mail server failure
tags: doctor
link: /doctor/Runbook_Mail_Server_Failure.html
type: Alert
---

{% include {{site.target}}/new_relic_tip.html%}
{% include {{site.target}}/load_oss_doctor_constants.md %}
__

## Purpose
Below are instructions to fix a _MAIL SERVER FAILURE: Mail server connection refused_ Pager Duty incident.

>**Note:** If you encounter a connection error in the instructions below, wait 10 - 20 minutes and try again.


## Instructions to Fix

1. Test the connection to the mail server, by trying to send a test message:

   1. Open a terminal on your local machine
   2. Type `telnet <MAIL_SERVER_FROM_PD_INCIDENT> 25` (for example: `telnet d23ml028.cn.ibm.com 25`)
   3. `helo a`
   4. `mail from: bm_ops_center@cn.ibm.com`
   5. `rcpt to: <YOUR_EMAIL_ADDRESS>` (for example: `rcpt to: shanec@ca.ibm.com`)
   6. `data`
   7. `Test email for PagerDuty incident.`
   8. `.`
   9. `quit`

    ![telnet test]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/mail_server_test.png){:width="700px"}

    ![email out]({{site.baseurl}}/docs/runbooks/doctor/images/telnet/mail_server_test_email_out.png){:width="700px"}

If you encounter a connection error in the instructions below, wait 10 - 20 minutes and try again.
If the test fails again after the second try the restart **doctor_mail** and try test again.
  - From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **CI&CD** from the left side menu.
  - Search for **doctor_mail**.
  - Restart the service using the icon under the _Action_ column.
  - Test again.

## Notes and Special Considerations

Check your email inbox to see if you receive the test email. May take up to ~5 minutes.
{% include {{site.target}}/tips_and_techniques.html %}

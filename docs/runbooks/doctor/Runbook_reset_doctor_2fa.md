---
layout: default
description: Instructions for Doctor users to reset their Doctor 2FA.
title: Reset Doctor 2FA
service: doctor
runbook-name: Reset Doctor 2FA
tags: oss, bluemix, doctor, ssh, logging, jumpbox, boshcli, 2FA
link: /doctor/Runbook_reset_doctor_2fa.html
type: Alert
---


{% include {{site.target}}/load_oss_doctor_constants.md %}


## Purpose

{% include_relative _ibm-includes/reset_2fa_email.html %}
__


## Technical Details

Reset 2FA for the user

## User Impact

If reset 2FA for the user failed, user can not login in Doctor page

## Instructions to Fix

A **reset doctor 2fa** Doctor alert will automatically be created for each reset request. Self healing will typically reset 2FA for the user automatically. You should receive a resolved notification in < ~1 minute.

### If automatic reset fails

  Reset 2FA manually

  1. Log in to [{{wukong-portal-name}}]({{wukong-portal-link}})
  2. Navigate to the **Users** tab.
  3. Search for the user by intranet id.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/search_user.png){:width="640px"}
  If you cannot find the user then you should click on the **Check USAM Requests** button to see if they have been approved
  in USAM and not yet added to the Doctor Access DB:
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/Approve_new_user.png){:height="280px"}
  <br>o If they are listed there, then select their entry and click **Save and Close**. Then, continue
  with the next step in this runbook.
  <br>o If they are not listed there, you can use email or Direct Message in Slack to ask them to apply for access
  as described [here]({{site.baseurl}}/docs/runbooks/doctor/Request_Doctor_Access.html). Then, stop following this 
  runbook until they have been approved in USAM.
  4. Once you have searched for the user ID and found it, click the **Edit** button.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/users/reset_2fa.png){:width="640px"}
  5. In the **2FA Issued** field, set value from **true** to **false**.
      > **Note:** If the value of the **2FA Issued** field is already set to **false**, simply resolve the incident.  The field was successfully set by automation and the incident was issued as a precaution.

  6. Click the **Save** button.
  > **Note:**  If the user does not have any _Role_, you might get an error after pressing the _Save_ button.<br>
  You will need to pick a Role for the user in order to _Save_. You might pick a less powerful _role_ , such as _read_only_ or _test_ ...

  7. If you had to set the field to **false**, send an email to the customer before you resolve the incident. Here are the details of the note to send:

      ```
      Subject:
      Your request: reset doctor 2fa

      Body:
      The doctor team has received a request to reset your 2fa (2-factor authentication) for Doctor.
      We have reset it.  Please capture the code the next time you logon to Doctor.  

      If you have any questions or problems, please reply to this email and CC Bluemix-Doctor-Dev.  

      Thank you.
      ```
  8. Once the user logs in again, they will receive a new QR code popup. After the user gets the new QR code, **2FA issued** in {{wukong-portal-name}} will automatically be changed to **true**.


## Notes and Special Considerations

  Here are some wiki pages which provide information for 2fa
  * [2FA Details](https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/2FA%20in%20Bluemix)
  * [2Fa FAQ](https://w3-connections.ibm.com/wikis/home?lang=en#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/2FA%20in%20Bluemix%20FAQ)

  * 2fa access to {{doctor-portal-name}} and {{ wukong-portal-name}} is the responsibility for the Doctor support team.

  * 2fa access to the Doctor Jump Box is handled by the security team. You can find members of this team at the [Doctor_Auth_Introduction page]({{site.baseurl}}/docs/runbooks/doctor/ibm-only/Doctor_Auth_Introduction.html#user-and-privilege-management) - search for `Bluemix security`.

  {% include {{site.target}}/tips_and_techniques.html %}

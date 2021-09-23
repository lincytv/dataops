---
layout: default
description: CIEBot User Authentication Guide
title: CIEBot User Authentication
service: ciebot
runbook-name: Runbook CIEBot Authentication Guide
tags: oss, edb, ciebot
link: /ciebot/Runbook_CIEBot_User_Authentication.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

Contact a developer ( {% include contact.html slack=oss-ciebot-slack name=oss-ciebot-name userid=oss-ciebot-userid notesid=oss-ciebot-notesid%} or {% include contact.html slack=oss-ciebot-2-slack name=oss-ciebot-2-name userid=oss-ciebot-2-userid notesid=oss-ciebot-2-notesid%} ) if you have any question.

## 1. Why Do I Need to Request for Access?

Due to a security requirement, Slack bots **ciebot** and **cietest** are upgraded in May 2020 to a new authentication model.

Prior to the upgrade, the bots interact with Service Now using a user-independent ID.
With the newly introduced authentication model, the bots interact with Service Now through API Platform on behalf of the bot user, using the user's slack identification.

Therefore, each bot user is required to 
- have access to Incidents in Service Now 
- join a specific user group to use API Platform

## 2. Check Service Now Access for Incidents

If you have been using Service Now for Incidents directly, you should already have access to Service Now. Proceed to the next step to request API Platform User Group.

If you have been working with Incidents exclusively using the pre-upgrade bots, you may or may not have access to Service Now Incidents.

Also please note that access rights to Production and Test Service Now are separate.

Environment           | Check Service Now Access | Request Service Now Access
--------------------- | ------------------------ | --------------------------
Production            | [check access](https://watson.service-now.com/ess_portal?id=ess_my_groups)     | [request access](https://watson.service-now.com/ess_portal?id=sc_cat_item&sys_id=9a1240ebdbcdef0472583c00ad9619ad)
Test                  | [check access](https://watsontest.service-now.com/ess_portal?id=ess_my_groups) | [request access](https://watsontest.service-now.com/ess_portal?id=sc_cat_item&sys_id=9a1240ebdbcdef0472583c00ad9619ad)

To check for access, click a link above.
In _My Groups --> Ticket_ tab, under _Can work/view_, if you have **Incident** in any of the _Group_ you have access to, then you have Service Now access for Incidents.

To make a request to access, click a link above.
For _Access Type_, consult with your manager to determine if a specific licensed group you should join. Otherwise, select _Licensed Access to Work Tickets_.

If you need to join a group, select _Join a Licensed Assignment Group_, a selection drop-down will be shown; select the group identified by your manager.

Keep your request ID. Your request will have to be approved by your manager. If there is no progress in your request status, contact your manager. _Please note: ciebot developers have no authority to speed up the approval process._

With access to Service Now Incidents, proceeds to the following step.

## 3. Submit an API Platform User Request

With access to Service Now incidents, all CIEBot users must also [apply](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/API-Platform-Usage) to join the API platform.

Each bot user needs to apply **separately** for production and staging Incident Management API usage.
Follow the steps in [How to Join in API Platform](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/API-Platform-Usage#how-to-join-in-api-platform):

Environment | Bot Name | URL for Request
----------- | -------- | -------------------------------------
Production  | ciebot   | [Production Environment Request Form](https://watson.service-now.com/ess_portal?id=sc_home)
Test        | cietest  | [Test Environment Request Form](https://watsontest.service-now.com/ess_portal?id=sc_home)

On the request page,
* Select the **Access** category on the left
* From the list of requests, select the **API Authorization Access Request** form.
* In **Business Justification**, you must include **[Your Service/team]**, **[Your role]** and **process CIEs using CIE bot**. (Even if you will use *ciebot* for *Bastion Connection* rather than *cie*, select **process CIEs using CIE bot** if there is no other more appropriate choice.)
* From the  _Groups_  drop-down in the request form, select **CIEbot Users**. (Before the _CIEBot User_ group was created, bot users were told to apply for _TIP Users_ group. A menbership in _TIP Users_ group still works for the purpose of using ciebot.)

If a user attempts to work with an incident before getting approval for the above request, a slack message will appear linking to the above page. 

**ATTENTION:** Your submitted request will not be processed until your functional manager has approved your request.  **Please notify your manager of your submitted request number and request they approve it ASAP.**  
If the approval of your request is delayed, please follow up with the next approver listed in Service Now. Note that bot developers do not have authority to speed up the approval for you.

**Managers** may view ServiceNow records pending their approval [here](https://ibm.biz/BdqPLs)

## 4. Confirmation

Two simple steps to confirm you are approved to use CIEBots:

1. Authenticate your Slack ID through IBM Cloud (**@[botname] [cie | incb]**)
2. Get info for a Service Now incident in a non-disruptive way: (**@[botname] [cie | incb] INC1234567**)
(Step 2 would behave the same as Step 1 if you have not done Step 1))

These steps are described below. **[botname]** is **ciebot** for production and **cietest** for staging.

### 4.1 Login Before Working with Incidents 
Upon entering the command **@[botname] [cie|incb]**, the bot checks if the user is logged in.

If the user has not logged in, or the previous login has experied, the the user would get a Slack messsage saying **Hello [your-id], please**  __authenticate as your-id@[country].ibm.com__  **then try the command again.**. 

Click on the hyperlink, your default browser will bring up a page to show the result of your logging in. 

### 4.1.1 If your login is successful
You will get 

"**Login Succeeded!** IBM Cloud authentication is complete!"

Just go back to issue the **@[botname] [cie]** command again, and continue with the actions.

### 4.1.2 If your login is unsuccessful

#### Different User ID 
"**Login Failed!** A different user ID was used during IBM Cloud authentication!"

There is a cookie in your default browser containing a user ID, which is not yours, for IBM Cloud authentication; and that ID was sent to IAM.
Due to security requirement, your email cannot be included in the URL sent to IAM.

Here are some ways to work around:
- Copy the authentication URL from Slack, and paste it to a different browser, which hopefully does not have a similar cookie.
- Delete cookies from your default browser.
- Copy the authentication URL from Slack, and paste it to an Incognito/Private browser. You'd have to go through the usual IAM 
authentication. If the "usual IAM authentication" fails, try once more in the same browser.

The authentication URL looks like this:
`https://xxxxx.cloud.ibm.com/oauth/api/v1/oauth/ibmcloud?auth_id=0000a000long000alphabetical000string1122233344455566677788899900`

On MAC, you can cursor over the link, press the Control key, click the link, you'd get a popup with the "Copy Link" action. 

On Windows, you can cursor over the link, right click to bring up a popup menu, which has the action "Copy Link Address".

#### Too many cookies 
"**400 Bad Request** Request Header or Cookies Too Large! nginx"

You have two options: clear cookies in your default browser, or copy the authentication URL to another browser as described above.

### 4.1.3 Expiration

Your login expires after a predetermined time (currently set to one hour).
The time span starts from your most recent login, not your last authenticated usage of the bot. 
So you may be asked to log in from time to time.

### 4.1.4 Across slack channels

You will need to login for each Slack channel separately.

### 4.1.5 More about oauth

For more information about the oauth service, see [OSS Auth API Runbook](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.oss-auth.html)

## 4.2 Verify Your Access to Service Now Incidents

You can verify your API Platform user group access by getting information for any incident (Section 4.2.1).
In addition, you can optionally try do something non-disruptive to an incident in a service you need to work with (Section 4.2.2).

### 4.2.1 Verify Your API Platform Access
When the bot receives a command **@[botname] cie CIEnnnnnnn** or **@[botname] incb CIEnnnnnnn**, the bot will make a call to Service Now.

For the purpose of verifying your API Platform access, you can use any incident number.

If you have access to Service Now Incidents, and you are approved for the CIEbot Users group, you will receive detailed information about the incident. All authenticated users have read access to all incidents.

If you do not have access to Service Now Incidents, follow Section 2 above to reqeust Service Now access for Incidents.

If you do not have approval for the CIEbot Users group, you will receive a message asking you to [Join API Platform](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/API-Platform-Usage#how-to-join-in-api-platform).

**Especially with production, do not create new cie or Bastion Connection** for the sake of testing the approval of your reqeust, since production bots create incidents in production Service Now, and will result in alerts sent to support teams.

### 4.2.2 Use Bot to Check API Platform Access
The **@[botname] chkauth** (used to be *cie auth*) command checks the API platform access for the bot user. The **@[botname] chkauth [email]** command checks the API platform access for another person with the given email.

For *cie* users:
If **@[botname] cie CIEnnnnnnn** works for you, you are all set, and don't need to run **@[botname] chkauth**.
If **@[botname] cie CIEnnnnnnn** doesn't work for you, **@[botname] chkauth** tells you one of two results:

- You have API Platform access. You should follow section 2 to get Service Now access to Incidents.
- You do not have API Platform access. You should follow section 3 to apply.

This command only **checks** for access rights (it does not login); after you get all necessary rights for a bot, you don't need to run it for the same bot in the future.

### 4.2.3 If you were a ciebot user before May 2020: Changes to Bot User Scope
If you have been a CIEBots user prior to the upgrade, you may notice that you can no longer create or modify some incidents, since you are now accessing Service Now with your own ID.

The new authentication model prevents a Slack user from creating and modifying an incident he/she isn't authorized to, and gives an erorr message like `ERROR: failed to create incident in ServiceNow.`.

If you must confirm you still have access to incidents of a certain service, you need to get an incident number for the service, and try to add a comment to it.

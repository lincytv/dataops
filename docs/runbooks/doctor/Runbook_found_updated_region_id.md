---
layout: default
description: When you see this alert, it means there is a Region ID mismatch in Doctor
title: Doctor Found Updated Region ID
service: doctor
runbook-name: Doctor Found Updated Region ID
tags: oss, bluemix, doctor, region_id
link: /doctor/Runbook_found_updated_region_id.html
type: Alert
---
{% include {{site.target}}/load_oss_doctor_constants.md%}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose

When you see this alert, it means the Region ID stored in Doctor does not match the latest Region ID provided by MCCP. It's possible that MCCP has changed the Region ID since Doctor's last update or the Region ID that is currently stored in Doctor is incorrect. Navigate to [{{doctor-portal-name}} -> Governance -> Provision Tool -> Account List]({{doctor-portal-link}}/#/provision_tool), and open account edit page to view the region ID.

![account list]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/provision_tool/account_list.png){:width="640px"}
![account details]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/provision_tool/account_dtls.png){:width="640px"}


## Technical Details

Get region ID by calling MCCP API.

## User Impact

The number of **DR** columns and details in [{{doctor-portal-name}}]({{doctor-portal-link}}/#/datacenter)  home page won't be shown if this alert gets triggered.

## Instructions to Fix

To fix this issue, follow these actions and check points.

> **Note**: MCCP may report the incorrect Region ID for the following two dev environments due to frequent redeploy testing. When the PagerDuty alert is raised for any of these two environments, check to see if the current Region ID setting in Doctor matches the following mapping. If yes, you can resolve the alert. If not, then go ahead with the following process to set it properly.
- **L_VMWARE-46-CHRISAHL -> vmware-46-chrisahl:prod:geo**
- **L_VMWARE-46-CHRISAHL2 -> vmware-46-chrisahl2:prod:eu-de**

### Update Region ID in Doctor

  * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
  * Select **Governance**.
  * Select **Provision Tool**.
  * From the drop-down list select **Account List**.
  * Select the **Type** from the drop-down list.
  * Search button to find the account.
    - e.g. _FOUND NEW REGION ID: region ID produban:prod:eu-de is available on environment D_PRODUBAN_ which will be indicated in the PagerDuty details, for this case _type_ is **dedicated** and _account_ **uban**
  * Click **Edit** button of the account.
    - To view the Region ID.
      - Click the **Get Lock** icon, next to **Eye** icon.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/provision_tool/account_list.png){:width="600px"}
      - Click on the **Pencil** icon to edit.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/provision_tool/edit_account.png){:width="600px"}
      - Click the **"Get"** button underneath Region ID field to pull the latest Region ID.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/provision_tool/get_region_id.png){:width="600px"}
      - if you get **unknown** as ID.
        * Click **Submit** at the bottom, and try again.
  * From MCCP, click the **"Submit"** button on the bottom right to save the new Region ID.

  > **Note 1:** Once you lock an account make sure to click on Submit, before you go to another option in Doctor or leave this page, otherwise the account will be lock for some minutes, eventually it will be unlocked, but you can save some time by submitting before leaving, the edit account page.

  > **Note 2:** The environment name in PD may not show up exactly on this page and you have to be creative - try clicking a few rows to see if you find the right one - the "Domain" field of the details screen should have the actual env name.


  ### Update Region ID in RTC Client Record

  * From [{{doctor-portal-name}}]({{doctor-portal-link}}).
  * Open the client record by clicking **Governance**.
  * Select **Client Record**.
  * Find an environment.
  * Click the icon in the **Client Record** column.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/client_record/account_lst.png){:width="640px"}
  * Log into RTC using your RTC user name.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/jazz/log_in.png){:width="640px" height="320px"}
    > Use `doctorbm@cn.ibm.com` if your RTC user name does not have access to the Bluemix Support Tracking RTC project.

    * Double check if the _Environment Name_ and _Environment ID_ fields match the new Region ID from MCCP.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/jazz/client_dtls.png){:width="640px"}
      - If not, please correct them in RTC client record.
      > If no Environment Name is listed in the dropdown selection menu, switch to the support team area.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

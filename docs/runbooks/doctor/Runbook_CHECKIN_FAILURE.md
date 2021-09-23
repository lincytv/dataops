---
layout: default
description: When this issue occurs, it means that some VM's firecall passwords were not checked in properly.
title: Doctor Firecall ID password check-in failure
service: admin
runbook-name: Doctor Firecall ID password check-in failure
tags: oss, bluemix, bbo, doctor, vm
link: /doctor/Runbook_CHECKIN_FAILURE.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose
This alert will be triggered if the firecall id password of some Bosh VM's passwords can't be checked in.

## Technical Details
The _Checked in_ action on target Bosh VM is done with the Doctor functional ID, so the reason for this alert could be one of:

1. Doctor functional ID does not exist on the failed VMs.
2. Doctor functional ID can't SSH to the failed VMs with SSH key.
3. Password of the Doctor functional ID in the failed VMs is not correct.
4. Functional ID was locked on the failed VMs.


## User Impact
User who checked out this firecall ID/password can't access the failed VMs reported in this alert.

## Instructions to Fix
{% if site.target == "ibm" %}
 {% include_relative _ibm-includes/xen7-migration.html %} __________________________
{% endif %}


**Please follow these steps:**

1. Currently the firecall ID checkout/checkin only covers Bosh VMs of Bluemix Fabric deployment. Therefore, when getting this incident, check the VM list in the incident body to see if there is a VM of Bluemix Fabric deployment. If not you can resolve this incident directly. If one exists, continue with the following steps. Regarding Bluemix Fabric deployment name, you can get it from the configuration file of each environment in [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}/tree/master/config), the value of field "cloud > bosh > deployments".
![details]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/config_yml.png)


2. Login to [{{site.data[site.target].oss-doctor.links.doctor-portal.name}}]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}).
3. Select the environment that the PagerDuty alert was generated for.
  >**Note:** If you can not tell what environment the PagerDuty alert was for in step 3 follow the next steps:

    - a. Copy the IP address from the PagerDuty alert.
    - b. Click **Home** in [{{doctor-portal-name}}]({{doctor-portal-link}}).
    - c. Expand **Quick Access**.
    - d. Paste in the IP address.
    - e. Click on **SSH**.
    - f. You should see the environment name in the console that opens.
    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/datacenter/quick_access.png)
4. Click on the hyperlink of the environment. This opens a new page.
5. For public, dedicated, and local environments:
   * Scroll down to find the **Details** section.
   * Click on the **Instances** tab in the **Details** section
   * Check whether at least one of the VMs listed in the PagerDuty incident has Status = **running** on the **Instances** tab:
     - If so, continue with this runbook.
     - If not, resolve the PagerDuty incident and do _NOT_ continue with this runbook.
![details]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/details.png)
6. Logon to [{{wukong-portal-name}}]({{wukong-portal-link}}).
7. Navigate to **Privilege ID Management**.
8. Select the environment in the drop list.
9. Click sync icon beside the user name that is mentioned in the PagerDuty alert.
![ssh icon]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/id_mgmt/sync_firecall.png){:width="600px"}
10. You will receive an email once the sync action is completed. It will contain the failed VM list which is still failed during sync action.
11. If you get an error message in step 9 or did not get an email in the next five minutes.
  - Navigate to **CI & CD**
  - Search for **doctor_security** on the **Continuous Deployment** field.
  - Look for the environment and restart the service by clicking on the icon.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/doctor_security_restart.png){:width="640px"}
  - Then try again from step 7.
    - If step 7 still fails, try to recreate **doctor_security**
      - Upgrade the version of doctor_security from CI & CD.
      - Follow the same steps on 11 but instead to restart. Check the latest version, from the version list on the upper right side.
      - Press the **Upgrade** button.
      ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/cicd/upgrade_doctor_security_version.png){:width="640px"}
      - Wait about 2-5 min and try step 7 again.
12. Resolve this alert.



>**Note**: Some local environments, don't have our system ID's, in that case, this function cannot be used. If you received this alert for such environments, just ignore it. {% if site.target == 'ibm' %}(it does not apply for the local environments RBCGCC and RBCSCC) {% endif %}

For any other issues, contact {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid %}.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

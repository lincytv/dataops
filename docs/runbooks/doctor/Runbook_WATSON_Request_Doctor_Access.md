---
layout: default
description: Instruction for requesting access to Doctor for Watson.
title: Watson Request Doctor Access
service: doctor
runbook-name: WATSON Request Doctor Access
tags: oss, vm, doctor
link: /doctor/Runbook_WATSON_Request_Doctor_Access.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}

Doctor access is managed by AccessHub. Below are the steps for requesting Doctor access.
For more information on Doctor use for Watson, please see the [IBM Cloud Doctor: Getting Started](https://github.ibm.com/watson-foundation-services/tracker/wiki/IBM-Cloud-Doctor:-Getting-Started) runbook.

- Request doctor group(add/modify/remove) on [{{access-hub-name}}]({{access-hub-link}}/), login with your W3ID.
- Click **Request or Manage Access** on the home page.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_request_access.png){:width="640px"}

- Under **ALL APPLICATIONS**, input **BMX-PIM1-Tools** in search box.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_input_application.png){:width="640px"}

- If you already get some access groups of this application, you just need to click **Modify Existing Access**, if not you need to click **Add To Cart**, then click **Checkout** button.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_checkout.png){:width="640px"}

- Filter the groups you want to request search for (`BMXDoctor-Operator-Watson`), click **Add** button next to the group , then click **Next** button.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_add_role.png){:width="640px"}

 * Find the group with the environment name, such as `BMXDoctor-Operator-Watson-<<env_name>>-User`
 * Find the correct role for the environment you need access too 

**NOTE:** There are two roles defined for each environment:
   * **xxxx_user:** Has the privileges for a normal operator
   * **xxxx_Root:** Have additional privileges to get root authentication

- Input business justification then click **Submit** button.

![]({{site.baseurl}}/docs/runbooks/doctor/images/accesshub_submit.png){:width="640px"}

- After your request is approved, you can find it on **View Existing Access** page.


## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}
---
layout: default
description: Configure Blink
title: Configure Blink
service: doctor
runbook-name: Runbook configure blink
tags: doctor
link: /doctor/Runbook_configure_blink.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

Estimation: 10 Minutes.

Below are the steps for managing Blink in [{{doctor-portal-name}}]({{doctor-portal-link}}).

  1. The Bluemix Doctor Blink page:
      * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
      * Select **Access**.
      * Select **Blink**, can be used to manage all Blink entries.

  2. For a new service, you can add a new column on the Blink page.
      * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
      * Select **Access**.
      * Select **Blink**.
      * Click on **Manage Services**.
      * Click on **Add Service**.  
      > **Note:** Use the **SETTING** button to determine which column you need to show.

       ![Doctor Blink Buttons]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/blink-buttons.png){:width="700px"}

  3. To add a new entry in Blink.
      * Go to [{{doctor-portal-name}}]({{doctor-portal-link}}).
      * Select **Access**.
      * Select **Blink**.
      * Click on **Manage Blink**.
      * Click on **Add Blink**.
      * You must choose the environment first.
      * Select a service name you want to classify.
      * Input the show name you want to display on the Blink page.
      * Input your URL.
      * Click **Add**
      > **Note:** Your URL should end with a Bluemix domain.

      ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/add_blink_entry.png)

  4. If your URL cannot be resolved by Cloud Platform DNS (e.g. just have IP address), you can assign a _fake_ hostname for your server on the Doctor Blink page.

      * Click the **Manage Blink** button.
      * Click **Add Blink**.
      * Find and click the **HOSTS** button.
      * Edit the content.
      * Assign a _fake_ hostname for your server.
      *  Click the **UPDATE** button to submit your change request.
      * Repeat step 3 to add your Blink entry.
      >**Note:** Your _fake_ hostname must end with a correct Bluemix Domain.

       ![Doctor Blink Hosts]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/Doctor-blink-hosts.png){:width="700px"}

  5. If there are two host contents in one environment, please update your change in both of them. That is for the Blink agent HA design.

     ![Doctor Blink Agent HA]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/Blink_agent_HA.png){:width="700px"}

  6. You can change and delete your Blink entries on the **Manage Blink** page.

     ![Doctor Blink edit]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/blink/Blink_edit.png){:width="700px"}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

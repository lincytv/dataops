---
layout: default
description: What actions to take when certificates are about to expire
title: Actions for Certificates are Expiring
service: doctor
runbook-name: Actions for Certificates are Expiring
tags: oss, doctor
link: /doctor/Runbook_certificates_expiring.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_api_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

# Actions to take when Certificates are Expiring

## Purpose
Certificates secure the public and intranet services in CTO.
Certificates expire after a certain amount of time - usually one, two, or three years.
When they expire, new certificates need to be issued.
Certificates can only be ordered and installed by a select few individuals

## User Impact
If certificates expire and they are not replaced by new certificates, services become unavailable.
For example, users are not able to log onto doctor, or failure in services may not result in a Pager Duty incident.

## Instructions to Fix

Certificates can only be ordered and installed by a select few individuals.
When you receive a PagerDuty incident for expiring certificates, please send an email containing the following details:

---

Subject: `Enter the subject of the PagerDuty incident`

---

Body:

   PagerDuty incident `provide the URL to the PagerDuty incident` indicates that the certificates are about to expire.
   Please order new certificates, register them with the Certifiate Manager, and deploy them for the servcies.

---

Send an email to the following individuals:

1. {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} , {% include contact.html slack=cloud-resource-bbo-slack name=cloud-resource-bbo-name userid=cloud-resource-bbo-userid notesid=cloud-resource-bbo-notesid %} and {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}
  >**NOTE** Contact in this section need to follow the runbook [How to request and deploy certificates to Nginx servers]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/How_to_deploy_certificates_to_Nginx_servers.html)

3. Depending on the service in the title of the PagerDuty incident, also send the email to the appropriate names from the following table. For example, if the title of the PagerDuty incident is "Certificates for Certificate Manager-**TIP** are about to expire", then select
the names for service **TIP**.



<table>
<tbody>
<tr><th>Service</th><th>Name</th></tr>
<tr><td>Doctor</td><td>  {% include contact.html slack=bosh-director-slack name=bosh-director-name userid=bosh-director-userid notesid=bosh-director-notesid %}  and  {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %}   </td></tr>
<tr><td>Marmot</td><td>ROBERTO RAGUSA/Italy/IBM  and Kris Kobylinski1/US/IBM</td></tr>
<tr><td>Operations Control Console (OCC)</td><td>Amit Joglekar/Lenexa/IBM  and  Satya s Kundeti/Lenexa/IBM</td></tr>
<tr><td>PnP</td><td> {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}  and  {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} </td></tr>
<tr><td>TIP</td><td> {% include contact.html slack=sosat-netcool-slack name=sosat-netcool-name userid=sosat-netcool-userid notesid=sosat-netcool-notesid %}  and  {% include contact.html slack=sosat-deploy-slack name=sosat-deploy-name userid=sosat-deploy-userid notesid=sosat-deploy-notesid %}  </td></tr>
<tr><td>TF</td><td>(no additional names)</td></tr>
</tbody>
</table>

   For example, for service **TIP** then send the email to{% include contact.html slack=sosat-netcool-slack name=sosat-netcool-name userid=tsosat-netcool-userid notesid=sosat-netcool-notesid %}  and  {% include contact.html slack=sosat-deploy-slack name=sosat-deploy-name userid=sosat-deploy-userid notesid=sosat-deploy-notesid %} as well.

>The contacts above may no be valid at the time you get this alert, please verify the names

Please **snooze** the PagerDuty incident until 10:00 AM on the next business day (Monday morning if the incident occurs on the weekend).

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

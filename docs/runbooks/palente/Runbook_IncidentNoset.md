---
layout: default
description: Describe the steps to follow when an Incident.audience set to 'not set' by PHE
title: PHE created a pCIE with a wrong audience
service: palente
runbook-name: pCIE created by PHE with the wrong audience
tags: oss, palente, phe, servicenow, newrelic
link: /palente/Runbook_IncidentNoset.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html %}


## Purpose
PHE created an incident (CIE) with wrong audience. PHE must create all incidents with audience set to 'not set'

## Technical Details
PHE uses heuristics techniques to detect a potential problem in a system that can became a Customer Impact Event (CIE), when PHE creates a CIE
the audience of the CIE must be set to 'not set', but if the audience is other than 'not set' it is a problem in the creation and the CIE may be exposed to a customer. If this happened [{{api-oss-csd-name}}]({{api-oss-csd-link}}) service must be set to Test mode immediately and notify the account manager and [Pa'lente team](#palente-contact-information) **as soon as possible**

## User Impact
User might be notified of a CIE that was not meant to happen. PHE must never create a CIE with audience different than 'not set'

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

If alert happened in `dev` or `staging` environment, just report to [Pa'lente team](#palente-contact-information), pCIE created in staging ServiceNow is not going out to customer.

If alert happened in `production`, find incident ID from alert and check in ServiceNow
```
https://watson.service-now.com/nav_to.do?uri=incident.do?sysparm_query=number=<incidentID>
```
Check the following fields to make sure it is created by PHE
1. Detection Source is `Monitoring Tool`
2. Monitoring Situation is `Created by PHE`
3. The very first work notes should contain
```
############################################
#
# Pa'lante Heuristic Engine worknote
#
############################################
```

If all above are true,
1. Inform AVM team right away Slack([{{slack-toc-avm-name}}]({{slack-toc-avm-link}}))
    - Mention: `PHE has created a CIE with the wrong audiende other than 'no set'`
    - Provide the incident ID,the Incident ID is part of the  [{{doctor-alert-system-name}}]({{doctor-alert-system-link}}) alert like the follow:
    - ![]({{site.baseurl}}/docs/runbooks/palente/images/pd/pd_cie_wrong_audience_details.png){:width="600px"}
    - Contact [Pa'lente team](#palente-contact-information)
2. Set PHE service to **Test mode**
  * Clone and open the following charts of the active account:
      >**NOTE:** At the time of written this runbook the active account is {{api-oss-csd-charts-nameOld}}

      - [{{api-oss-csd-charts-nameOld}}]({{api-oss-csd-charts-linkOld}})
      - [{{api-oss-csd-charts-nameNew}}]({{api-oss-csd-charts-linkNew}})

  * Set the value **Test Mode** to **true**
    - `TestMode: true`

  * Re-deploy charts
    - Login to the OSS Account if you are not already in.
      - If you don't know how to configure `kubectl` for each region, see [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)
    - Connect to each production environment (useast/ussouth/[eugb/eude])
    - Run kdep for each environment.
      - `kdep useast-production-values.yaml`
      - `kdep ussouth-production-values.yaml`
      - `kdep eugb-production-values.yaml` / `kdep eude-production-values.yaml`
      - Need help [How to redeploy]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-redeploy-palente-services)

3. Manually close the incident from New Relic.
    - Open the URL of the alert provided in [{{doctor-alert-system-name}}]({{doctor-alert-system-link}})
    - ![]({{site.baseurl}}/docs/runbooks/palente/images/pd/newrelic_alert_id.png){:width="600px"}
    - It will direct you to the NewRelic alert, from there, manually close the alert.
    - ![]({{site.baseurl}}/docs/runbooks/palente/images/newrelic/manually_close_alert.png){:width="600px"}



## Palente contact information

{% include {{site.target}}/palente_contact_info.md %}


## Notes and Special Considerations
Include the contacts for escalation when applicable.

{% include {{site.target}}/palente_tips.html %}

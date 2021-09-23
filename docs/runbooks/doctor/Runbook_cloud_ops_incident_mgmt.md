---
layout: default
description: Cloud Ops Incident Management
title: Cloud Ops Incident Management
service: doctor
runbook-name: Runbook cloud ops incident management
tags: oss, vm, doctor
link: /doctor/Runbook_cloud_ops_incident_mgmt.html
type: Informational
---

## Incident Object
Create an Incident Object to abstract incidents in a different system: PagerDuty, SL ticket, ServiceNow.

## Incident status timeline view
One view to show an incident lifecycle status history.

## Scenario
1. Incident creation
2. Handling Incident (Incident_transition, Incident handling history)
3. Incident resolved
4. Customer Notification (lower priority and external dependency)

### Incident creation
* Create CIE: manually and automatically on Pagerduty, Doctor, Slack bot
* When CIE is created, automatically create a slack group for this CIE and pull on-call people in the group to start discussion
* Create Incident status timeline view on doctor
* Create Bailey or ServiceNow RCA record

### Handling Incident
Make a page for history and evidence of the incident transition along different SRE/RE within one Tribe (different on-shift schedule) or different Tribes
1. Incident_transition: assign to different owner
2. Incident handling timeline
3. Environment current status

#### Incident_transition
* Support reassign incident to within an incident management or outside different incident systems: Pagerduty, SL ticket, ServiceNow etc.
* Account time spent for each owner: current owner duration/total duration

#### Incident handling timeline record
* Automatically record slack messages to timeline, Bailey or ServiceNow
* Provide rich tool support so the SRE can take action to fix the problem: ssh, script, bbo, api etc.
* Manually/Automatically record the SRE action taken on the environment (through doctor)
* Support the post message and the SRE action and record to slack, Bailey or ServiceNow

#### Environment current status
There are two options to show the live status of the incident on its environment:  
1. Link to gravity wave
2. Provide critical status

### Incident Resolved
* Resolve CIE on Pagerduty, Doctor, Slack bot
* When CIE is resolved, open a slack group for this CIE and pull on-call people in the group to start discussion
* Initial Follow up action for RCA - need to discuss with ERM/AVM

## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

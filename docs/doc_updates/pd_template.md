---
layout: default
title: PD Alert Template
---

This is a sample template for what a PD alert should look like. 

# PD Description
  The description of the PD should be all inclusive it should have the following where available
  * environment
  * cloud
  * service name
  * component

### example
  * *Description*: $environment-$cloud/$service/$component : error message

# PD Details
 
Some of the fields listed are extremely important and some less so, but all points are intended to help conductors reach a resolution within the 23 minutes SLA and to avoid paging out dedicated service squads

### Required
  * a direct link to the runbook. this is crucial. it saves time for the conductor in identifying the correct runbook. 
  * name of the component of the service that is borked - in the 23 minutes available for our SLA it is unrealistic to expect conductors to identify an issue AND resolve it 
  * PD escalation policy for this component of the service
  * consider prioritising the PD urgency - a PD "service" for high urgency and a PD "service" for low urgency - note this means the service squad will require TWO services to be set up in the PD, one for each urgency

### Nice to have
  * a link to the incident log if necessary, kibana etc
  * the sensu test - if provided, conductors can rerun the test use the results to with the PD alert and if no longer valid can manually resolve the PD

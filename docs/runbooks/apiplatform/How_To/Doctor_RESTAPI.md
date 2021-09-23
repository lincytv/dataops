---
layout: default
title: Bluemix Doctor Public REST API
type: Informational
runbook-name: "Doctor_RESTAPI"
description: How to work with the Doctor REST API.
service: tip-api-platform
tags: doctor,restapi
link: /apiplatform/How_To/Doctor_RESTAPI.html
---

{% capture sosat-availability-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.slack }}{% endcapture %}
{% capture sosat-availability-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.name }}{% endcapture %}
{% capture sosat-availability-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.userid }}{% endcapture %}
{% capture sosat-availability-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.notesid }}{% endcapture %}

{% capture sosat-netcool-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.slack }}{% endcapture %}
{% capture sosat-netcool-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.name }}{% endcapture %}
{% capture sosat-netcool-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.userid }}{% endcapture %}
{% capture sosat-netcool-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.notesid }}{% endcapture %}


## Purpose

Basic description of the Bluemix Doctor Public REST API.

## Technical Details

Bluemix Doctor exposes most services for external use. All Doctor REST APIs can be accessed from the following endpoint:  
[{{site.data[site.target].oss-doctor.links.doctor-rest-apis.link}}]({{site.data[site.target].oss-doctor.links.doctor-rest-apis.link}})

### Links to Documentation

[Bluemix Doctor Public REST APIs]({{site.data[site.target].oss-doctor.links.doctor-portal.link}}/partials/api_doc_v3/index.html)

### Credentials

Username: doctor  
Password: [doctor.pw]({{site.data[site.target].ghe.repos.sosat-gh-secrets.link}}/blob/master/doctor/REST_API/doctor.pw)

### Sample curl

Replace doctor.pw with the password here: [doctor.pw]({{site.data[site.target].ghe.repos.sosat-gh-secrets.link}}/blob/master/doctor/REST_API/doctor.pw)

`curl -u doctor:doctor.pw http://dl9-pl-evtnco03:8080/objectserver/restapi/alerts/status?filter=Severity%3D5`  


## Notes and Special Considerations

## Contacts

**PagerDuty**
* Production [{{site.data[site.target].oss-sosat.links.sosat-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-critical-alerts.link}})
* Dev or Test [{{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.name}}]({{site.data[site.target].oss-sosat.links.sosat-non-critical-alerts.link}})

**Slack**
* [{{site.data[site.target].oss-slack.channels.sosat-monitor-prod.name}}]({{site.data[site.target].oss-slack.channels.sosat-monitor-prod.link}})

**Runbook Owners**
* {% include contact.html slack=sosat-netcool-slack name=sosat-netcool-name userid=sosat-netcool-userid notesid=sosat-netcool-notesid %}
* {% include contact.html slack=sosat-availability-slack name=sosat-availability-name userid=sosat-availability-userid notesid=sosat-availability-notesid %}

---
layout: default
title: "API Platform - PnP Notifications Adapter"
type: Alert
runbook-name: "api.pnp-notifications-adapter.down"
description: "Top level runbook to drill into problems related to the notifications adapter which is responsible for pulling Announcement and Security Notice notifications."
service: tip-api-platform
tags: pnp, apis, notifications
link: /apiplatform/api.pnp-notifications-adapter.down.html   
---

## Purpose

This runbook contains pointers to runbooks pertaining to the PnP Notifications Adapter.  Below you will find ServiceNow short descriptions and New Relic incident titles and then a pointer to the appropriate runbook.  Therefore, when you are working on an incident, look at the title, then looking below to see which runbook you should look at based on the title.

## Technical Details

The notifications adapter is used to pull Announcements and Security Notice type notifications.  Some components of the notifications adapter are known to be reused by other microservices in PnP.

## User Impact

Generally the user impact of this adapter being down is users will not receive new or updated Announcements or Security Notices.  In general, this is not considered a highly critical condition since these alerts do not contribute to the status of a resource.

## Instructions to Fix

### Notification Adapter Postgres Errors

Runbook: [Postgres down for Notifications](api.pnp-notifications-adapter-postgres.down.html)

This runbook applies to:
- ServiceNow incidents with titles: 
  - `api-pnp-notifications-adapter failed in Postgres database query`
  - `api-pnp-notifications-adapter failed in parsing records from Postgres`
- New Relic incidents with the title containing text: 
  - `api-pnp-notif-adapter_postgresDBFail`
  - `api-pnp-notif-adapter_parsePostgresFail`

### Notification Adapter OSS Catalog Errors

Runbook: [OSS Catalog down for Notifications](api.pnp-notifications-adapter-osscatalog.down.html)

This runbook applies to:
- ServiceNow incidents with a title: 
  - `api-pnp-notifications-adapter failed in OSS Catalog database query`
  - `api-pnp-notifications-adapter failed in parsing records from OSS Catalog`
- New Relic incidents with the title containing text: 
  - `api-pnp-notif-adapter_ossCatalogDBFail` 
  - `api-pnp-notif-adapter_parseOSSCatFail`

### Notification Adapter Message Queue Errors

Runbook: [MQ down for Notifications](api.pnp-notifications-adapter-mq.down.html)

This runbook applies to:
- ServiceNow incidents with a title: 
  - `api-pnp-notifications-adapter failed in posting MQ`
- New Relic incidents with the title containing text: 
  - `api-pnp-notif-adapter_MQPostFail`


### Notification Adapter Global Catalog Errors

Runbook: [Global Catalog down for Notifications](api.pnp-notifications-adapter-globalcatalog.down.html)

This runbook applies to:
- ServiceNow incidents with a title: 
  - `api-pnp-notifications-adapter failed in Global Catalog database query`
  - `api-pnp-notifications-adapter failed in parsing records from Global Catalog`
- New Relic incidents with the title containing text: 
  - `api-pnp-notif-adapter_globalCatalogDBFail`
  - `api-pnp-notif-adapter_parseGlobalCatFail`


### Notification Adapter Cloudant Errors

Runbook: [Cloudant down for notifications](api.pnp-notifications-adapter-cloudant.down.html)

This runbook applies to:
- Service now incidents with a title: 
  - `api-pnp-notifications-adapter failed in Cloudant database query` 
  - `api-pnp-notifications-adapter failed in parsing records from Cloudant`
- New Relic incidents with the title containing text: i
  - `api-pnp-notif-adapter_cloudantDBFail`
  - `api-pnp-notif-adapter_parseCloudantFail`

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

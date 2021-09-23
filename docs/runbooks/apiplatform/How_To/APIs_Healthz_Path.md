---
layout: default
title: URL's of all healthz paths for each API
type: Informational
runbook-name: "APIs_Healthz_Path"
description: URL's of all healthz paths for each API
service: tip-api-platform
tags: apis, healthz
link: /apiplatform/How_To/APIs_Healthz_Path.html
---


## Purpose

List of all healthz paths for all APIs in the API Platform, including different environments.

## Catalog API
- Production  
`curl {{site.data[site.target].oss-apiplatform.links.catalog-api-prod.link}}`
- Staging  
`curl {{site.data[site.target].oss-apiplatform.links.catalog-api-stage.link}}`
- Development  
`curl {{site.data[site.target].oss-apiplatform.links.catalog-api-dev.link}}`

## Key Service API
- Production  
`curl {{site.data[site.target].oss-apiplatform.links.key-service-prod.link}}`
- Staging  
`curl {{site.data[site.target].oss-apiplatform.links.key-service-stage.link}}`
- Development  
`curl {{site.data[site.target].oss-apiplatform.links.key-service-dev.link}}`

## Incident Management API
- Production  
`curl {{site.data[site.target].oss-apiplatform.links.incidentmgmtapi-api-prod.link}}`
- Staging  
`curl {{site.data[site.target].oss-apiplatform.links.incidentmgmtapi-api-stage.link}}`
- Development  
`curl {{site.data[site.target].oss-apiplatform.links.incidentmgmtapi-api-dev.link}}`

## Subscription API
- Production  
`curl {{site.data[site.target].oss-apiplatform.links.subscription-api-prod.link}}`
- Staging  
`curl {{site.data[site.target].oss-apiplatform.links.subscription-api-stage.link}}`
- Development  
`curl {{site.data[site.target].oss-apiplatform.links.subscription-api-dev.link}}`

## Doctor API
- Production  
`curl {{site.data[site.target].oss-apiplatform.links.doctor-api-prod.link}}`
- Staging  
`curl {{site.data[site.target].oss-apiplatform.links.doctor-api-stage.link}}`
- Development  
`curl {{site.data[site.target].oss-apiplatform.links.doctor-api-dev.link}}`

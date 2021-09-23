---
layout: default
title: ServiceNow URLs for each environment
type: Informational
runbook-name: "ServiceNow-URLs"
description: ServiceNow URLs for each environment
service: tip-api-platform
tags: apis, pnp, ServiceNow
link: /apiplatform/How_To/ServiceNow-URLs.html
---

## Purpose

List all ServiceNow URLs for each environment. There are 3 different URLs for different environments(Production/Staging/Dev)

### Credentials

The ServiceNow credentials for each environment can be found [here]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html).

## ServiceNow Production
   - change_request table:
     [{{site.data[site.target].oss-apiplatform.links.service-now-cr.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cr.link}})

   - cmdb_ci table
      [{{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci.link}})

   - u_environment table
       [{{site.data[site.target].oss-apiplatform.links.service-now-env.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-env.link}})



## ServiceNow Staging
   - change_request table:
      [{{site.data[site.target].oss-apiplatform.links.service-now-cr-stage.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cr-stage.link}})

   - cmdb_ci table
      [{{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci-stage.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci-stage.link}})

   - u_environment table
       [{{site.data[site.target].oss-apiplatform.links.service-now-env-stage.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-env-stage.link}})


## ServiceNow Dev

   - change_request table:
      [{{site.data[site.target].oss-apiplatform.links.service-now-cr-dev.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cr-dev.link}})

   - cmdb_ci table
      [{{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci-dev.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-cmdb_ci-dev.link}})

   - u_environment table
       [{{site.data[site.target].oss-apiplatform.links.service-now-env-dev.link}}]({{site.data[site.target].oss-apiplatform.links.service-now-env-dev.link}})



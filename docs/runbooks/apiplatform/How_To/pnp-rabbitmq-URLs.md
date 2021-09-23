---
layout: default
title: RETIRED - PnP RabbitMQ URLs for each region and environment
type: Informational
runbook-name: "pnp-rabbitmq-URLs"
description: PnP RabbitMQ URLs for each region and environment
service: tip-api-platform
tags: apis, pnp, rabbitmq
link: /apiplatform/How_To/pnp-rabbitmq-URLs.html
---


{% capture str-note %}When calling the below URL's use the login credentials from the [Credentials]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html) section{% endcapture %}

## Purpose

List all PnP RabbitMQ URLs for each region and environment. Note that both URL1 and URL2 point to the same RabbitMQ server. The idea of having 2 URLs is that if one of them is not working, and considering RabbitMQ server is working, then there is a backup URL that can be used.  

### Credentials

<div class="alert alert-warning">

The RabbitMQ credentials for each region can be found <a href="{{site.baseurl}}/docs/runbooks/apiplatform/ibm/API_PnP_credentials.html">here</a>.

</div>



## RabbitMQ Production
>Note: {{str-note}}

- us-east  

URL1: [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-east-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-east-1.link}})  
URL2: [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-east-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-east-2.link}})

- us-south  

URL1: [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-south-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-south-1.link}})  
URL2: [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-south-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-us-south-2.link}})

- eu-de

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-eu-de-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-eu-de-1.link}})   
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-eu-de-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-prod-eu-de-2.link}})   

## RabbitMQ Staging
>Note: {{str-note}}

- us-east  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-east-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-east-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-east-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-east-2.link}})

- us-south  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-south-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-south-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-south-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-us-south-2.link}})

- eu-de  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-eu-de-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-eu-de-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-eu-de-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-stage-eu-de-2.link}})

## RabbitMQ Dev
>Note: {{str-note}}

- us-east  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-east-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-east-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-east-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-east-2.link}})

- us-south  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-south-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-south-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-south-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-us-south-2.link}})

- eu-de  

URL1:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-eu-de-1.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-eu-de-1.link}})  
URL2:  [{{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-eu-de-2.link}}]({{site.data[site.target].oss-apiplatform.links.rabbitmq-dev-eu-de-2.link}})

---
layout: default
description: How to Add a New API to API Platform
title: Add New API to API Platform
service: tip-api-platform
runbook-name: "Add_New_API_to_APIPlatform"
tags: add, api, new, apiplatform, nginx, istio
link: /apiplatform/How_To/Add_New_API_to_APIPlatform.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}


## Overview

The API specifications are configured using istio, we have CI/CD set up for this so any changes should be done by updating the [api-istio charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}/tree/staging/api-istio).

All the configs are on these yaml files. The regional files (e.g. eugb-staging-values.yaml) hold the config for that region&env.  

The `development-values.yaml`, `staging-values.yaml` and `production-values.yaml` files are not used for istio configuration.  

The `values.yaml` file holds the config that is used in all regions&envs, meaning if a change is made there then it affects all regions&envs.  

There are 5 types of configs: DestinationRule, Gateway, PeerAuthentication, ServiceEntry, VirtualService.  
Each of them with different purpose, for detailed information see the [istio website](https://istio.io/latest/docs/reference/config/networking/).  

This document only pertains with updating configuration for kind VirtualService.

## Prerequisites

1. Get {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} approval on the new API's Swagger specifications.  
2. (Optional) Work with {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} to add any IAM authorization policies.  
3. (Optional) Deploy the application(s) to the development, staging, and/or production Kubernetes clusters.


## Procedure

Choose which option is for you: *(a)* or *(b)*

### (a) If the purpose is to add a new API route in all regions and environments(dev/test/prod)

1. Clone the [oss-charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}) repo, and create a new branch
2. In `api-istio` folder, open `values.yaml` file, locate `virtualServicesRoutesEqualAllEnvsRegions`  
3. Under this list you will find `routes`  
4. You will see all route configs, go to the bottom of the routes to add a new one
5. Copy an existing route, such as:
    ```yaml
         - match:
           - uri:
               prefix: /bastion
           route:
           - destination:
               host: api-bastion-api.api.svc.cluster.local
               port:
                 number: 80
    ```
This config means any request path that starts with "/bastion" is routed to service "api-bastion-api", in namespace "api", in the local cluster on port 80.  
So for this to work it must have a service running with these exact details, or else a 404 is returned.  
**Ensure the correct indentation is used**  
6. Replace the values as needed, also see other examples for additional configuration options.
All config options can be found on the [istio website](https://istio.io/latest/docs/reference/config/networking/virtual-service/).  
7. Add {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} as a reviewer to your PR.  
8. After the PR is merged, the istio changes will be deployed to development, staging, and eventually production by the CI/CD process.

### (b) If the purpose is to add a new route only in specific regions and environments

1. Clone the [oss-charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}) repo, and create a new branch.
2. In `api-istio` folder, find the regional files that you want your route to exist and open them.  
For example if you want the new route only in `us-east`, `dev` or `staging`, the files are `useast-development-values.yaml` and `useast-staging-values.yaml`.
3. Locate `virtualServiceEntries` for each of the files
4. Under this list you might find `routes`, but it could not exist
In case it is not there, you need to add it.  
See [this example]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}/blob/staging/api-istio/useast-staging-values.yaml#L31-L50) as base.
5. Copy an existing route, souch as:
    ```yaml
         - match:
           - uri:
               prefix: /bastion
           route:
           - destination:
               host: api-bastion-api.api.svc.cluster.local
               port:
                 number: 80
    ```
This config means any request path that starts with "/bastion" is routed to service "api-bastion-api", in namespace "api", in the local cluster on port 80.  
So for this to work it must have a service running with these exact details, or else a 404 is returned.  
**Ensure the correct indentation is used**
6. Replace the values as needed, also see other examples for additional configuration options.
All config options can be found on the [istio website](https://istio.io/latest/docs/reference/config/networking/virtual-service/).  
7. Create a PR and add {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} as a reviewer to your PR
8. After the PR is merged, the istio changes will be deployed to development, staging, and eventually production by the CI/CD process.


## Runbook Owners

- {% include contact.html slack=sosat-tools-slack name=sosat-tools-name userid=sosat-tools-userid notesid=sosat-tools-notesid %}

---
layout: default
description: How to Add a New Service Entry to API Platform
title: Add New Service Entry to API Platform
service: tip-api-platform
runbook-name: "Add_New_Service_Entry_to_APIPlatform"
tags: add, api, new, apiplatform, nginx, istio
link: /apiplatform/How_To/Add_New_Service_Entry_to_APIPlatform.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}


## Overview

The service entries are used to create access rule to external services, similar to firewall rules.  

The API specifications are configured using istio, we have CI/CD set up for this so any changes should be done by updating the [api-istio charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}/tree/staging/api-istio).

All the configs are in these yaml files. The regional files (e.g. eude-staging-values.yaml) hold the config for that region&env.  

The `development-values.yaml`, `staging-values.yaml` and `production-values.yaml` files are not used for istio configuration.  

The `values.yaml` file holds the config that is used in all regions&envs, meaning if a change is made there then it affects all regions&envs.  

There are 5 types of configs: DestinationRule, Gateway, PeerAuthentication, ServiceEntry, VirtualService. Each of them has a different purpose, for detailed information see the [istio website](https://istio.io/latest/docs/reference/config/networking/).  

This document only pertains with updating configuration for kind ServiceEntry.

## Prerequisites

1. Get {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} approval on the new API's Swagger specifications.  
2. (Optional) Work with {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} to add any IAM authorization policies.  
3. (Optional) Deploy the application(s) to the development, staging, and/or production Kubernetes clusters.


## Procedure

Choose which option is for you: (_a_) or (_b_)

### (a) If the purpose is to add a new service entry in all regions and environments(dev/test/prod)

1. Clone the [oss-charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}) repo, and create a new branch
2. In `api-istio` folder, open `values.yaml` file, locate `serviceEntriesEqualAllEnvsRegions`  
3. Under this list you will find service entries
4. You will see all service entries configs, go to the bottom to add a new one
5. Copy an existing service entry, such as:
    ```yaml
         - metadata:
             name: vault-service-api
           spec:
             hosts:
             - "vserv-us.sos.ibm.com"
             location: MESH_EXTERNAL
             ports:
             - number: 8200
               name: vault-us-api
               protocol: TLS
    ```
This service entry means that "vserv-us.sos.ibm.com" on port 8200 using TLS is accessable externally.  
**Ensure the correct indentation is used**  
6. Replace the values as needed, also see other examples for additional configuration options.
All config options can be found on the [istio website](https://istio.io/latest/docs/reference/config/networking/service-entry/).  
7. Add {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} as a reviewer to your PR.  
8. After the PR is merged, the istio changes will be deployed to development, staging, and eventually production by the CI/CD process.  

### (b) If the purpose is to add a new service entry only in specific regions and environments

1. Clone the [oss-charts]({{site.data[site.target].oss-apiplatform.links.oss-charts.link}}) repo, and create a new branch.
2. In `api-istio` folder, open `values.yaml` file, locate `serviceentries`  
2. In `api-istio` folder, find the regional files where you wish to add a new service entry and open them.  
For example if you want the new service entry only in `us-east`, `dev` or `staging`, use the files `useast-development-values.yaml` and `useast-staging-values.yaml` respectively.
3. In each of the files look for `serviceentries`, but it might not exist
In case it is not there, you need to add it.
4. If it already exists, you will see all service entries configs
Go to the bottom to add a new one.
5. Copy an existing service entry, such as:
    ```yaml
         - metadata:
             name: vault-service-api
           spec:
             hosts:
             - "vserv-us.sos.ibm.com"
             location: MESH_EXTERNAL
             ports:
             - number: 8200
               name: vault-us-api
               protocol: TLS
    ```
This service entry means that "vserv-us.sos.ibm.com" on port 8200 using TLS is accessable externally.  
**Ensure the correct indentation is used**
6. Replace the values as needed, also see other examples for additional configuration options.
All config options can be found on the [istio website](https://istio.io/latest/docs/reference/config/networking/service-entry/).  
7. Create a PR and add {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %} as a reviewer to your PR  
8. After the PR is merged, the istio changes will be deployed to development, staging, and eventually production by the CI/CD process.  


## Runbook Owners

- {% include contact.html slack=oss-auth_2-slack name=oss-auth_2-name userid=oss-auth_2-userid notesid=oss-auth_2-notesid %}

---
layout: default
title: How to update the OSS CIS IP White list
type: Alert
runbook-name: api-cis-ip-change
description: "How to update the OSS CIS IP White list"
service: tip-api-platform
tags: CIS, cis, IP, ip, cloud, Internet
link: /apiplatform/api-cis-ip-change.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Overview

This runbook provides details for changing the CIS (IBM Cloud Internet Services) white list rules addresses to ensure that our APIs continue to work. When the CIS team change the IP addresses, we need to update our rules in CIS, the [Calico Github](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/network-calico/allow-443-inbound-alb.yaml), `the list is under the source > nets section`, whitelist that is in use in our clusters and the [NewRelic Synthetics](https://synthetics.newrelic.com/accounts/1926897/monitors/54730ea2-2819-439b-b36d-84ce21dbc803/script) script.

- Alert [api-cis-address-list](https://synthetics.newrelic.com/accounts/1926897/monitors/54730ea2-2819-439b-b36d-84ce21dbc803)

The NewRelic alert will call the [CIS API](https://cloud.ibm.com/docs/cis?topic=cis-cis-allowlisted-ip-addresses) to obtain the list and compare it to a hardcoded list of IPs we currently use. If the list found to be different, an alert is triggered

## What is Calico?
Calico is an open source networking and network security solution for containers, virtual machines, and native host-based workloads. Calico supports a broad range of platforms including Kubernetes, OpenShift, Docker EE, OpenStack, and bare metal services.

Calico combines flexible networking capabilities with run-anywhere security enforcement to provide a solution with native Linux kernel performance and true cloud-native scalability. Calico provides developers and cluster operators with a consistent experience and set of capabilities whether running in public cloud or on-prem, on a single node or across a multi-thousand node cluster. For more information, visit the [Calico](https://www.projectcalico.org/) Project


## How to verify the alert

To verify that the list is actually changed, follow these steps:

* Open the NewRelic Incident from the alert. Select `Go to api-cis-address-list overview`, this will take you to the Synthetics monitor result page which shows the list of IP's. Take a note of the list
* Run the following curl command to obtain the new list: `curl --silent https://api.cis.cloud.ibm.com/v1/ips | jq`
* You can also access the list from the [Calico Github](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/network-calico/allow-443-inbound-alb.yaml) repository,`the list is under the source > nets section`
* Compare the Two lists


## How to update the CIS whitelist IPs in the Calico polices

- Obtain the current list of CIS whitelist IPs from CIS API. See [How to verify the alert](#how-to-verify-the-alert)
- Update the `source > nets` in the [allow-443-inbound-alb.yaml](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/network-calico/allow-443-inbound-alb.yaml) file with the updated IPs from step 1 (ipv4_cidrs)
- Create a pull request for the Calico Github with the changes. Have the changes reviewed by {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %} or {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}
- After approval, merge in the PR
- For every cluster, execute the steps in the [How to apply the network polices](#how-to-apply-the-network-polices) section below for the `allow-443-inbound-alb.yaml` network config yaml file    

## How to apply the allow-443-inbound-alb network policy

Note the following requirement:

- Ensure to open a `New` issue in our [ToolsPlatform](https://github.ibm.com/cloud-sre/ToolsPlatform) github repository for tracking purposes
- Admin access on the clusters is required
- A Change record should be opened for each production environment before the changes are made in production

1. Run the following command to obtain the list of clusters and their IPs:
   ```
   ibmcloud ks clusters
   ```
2. Run the following command to obtain the calico configuration data (calicoctl.cfg):
   ```
   ibmcloud ks cluster config --cluster <CLUSTER_ID> --admin --network
   ```
3. Create the `/etc/calico/` folder if it does not already exist
4. Copy the calicoctl.cfg file into the `/etc/calico/` folder
5. Run the following command for each of the network config yaml files:
    ```
    calicoctl apply -f allow-443-inbound-alb.yaml --config=/etc/calico/calicoctl.cfg
    ```

## Update NewRelic monitor

- Open the [NewRelic Synthetics](https://synthetics.newrelic.com/accounts/1926897/monitors/54730ea2-2819-439b-b36d-84ce21dbc803/script) script
- Find the section with the list of IP's. List is under the `var currentCISIPs`
- Update the list with the changes from CIS whitelist IPs obtained above and click `Save script`
- The alert should auto resolve on the next NewRelic check, however it's important to validate that the incident is actually resolved
- Only users with `admin` or `Synthetics manager` roles will be able to update the script. If you do not have permission to update the script, please contact {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}

## Runbook Owners

- {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

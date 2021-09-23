---
layout: default
description: TF Service Incidents Alert
title: "Runbook TF Service Incidents"
service: doctor
runbook-name: "Runbook TF Service Incidents"
tags: oss, bluemix, doctor, scorecard
link: /doctor/Runbook_TF_Service_Incidents.html
type: Alert

---
{% include {{site.target}}/new_relic_tip.html%}
{% include {{site.target}}/load_cloud_constants.md %}


# tf_kube_[prod|stage|dev]_[cpu|memory|filesys|syspod|pulse|network] incidents

# TF Service Incidents

## Purpose
This alert happens when the health check URL for a Kubernetes service is unreachable.

## Technical Details
Ping from New Relic to a service running in the `tf` namespace in a Kubernetes cluster didn't receive the expected response.
The name of the service and cluster it is running in can be found from the alert description:
"Violated New Relic condition: ping-tf-[service short name]-[global|useast|ussouth|eugb]-[prd|stg]-condition"
If the above condition name contains "global", then the service cannot be reached with its global URL; If the condition indicates a region, it's the region's regional URL that's unreachable.

Use the service short name in the alert to look for the corresponding names below:
| Alert service short name | CIS Production Load Balancer name | CIS Staging Load Balancer name | Kubernetes service name, pod name prefix, ingress name prefix
| status-backend | status-backend.w3 | status-backend.w3.staging | osssatus-backend
| status | status.w3 | status.w3.staging | ossstatus-portal

## User Impact
If the alert is for a regional URL, the service is unavailable for the region, but users may still be available access the service using its URL for another region.
If the alert is for a global URL. depending on the configuration of the load balancer, the service may or may not be accessible at certain region(s).

## Instructions to Fix

### Check the reachability of the health URL
Follow the "Failure link" to see the New Relic monitor. The health check URL being pinged can be found in the "General" tab.
Curl the URL from within the IBM intranet.

### Failed URL is global
Most likely, there is at least one active alert for the same service in one of the regions.
Browse the list of current active New Relic or Pager Duty incidents to find out in each region the service is up or down.

If the service can be restored quickly in all the failed regions, then no action is needed for the failed global URL. It should be recovered after the recovery in all regions.
Otherwise, if the service is up in at least one region, follow the steps below to modify the load balancer to point to the region where the service is up.
If you do not have the authority to perform the following actions, assign the alert to the secondary on-call, or to someone with the required access.
* Go to [console for IBM cloud](https://console.cloud.ibm.com/resources)
* Log into {{oss-account-full-name}} account
* On the dashboard, click on the "CIS-OSS-Prod" under "Services"
* Click on "Global Load Balancers" under "Reliability"
* Find the load balancer (look up for the load balancer name in the table at the top of the page) for the service
* Click on the three dots at the right of the table, invoke "Edit load balancer"
* In the "Default origin pools" and each "Geo Routes" (if configured), use the up and down arrows under "Priority" to switch the priority orders of the original pools so that the first pool is at the region that the service is up.
* Press "Apply Changes"
* Check the reachability of the service URL again
* Wait for New Relic to resolve the incident.

### Failed URL is regional
Look up for the Kubernetes resource names in the table at the top of the page.
Use the Kubernetes dashboard or command line to check the state of the cluster, ingress, service, and pod, etc. Restore them to running state.
If you do not have the authority to perform these actions, assign the alert to the secondary on-call, or to someone with the required access.

For GUI administration for Kubernetes:
* Go to [console for IBM cloud](https://console.bluemix.net/)
* Log into {{oss-account-full-name}} account
* Click on the cluster being reported
* Click on "Kubernetes Dashboard (beta)" on the top right

Commands might be useful:
* `kubectl oss node get` to check all nodes are in "Ready" state
* `kubectl get ing -n tf` to confirm the URL being tested is one of the HOSTs defined
* `kubectl get services -n tf` to confirm the service is defined and check the service age
* `kubectl get pods -n tf | grep [pod name prefix]` to see if the pod is running

## Notes and Special Considerations
None.

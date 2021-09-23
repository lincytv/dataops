---
layout: default
title: OSS Auth API
type: Alert
runbook-name: "api.oss-auth"
description: "Runbook for the oss-auth API"
service: oss-auth
tags: api-oss-auth,oauth
link: /apiplatform/api.oss-auth.html
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}



# Policies covered by this runbook
* oss_oauth_synthetics_prd
* oss_oauth_synthetics_stg

The NewRelic policies cover Two types of conditions:
* Ping monitors for the regional and global URLs. I.e ping-api-oauth-global-prd
* Pod down monitors. I.e. api-oauth_pod_down:eu-de:prd


## Purpose
Use this runbook to confirm and resolve the issue.
Contact a developer ( {% include contact.html slack=oss-auth-slack name=oss-auth-name userid=oss-auth-userid notesid=oss-auth-notesid%} or {% include contact.html slack=oss-auth_2-slack name=oss-auth_2-name userid=oss-auth_2-userid notesid=oss-auth_2-notesid%} ) if the steps here isn't sufficient to resolve the problem, or if the instruction says to contact a developer.

## Technical Details
The oss-auth API provides a /oauth/api/v1/oauth/ibmcloud/tokens POST API whose only consumer is the ciebot. The ciebot calls this /tokens API to get the public IAM token of user. Here is a highlevel flow of how a user interacts with the ciebot which then users the oss-auth API to authenticate the user:

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/api.oss-oauth_overview.png){:width="720px"}

The oss-auth API runs in the api namespace in all three production and staging clusters. There is only one replica in each region as caching is done within the pod itself. There is communication between the api-oss-auth pods across regions to sync their caches though.

Communication to the api-oss-auth pods is from CIS to the api-ingress ingress in the api namspace to the api-oss-auth service in the api namespace to the api-oss-auth pod in the api namespace.

## User Impact
If there is a problem with the oss-auth API users may not be able to login to use the ciebot. This can severly impact AVMs and service teams who are trying to open or update CIEs.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Do not mark {{doctor-alert-system-name}} incident _resolved_
Once the underline issue is fixed, {{new-relic-porta-name}} will recognize the violation no longer exists, and send a _resolved_ signal to TIP, and the ServiceNow and {{doctor-alert-system-name}} incidents will become resolved on their own.

### How to resolve global URL Ping incidents

NewRelic Synthetics Ping monitor:    
- [Production](https://synthetics.newrelic.com/accounts/1926897/monitors/3ff1d537-162a-4797-9129-61c39f2feb9e)
- [Staging](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJpc092ZXJ2aWV3Ijp0cnVlLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmRGswT1RGbFpHTm1MVFU0T1RVdE5EY3pZeTFpWlRNeUxUQTFZakF3TVRJMk5UUmxaUSJ9&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRrME9URmxaR05tTFRVNE9UVXRORGN6WXkxaVpUTXlMVEExWWpBd01USTJOVFJsWlEiLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIGxpa2UgJ29hdXRoJyBvciBpZCA9ICdvYXV0aCcgb3IgZG9tYWluSWQgPSAnb2F1dGgnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)

Tests the following URLs. depending if Production or Staging from the Columbus (Dallas), WDC, and London locations:    
  - [https://pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)    
  - [https://pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)

Steps:

1. If all three locations are having trouble calling the URL, this is a severity 1 situation
2. Test whether you can successfully call all the regional URLs:
    Production:
     - [https://us-east.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-east.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
     - [https://us-south.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-south.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
     - [https://eu-de.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://eu-de.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)

    Staging:
    - [https://us-south.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-south.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
    - [https://us-east.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-east.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
    - [https://eu-de.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://eu-de.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)


3. Test whether you can successfully call the global URLs:
     - [https://pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
     - [https://pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
4. If all the URLs in step 2 and 3 are successful, the problem is most likely a false alarm
5. If all the URLs in step 2 are successful, but the URL in step 3 fails, the problem is mostly a CIS or a general network problem
6. If all the URLs in step 2 and 3 fail, the problem is most likely a problem with the `api-oss-auth` pod or a dependency like IAM
7. If a subset of the URLs in step 2 fail, the problem is most likely a general network problem in the failing regions

### How to resolve regional URL Ping incidents

- Tests the following URLs:

  Production:
     - [https://us-east.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-east.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
     - [https://us-south.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-south.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
     - [https://eu-de.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://eu-de.pnp-api-oss.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)

  Staging:
    - [https://us-south.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-south.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
    - [https://us-east.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://us-east.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)
    - [https://eu-de.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud](https://eu-de.pnp-api-oss.test.cloud.ibm.com/oauth/api/v1/oauth/login/succeeded?status=1&provider=IBM+Cloud)

Steps:

1. Test whether you can successfully call the regional URLs from above list
2. If the test from 1 is successful, this is a false alarm
3. If the test from 1 fails, narrow down the problem to see whether the problem is in CIS, ingress, the `api-oss-auth` pod, or a dependency like IAM

### How to resolve Pod down incidents
#### Kubernetes access and command line basics
* [Access]({{repos-cloud-sre-tools-platform-link}}/wiki/How-to-Access-OSS-Armada-Cluster) Armada OSS [kubernetes clusters]( https://cloud.ibm.com/kubernetes/clusters)
* Get started with [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cli-getting-started)
* Kubernetes command line [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/)
* Kubenetest pods can be deleted, and Kubenetes will recreate them. By deleting and having Kubernetes to recreate pods, issue might be resolved.


#### Verify the issue
* Access privilege may be required for the Ops support to view the Kubernetes system performance information in {{new-relic-portal-name}}.

* Follow the incident link to confirm the {{new-relic-portal-name}} alert condition violated, or start from [{{new-relic-portal-name}} Insights]({{new-relic-portal-link-insights}}), to view the overall system performance.

 * A Newrelic Dashboard have been created to assist you with the investigating. Access the [Kubernetes Integration - Infrastructure](https://insights.newrelic.com/accounts/1926897/dashboards/546408) and view each Panel based on the incident reported. You can filter on the component name by searching for the name. I.e. oauth

* Verify that the number of running pods using `kubectl oss pod get -napi | grep oauth` and make sure it match with NewRelic

#### Resolve the issue
* If you find any Pods with status other than `Running`, this could cause the error
* Check the pods logs using `kubectl logs -napi api-oauth-xxxxx -c api-oauth` and check for errors
* View Logs in [Oauth logDNA]({{site.baseurl}}/docs/runbooks/apiplatform/ibm/APIs_logDNA_links.html) under `API PLATFORM` view
* If a Pod not running, you can delete it and have Kubernetes to recreate it using `kubectl oss pod delete [pod name] -n [pod namespace]`

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

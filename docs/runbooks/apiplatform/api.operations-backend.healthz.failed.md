---
layout: default
title: "RMC Operations Backend Healthz Failure"
type: Alert
runbook-name: "api.operations-backend.healthz.failed"
description: "This alert will be triggered when calling the RMC Operations Backend healthz API failed"
service: tip-api-platform
tags: rmc, operations-backend, healthz
link: /apiplatform/api.operations-backend.healthz.failed.html
---

## Purpose
Alert will be triggered when the api-operations-backend healthz API can not successfully be called.

## Technical Details
The api-operations-backend service is deployed in Kubernetes in the `us-south`, `us-east` and `eu-de` regions. In each region, there is one pod instance running which can automatically scale to a maximum of two pods.

Staging and production API synthetic monitors have been set up in New Relic to monitor the global healthz endpoint from multiple locations and the us-south, us-east, and eu-de regional healthz endpoints.

#### Production Policy, Conditions, and Synthetics:
- Policy: [oss-platform-registry-prd](https://one.newrelic.com/launcher/nrai.launcher?platform[accountId]=1926897&pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjEyODQ3MDQifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ)
    - api-operations-backend-healthz-global-prd-Condition
        - [api-operations-backend-healthz-global-prd](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmR1JsWkRVd1pUYzVMVE5rTURJdE5EVTBaQzFpT1RVNExUUXlPV1U1TlRsaFlqZzFOZyIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoibnIxLWNvcmUuZXhwbG9yZXIiLCJuZXJkbGV0SWQiOiJucjEtY29yZS5saXN0aW5nIn0sIkxvY2F0aW9uU3RhdHVzQ2hhcnRDb250YWluZXIiOnRydWV9&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkdSbFpEVXdaVGM1TFROa01ESXRORFUwWkMxaU9UVTRMVFF5T1dVNU5UbGhZamcxTmciLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=Iihkb21haW4gPSAnU1lOVEgnIEFORCB0eXBlID0gJ01PTklUT1InKSBBTkQgKG5hbWUgTElLRSAnb3BlcmF0aW9ucycgT1IgaWQgPSAnb3BlcmF0aW9ucycgT1IgZG9tYWluSWQgPSAnb3BlcmF0aW9ucycpIg==&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
    - api-operations-backend-healthz-washington-prd-Condition
         - [api-operations-backend-healthz-washington-prd](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmREJsWkRoaVkyTTNMV1EzWlRjdE5HVTNaUzA1TlRJeUxUUm1NRE0yTUdJM1lXTXpOdyIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoibnIxLWNvcmUuZXhwbG9yZXIiLCJuZXJkbGV0SWQiOiJucjEtY29yZS5saXN0aW5nIn0sIkxvY2F0aW9uU3RhdHVzQ2hhcnRDb250YWluZXIiOnRydWV9&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRCbFpEaGlZMk0zTFdRM1pUY3ROR1UzWlMwNU5USXlMVFJtTURNMk1HSTNZV016TnciLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=Iihkb21haW4gPSAnU1lOVEgnIEFORCB0eXBlID0gJ01PTklUT1InKSBBTkQgKG5hbWUgTElLRSAnb3BlcmF0aW9ucycgT1IgaWQgPSAnb3BlcmF0aW9ucycgT1IgZG9tYWluSWQgPSAnb3BlcmF0aW9ucycpIg==&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
     - api-operations-backend-healthz-dallas-prd-Condition
         - [api-operations-backend-healthz-dallas-prd](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmRFl3TURFd056QmpMVGN4TUdNdE5HSTVNeTFpWmpaaExUQXlOREkwWXpobU9URTROdyIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoibnIxLWNvcmUuZXhwbG9yZXIiLCJuZXJkbGV0SWQiOiJucjEtY29yZS5saXN0aW5nIn0sIkxvY2F0aW9uU3RhdHVzQ2hhcnRDb250YWluZXIiOnRydWV9&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRZd01ERXdOekJqTFRjeE1HTXROR0k1TXkxaVpqWmhMVEF5TkRJMFl6aG1PVEU0TnciLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=Iihkb21haW4gPSAnU1lOVEgnIEFORCB0eXBlID0gJ01PTklUT1InKSBBTkQgKG5hbWUgTElLRSAnb3BlcmF0aW9ucycgT1IgaWQgPSAnb3BlcmF0aW9ucycgT1IgZG9tYWluSWQgPSAnb3BlcmF0aW9ucycpIg==&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
     - api-operations-backend-healthz-frankfurt-prd-Condition
         - [api-operations-backend-healthz-frankfurt-prd](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmRFl3TlRrM05tWmlMVFJtT0RFdE5HVTJPUzFoTjJRMExUQmpZakppT1dabFl6Z3pPQSIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoic3ludGhldGljcy1uZXJkbGV0cy5ob21lIiwibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLWxpc3QifSwiTG9jYXRpb25TdGF0dXNDaGFydENvbnRhaW5lciI6dHJ1ZX0=&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRZd05UazNObVppTFRSbU9ERXROR1UyT1MxaE4yUTBMVEJqWWpKaU9XWmxZemd6T0EiLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIExJS0UgJ29wZXJhdGlvbnMnIE9SIGlkID0gJ29wZXJhdGlvbnMnIE9SIGRvbWFpbklkID0gJ29wZXJhdGlvbnMnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)

#### Staging Policy, Conditions, and Synthetics:
- Policy: [oss-platform-registry-stg](https://one.newrelic.com/launcher/nrai.launcher?platform[accountId]=1926897&pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjEyODQ2OTUifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ)
    - api-operations-backend-healthz-global-stg-Condition
         - [api-operations-backend-healthz-global-stg](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmR1kzTmpNNE9HSmpMVFEzWkdZdE5EWTRaaTA0TlRaaExXRmtOREV4TWpVNE1HWmhZUSIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoic3ludGhldGljcy1uZXJkbGV0cy5ob21lIiwibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLWxpc3QifSwiTG9jYXRpb25TdGF0dXNDaGFydENvbnRhaW5lciI6dHJ1ZX0=&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkdZM05qTTRPR0pqTFRRM1pHWXRORFk0WmkwNE5UWmhMV0ZrTkRFeE1qVTRNR1poWVEiLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIExJS0UgJ29wZXJhdGlvbnMnIE9SIGlkID0gJ29wZXJhdGlvbnMnIE9SIGRvbWFpbklkID0gJ29wZXJhdGlvbnMnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
    - api-operations-backend-healthz-washington-stg-Condition
         - [api-operations-backend-healthz-washington-stg](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmRGsyTUdObFl6WmtMVGRtWlRVdE5HVXpNUzA0WXprd0xUazNaREF6WlRSaE1XUm1PQSIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoic3ludGhldGljcy1uZXJkbGV0cy5ob21lIiwibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLWxpc3QifSwiTG9jYXRpb25TdGF0dXNDaGFydENvbnRhaW5lciI6dHJ1ZX0=&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRrMk1HTmxZelprTFRkbVpUVXROR1V6TVMwNFl6a3dMVGszWkRBelpUUmhNV1JtT0EiLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIExJS0UgJ29wZXJhdGlvbnMnIE9SIGlkID0gJ29wZXJhdGlvbnMnIE9SIGRvbWFpbklkID0gJ29wZXJhdGlvbnMnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
    - api-operations-backend-healthz-dallas-stg-Condition
         - [api-operations-backend-healthz-dallas-stg](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmRGRrT0dNNFlUZ3pMVEExTWpRdE5HRmlOaTFpTVRCbExUSmhZVGs1T1RBd05HSmlZdyIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoic3ludGhldGljcy1uZXJkbGV0cy5ob21lIiwibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLWxpc3QifSwiTG9jYXRpb25TdGF0dXNDaGFydENvbnRhaW5lciI6dHJ1ZX0=&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkRka09HTTRZVGd6TFRBMU1qUXROR0ZpTmkxaU1UQmxMVEpoWVRrNU9UQXdOR0ppWXciLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIExJS0UgJ29wZXJhdGlvbnMnIE9SIGlkID0gJ29wZXJhdGlvbnMnIE9SIGRvbWFpbklkID0gJ29wZXJhdGlvbnMnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)
    - api-operations-backend-healthz-frankfurt-stg-Condition
        - [api-operations-backend-healthz-frankfurt-stg](https://one.newrelic.com/launcher/nr1-core.explorer?pane=eyJuZXJkbGV0SWQiOiJzeW50aGV0aWNzLW5lcmRsZXRzLm1vbml0b3Itb3ZlcnZpZXciLCJlbnRpdHlJZCI6Ik1Ua3lOamc1TjN4VFdVNVVTSHhOVDA1SlZFOVNmR0ZpTW1KbVpEa3pMV0l4TVRjdE5EZGlPQzA1WVRRNUxUTXhORGhqWlRBMFpUbGtNUSIsImlzT3ZlcnZpZXciOnRydWUsInJlZmVycmVycyI6eyJsYXVuY2hlcklkIjoic3ludGhldGljcy1uZXJkbGV0cy5ob21lIiwibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLWxpc3QifSwiTG9jYXRpb25TdGF0dXNDaGFydENvbnRhaW5lciI6ZmFsc2V9&sidebars[0]=eyJuZXJkbGV0SWQiOiJucjEtY29yZS5hY3Rpb25zIiwiZW50aXR5SWQiOiJNVGt5TmpnNU4zeFRXVTVVU0h4TlQwNUpWRTlTZkdGaU1tSm1aRGt6TFdJeE1UY3RORGRpT0MwNVlUUTVMVE14TkRoalpUQTBaVGxrTVEiLCJzZWxlY3RlZE5lcmRsZXQiOnsibmVyZGxldElkIjoic3ludGhldGljcy1uZXJkbGV0cy5tb25pdG9yLW92ZXJ2aWV3IiwiaXNPdmVydmlldyI6dHJ1ZX19&platform[accountId]=1926897&platform[filters]=IihuYW1lIExJS0UgJ29wZXJhdGlvbnMnIE9SIGlkID0gJ29wZXJhdGlvbnMnIE9SIGRvbWFpbklkID0gJ29wZXJhdGlvbnMnKSI=&platform[timeRange][duration]=1800000&platform[$isFallbackTimeRange]=true)

## User Impact
The operations-backend API is used called by base RMC when an RMC resource is being promoted to production. If the operations-backend API is not available, calls from RMC could be missed and the associated OSS registry entry and ServiceNow CI entry may not be updated. Not critical because the user has the option to promote the RMC Operations page seperately in the RMC editor.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

1. From the PagerDuty incident, determine what environment (production and/or staging) and what region (global, us-south, us-east, and/or eu-de) the failure is occurring in
2. Check [New Relic status page](https://status.newrelic.com/) to see if there is an ongoing outage or maintenance. The alert may be a false alarm.
3. Open the incident in NewRelic, click the link for the synthetic name (for example, api-operations-backend-healthz-washington-prd), and then press the `Re-check` button to see if the problem is already fixed
4. Check whether the api-operations-ui pod is running in the associated Kubernetes clusters by running the following command:
   ```
   kubectl oss pod get -n api | grep operations-backend
   ```
5. If the pod is not running, try deleting the pod by running the following command to see if the pod gets recreated successfully:
   ```
   kubectl oss pod delete <POD> --namespace=api
   ```
6. Run the following commands to obtain more information about why the pod is failing:
    ```
    kubectl describe pod -napi <POD>
    kubectl logs -napi <POD> -c api-operations-backend
    ```
7. If there are still problems, check whether any recent changes have been delivered
8. If the pod is running fine and not logging any errors, the problem may be with Kubernetes or the network. Look for other incidents open at the same time.
9. If you are stuck, reach out to Shane Cartledge

## Contacts
**PagerDuty**
* [{{site.data[site.target].oss-apiplatform.links.pagerduty.name}}]({{site.data[site.target].oss-apiplatform.links.pagerduty.link}})

**Slack**
* [#oss-platform-onshift](https://ibm-cloudplatform.slack.com/archives/G01S292026S)

---
layout: default
description: Doctor support import inventory(IaaS VMs) to doctor server.
title: Import Inventory
service: doctor
runbook-name: Import Inventory
tags: doctor, cloud
link: /doctor/Runbook_Import_Inventory.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

Doctor support import inventory (IaaS Virtual Machines) to Doctor server.

## Export Your Doctor API Key

```
export API_KEY=<your api key>
export ENV_NAME=WATSON_HEALTH_TEST01
```

You can get your [API Key by Doctor portal]({{site.baseurl}}/docs/runbooks/doctor/Runbook_how_to_get_doctor_api_key.html).

## 1. Import API

```
curl -X POST -H "authorization:${API_KEY}" -H "Content-Type: application/json" -d @inventories.json '{{doctor-rest-apis-link}}/doctorapi/api/doctor/inventory/import'
```

inventories.json structure:

```
{
  "env_name": "",
  "inventories": [
      {
        "id": "<unique number>",
        "fullyQualifiedDomainName": "<host name>",
        "primaryBackendIpAddress": "<ip address>",
        "serverType": "virtual_guest",
        "primaryBackendPod": "<pod name>",
        "server_state": "<status>"
      }
  ]
}
```
inventories.json example:

```
{
  "env_name": "WATSON_HEALTH_TEST01",
  "inventories": [
    {
        "id": "001",
        "fullyQualifiedDomainName": "1575-lon02-Prd-Lon2-CSN-PROTYZ.whc.sl.edst.ibm.com",
        "primaryBackendIpAddress": "10.164.206.84",
        "serverType": "virtual_guest",
        "primaryBackendPod": "",
        "operatingSystem": {
            "softwareLicense": {
              "softwareDescription": {
                "longDescription": "Ubuntu 14.04-64 Minimal for VSI",
                "manufacturer": "Ubuntu",
                "name": "Ubuntu",
                "version": "14.04-64 Minimal for VSI"
              }
            }
        },
        "server_state": "running"
      },
     {
        "id": "002",
        "fullyQualifiedDomainName": "1555-lon02-Prd-Lon2-CSN-PROTYZ.whc.sl.edst.ibm.com",
        "primaryBackendIpAddress": "10.164.206.85",
        "serverType": "virtual_guest",
        "primaryBackendPod": "bcr02a.lon02",
        "operatingSystem": {
            "softwareLicense": {
              "softwareDescription": {
                "longDescription": "Debian 8.0.0-64 Minimal for VSI",
                "manufacturer": "Debian",
                "name": "Debian",
                "version": "8.0.0-64 Minimal for VSI"
              }
            }
        },
        "server_state": "running"
      },
      {
          "id": "003",
          "fullyQualifiedDomainName": "PluginUpgradeNoNIC232.ibm.com",
          "primaryBackendIpAddress": "10.155.107.158",
          "serverType": "virtual_guest",
          "primaryBackendPod": "bcr02a.lon02",
          "operatingSystem": {
              "softwareLicense": {
                "softwareDescription": {
                  "longDescription": "Redhat EL 7.0-64 Minimal for VSI",
                  "manufacturer": "Redhat",
                  "name": "EL",
                  "version": "7.0-64 Minimal for VSI"
                }
              }
          },
          "server_state": "running"
        }
  ]
}
```

## 2. Query API

```
curl -X GET -H "authorization:${API_KEY}" '{{doctor-rest-apis-link}}/doctorapi/api/doctor/inventory/list?env_name=${ENV_NAME}'

```

## 3. Delete API


```
curl -X DELETE -H "authorization:${API_KEY}" -H "Content-Type: application/json" "{{doctor-rest-apis-link}}/doctorapi/api/doctor/inventory/delete?id=001&env_name=${ENV_NAME}"

```

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

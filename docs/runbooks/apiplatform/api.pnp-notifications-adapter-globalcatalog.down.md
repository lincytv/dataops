---
layout: default
title: "API Platform - PnP Notifications Adapter Global Catalog Errors"
type: Alert
runbook-name: "api.pnp-notifications-adapter-globalcatalog.down"
description: "Runbook to drill into errors related to Global Catalog via the Notifications Adapter"
service: tip-api-platform
tags: pnp, apis, notifications, catalog
link: /apiplatform/api.pnp-notifications-adapter-globalcatalog.down.html   
---

## Purpose
The pnp-notification-globalcatalog-GetRecords transaction provides information about transactions with the global catalog used to retrieve information about services.  For the notification adapter, the global catalog is merely used to get the service display name. An error in this transaction indicates that the global catalog is either non-responsive or returning data in an incorrect format.

This alert applies to appName=`api-pnp-notifications-adapter-*` and:
- Service now incidents with a title: `api-pnp-notifications-adapter failed in Global Catalog database query` or `api-pnp-notifications-adapter failed in parsing records from Global Catalog`
- New Relic incidents with the title containing text: `api-pnp-notif-adapter_globalCatalogDBFail` or `api-pnp-notif-adapter_parseGlobalCatFail`

## Technical Details
Two types of error may occur in this transaction:

- pnp-db-failed - indicates there was a failure during the request to the global catalog. This is more likely that there is a networking issue.  Less likely is the presence of an error with the global catalog itself.
- pnp-parse-failed - indicates there was a failure trying to parse the response from the database.  More likely this is due to receiving some kind of error in response to the global catalog request.  The less likely scenario is that the global catalog has changed the format of data being returned.

## User Impact
When either of the error conditions occur (pnp-db-failed or pnp-parse-failed), then there was an issue acquiring the language translated version of the display names for one or more services.  When the language specific names cannot be acquired from the Global Catalog, then the adapter will look at two other sources to get the name.  The other sources only have english versions of the name.  As of now, there are very few services which have translated their display name.  Therefore, for the most part this alert will be completely benign.  

This alert should be treated with low priority and can be fixed during the next business day.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Step 1

If this is a parse error, then this error must be reported to PnP. Reassign the PagerDuty incident to `tip-api-platform level 2`.  You are done.


#### Operator Response

This error must be reported to PnP. reassign the PagerDuty incident to `tip-api-platform level 2`. You are done.

If no problem, proceed to Step 2

### Step 2

A quick item to check.

Attempt to navigate to the Global Catalog UI.  Open a browser and navigate to:
```
https://resource-catalog.bluemix.net
```
Attempt to search for a well known service such as `cloudantnosql`.  If any of this fails, or the search does not find Cloudant, then there is a problem with the Global Catalog.  An issue should be created with the Global Catalog team.

#### Operator Response

If the above fails, then there is a problem with the Global Catalog.  Open a Sev2 incident in ServiceNow for the Global catalog.  Open it against the Configuration Item: `globalcatalog`.

If no problem, proceed to Step 3

### Step 3
If everything is successful with Step 1 and 2, then verify that a query can be executed against the global catalog similar to the queries that the PnP adapter will execute.  Execute the following from anywhere that can access the internet.

```
curl -v -G 'https://resource-catalog.bluemix.net/api/v1'
```

There will be a lot of output, but it will look similar to (though not identical):

```
{"offset":0,"limit":50,"count":314,"resource_count":50,"first":"https://resource-catalog.bluemix.net/api/v1?languages=%2A","next":"https://resource-catalog.bluemix.net/api/v1?_offset=50&languages=%2A","resources":[{"active":true,"catalog_crn":"crn:v1:bluemix:public:globalcatalog::::iaas:22","children_url":"https://resource-catalog.bluemix.net/api/v1/22/%2A","created":"2017-08-24T18:16:39.938Z","disabled":false,"id":"22","images":{"image":"https://resource-catalog.cdn.s-bluemix.net/static/cache/378-fbb60ad3d95e3c95/images/uploaded/direct-link.png"},"kind":"iaas","metadata":{"callbacks":{"broker_proxy_url":"https://console.ng.bluemix.net","broker_url":"https://console.ng.bluemix.net"},"extension":{},"extension_point":{"requires_approval":false},"other":{"softlayer":{"accountDefinedNetworks":true,"allOf":["TICKET_ADD","TICKET_VIEW","SERVICE_ADD"]}},"rc_compatible":false,"ui":{"strings":{"de":{"bullets":[{"description":"Unabhängig
davon, ob sich die Ressourcen im Rechenzentrum oder in der IBM Cloud befinden, können Sie die Geschwindigkeit und Sicherheit nutzen, die für Ihr Unternehmen erforderlich ist.","title":"Vollständig integrierte Hybridumgebung"},{"description":"Stellen Sie Ihre Ressourcen dort bereit, wo Sie sie im sicheren Netz von IBM Cloud benötigen. Sie brauchen keine Leistung für Sicherheit und Komfort opfern.","title":"Sichere, dedizierte Konnektivität"},{"description":"Wählen Sie eine der
Portgeschwindigkeiten 1, 2, 5 oder 10 Gb/s in einem der globalen IBM Cloud-Rechenzentren aus. Wenn Sie Ihre Anforderungen ändern, können Sie die Geschwindigkeiten ohne Reibungsverluste ändern.","title":"Herausragende Auswahlmöglichkeiten und Investitionsschutz"}]},"en":{"bullets":[{"description":"Whether your resources are in your datacenter or on the IBM Cloud, you can operate with the speed and security that your business requires.","title":"Fully Integrated Hybrid
Environment"},{"description":"Deploy your resources where you need them on IBM Cloud's secure network. You need not sacrifice performance quality for security and compliance.","title":"Secure Dedicated Connectivity"},{"description":"Choose port speeds of 1, 2, 5, or 10 Gbps in one of IBM Cloud's global data centers. As your needs change, you can transition your speeds seamlessly.","title":"Unmatched choice and investment protection"}]
```

For reference, the swagger documentation for the global catalog can be retrieved from here:

```
https://resource-catalog.bluemix.net/swagger
```

If the curl command fails, then there is a problem with the global catalog.  Try to notice if the problem is a network error or actually an error being returned from the catalog.  In either case, the problem may resolve itself, so open a git issue to be resolved during business hours.


#### Operator Response

If the curl command fails, then there is a problem with the global catalog.  Try to notice if the problem is a network error or actually an error being returned from the catalog. Open a Sev2 incident in ServiceNow for the Global catalog.  Open it against the Configuration Item: `globalcatalog`.  Please note the error in from the commands in the ServiceNow incident.

If no errors on this step, proceed to Step 4.

### Step 4

If the above has all worked successfully, it is possible that there is a connection issue from the adapter container to the global catalog.

```
kubectl exec -it api-pnp-notifications-adapter-645c8bfb9f-88m87 -- /bin/sh
```
Of course substitute `api-pnp-notifications-adapter-645c8bfb9f-88m87` with the actual name of the notifications-adapter container. Then issue the above curl commands.  If curl does not exist, it can be added via the following command:
```
apk --update add curl
```

Follow the same commands as outlined in Step 2 to see if there is an issue from the container.


#### Operator Response

If the curl commands fail in the container but do not fail from another box, then there is a networking or environmental problem between the notification-adapter container and the global catalog.  The foundation team should be engaged.  See [Contacting TF](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/ibm/Contact_Technical_Foundation.html)

If nothing wrong in this step, proceed to Step 5

### Step 5

In this case, take a look at the logs.  See the "Viewing Logs" section. Look for a log such as:

`ERROR (GetCloudResources): Failed to get resources from global catalog url (https://resource-catalog.bluemix.net/api/v1?languages=%2A): XXX`

`XXX` will denote the error.

Attempt to run a curl command against the shown URL to see if it fails.  If it fails, note the error and open a Sev2 incident in ServiceNow for the Global catalog.  Open it against the Configuration Item: `globalcatalog`.

`ERROR (AddDisplayNames) getting global catalog resource records: ERROR (GetCloudResources): Failed to decode the result from cloud notifications API: XXX`

`XXX` will provide additional information about the parse error.  Attempt to run the following curl command:

`curl -G https://resource-catalog.bluemix.net/api/v1?languages=%2A`

Note the response.  Reassign the PagerDuty incident to `tip-api-platform level 2`.  Add any errors to the incident.


## Notes and Special Considerations

### Viewing Logs

Unfortunately at this time, our logDNA solution is not complete.  logDNA is dropping data after the data limit has been reached.  Therefore it will be necessary to find the system manually via kubectrl commands.

Examination of the logs from the notification adapter container should provide a clue.  Issue command such as:
```
kubectl logs api-pnp-notifications-adapter-645c8bfb9f-88m87 -c api-pnp-notifications-adapter
```

Where `api-pnp-notifications-adapter-645c8bfb9f-88m87` is the pod name of the notification-adapter.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

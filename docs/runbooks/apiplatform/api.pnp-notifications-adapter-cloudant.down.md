---
layout: default
title: "API Platform - PnP Notifications Adapter Cloudant Errors"
type: Alert
runbook-name: "api.pnp-notifications-adapter-cloudant.down"
description: "Addresses issues with Cloudant as it pertains to the Notifications Adapter."
service: tip-api-platform
tags: pnp, apis, notifications, cloudant
link: /apiplatform/api.pnp-notifications-adapter-cloudant.down.html   
---

## Purpose
The pnp-notification-cloudant-GetNotifications transaction provides information about transactions with the cloudant database used to retrieve Announcement and Security Notice notifications. An error with this transaction indicates that the cloudant database cannot be reached or the data being returned is not in the expected format.

This alert applies to:
- Service now incidents with a title: `api-pnp-notifications-adapter failed in Cloudant database query` or `api-pnp-notifications-adapter failed in parsing records from Cloudant`
- New Relic incidents with the title containing text: `api-pnp-notif-adapter_cloudantDBFail` or `api-pnp-notif-adapter_parseCloudantFail`

Notice that the cloudant database is *only* used for Announcements and Security Notifications.  Notifications such as incident (aka BSPN) and maintenance (aka change) are retrieved from other locations.  Incident notifications come from ServiceNow, and maintenance notifications come from RTC or ServiceNow (eventually all maintenance notifications will come from ServiceNow as the transition to ServiceNow proceeds).  For this alert, you are not concerned with maintenance or incident notifications.

## Technical Details
The cloudant database is the same one that the original bluemix status page uses.  For PnP, we use this cloudant database to pull 2 of the 4 different kinds of notifications.  There are two associated error columns in New Relic that can indication trouble:

- pnp-db-failed - indicates there was a failure during the request to the database. This is more likely that there is a networking issue.  However, there could also be an issue with authorization or the database itself could be down.
- pnp-parse-failed - indicates there was a failure trying to parse the response from the database.  More likely this is due to the database responding with some kind of error.  The less likely scenario is that database has changed the format of data being returned.

Insights can be queried directly with a NRQL query such as:

For the staging environment
```
SELECT * FROM Transaction WHERE appName='api-pnp-notifications-adapter-stage'
and apiKubeClusterRegion='us-south' and `pnp-parse-failed` is true

SELECT * FROM Transaction WHERE appName='api-pnp-notifications-adapter-stage'
and apiKubeClusterRegion='us-south' and `pnp-db-failed` is true
```

For the staging environment
```
SELECT * FROM Transaction WHERE appName='api-pnp-notifications-adapter'
and apiKubeClusterRegion='us-south' and `pnp-parse-failed` is true

SELECT * FROM Transaction WHERE appName='api-pnp-notifications-adapter'
and apiKubeClusterRegion='us-south' and `pnp-db-failed` is true
```

## User Impact
When either of the error conditions occur (pnp-db-failed or pnp-parse-failed), as long as it is not being called when the PnP datastore is empty, then this is not a highly critical alert.  PnP does store the information for notifications in its own datastore, so it has the latest information.  If this alert is triggered, it merely means if a new notification is created, it will not be picked up by PnP.  Given that notifications are not created continuously, we will not be missing critical time-sensitive information.

The biggest impact is customer facing descriptions of announcements and security notifications will not be available for viewing on the status page.  However, this is completely unrelated to incident data which controls the status of resources on the status page.

This alert should be treated with medium priority and can be fixed during the next business day as long as this is not occurring on an initial load of the internal PnP database which would cause no announcements or security notices to be available via the PnP API.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Step 1
The first thing to check is if there is an issue with cloudant.  This can be accomplished via a few simple curl requests from anywhere that has access to the internet.

#### Command 1

Execute `Step1Command1` in https://github.ibm.com/cloud-sre/pnp-runbook-private/tree/master/api-pnp-notifications-adapter/pnp-notification-cloudant-GetNotifications


Output should be similar (not identical) to the below:

```
{"_id":"Category_PLATFORM","_rev":"14-b355198e140d0e97b4816184e7201f4a","displayName":"Platform",
"components":[{"serviceName":"console","id":"cloudoe.sop.enum.paratureCategory.literal.l133",
"displayName":"IBM Cloud Platform"},{"displayName":"IBM Cloud Kubernetes Service",
"id":"cloudoe.sop.enum.paratureCategory.literal.l185"},{"displayName":"Functions",
"id":"cloudoe.sop.enum.paratureCategory.literal.l320"},{"id":"cloudoe.sop.enum.paratureCategory.literal.l184",
"displayName":"Virtual Servers"}],"type":"Category","id":"PLATFORM"}
```

#### Command 2

Execute `Step1Command2` in https://github.ibm.com/cloud-sre/pnp-runbook-private/tree/master/api-pnp-notifications-adapter/pnp-notification-cloudant-GetNotifications


Output should be similar (not identical) to the below:

```
{"_id":"Category_RUNTIMES","_rev":"10-2b646aa034ddbbe9a4448d2969b6e4e7","displayName":"Runtimes",
"components":[{"displayName":"ASP.NET Core","id":"cloudoe.sop.enum.paratureCategory.literal.l167",
"serviceName":"dotnetcore"},{"displayName":"Go","id":"cloudoe.sop.enum.paratureCategory.literal.l162",
"serviceName":"Go"},{"serviceName":"Liberty runtime","id":"cloudoe.sop.enum.paratureCategory.literal.l10",
"displayName":"Liberty for Java"},{"id":"cloudoe.sop.enum.paratureCategory.literal.l12",
"displayName":"SDK for Node.js","serviceName":"Node.JS runtime"},
{"id":"cloudoe.sop.enum.paratureCategory.literal.l163","displayName":"PHP","serviceName":"PHP"},
{"serviceName":"Python","displayName":"Python","id":"cloudoe.sop.enum.paratureCategory.literal.l164"},
{"id":"cloudoe.sop.enum.paratureCategory.literal.l42","displayName":"Ruby",
"serviceName":"Ruby(Rails) runtime"},{"displayName":"Ruby Sinatra",
"id":"cloudoe.sop.enum.paratureCategory.literal.l43"},{"serviceName":"Swift",
"id":"cloudoe.sop.enum.paratureCategory.literal.l321","displayName":"Runtime for Swift"},
{"serviceName":"Java(Tomcat) runtime","id":"cloudoe.sop.enum.paratureCategory.literal.l46",
"displayName":"Tomcat"},{"serviceName":"XPages","displayName":"XPages",
"id":"cloudoe.sop.enum.paratureCategory.literal.l215"}],"type":"Category","id":"RUNTIMES"}
```

#### Command 3

Execute `Step1Command3` in https://github.ibm.com/cloud-sre/pnp-runbook-private/tree/master/api-pnp-notifications-adapter/pnp-notification-cloudant-GetNotifications

The output will be very long.  The following is a sample of the beginning of the response.  The beginning of the response should be similar (not identical) to the below:

```
{"_id":"Category_SERVICES","_rev":"102-b9570f6f354a2b985b9c29f8cb78e6ae","displayName":"Services",
"components":[{"displayName":"API Connect","estado_dedicated":"APIConnect Dedicated",
"id":"cloudoe.sop.enum.paratureCategory.literal.l309","serviceName":"APIConnect"},
{"displayName":"API Harmony","id":"cloudoe.sop.enum.paratureCategory.literal.l190",
"serviceName":"apiHarmony"},{"displayName":"API Management",
"id":"cloudoe.sop.enum.paratureCategory.literal.l177"},{"displayName":"Active Deploy",
"id":"cloudoe.sop.enum.paratureCategory.literal.l216","serviceName":"activedeploy"},
{"displayName":"Activity Tracker","id":"cloudoe.sop.enum.paratureCategory.literal.l247",
"serviceName":"accessTrail"},{"displayName":"AlchemyAPI",
"id":"cloudoe.sop.enum.paratureCategory.literal.l199"},{"displayName":"Alert Notification",
"id":"cloudoe.  sop.enum.paratureCategory.literal.l251","serviceName":"alertnotification"},
{"displayName":"Analytics Engine","id":"cloudoe.sop.enum.paratureCategory.literal.l429"},
{"displayName":"Analytics Exchange","id":"cloudoe.sop.enum.paratureCategory.literal.l288"},
{"displayName":"Analytics for Apache Hadoop","id":"cloudoe.sop.enum.paratureCategory.literal.l110"},
{"displayName":"Apache Spark","id":"cloudoe.sop.enum.paratureCategory.literal.l195",
"serviceName":"spark"},{"displayName":"App Connect","id":"cloudoe.sop.enum.paratureCategory.literal.l377",
"serviceName":"AppConnect"},{"displayName":"App ID","id":"cloudoe.sop.enum. paratureCategory.literal.l157",
"serviceName":"AppID"},{"displayName":"App Launch","id":"cloudoe.sop.enum.paratureCategory.literal.l448",
"serviceName":"AppLaunch"},{"displayName":"Application Security Manager",    
"id":"cloudoe.sop.enum.paratureCategory.literal.l205"},{"displayName":"Application Security on Cloud",
"id":"cloudoe.sop.enum.paratureCategory.literal.l249","serviceName":"Application Security on Cloud"},
{"displayName":"Auto-Scaling","estado_dedicated":"Auto-Scaling-dedicated",
"id":"cloudoe.sop.enum.paratureCategory.literal.l24","serviceName":"Auto-Scaling"},
{"displayName":"Automated Accessibility Tester","id":"cloudoe.sop.enum.paratureCategory.literal.l228",
"serviceName":"ecs-dashboard"},{"displayName":"Availability Monitoring",
"id":"cloudoe.sop.enum.paratureCategory.literal.l308","serviceName":"AvailabilityMonitoring"},
{"displayName":"BigInsights for Apache Hadoop","id":"cloudoe.sop.enum.paratureCategory.literal.l136"},
{"displayName":"BlazeMeter","id":"cloudoe.sop.enum.paratureCategory.literal.l122"},  
{"displayName":"Block Storage","id":"cloudoe.sop.enum.paratureCategory.literal.l254"},
```

#### Command 4

Execute `Step1Command4` in https://github.ibm.com/cloud-sre/pnp-runbook-private/tree/master/api-pnp-notifications-adapter/pnp-notification-cloudant-GetNotifications

The output will be very long.  The following is a sample of the top few lines as an example.  The first few lines of output should be similar (not identical) to the below:

```
{"total_rows":1836,"offset":0,"rows":[
 {"id":"Hexadecimal Value Here","key":"Hexadecimal Value Here",
 "value":{"rev":"1-acb188f25c25cded04eef57cde1f0b7b"},
 "doc":{"_id":"HexadecimalValueHere","_rev":"1-acb188f25c25cded04eef57cde1f0b7b",
 "title":"Announcement: The Liberty for Java V3.26 buildpack is now available",
 "type":"ANNOUNCEMENT","text":"<b>Update Description</b>: This buildpack provides the following code  
 releases:\n<ul>\n<li><a href=\"https://developer.ibm.com/wasdev/\">2018.10.0.0 Liberty monthly Beta
 release</a></li>\n<li><a href=\"https://developer.ibm.com/javasdk/2018/10/02/ibm-sdk-java-technology-edition-
 version-8-service-refresh-5-fix-pack-22/\">Java Runtime Environment (JRE) for IBM Version 8 Service Refresh 5
 Fix Pack 22</a></li>\n</ul>\n<b>User Impact Description</b>: An existing application will not be       
 affected by the new buildpack until you redeploy it. After your redeploy, existing applications
 should continue to run \"as is\" without any additional changes. New applications will automatically use
 the new     buildpack.","category":"RUNTIMES","subCategory":"cloudoe.sop.enum.paratureCategory.literal.l10",
 "regionsAffected":[{"id":"AU-SYD"},{"id":"EU-DE"},{"id":"EU-GB"},{"id":"US-EAST"},{"id":"US-SOUTH"}],
 "archived":false,"eventTime":{"start":"2018-10-30T15:42:46.580Z"},
 "creation":{"time":"2018-10-30T16:02:24.304Z","email":"wkwentw@us.ibm.com"},
 "lastUpdate":{"time":"2018-10-30T16:02:24.304Z","email":"wkwentw@us.ibm.com"}}},
 {"id":"Hexadecimal Value Here","key":"Hexadecimal Value Here",
 "value":{"rev":"3-3483763c22b95e00dd031601bb892168"},
 "doc":{"_id":"HexadecimalValueHere","_rev":"3-3483763c22b95e00dd031601bb892168",
 "title":"Maintenance: Deploy API Connect service updates","type":"MAINTENANCE",
 "text":"Update now scheduled for 11/21/2016, 20:00 UTC\n<br><br>\n<b>Update Description</b>: API    
 Connect will be upgraded from version 5040 to version 5050.\n<br><br>\n<b>Disruptive Impact</b>:
 Yes\n<br><br>\n<b>Type of Disruption</b>: Console access, application management, existing service
 instances, and   provisioning new service instances\n<br><br>\n<b>Disruptive Description</b>: This
 disruption of service will block the end user from accessing the API designer and the user interface.
 This outage will not impact  the consumption of the published APIs. During the outage, you will be
 unable to provision new service instances, log in to the API designer, or launch the management console
 for existing instances. APIs and       Applications that are already running will be unaffected.\n<br>
 <br>\n<b>Disruption Duration</b>: 60 minutes\n<br><br>\n<b>Change Description</b>: The changes include
 improvements to service quality, usability,    serviceability, and reliability. New features
 include:\n<ul>\n<li>Spaces support on a catalog, which allows different groups to syndicate APIs and
 products to a common catalog</li>\n<li>Secure Gateway Tech        Preview, which leverages on-premises
 API resources through API Connect with Secure Gateway</li>\n</ul>\n<b>User Roles Impacted</b>:
 Developers and administrators\n<br><br>\n<b>Areas of User Impact</b>: User       interface, creating
 new service instances, catalog, and existing service instances\n<br><br>\n<b>Types of User
 Impact</b>: New functionality, usability, quality, serviceability, and                                
 reliability\n<br><br>\n<b>User Impact Description</b>: After the upgrade is complete, there will not be
 any actions for you to complete.","category":"SERVICES","subCategory":"cloudoe.sop.enum.paratureCategory.literal.l309",
 "regionsAffected":[{"id":"EU-GB"}],"url":"","archived":true,"alerts":"",
 "eventTime":{"start":"2016-11-21T20:00:00.000Z","end":"2016-11-21T23:00:00.000Z"},
 "creation":{"time":"2016-11-16T20:42:49.815Z","email":"wkwentw@us.ibm.com"},
 "lastUpdate":{"time":"2017-02-20T00:30:02.001Z","email":"Notification-Archive-Bot"}}},
 {"id":"Hexadecimal Value Here","key":"Hexadecimal Value Here",
 "value":{"rev":"1-ce8032a3179fa9229e23bedb4db03d33"},"doc":{"_id":"HexadecimalValueHere",
 80_rev":"1-                    ce8032a3179fa9229e23bedb4db03d33","title":"Security Bulletin: Potential
 spoofing attack in Liberty for Java for IBM Cloud (CVE-2017-1788)","type":"SECURITY",
 "text":"There is a potential spoofing attack in         WebSphere Application Server using Form
 Login.\n<br><br>\nA user action is needed to update Liberty for Java for IBM Cloud.\n<br>
 <br>\nFor more information, see the <u><a href=\"http://www.ibm.com/support/        
 docview.wss?uid=swg22015292\"target=\"_blank\">security bulletin</a></u>.",
 "category":"RUNTIMES","subCategory":"cloudoe.sop.enum.paratureCategory.literal.l10",
 "regionsAffected":[{"id":"AU-SYD"},{"id":"EU-DE"},    {"id":"EU-GB"},{"id":"US-EAST"},
 {"id":"US-SOUTH"}],"archived":false,"eventTime":{"start":"2018-04-04T20:41:58.276Z"},
 "creation":{"time":"2018-04-04T20:44:05.992Z","email":"wkwentw@us.ibm.com"},
 "lastUpdate":       {"time":"2018-04-04T20:44:05.992Z","email":"wkwentw@us.ibm.com"}}},
 {"id":"Hexadecimal Value Here","key":Hexadecimal Value Here",
 "value":{"rev":"2-462c0750e577ce0e97f9d1d716bf1caf"},
 "doc":{"_id":"Hexadecimal Value Here","_rev":"2-462c0750e577ce0e97f9d1d716bf1caf",
 "title":"Maintenance: Streaming Analytics service","type":"MAINTENANCE",
 "text":"<b>Update Description</b>: The Streaming Analytics service will undergo scheduled
 maintenance to   apply operating system security patches and a fix pack to the Streams
 product.\n<br><br>\n<b>Maintenance Duration:</b> 60 minutes\n<br><br>\n<b>Type of
 Disruption</b>: Console access, running applications,        application management, existing
 service instances, and provisioning new service instances\n<br><br>\n<b>Disruptive
 Description</b>: During this maintenance period, all instances of the Streaming Analytics        
 service will be stopped and the service will be unavailable.\n<br><br>\n
 <b>Disruption Duration</b>: 60 minutes\n<br><br>\n<b>Customer Action Description</b>:
 You must restart your Streaming Analytics service      instances and resubmit your applications.",
 "category":"SERVICES","subCategory":"cloudoe.sop.enum.paratureCategory.literal.l224",
 "regionsAffected":[{"id":"EU-GB"}],"url":"","archived":true,
 "eventTime":{"start":    "2017-04-13T19:00:00.000Z","end":"2017-04-13T20:00:00.000Z"},
 "creation":{"time":"2017-04-12T17:50:24.963Z","email":"wkwentw@us.ibm.com"},"alerts":"",
 "lastUpdate":{"time":"2017-07-14T00:30:01.001Z","email":        "Notification-Archive-Bot"}}},
```

#### Operator Response

If no error above, proceed to Step 2.

If there is a failure in the above curl commands, it means there is potentially one of three problems:

1. A cloudant problem: an issue should be raised with the cloudant team.  Likely there already is, but would be good to check.  See "Opening an issue with the Cloudant team" below.
2. Possible network issue: Potentially there is a problem reaching the cloudant endpoints.  See "Opening an issue with the Cloudant team" below.
3. There is an authorization issue: Potentially the credentials being used have expired or have been changed for cloudant.  The console team needs to be contacted as they originally owned the database. ({{site.data[site.target].oss-contacts.contacts.notifications-cloudant-owner.userid}})

The above issues can be distinguished through examination of the response received from the failing curl command.

In the case of a parse error, the above curl commands will work, but upon examination of the returned data, there is a difference in the json format, then this indicates a change in the cloudant implementation.  The cloudant (or console team) should be contacted to verify that the data formats have changed.  Code changes will be required by PnP to adapt.  

Examination of the logs from the notification adapter container should provide a clue.  See the "Viewing Logs" section below for more information.

Look for a message like:
```
ERROR (cloudant.api.GetNotifications): Failed to decode the result from Cloudant: XXX
```
where XXX will contain the parse error information.


### Step 2

If the curl commands in Step 1 are all successful and the data formats match, then the error could be due to connection problems from the notification adapter container to cloudant.  To test this, log directly into the notification-adapter container using the following command:

```
kubectl exec -it api-pnp-notifications-adapter-645c8bfb9f-88m87 -- /bin/sh
```
Of course substitute `api-pnp-notifications-adapter-645c8bfb9f-88m87` with the actual name of the notifications-adapter pod. Then issue the above curl commands.  If curl does not exist, it can be added via the following command:
```
apk --update add curl
```

Follow the same commands as outlined in Step 1 to see if there is an issue from the container.

#### Operator Response

If no error above, proceed to Step 3.

If the same curl commands that succeeded in Step 1 failed in this step, then there is a specific connection error between our armada containers and cloudant.
This indicates an environmental problem such as a possible network issue.  The foundation team should be engaged.  See [Contacting TF](ibm/Contact_Technical_Foundation.html)

### Step 3

If all of the above tests work, then the logs should be checked to see what error may exist.  In the log files, please look for any text such as "ERROR" to see if there is an error indication that shows the problem.  Possible errors:

```
ERROR (cloudant.api.GetNotifications)->(utils/GetFromCloudant): Failed to get data from cloudant: Get ${URL}: ${ERROR}
```

Indicates that the connection to cloudant failed.  
- ${URL} will be replaced with the actual URL that was attempted.  Verify that this URL matches the URLs above.  If it does not match, please reassign the PagerDuty incident to `tip-api-platform level 2` to request an update to the environment variable for the cloudant URL in the deployment and redeploy the module.  The Notifications URL is controlled by the environment variable: PNP_NOTIFICATIONS_URL
- ${ERROR} will be replaced with error text received by the code

```
ERROR (cloudant.api.GetNotifications): Failed to decode the result from Cloudant: invalid character 'H' looking for beginning of value
```

In this error, the portion after the `:` indicates the problem with the parse.  Many times you will get an error such as above which mean the parser hit an unexpected character.  Typically this is because JSON was not received.  JSON mostly is not received if an error is returned by the server.  This case should have been caught by the curl tests above.

Reassign the PagerDuty incident to `tip-api-platform level 2`. Note all error responses in the corresponding ServiceNow incident.

## Notes and Special Considerations

### Viewing Logs

Unfortunately at this time, our logDNA solution is not complete.  logDNA is dropping data after the data limit has been reached.  Therefore it will be necessary to find the system manually via kubectrl commands.

Examination of the logs from the notification adapter container should provide a clue.  Issue command such as:
```
kubectl logs api-pnp-notifications-adapter-645c8bfb9f-88m87 -c api-pnp-notifications-adapter
```

Where `api-pnp-notifications-adapter-645c8bfb9f-88m87` is the pod name of the notification-adapter.  It's recommended to use `--tail` to limit the output or pipe the output through grep.

### Opening an issue with the Cloudant team
A Severity 2 incident should be opened in ServiceNow against the configuration item `cloudantnosqldb`.  Do not directly include the above URLs in the ticket as they are sensitive credential information.

## OSS Links
[{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}]({{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}})

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

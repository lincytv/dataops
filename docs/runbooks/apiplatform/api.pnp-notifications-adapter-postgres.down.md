---
layout: default
title: "API Platform - PnP Notifications Adapter Postgres Errors"
type: Alert
runbook-name: "api.pnp-notifications-adapter-postgres.down"
description: "Runbook to drill into errors related to Postgres via the Notifications Adapter"
service: tip-api-platform
tags: pnp, apis, notifications, postgres
link: /apiplatform/api.pnp-notifications-adapter-postgres.down.html   
---

## Purpose
The purpose of the pnp-notification-postgres-GetNotifications transaction is to provide information about transactions with the internal PnP postgres database.  The postgres database is where all notifications get stored.

This alert applies to:
- Service now incidents with a title: `api-pnp-notifications-adapter failed in Postgres database query` or `api-pnp-notifications-adapter failed in parsing records from Postgres`
- New Relic incidents with the title containing text: `api-pnp-notif-adapter_postgresDBFail` or `api-pnp-notif-adapter_parsePostgresFail`

## Technical Details
Two types of error may occur in this transaction:

- pnp-db-failed - indicates there was a failure during the request to the database.  This means that there is a problem with the postgres database.
- pnp-parse-failed - indicates there was a failure trying to parse the response from the database. This means that there was a problem parsing the response from the postgres database.  The reality is the only time this will occur is if the HTTP request to the postgres database fails because actual changes in what postgres sends back should be caught at development time.

## User Impact
When either of the error conditions occur (pnp-db-failed or pnp-parse-failed), then there is an issue acquiring notification data from the postgres database.  The reason that the adapter queries the postgres database is to look for existing notifications to determine if an update is required for a new notification.  The default behavior of the notification adapter when this occurs is to not process the notifications in order to avoid unnecessary spamming of subscribed clients.  This is a reasonable action to take because the notifications adapter will retry sending the notifications on the next interval which is typically 1 hour.  The situation with postgres may likely resolve and the notifications will flow normally.

Please note that the notification adapter only handles announcements and security notices.  These are not published frequently.

Errors with this alert should be treated with medium priority because subscribers will not receive new notifications until the problem has been cleared up; however this is not viewed as critical.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Step 1

Look in the log to get any additional details on the error. (See "Viewing Logs" section below)

`INFO: GetAllNotifications: recieved error XXX`

Where `XXX` will be additional error information.  This information will be provided when the DB failure alert is provided.


`INFO: GetAllNotifications: recieved HTTP error XXX - trying to continue`

Where `XXX` is the HTTP error code received from the postgres database.

#### Operator Response

The above is just some fact finding to use in Step 2.  Proceed to step 2.

### Step 2

This is indicating an issue with postgres; therefore, at this time the postgres runbooks should be used for further work.

#### Operator Response

The operator should look for alerts pertaining to postgres.  The following runbooks should be consulted to dive into postgres issues.

- [Postres down Runbook](api.postgres.down.html)

## Notes and Special Considerations

### Viewing Logs

Unfortunately at this time, our logDNA solution is not complete.  logDNA is dropping data after the data limit has been reached.  Therefore it will be necessary to find the system manually via kubectrl commands.

Examination of the logs from the notification adapter container should provide a clue.  Issue command such as:
```
kubectl logs api-pnp-notifications-adapter-645c8bfb9f-88m87 -c api-pnp-notifications-adapter
```

Where `api-pnp-notifications-adapter-645c8bfb9f-88m87` is the pod name of the notification-adapter.

## OSS Links

[OSS Logging in Armada]({{site.data[site.target].oss-apiplatform.links.oss-logging-armada.link}})

[Load Balance for OSS in Armada]({{site.data[site.target].oss-apiplatform.links.oss-lb-armada.link}})

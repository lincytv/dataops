---
layout: default
title: "IAM health check failed"
type: Alert
runbook-name: "api.iam-authorize_iamHealthCheckFailure"
description: "This alert will be triggered when an IAM health check fails"
service: tip-api-platform
tags: iam, breakglass
link: /apiplatform/api.iam-authorize_iamHealthCheckFailure.html
---

## Purpose
This alert is triggered when the IAM health check running within a pod detects that IAM is down. This alert indicates that we have entered IAM break glass mode.

## Technical Details
The IAM health check runs in a number of microservice pods. The IAM health check attempts to obtain an IAM token from an IAM API key, and then attempts to validate the IAM token. If there is one failed attempt, one of the following alerts will fire depending on the environment:

- Production ([oss_iam_health_prd](https://one.newrelic.com/launcher/nrai.launcher?pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjExMDc4NTUifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ&platform[accountId]=1387904) policy for TIP services and [oss_iam_health_prd](https://one.newrelic.com/launcher/nrai.launcher?pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjEwMDU4NTUifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ&platform[accountId]=1926897) policy for all other services):

  - iam-authorize_iamHealthCheckFailure:eu-de:1:prod
  - iam-authorize_iamHealthCheckFailure:us-east:1:prod
  - iam-authorize_iamHealthCheckFailure:us-south:1:prod

- Staging ([oss_iam_health_stg](https://one.newrelic.com/launcher/nrai.launcher?pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjExMDc4MDkifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ&platform[accountId]=1387904) policy for TIP services and [oss_iam_health_stg](https://one.newrelic.com/launcher/nrai.launcher?pane=eyJuZXJkbGV0SWQiOiJhbGVydGluZy11aS1jbGFzc2ljLnBvbGljaWVzIiwibmF2IjoiUG9saWNpZXMiLCJwb2xpY3lJZCI6IjEwMDYxNjcifQ&sidebars[0]=eyJuZXJkbGV0SWQiOiJucmFpLm5hdmlnYXRpb24tYmFyIiwibmF2IjoiUG9saWNpZXMifQ&platform[accountId]=1926897) policy for all other services):

   - iam-authorize_iamHealthCheckFailure:eu-de:1:stg
   - iam-authorize_iamHealthCheckFailure:us-east:1:stg
   - iam-authorize_iamHealthCheckFailure:us-south:1:stg

The [IAM Health Monitor](https://insights.newrelic.com/accounts/1387904/dashboards/1459667) New Relic dashboard for TIP services and the [IAM Health Monitor](https://insights.newrelic.com/accounts/1926897/dashboards/1452859) New Relic dashboard for PnP services and API services have details about narrowing down the source service (microservice) where the IAM health check is failing.

The two New Relic dashboards also provide information for:
- Health check triggered and IAM is down (see number of break glass hits and misses)
- Health check triggered and IAM is up (no action needed)
- Status of IAM break glass retrieving and storing data in Elasticsearch

## User Impact
If IAM is unhealthy, the OSS APIs will no longer be able to authorize users using IAM. In this case, the OSS APIs move into IAM break glass mode where only IAM API keys or IAM tokens previously seen by the OSS API in the last 60 days will be authorized to continue. This means that some services may no longer be able to call OSS APIs.

## Instructions to Fix
1. In general, no action is needed other than monitoring the alerts to ensure they automatically close. If the alerts do not close automatically for hours, proceed to the next step.
2. Check [New Relic status page](https://status.newrelic.com/) to see if there is an ongoing outage or maintenance. The alerts may be a false alarm.
3. Confirm that there is a real problem by:
   1. For `iamHealthCheckFailure` alerts, check the [IAM Health Monitor](https://insights.newrelic.com/accounts/1387904/dashboards/1459667) New Relic dashboard for TIP services and the [IAM Health Monitor](https://insights.newrelic.com/accounts/1926897/dashboards/1452859) New Relic dashboard for PnP services and API services. Make sure you are looking at the right one. For detailed breakdown of the dashboards, please refer to New Relic dashboard breakdown section below.
   2. If the *Health check triggered (IAM is down)* chart at the top of the dashboards is showing data persistently and the `RESULTS` column is showing a number `> 5`, there is a possibility that IAM is down or has connectivity issue in the environment and in the region specified. If the `RESULTS` number is decreasing or there is no incoming data on the *Number of break glass hits(or misses) in dev/staging/prod* graph, IAM is recovering and alerts will automatically close soon.
   3. Error information is also available in logDNA if needed. Check logDNA in the specified region and search for `MonitorIAMUntilHealthy` for `health = false` results. If the unhealthy search result persists, IAM is either down or having connectivity issue.
4. Check the [#iam-issues](https://ibm-cloudplatform.slack.com/archives/C3C46LY7N) and [#iam-cie](https://ibm-cloudplatform.slack.com/archives/C5T7AUCKD) Slack channels to see if there is an IAM CIE occurring.
5. If there is an active IAM CIE, open our own CIE if our users are reporting problems (i.e. the IAM break glass is insufficient). Tip: the *Services with break glass misses* charts in the New Relic dashboards provide information on cache misses. Cache miss means that users cannot be authorized when break glass cache is in use since authorization data requested is not found in the break glass cache. The more cache misses, the more users fail to get authorized.
6. If there is not an active IAM CIE, ask on the [#iam-issues](https://ibm-cloudplatform.slack.com/archives/C3C46LY7N) Slack channel whether there is an ongoing problem.
7. Monitor the root problem (IAM or other).
8. If the alerts do not automatically close themselves for hours, please contact Shane Cartledge or Rui Sun.

## New Relic dashboard breakdown
```
IAM Health Monitor dashboard
│
└─── Health check triggered (IAM is down) - Running in IAM break glass mode. See break glass hits(users can be authorized) and misses(users cannot be authorized) graphs. 
│   │   Hit: user record is cached and user can be authorized
│   │   Miss: user record is not cached and user cannot be authorized
│   │
│   └─── Services with break glass hits
│   │       Number of break glass hits in prod 
│   │       Number of break glass hits in staging
│   │       Number of break glass hits in dev
│   │       Services with break glass hits in prod 
│   │       Services with break glass hits in staging
│   │       Services with break glass hits in dev
│   │
│   └─── Services with break glass misses 
│           Number of break glass misses in prod 
│           Number of break glass misses in staging
│           Number of break glass misses in dev
│           Services with break glass misses in prod
│           Services with break glass misses in staging
│           Services with break glass misses in dev
│   
└─── Health check triggered (IAM is up) - No action needed.
│   │   Health check triggered in prod
│   │   Health check triggered in staging
│   │   Health check triggered in dev
│   │   Prod liveness
│   │   Staging liveness
│   │   Dev liveness
│   │   Note: for the above 6 graphs, data is in place only when health check is triggered.
│   │   
│   └─── Services with functional IAM
│           Services with functional IAM in prod
│           Services with functional IAM in staging
│           Services with functional IAM in dev
│
└─── Status of IAM break glass retrieving and storing data in Elasticsearch - No alerts involved.
        syncWithElasticsearch - retrieve data
        AddAuthorization - store API key data
        AddUser - store token data
        Note: pay attention to failures.
```

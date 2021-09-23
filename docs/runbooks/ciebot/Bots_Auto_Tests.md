---
layout: default
description: CIEBOT and GOBOT monitor policy, notification, and automated test cases
title: Monitor CIEBOT and GOBOT in New Relic
service: ciebot
runbook-name: CIEBOT and GOBOT Monitoring
tags: oss, ciebot
link: /ciebot/Bots_Auto_Tests.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}


## Purpose
This is a summary of automatic test cases for ciebot and gobot, and the New Relic policies and notification settings.

- The production **ciebot** is set to aoutomatically HA & LB, therefore each instance in each region needs to be continuously tested.
- The production **gobot** is set to manuall HA & LB when needed, therefore each instance in each region needs to be continuously tested.
- The staging **cietest1** is set to mimic **ciebot** and **gobot**, therefore each instance in each region needs to be continuously tested.
- Most staging and dev services are being continuously tested.

## Policies and Notifications

| NR Policy                  | Bots & functions tested | Notification channels                                     |
|:---------------------------|:------------------------|:----------------------------------------------------------|
|[ciebot-prd-availability](https://one.nr/0JBQrxNk6RZ)| **ciebot** | [ciebot-prd-availibility](https://one.nr/0dOQMkA8eRG) |
|[ciebot-stg-availability](https://one.nr/0kERzoYYEjr)| **cietest** | [ciebot-stg-availibility](https://one.nr/0nVjY6MXXQ0) |
|[ciebot prod policy](https://one.nr/0PLREAnyrRa)| **ciebot** and **ciebotwdp** | [ciebot_prod_webhook](https://one.nr/0LkjnYz70Ro), [Incidents to Insight](https://one.nr/0PLREo9eqQa), [tip-api-platform Pager Duty Service](https://one.nr/08dQe1zyDQe), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), and other slack channels, developer emails |
|[ciebot stage policy](https://one.nr/06vjAoNAvwP)| **cietest** and ciebot-related tests for **cietest1** | [ciebot_stage_webhook](https://one.nr/0xZw0D033wv), [Incidents to Insight](https://one.nr/0PLREo9eqQa), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), developer emails |
|[ciebot dev policy](https://one.nr/0e1wZK8G4R6)| ciebot-related tests for **cietdev1** |[Incidents to Insight](https://one.nr/0PLREo9eqQa), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), developer emails |
|[gobot prod policy](https://one.nr/0xZw0ZeBpjv)| **gobot** | [gobot_prod_webhook](https://one.nr/0mMRNEBqKwn), [Incidents to Insight](https://one.nr/0PLREo9eqQa), [tip-api-platform Pager Duty Service](https://one.nr/08dQe1zyDQe), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), and other slack channels, developer emails |
|[gobot stage policy](https://one.nr/0EPwJpPNBj7)| gobot-related tests for **cietest1** | [gobot_stage_webhook](https://one.nr/0PoR8AMqYjG), [Incidents to Insight](https://one.nr/0PLREo9eqQa), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), developer emails |
|[gobot dev policy](https://one.nr/0eqwyD91mQn)| gobot-related tests for **cietdev1**| [Incidents to Insight](https://one.nr/0PLREo9eqQa), [#bot-nr-alerts](https://ibm-cloudplatform.slack.com/archives/C016Q81A7S9), developer emails      |

|Webhook setting       | Severity | Pager |
|-----------------------|----------|-------|
| [ciebot-prd-availibility](https://one.nr/0dOQMkA8eRG) | N/A | N/A  |
| [ciebot_prod_webhook](https://one.nr/0LkjnYz70Ro)  | 1 | true  |
| [ciebot_stage_webhook](https://one.nr/0xZw0D033wv) | 2 | true  |
| [gobot prod policy](https://one.nr/0xZw0ZeBpjv)    | 2 | true  |
| [gobot_stage_webhook](https://one.nr/0PoR8AMqYjG)  | 3 | false |


## Test Cases

Each bot is subject to following types of tests:

- End-to-End test for global and send availability data to scorecard: invoke the *help* command, see response in Slack channel [bot-liveliness](https://ibm-cloudplatform.slack.com/archives/C01QPPBBQG2)
- Send regional availability data to Scorecard for critical services: policy [ciebot-prd-availability](https://one.nr/0JBQrxNk6RZ) 
- Rabbit MQ queue status: synthetic ping test the to RMQ queue for the bot
- Slack-consumer URL health: ping the URL
- Incoming-webhook URL health: ping the URL
- Micro-service heartbeat: run NRQL to query heartbeat count


### End-to-end tests

Use the bot cietest1 to test bots by invoking the "help" command, check response content and time.
See [test script](https://github.ibm.com/aria/bot-monitor/blob/master/scripts/e2e.sh).
Using EDB map integrated with TIP, the script:
- run the test
- send result to EDM
- raise alert when conditions are met.


### RabbitMQ Queue tests

Test the RabbitMQ queues in each region.

Policy Name         | Region    | Queue used by           | Testcase                          |
------------------- |:----------|:------------------------|:----------------------------------|
ciebot-prod-policy  | US East   | ciebotwdp, ciebot, gobot|[prd-us-east-rabbitmq-queue-check](https://one.nr/0xZw0ZyPpjv)|
ciebot-prod-policy  | US South  | ciebot, gobot           |[prd-us-south-rabbitmq-queue-check](https://one.nr/04ERPpB2GRW)|
ciebot-prod-policy  | EU DE     | ciebot, gobot           |[prd-eu-de-rabbitmq-queue-check](https://one.nr/0NgR7nZZ9wo)|
ciebot-stage-policy | US East   | cietest, cietest1       |[stage-us-east-rabbitmq-queue-check](https://one.nr/0Y8wp2odzjO)|
ciebot-stage-policy | US South  | cietest1                |[stage-us-south-rabbitmq-queue-check](https://one.nr/0x0jl0PNBjW)|
ciebot-stage-policy | EU DE     | cietest1                |[stage-eu-de-rabbitmq-queue-check](https://one.nr/0a2wdvYGXjE)|
ciebot-dev-policy   | US East   | ciedev1                 |[dev-us-east-rabbitmq-queue-check](https://one.nr/04ERPpEk6RW)|





### Production slack consumer URL tests

Test the slack consumer of each production bot in each region.

Policy Name        | Monitored URL                                                      | New Relic Monitor Name and Link  |
-------------------|:-------------------------------------------------------------------|:---------------------------------|
ciebot-prod-policy | https://us-east.pnp-api-oss.cloud.ibm.com/ciebot-consumer/healthz  | [ciebot-us-east-prod-consumer](https://one.nr/0YBR6vLxdRO) |
ciebot-prod-policy | https://us-south.pnp-api-oss.cloud.ibm.com/ciebot-consumer/healthz | [ciebot-us-south-prod-consumer](https://one.nr/0Zyw4YMYmR3) |
ciebot-prod-policy | https://eu-de.pnp-api-oss.cloud.ibm.com/ciebot-consumer/healthz    | [ciebot-eu-de-prod-consumer](https://one.nr/0x0jl0L0BjW) |
gobot-prod-policy  | https://us-east.pnp-api-oss.cloud.ibm.com/gobot-consumer/healthz   | [gobot-us-east-prod-consumer](https://one.nr/0NgR7ne1kwo) |
gobot-prod-policy  | https://us-south.pnp-api-oss.cloud.ibm.com/gobot-consumer/healthz  | [gobot-us-south-prod-consumer](https://one.nr/0LkjnLG4awo) |
gobot-prod-policy  | https://eu-de.pnp-api-oss.cloud.ibm.com/gobot-consumer/healthz     | [gobot-eu-de-prod-consumer](https://one.nr/0oqQapLWZj1) |



### Staging slack consumer URL tests

Test the slack consumer of each production bot in each region.

Policy Name         | Monitored URL                                                            | New Relic Monitor Name and Link  |
--------------------|:-------------------------------------------------------------------------|:---------------------------------|
ciebot-stage-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/cietest1-consumer/healthz | [cietest1-us-east-stage-consumer](https://one.nr/0a2wdvEVpjE) |
ciebot-stage-policy | https://us-south.pnp-api-oss.test.cloud.ibm.com/cietest1-consumer/healthz| [cietest1-us-south-stage-consumer](https://one.nr/037jbM7pkRy) |
ciebot-stage-policy | https://eu-de.pnp-api-oss.test.cloud.ibm.com/cietest1-consumer/healthz   | [cietest1-eu-de-stage-consumer](https://one.nr/0LkjnLlYYwo) |
ciebot-stage-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/cietest-consumer/healthz  | [cietest-us-east-stage-consumer](https://one.nr/0PLREAno5Ra) |



### Dev slack consumer URL tests

Test the slack consumer of each production bot in each region.

Policy Name       | Monitored URL                                                           | New Relic Monitor Name and Link|
------------------|:------------------------------------------------------------------------|:-------------------------------|
ciebot-dev-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/ciedev1-consumer/healthz | [ciedev1-us-east-dev-consumer](https://one.nr/0dOQMObB9RG) |



### Production incoming webhook URL tests

Test the incoming-webhooks-app of each production bot in each region.

Policy Name        | Monitored URL                                             | New Relic Monitor Name and Link |
-------------------|:----------------------------------------------------------|:--------------------------------|
ciebot-prod-policy | https://us-east.pnp-api-oss.cloud.ibm.com/ciebot/healthz  | [ciebot-us-east-prod-webhooks](https://one.nr/0kLwGL0GvR6) |
ciebot-prod-policy | https://us-south.pnp-api-oss.cloud.ibm.com/ciebot/healthz | [ciebot-us-south-prod-webhooks](https://one.nr/0gbRK90bzQE) |
ciebot-prod-policy | https://eu-de.pnp-api-oss.cloud.ibm.com/ciebot/healthz    | [ciebot-eu-de-prod-webhooks](https://one.nr/0eqwyDG2dQn) |
gobot-prod-policy  | https://us-east.pnp-api-oss.cloud.ibm.com/gobot/healthz   | [gobot-us-east-prod-webhooks](https://one.nr/0Z2R5AEZ0Rb) |
gobot-prod-policy  | https://us-south.pnp-api-oss.cloud.ibm.com/gobot/healthz  | [gobot-us-south-prod-webhooks](https://one.nr/0oqQapLWBj1) |
gobot-prod-policy  | https://eu-de.pnp-api-oss.cloud.ibm.com/gobot/healthz     | [gobot-eu-de-prod-webhooks](https://one.nr/0LkjnLG4Jwo) |



### Staging incoming webhook URL tests

Test the incoming-webhooks-app of each staging bot in each region.

Policy Name         | Monitored URL                                                   | New Relic Monitor Name and Link  |
--------------------|:----------------------------------------------------------------|:---------------------------------|
ciebot-stage-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/cietest1/healthz | [cietest1-us-east-stage-webhooks](https://one.nr/0Z2R5AJBLRb) |
ciebot-stage-policy | https://us-south.pnp-api-oss.test.cloud.ibm.com/cietest1/healthz| [cietest1-us-south-stage-webhooks](https://one.nr/0e1wZK0MKR6) |
ciebot-stage-policy | https://eu-de.pnp-api-oss.test.cloud.ibm.com/cietest1/healthz   | [cietest1-eu-de-stage-webhooks](https://one.nr/0xVwgvm2dQJ) |
ciebot-stage-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/cietest/healthz  | [cietest-us-east-stage-webhooks](https://one.nr/04ERPp0EYRW) |



### Dev incoming webhook URL tests

Test the incoming-webhooks-app of each staging bot in each region.

Policy Name       | Monitored URL                                                  | New Relic Monitor Name and Link |
------------------|:---------------------------------------------------------------|:--------------------------------|
ciebot-dev-policy | https://us-east.pnp-api-oss.test.cloud.ibm.com/ciedev1/healthz | [ciedev1-us-east-dev-webhooks](https://one.nr/0eqwyDOKAQn) |



### Heartbeats from ciebot and gobot microservices
Those "New Relic Condition Link" without a hyperlink are pods who's heartbeat are not being counted.

Policy Name         | Location | Microservice                            | New Relic Condition Link         |
--------------------|:---------|:----------------------------------------|:---------------------------------|
ciebot-prod-policy  | US East  | ciebot-handler | [prd-useast-ciebot-handler](https://one.nr/01qwLd7VWw5) |
ciebot-prod-policy  | US South | ciebot-handler | [prd-ussouth-ciebot-handler](https://one.nr/0EPwJpaWDj7) |
ciebot-prod-policy  | EU GB    | ciebot-handler | [prd-eugb-prod-ciebot-handler](https://one.nr/0X8wo1vyWjx) |
ciebot-prod-policy  | US East  | ciebotwdp-handler | [prd-useast-ciebotwdp-handler](https://one.nr/0PLREWK15Qa) |
ciebot-prod-policy  | US East  | ciebot-miscellaneous-commands-processor | [prd-useast-ciebot-miscellaneous-commands-processor](https://one.nr/0znQx34VpjV) |
ciebot-prod-policy  | US South | ciebot-miscellaneous-commands-processor | [prd-ussouth-ciebot-miscellaneous-commands-processor](https://one.nr/0a2wdVrDGjE) |
ciebot-prod-policy  | EU GB    | ciebot-miscellaneous-commands-processor | [prd-eugb-prod-ciebot-miscellaneous-commands-processor](https://one.nr/0kERzlBqEQr) |
ciebot-prod-policy  | US East  | ciebotwdp-miscellaneous-commands-processor | [prd-useast-ciebotwdp-miscellaneous-commands-processor](https://one.nr/037jbpyg9wy) |
ciebot-stage-policy | US East  | cietest-handler | [stg-useast-cietest-handler](https://one.nr/0kLwG6LqeQ6) |
ciebot-stage-policy | US east  | cietest1-handler | [stg-useast-cietest1-handler](https://one.nr/0gbRKq9PlQE) |
ciebot-stage-policy | US South | cietest1-handler | [stg-ussouth-cietest1-handler](https://one.nr/0e1wZqKnBQ6) |
ciebot-stage-policy | EU GB    | cietest1-handler | [stg-eugb-cietest1-handler](https://one.nr/0kERzl3zpQr) |
ciebot-stage-policy | US East  | cietest-miscellaneous-commands-processor | [stg-useast-cietest-miscellaneous-commands-processor](https://one.nr/0xVwgWx58wJ) |
ciebot-stage-policy | US east  | cietest1-miscellaneous-commands-processor | [stg-useast-cietest1-miscellaneous-commands-processor](https://one.nr/0eqwyekXewn) |
ciebot-stage-policy | US South | cietest1-miscellaneous-commands-processor | [stg-ussouth-cietest1-miscellaneous-commands-processor](https://one.nr/0e1wZqKnBQ6) |
ciebot-stage-policy | EU GB    | cietest1-miscellaneous-commands-processor | [stg-eugb-cietest1-miscellaneous-commands-processor](https://one.nr/0mMRNq3e7wn) |
ciebot-dev-policy   | US East  | ciedev1-handler | [dev-useast-ciedev1-handler](https://one.nr/0Z2R5AX0rRb) |
ciebot-dev-policy   | US East  | ciedev1-miscellaneous-commands-processor | [dev-useast-ciedev1-miscellaneous-commands-processor](https://one.nr/0GbRmoP5gQy) |
gobot-prod-policy   | US East  | gobot-alias-command-processor  | [prd-useast-alias-command-processor]|
gobot-prod-policy   | US South | gobot-alias-command-processor  | [prd-ussouth-alias-command-processor](https://one.nr/0GbRmoDZBQy) |
gobot-prod-policy   | EU GB    | gobot-alias-command-processor  | [prd-eugb-alias-command-processor]|
gobot-prod-policy   | US East  | gobot-dutymgr-command-processor | [prd-useast-declarative-deployment-tools]|
gobot-prod-policy   | US South | gobot-dutymgr-command-processor | [prd-ussouth-declarative-deployment-tools](dutymgr-command-processor) |
gobot-prod-policy   | EU GB    | gobot-dutymgr-command-processor | [prd-eugb-declarative-deployment-tools]|
gobot-prod-policy   | US East  | gobot-help-command-registry | [prd-useast-help-command-registry]|
gobot-prod-policy   | US South | gobot-help-command-registry | [prd-ussouth-help-command-registry](https://one.nr/0PLREWAVrQa) |
gobot-prod-policy   | EU GB    | gobot-help-command-registry | [prd-eugb-help-command-registry]|
gobot-prod-policy   | US East  | gobot-iae-handler | [prd-useast-iae-handler]|
gobot-prod-policy   | US South | gobot-iae-handler | [prd-ussouth-iae-handler](https://one.nr/0DvwBm151Qp) |
gobot-prod-policy   | EU GB    | gobot-iae-handler | [prd-eugb-iae-handler]|
gobot-prod-policy   | US East  | gobot-link-command-processor | [prd-useast-link-command-processor]|
gobot-prod-policy   | US South | gobot-link-command-processor | [prd-ussouth-link-command-processor](https://one.nr/0bEjOgenAj6) |
gobot-prod-policy   | EU GB    | gobot-link-command-processor | [prd-eugb-link-command-processor]|
gobot-prod-policy   | US East  | gobot-miscellaneous-commands-processor | [prd-useast-miscellaneous-commands-processor]|
gobot-prod-policy   | US South | gobot-miscellaneous-commands-processor | [prd-ussouth-miscellaneous-commands-processor](https://one.nr/08dQe6Vodwe) |
gobot-prod-policy   | EU GB    | gobot-miscellaneous-commands-processor | [prd-eugb-miscellaneous-commands-processor]|
gobot-prod-policy   | US East  | gobot-pagerduty-handler | [prd-useast-pagerduty-handler]|
gobot-prod-policy   | US South | gobot-pagerduty-handler | [prd-ussouth-pagerduty-handler](https://one.nr/04ERPepqgjW) |
gobot-prod-policy   | EU GB    | gobot-pagerduty-handler | [prd-eugb-pagerduty-handler]|
gobot-prod-policy   | US East  | gobot-ticket-command-processor | [prd-useast-ticket-command-processor]() |
gobot-prod-policy   | US South | gobot-ticket-command-processor | [prd-ussouth-ticket-command-processor](https://one.nr/0JBQrqKoNjZ) |
gobot-prod-policy   | EU GB    | gobot-ticket-command-processor | [prd-eugb-ticket-command-processor]|
gobot-stage-policy  | US East  | cietest1-alias-command-processor  | [prd-useast-alias-command-processor] |
gobot-stage-policy  | US South | cietest1-alias-command-processor  | [prd-ussouth-alias-command-processor](https://one.nr/0M8jqnWY1Ql) |
gobot-stage-policy  | EU GB    | cietest1-alias-command-processor  | [prd-eugb-alias-command-processor]|
gobot-stage-policy  | US East  | cietest1-dutymgr-command-processor | [prd-useast-dutymgr-command-processor]|
gobot-stage-policy  | US South | cietest1-dutymgr-command-processor | [prd-ussouth-dutymgr-command-processor](https://one.nr/0znQx3LEBjV) |
gobot-stage-policy  | EU GB    | cietest1-dutymgr-command-processor | [prd-eugb-dutymgr-command-processor]|
gobot-stage-policy  | US East  | cietest1-help-command-registry | [prd-useast-help-command-registry]|
gobot-stage-policy  | US South | cietest1-help-command-registry | [prd-ussouth-help-command-registry](https://one.nr/0NgR7DnWZjo) |
gobot-stage-policy  | EU GB    | cietest1-help-command-registry | [prd-eugb-help-command-registry] |
gobot-stage-policy  | US East  | cietest1-iae-handler | [prd-useast-iae-handler]|
gobot-stage-policy  | US South | cietest1-iae-handler | [prd-ussouth-iae-handler](https://one.nr/0oqQa3pBGR1) |
gobot-stage-policy  | EU GB    | cietest1-iae-handler | [prd-eugb-iae-handler]|
gobot-stage-policy  | US East  | cietest1-link-command-processor | [prd-useast-link-command-processor]|
gobot-stage-policy  | US South | cietest1-link-command-processor | [prd-ussouth-link-command-processor](https://one.nr/0oqQa3pW0R1) |
gobot-stage-policy  | EU GB    | cietest1-link-command-processor | [prd-eugb-link-command-processor]|
gobot-stage-policy  | US East  | cietest1-pagerduty-handler | [prd-useast-pagerduty-handler]|
gobot-stage-policy  | US South | cietest1-pagerduty-handler | [prd-ussouth-pagerduty-handler](https://one.nr/0M8jqnWX0Ql)|
gobot-stage-policy  | EU GB    | cietest1-pagerduty-handler | [prd-eugb-pagerduty-handler]|
gobot-stage-policy  | US East  | cietest1-ticket-command-processor | [prd-useast-ticket-command-processor]|
gobot-stage-policy  | US South | cietest1-ticket-command-processor | [prd-ussouth-ticket-command-processor](https://one.nr/08dQe6VAVwe) |
gobot-stage-policy  | EU GB    | cietest1-ticket-command-processor | [prd-eugb-ticket-command-processor]|
gobot-dev-policy    | US East  | ciedev1-alias-command-processor | [prd-useast-alias-command-processor](https://one.nr/0GbRmoDxNQy) |
gobot-dev-policy    | US East  | ciedev1-dutymgr-command-processor | [prd-ussouth-dutymgr-command-processor](https://one.nr/06vjAXovnRP) |
gobot-dev-policy    | US East  | ciedev1-help-command-registry | [prd-useast-help-command-registry](https://one.nr/0xVwgWvolwJ) |
gobot-dev-policy    | US East  | ciedev1-iae-handler | [prd-ussouth-iae-handler](https://one.nr/0WBQ1pAOgjx) |
gobot-dev-policy    | US East  | ciedev1-link-command-processor | [prd-useast-link-command-processor](https://one.nr/0DvwBm1vVQp) |
gobot-dev-policy    | US East  | ciedev1-pagerduty-handler | [prd-useast-pagerduty-handler](https://one.nr/0xZw06Z0pjv) |
gobot-dev-policy    | US East  | ciedev1-ticket-command-processor | [prd-ussouth-ticket-command-processor](https://one.nr/0kLwG6LvEQ6) |





## Contacts
For any questions, contact
- {% include contact.html slack=oss-ciebot-slack name=oss-ciebot-name userid=oss-ciebot-userid notesid=oss-ciebot-notesid%}
- {% include contact.html slack=oss-ciebot-2-slack name=oss-ciebot-2-name userid=oss-ciebot-2-userid notesid=oss-ciebot-2-notesid%}

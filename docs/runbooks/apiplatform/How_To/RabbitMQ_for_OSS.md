---
layout: default
description: RabbitMQ setup and support for OSS tooling
title: RabbitMQ Instance URLs and Secrets for OSS Tooling
service: tip-api-platform
runbook-name: RabbitMQ_for_OSS
tags: tip-api-platform, edb, pnp, ciebot, gobot, rabbitmq
link: /apiplatform/How_To/RabbitMQ_for_OSS.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Messages for RabbitMQ in OSS Tooling
PnP, EDB, and CIEBot/Gobot are sharing the same instances Message for RabbitMQ.
There are 9 instances of RMQ per account, one in each region each environment.
See [cloud resources]({{ibm-cloud-dashboard-link}}resources), under **Services**.

There are 2 sets of credentials for each Account.  
- RMQ Management credentials are to be used by oncall operators who need to monitor queues.
- RMQ Administration credentials are to be used by developers who need to configure queues, bindings and exchanges.

### RMQ Management (OSS ACCOUNT {{oss-account-account}})
Use a browser to monitor RMQ queues. The URL to the Management UI, user id, password are kept in PIM. Each instance has its own URL.

| Instance       | PIM path                                                       |
| :------------- | :------------------------------------------------------------- |
| us-south prod  | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46451](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46451) |
| us-east prod   | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46450](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46450) |
| eu-de prod     | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46449](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46449) |
| us-south stage | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46448](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46448) |
| us-east stage  | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46447](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46447) |
| eu-de stage    | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46446](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46446) |
| us-south dev   | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46445](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/4644) |
| us-east dev    | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46444](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46444) |
| eu-de dev      | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46443](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46443) |

### RMQ Administration (OSS ACCOUNT {{oss-account-account}})
Use a browser to configure RMQ queues, bindings, etc. The URL to the Management UI, user id, password are kept in PIM. Each instance has its own URL.

| Instance       | PIM path                                                       |
| :------------- | :------------------------------------------------------------- |
| us-south prod  | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46459](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46459) |
| us-east prod   | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46457](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46457) |
| eu-de prod     | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46453](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46453) |
| us-south stage | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46460](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46460) |
| us-east stage  | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46455](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46455) |
| eu-de stage    | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46454](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46454) |
| us-south dev   | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46458](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46458) |
| us-east dev    | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46456](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46456) |
| eu-de dev      | [https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46452](https://pimconsole.sos.ibm.com/SecretServer/app/#/secret/46452) |

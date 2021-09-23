---
layout: default
description: Cloudant setup and support for OSS tooling
title: Cloudant Instance URLs for OSS Tooling
service: tip-api-platform
runbook-name: Cloudant_for_OSS
tags: tip-api-platform, edb, pnp, ciebot, gobot, cloudant
link: /apiplatform/How_To/Cloudant_for_OSS.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Cloudant in OSS Tooling
EDB and CIEBot/Gobot are sharing the same instances of Cloudant.
There are 2 Cloudant instances per environment, one in us-south and the other in us-east region. Most databases are configured for continuous replication across both regions.
See [cloud resources]({{ibm-cloud-dashboard-link}}resources), under **Services**.

### Cloudant (OSS ACCOUNT {{oss-account-account}})
Use the `Sign in with IBMid` option to login to Cloudant dashboard.

| Instance       | Dashboard URL                                                                                                                                                        |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| us-south prod  | [https://e354acfd-a374-4a16-a295-69fb8b57a723-bluemix.cloudant.com/dashboard.html](https://e354acfd-a374-4a16-a295-69fb8b57a723-bluemix.cloudant.com/dashboard.html) |
| us-east prod   | [https://907e02c4-4c52-4d74-9b10-55374eb1e7af-bluemix.cloudant.com/dashboard.html](https://907e02c4-4c52-4d74-9b10-55374eb1e7af-bluemix.cloudant.com/dashboard.html) |
| us-south stage | [https://154ee91a-dc32-4b30-8666-eda6507364f4-bluemix.cloudant.com/dashboard.html](https://154ee91a-dc32-4b30-8666-eda6507364f4-bluemix.cloudant.com/dashboard.html) |
| us-east stage  | [https://227ff1b3-8453-43be-9d44-84ddae668eed-bluemix.cloudant.com/dashboard.html](https://227ff1b3-8453-43be-9d44-84ddae668eed-bluemix.cloudant.com/dashboard.html) |

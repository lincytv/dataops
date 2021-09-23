---
layout: default
description: Consul Failed Alert
title:  Consul Failed Alert
service: doctor
runbook-name: Runbook consul failed alert
tags: doctor, vault
link: /doctor/Runbook_Consul_Failed_Alert.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}

## 1. Verify the real consul monitor status  

[{{prometheus-name}}  Consul health node status]({{ prometheus-link}}?g0.range_input=1h&g0.expr=consul_health_node_status&g0.tab=0).

![]({{site.baseurl}}/docs/runbooks/doctor/images/prometheus/consul_health_node_status.png){:width="700px"}

## 2. Verify if the consul service is down

1. Log in in the consul service node via [{{wukong-portal-name}}]({{wukong-portal-link}}).
2. Select **Remote Command**.
3. Search the service.

| Consul     | Environment    |
| :------------- | :------------- |
| Service 1      | DOCTOR_VAULT_1       |
| Service 2      | DOCTOR_VAULT_2 |
| Service 3 | DOCTOR_VAULT_3|  
| Service 4 | DOCTOR_VAULT_4 |
| Service 5 | DOCTOR_VAULT_5 |

4. Enter `docker ps` to check the container status.
5. Click on **Run**.
6. If a container failed.
  * Run the command `curl -k https://127.0.0.1:5999/compose/up` to start it.

![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/consul_test.png){:width="700px"}

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

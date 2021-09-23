---
layout: default
description: EU vault is down.
title: EU Vault is down
service: vault
runbook-name: Runbook EU Vault is down
tags: oss, doctor, vault
link: /doctor/Runbook_EU_Vault_down.html
type: Alert
---

{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose

EU vault is down


## User Impact

Unable read/write EU data from/to EU vault, if you get this alert. Some services(e.g YP_FRANKFURT) may fail to restart.

## Instructions to Fix

### Verify if vault is down

  `curl -X GET -i 'http://9.66.246.4:4991/cipherkeeper/eu-vault-status' -vv`

  ![]({{site.baseurl}}/docs/runbooks/doctor/images/vault/eu_vault_status.png){:width="700px"}

  If the http response is 200, resolve the alert, otherwise send message to slack channel [{{slack-vault-name}}]({{slack-vault-link}}).

## Notes and Special Considerations

  {% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
title: How to use the Privileged Identity Management (PIM) Secrets
runbook-name: How to use the Privileged Identity Management (PIM) Secrets
description: "How to use the Privileged Identity Management (PIM) Secrets"
service: tip-api-platform
tags: pim, secrets, passwords
link: /apiplatform/how_use_pim_secrets.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Overview

The Privileged Identity Management (PIM) is an SOS service that allows a way to manage privileged accounts to achieve and maintain regulatory compliance and operational efficiency in a secure way across different resources and systems. With PIM implemented you can easily meet auditing and compliance requirements PIM allows you to create, share, and automatically change enterprise passwords. You can also assign user permissions and track password usage with full audit reports. Organize secrets in intuitive, nested folders and do it all through a simple, customizable dashboard and enhanced security.

For more information, visit the [SOS PIM Gihub](https://pages.github.ibm.com/SOSTeam/SOS-Docs/pim/privileged_identity_manager.html)

PIM will be replacing the existing Private credential github repository.

## Request access to PIM

In order to view the secrets in PIM UI, first you will need to request access to the service in AccessHub. The following [runbook]({{site.baseurl}}/docs/runbooks/apiplatform/Request_PIM_Access_In_AH.html) will provide details on how request appropriate access for your needs.

## View Secrets

- Login to [{{pim-console-name}}]({{pim-console-link}}/) with your SSO ID
- From the Domain dropdown, select `sso`

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pim_login.jpg){:width="400px"}

- The main page will load All available secrets. You can search for a keyword in the search box to list available secrets

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pim_dash_search.jpg){:width="400"}

- The secrets have been categorized by component/service. You can filter by drilling down by the corresponding folder

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pim_categories.jpg){:width="400"}{:height="700"}

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pim_categories_filter.jpg){:width="500"}

- To view a secret values, click anywhere on the secret and will display the entries. To view the password/key, click on `Show` next the masked value so that you can view/copy it

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pim_secret_details.jpg){:width="700"}

## Create/Modify Secrets

- To add new or modify a secret, please contact the following team members with the details

* {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}
* {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}

## Runbook Owners

- {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

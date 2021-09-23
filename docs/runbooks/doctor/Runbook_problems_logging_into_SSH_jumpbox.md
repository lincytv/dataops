---
layout: default
description: This runbook provides instructions on how to fix problems users may have SSH'ing into the BoshCLI SSH Jumpbox.
title: Problems logging into Doctor SSH jumpbox
service: jumpbox
runbook-name: Problems logging into Doctor SSH Jumpbox
tags: oss, bluemix, doctor, ssh, logging, jumpbox, boshcli
link: /doctor/Runbook_problems_logging_into_SSH_jumpbox.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}

## Purpose
This runbook provides instructions on how to fix problems, when trying SSH into ``{{bosh-cli-link}}`` (SSH Jumpbox).

## Technical Details
The reason for this alert maybe:

  * Account locked due to X failed logins.
  * Verification code forgotten or needs to be reset.

## User Impact
User can not ssh into ``{{bosh-cli-link}}`` [SSH Jumpbox]({{site.baseurl}}/docs/runbooks/doctor/Doctor_SSH_Jumpbox.html).

## Instructions to Fix
Contact {%include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid %} via email, asking to unlock your user ID or to reset your verification code.

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

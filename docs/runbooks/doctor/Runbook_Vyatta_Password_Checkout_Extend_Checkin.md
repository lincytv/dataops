---
layout: default
description: Instructions for the Scorecard API.
title: Vyatta Password Checkout Extend Checkin
service: doctor
runbook-name: Vyatta Password Checkout Extend Checkin
tags: oss, bluemix, doctor, scorecard
link: /doctor/Runbook_Vyatta_Password_Checkout_Extend_Checkin.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

# Vyatta Password Checkout/Extend/Checkin

## Purpose
This runbook describes how to checkout/extend/checkin the password of user _vyatta_ for Vyatta devices.

## Technical Details
On the Vyatta list page, a column name "PWD" is shown with a colored eye icon.

  - Green icon indicates the state of "Available"
  - Blue icon indicates the state of "In Use (by yourself)"
  - Yellow-green icon indicates the state of "In Use (by others)"
  - Red icon indicates the state of "Not Available"

## User Impact

## Instructions to Fix
### Checkout Vyatta Password
The checkout action is available with the state of "Available" or "In Use".

  1. Click the colored eye icon.
  2. In the popped up dialog, input a valid RTC or PagerDuty number. Then click checkout button.
     As the result, the password of Vyatta will be shown in the right-top message box. It will expire in two hours.

### Extend Vyatta Password
Extending the action is available if the Vyatta password was checked out by the current user.

  1. Click the colored eye icon.
  2. In the popped up dialog, click extend button.

The expired time will be extended for two more hours.

### Checkin Vyatta Password
Extending the action is available if the Vyatta password was checked out by the current user.

  1. Click the colored eye icon.
  2. In the popped up dialog, click the checkin button.

The password will be changed immediately.

Conclude with the expected outcome of the instructions.

## Notes and Special Considerations
Contact {% include contact.html slack=checkin-failure-slack name=checkin-failure-name userid=checkin-failure-userid notesid=checkin-failure-notesid %} if you have any questions about this runbook.

{% include {{site.target}}/tips_and_techniques.html %}

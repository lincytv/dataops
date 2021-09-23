---
layout: default
description: If Doctor login fails, ssh to the doctor.bluemix.net VM.
title: Doctor login - ibm allenvs fabric doctor availability
service: doctor
runbook-name: User unable to log in to Doctor
tags: oss, bluemix, doctor, SSH
link: /doctor/Runbook_Login_ibm-allenvs-fabric-doctor_availability-DoctorLogin.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
__

## Purpose

This alert will be triggered if a user cannot login to Doctor.

## Technical Details

The reason for this alert could be:

1. There is a network problem with the [{{doctor-portal-name}}]({{doctor-portal-link}}) VM.
2. There is something wrong with the Doctor user service.

## User Impact

User cannot login to Doctor.

## Instructions to Fix

### Steps

DOCTOR_BUS2

1. Verify login manually.
2. If login fails, ssh to the [{{doctor-portal-name}}]({{doctor-portal-link}}) VM.
3. Run command `nc 158.85.241.85 4567 -w 3`.
4. Run command `echo $?`.
  * If the command returns 1, this indicates a network connection problem. You need to contact the network team [{{sre-platform-onshift-name}}]({{sre-platform-onshift-link}}) or create a defect and assign it to them.
5. If the network is Ok.
  * Check the doctor user service log by running the `docker logs --tail=500 docker_user_XXX` command.
  * If there is an exception in the log, you should create a defect and assign it to doctor team or contact {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %}.

## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

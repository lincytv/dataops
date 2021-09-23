---
layout: default
description: Deploy Doctor Agent in Dedicated SL Account
title: Deploy Doctor Agent in Dedicated SL Account
service: doctor
runbook-name: Runbook Deploy Doctor Agent In Dedicated SL Account
tags: doctor
link: /doctor/Runbook_Deploy_Doctor_Agent_In_Dedicated_SL_Account.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}

Estimation: 60 Minutes.

1. Provision a Virtual Machine from the Doctor Agent Virtual Machine template image. This includes all Doctor dependencies, e.g., Docker engine, Doctor Keeper, Supervisor and various IDs and SSH Keys. The Doctor Agent Virtual Machine template image was created in SL Staging account 27844, named _OSS-Doctor-service-onboarding-image-20180109_. Please contact {% include contact.html slack=sre-platform-chief-architect-slack name=sre-platform-chief-architect-name userid=sre-platform-chief-architect-userid notesid=sre-platform-chief-architect-notesid %} to share the image to your Softlayer account.

2. Once the Virtual Machine is provisioned and started, log on with Doctor (default password: Doctor4serviceonboard) and `sudo -i` to get root privilege.

3. Go to the _/opt/doctor-keeper/config/_ folder and edit _keeper.yml_. Change the _ENVIRONMENT_NAME_ to be the actual environment name, then run the command 'supervisorctl restart doctor_keeper'.

4. Contact the Doctor team to initialize a Doctor agent configuration yml and a docker compose configuration yml. Then copy the docker compose configuration (_{{doctor-compose-file-name}}_) to the directory _/opt/doctor-keeper/config/_ on the agent Virtual Machine.

5. Start Doctor services on agent Virtual Machine with the command `curl -k https://127.0.0.1:5999/compose/up`.   

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

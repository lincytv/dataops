---
layout: default
description: Enable checkin/checkout for new users.
title: Enable checkin/checkout for new users
service: doctor
runbook-name: Enable checkin/checkout for new users
tags: doctor, checkin, checkout
link: /doctor/Runbook_Shared_ID_Checkin_Checkout.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}


## Update Doctor Agent Configuration File
Find the configuration file in [{{doctor-config-repo-name}}]({{doctor-config-repo-link}}).
Find "security" section add new user id to "nonroot_local_users".

```
security:
    nonroot_local_users:
        - whc_test
```

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

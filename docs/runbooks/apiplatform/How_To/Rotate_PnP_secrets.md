---
layout: default
description: How to rotate credentials For PnP
title: How to rotate credentials for PnP
service: tip-api-platform
runbook-name: How to rotate credentials for PnP
tags: oss, pnp, runbook, secrets, vault, password, credentials, rotation
link: /apiplatform/How_To/Rotate_PnP_secrets.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose
This runbook illustrates the necessary steps to rotate the PnP related secrets.

PnP relies on Postgres for some of its functionality. The `admin` account is __NOT__ used and should not be modified.

## IBM Cloud Postgres Database credentials

Follow these instructions to rotate the credentials for the Postgres DB:

Navigate to [IBM Cloud Console Resources](https://cloud.ibm.com/resources), search for postgres within the list of available services. You can use the search bar under the name property to find the entries related to Postgres.

1. Search for Postgres service.
2. Select the appropriate Postgres instance; the selected instance resource page opens.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pnp_password_rotate_1.png)

3. Navigate to `Service credentials`.
4. Add new credentials by clicking on the `New credential` button.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pnp_password_rotate_2.png)

5. Create the new __vault__ credential and name it following this pattern: `service-credential-dev-vault-postgresql-ussouth-#` where `#` represents the number of the credential. This number should increment with each rotation. For example, if this is the first time rotating the password, you might use the name `service-credential-dev-vault-postgresql-ussouth-1`, when the next rotation is due, that number will be 2. You should end up with two credentials. **Do not delete the existing credentials until after updating vault with the new credentials**.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pnp_password_rotate_3.png)

Click on the `Add` button to complete the creation step.

Write the newly created credentials to `vault`

```
vault write <vault path> 'value=<new value>' 'about=<information about the secret>'
```

Example:

```
vault write /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/shared/postgresql/ussouth.user value=service-credential-dev-vault-postgresql-ussouth-1

vault write /generic/crn/v1/dev/local/tip-oss-flow/global/otdev/shared/postgresql/ussouth.pass value=<value_from_created_credential>
```

Repeat this step for each Postgres reference in each environment values yaml file.


To obtain the `user` and `password` values, from the `Resources` section, select the appropriate credential and expand its contents.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pnp_password_rotate_4.png)

Find the `postgres` section which contains the user and password values you need to use for the rotation.

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pnp_password_rotate_4.png)


### Deploy the service
Search oss-charts with the vault path to find all components that need to be redeployed.  The developer can update the `version` value in the `Chart.yaml` file to a minor version change, and merge the change to oss-charts staging branch to trigger a new deployment. 
       
Check logDNA for any authentication errors.

If after a few days there are no issues, delete the old keys.

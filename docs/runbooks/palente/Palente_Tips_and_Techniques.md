---
layout: default
description: A list of tips and techniques useful for on-call duties
title: Tips and techniques
service: palente
runbook-name: Palente and in general tips and techniques for operations
tags: oss, bluemix, runbook, oncall, ssh, phe, palente
link: /palente/Palente_Tips_and_Techniques.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}

## Purpose

To give some helpful tips and techniques useful for users while they are on call Pager Duty.


## How to's

### How to check Github status

- When GHE is down you can check the [status](https://status.whitewater.ibm.com/) or #whitewater-github on Slack

### How to check NewRelic status

- When GHE is down you can check the [status](https://status.newrelic.com/)

### How to check PagerDuty status

- When GHE is down you can check the [status](https://status.pagerduty.com/)


### How to set up Github runbook pages in my local machine when github has a scheduled maintenance

- Clone the [{{repos-ibm-cloud-runbooks-name}}]({{repos-ibm-cloud-runbooks-link}}) repository.
  - \$ git clone https://github.ibm.com/cloud-sre/runbooks.git.
- If you don't have Ruby installed, install Ruby 2.1.0 or higher. We recommend using [RVM](https://rvm.io/).
- Install bundler.
  - \$ gem install bundler
- Install Jekyll and other dependencies from the GitHub Pages gem.
  - \$ bundle install
- Navigate to the root of the runbook repository.
- Run your Jekyll site locally.
  - \$ bundle exec jekyll serve
- Alternatively, if you have docker installed, from the root of the documentation repository, you can run the site by entering the following command:
  - docker run -v \$PWD:/srv/jekyll-p 4000:4000 -w /srv/jekylljekyll/jekylljekyllserve.
- The site can then be accessed at http://localhost:4000/ to run and visually test the pages.

### How to track down a {{doctor-alert-system-name}} incident generate in {{new-relic-portal-name}}

Track down incident creation: New Relic --> Kibana --> ServiceNow --> PagerDuty

- For a [{{new-relic-portal-name}} incident]({{new-relic-portal-link-alert|strip}}incidents/35272543/violations
  with {{new-relic-portal-name}}) account number nnnnnnn (1926897) and incident number iiiiiii (35272543)

- Log into [{{kibana-portal-name}}]({{kibana-portal-link}}) with IBM intranet w3 credentials.
- Click on **Add a filter** and create a filter using for alert_id with the {{new-relic-portal-name}} account number and incident number.
- Click on **Save**.
- Adjust the time range at the top right if needed.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/add_new_filter.png){:width="640px"}
- Click on the triangle on the left to see the details of the incident, or click the "INCnnnnn" link to go to ServiceNow.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/new_filter_result_set.png){:width="640px"}
- The ServiceNow incident URL can be seen after scrolling down.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/kibana/new_filter_full_results.png){:width="640px"}
- In ServiceNow, Look for the word "PagerDuty" to find the PD identifier
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/servicenow/activities.png){:width="640px"}
- In this case the [PD PWZEZPD will be](https://ibm.pagerduty.com/incidents/PWZEZPD)


## How to access IBM cloud

- From [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
- Log into **{{oss-account-full-name}}**.
- ![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/switch_acct.png){:width="300px" height="288px"}
- On the Resource summary you will see the resources you have access to
- ![]({{site.baseurl}}/docs/runbooks/palente/images/cloud/resources.png){:width="640px"}

## How to access Kubernetes Dashboards

- From [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
- Log into **{{oss-account-full-name}}**.
- ![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/switch_acct.png){:width="300px" height="288px"}
- On the Resource summary you will see the resources you have access to
- ![]({{site.baseurl}}/docs/runbooks/palente/images/cloud/resources.png){:width="640px"}
- Select Clusters, you will see a list like the follow:
- ![]({{site.baseurl}}/docs/runbooks/palente/images/cloud/clusters_list.png){:width="640px"}
- Select the region to access the Dashboard of it.
- Will open the cluster overview
- On the upper right side you will see Kubernetes Dashboard , click on it to access the dashboard.
- ![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/kube_dashboard.png){:width="640px"}

## How to restart Palente services

{% include {{site.target}}/oss_bastion_guide.html %}

1. Connect to the cloud account,`ibmcloud login --sso -c 5b7a6f946d2f49fcb38451ccfe5b25b6`
2. [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)
> At the time of writing this runbook, pa'lente, oss-csd, service only runs at us-east for the production environment
3. Delete the pod.
  - `kubectl oss pod delete -l app=api-oss-csd -n api`
  - If `api-oss-csd-rules` needs to be restarted: `kubectl oss pod delete -l app=api-oss-csd-rules -n api` 
  -  Deleting the pod will force Kubernetes to start a new service
4. Some PagerDuty alerts might tigger while the service gets restarted. You may snooze them.
5. If the service keeps failing try to remove the service and re-deploy it
  - `helm delete api-oss-csd` or `helm delete api-oss-csd-rules` (for rules API)
  - `kdep <region>-production-values.yaml` e.i. `kdep useast-production-values.yaml` 
  > Currently only IKS administrators can execute the above commands, [contact an IKS admin](#how-to-contact-iks-administrators) for help

## How to redeploy Palente services

{% include {{site.target}}/oss_bastion_guide.html %}

1. Connect to the cloud account, `ibmcloud login --sso -c 5b7a6f946d2f49fcb38451ccfe5b25b6`
2. [Access IKS clusters via Bastion](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-Bastion-User-Guide---Account-Migration#a1-2)
> At the time of writing this runbook, pa'lente, oss-csd, service only runs at us-east for the production environment
3. Clone [api-oss-csd charts]({{api-oss-csd-charts-link}}) repo or [api-oss-csd-rules charts]({{api-oss-csd-rules-charts-link}}) repo
4. redeploy using [kdep](https://github.ibm.com/cloud-sre/declarative-deployment-tools)
  - `kdep useast-production-values.yaml`
  > Currently only IKS administrators can execute the above commands, [contact an IKS admin](#how-to-contact-iks-administrators) for help

## How to get a kube secret

{% include {{site.target}}/oss_bastion_guide.html %}

- Describe the pod to find the secret name and id
  - `kubectl describe pod -napi -l app=api-oss-csd`
  ```
       SECRETCREDENTIALS_edb-yp:                            <set to the key 'value' in secret 'auto-configured-secret-from-vault-f9fd3b51bdcf1aadf14bb9d49f071ca543661c9813e37291f1dd15c2f59e2c78'>  Optional: false
       SECRETCREDENTIALS_csd-yp:                            <set to the key 'value' in secret 'auto-configured-secret-from-vault-f9fd3b51bdcf1aadf14bb9d49f071ca543661c9813e37291f1dd15c2f59e2c78'>  Optional: false
       SECRETKEY_catalog-yp:                                <set to the key 'value' in secret 'auto-configured-secret-from-vault-cbb056645492159164ef2cab0a67a9f1a7c64671cb18abaf1f1304685a4d7e42'>  Optional: false
       SECRETKEY_tip-yp:                                    <set to the key 'value' in secret 'auto-configured-secret-from-vault-cbb056645492159164ef2cab0a67a9f1a7c64671cb18abaf1f1304685a4d7e42'>  Optional: false
       SECRETKEY_sn-yp:                                     <set to the key 'value' in secret 'auto-configured-secret-from-vault-7ef9ddeedfe9bb70ea97083540241e54e07da8c427d690fe37679c201fcd8c20'>  Optional: false
       SECRETCREDENTIALS_es_key:                            <set to the key 'value' in secret 'auto-configured-secret-from-vault-78e540401d2fc83af685d938548eb47eaa1442c34995c784ad9894abeb5a83f7'>  Optional: false
       NR_LICENSE:                                          <set to the key 'value' in secret 'auto-configured-secret-from-vault-02ceedea93f9bf460826b71c25d6d251f88a71993c0579decaf0c1689cf56a03'>  Optional: false
       NR_APPNAME:                                          api-oss-csd
       KUBE_APP_DEPLOYED_ENV:                               prod
       KUBE_CLUSTER_REGION:                                 us-east
```
- Get the YAML/JSON for the secret:
  - `kubectl get secret -n api auto-configured-secret-from-vault-xxxx -o yaml > secret.yaml`
  - `kubectl get secret -n api auto-configured-secret-from-vault-xxxx -o json > secret.json`
  - Where xxx is the secret id. In the example above it is *7ef9ddeedfe9bb70ea97083540241e54e07da8c427d690fe37679c201fcd8c20* for _SECRETCREDENTIALS_es_key_
  - Example:
    - ```
      kubectl get secret -n api auto-configured-secret-from-vault-cbb056645492159164ef2cab0a67a9f1a7c64671cb18abaf1f1304685a4d7e42 -o yaml > secret.yaml
      ```
  > Currently only IKS administrators can execute the above commands, [contact an IKS admin](#how-to-contact-iks-administrators) for help

- Get the data.value from the secret or any other value
- If JSON
  - `cat secret.json |jq .data.value |sed 's/"//g' | base64 --decode`
- If YAML
  - `cat secret.yaml`
  - Get the `<data.value>` from the ymal file
  - `echo '<data.value>' | base64 --decode`
- To update a secret
  - Edit the value using the editor of your choice e.i. `vi secret.yaml / vi secret.json`
  - Save your changes
  - Apply the updated secret
    - `kubectl apply -f secret.yaml` / `kubectl apply -f secret.json`


## How to contact IKS administrators

{% include {{site.target}}/iks_admin_contacts.md %}




## Outages

- {{usam-short}} outages go to [{{onestatus-name}}]({{onestatus-link}}).

## Password expired

If a password has expired then you can reset the expiry date with:

```
chage -d `date +%Y-%m-%d` sshhub example TODAY=`date +%Y-%m-%d`; chage -d $TODAY <user>
```

Change the userid (in this case _sshhub_) as appropriate. You can run this command in remote command for a Doctor Agent. Note that this can be useful if the password is expired for sshhub which is used when running SSH from Wukong Doctor Keeper. For more information [How to solve an alert for root password expire on local env]({{site.baseurl}}/docs/runbooks/doctor/Runbook_st_passwd_expiration_root.html)


## Slack channels

| Channel                | Description                                                                                                                                                                                                                                             |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| #admin-requests        | Admin requests for the Cloud Platform Slack team                                                                                                                                                                                                        |
| #bluemix-local         | discuss bluemix local development                                                                                                                                                                                                                       |
| #bluemix-admin         | public channel for support cases and incident management with PaaS Admin Team                                                                                                                                                                           |
| #bluemix-xen7-migrate  | Discuss the move of Bluemix VMs to Xen7                                                                                                                                                                                                                 |
| #cto-oss-tip-internal  | For discussion between the internal OSS TIP team about design and development issues.                                                                                                                                                                   |
| #cto-sre-dashboard     | Questions related to the CTO STS Dashboard/Scorecard                                                                                                                                                                                                    |
| #cto-sre-product-ci    | Travis CI job status for CTO SRE Productization team                                                                                                                                                                                                    |
| #cto-sre-product-squad | Welcome to the Productization squad private channel! This is a great place to share information and ask questions.                                                                                                                                      |
| #dept_wh4a             | Items for discussion related to Department WH4A and intended for use in place of scheduled department meetings.                                                                                                                                         |
| #devit-usam            | USAM Admin teams discussion                                                                                                                                                                                                                             |
| #doctor-ic             | deprecated, replaced by #oss-doctor                                                                                                                                                                                                                     |
| #doctor-on-call-shift  | Slack channel dedicated for passing Bluemix Doctor on-call info/tips to the next shift. See also https://ibm.ent.box.com/folder/45327391663                                                                                                             |
| #doctor-setup-4-watson | Setting up Doctor fot Watson Environment - Test                                                                                                                                                                                                         |
| #eu-emerg-approvers    | channel with EU approvers for the purpose of collaborating on non-EU engineers requiring EU emergency access                                                                                                                                            |
| #local-builds-ic       | Deployment of Local Bluemix                                                                                                                                                                                                                             |
| #oss-doctor            | Doctor collaboration.                                                                                                                                                                                                                                   |
| #oss-kube-work         | This channel is for everything related to moving OSS Platform to Kubernetes. See wiki for more info: https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-on-Kubernetes                                                                              |
| #oss-tip-message-log   | Incidents from the TIP message flow                                                                                                                                                                                                                     |
| #sre-platform-onshift  | Bluemix private channel for the operations team, including primary and secondary members, geo leads, key participants from the network or management teams, etc. If specific issues need to be covered, don’t hesitate to fork out in another priv grp. |

## Why's

## Another topic...

Add details for another topic here.

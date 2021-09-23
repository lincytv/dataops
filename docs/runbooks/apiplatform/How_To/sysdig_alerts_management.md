---
layout: default
title: Sysdig alerts management
type: Informational
runbook-name: "Sysdig alerts management"
description: Describe how maintain and manage Sysdig alerts set in ICD services such as Redis, RabbitMQ
service: tip-api-platform
tags: Sysdig, slack, PD
link: /apiplatform/How_To/sysdig_alerts_management.html
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

## Purpose

List all Sysdig alerts created for production and staging environments. This is an information runbook only to help future setup in case updates are required

IBM Cloud™ Monitoring with Sysdig is a cloud-native, and container-intelligence management system that you can include as part of your IBM Cloud architecture. Use it to gain operational visibility into the performance and health of your applications, services, and platforms. If you are cloud admin or want to know more see the follow [IBM Cloud Monitoring with Sysdig](https://cloud.ibm.com/docs/Monitoring-with-Sysdig?topic=Monitoring-with-Sysdig-getting-started)


## Access Sysdig

1. Log to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
2. Click the person icon in the top right corner. Select **{{oss-account-full-name}}** under accounts.
3. From the resource list select Services and filter out using **Sysdig**
4. You should see Sysdig services


## Sysdig alerts  

Each region listed in the chart below contains alerts previously setup, but dev environment.Click on the link from the table to access Sysdig Monitoring console by environment.

Name|Group|Location|
------ | ------|------|
Sysdig-oss-dev-eu-de| oss-dev | [Frankfurt](https://eu-de.monitoring.cloud.ibm.com/#/overview/4603?scope=host.hostName%20as%20%22Host%20Name%22%20%3D%20%3F)
Sysdig-oss-staging-us-east| oss-staging | [Washington DC](https://us-east.monitoring.cloud.ibm.com/#/overview/1690?scope=host.hostName%20as%20%22Host%20Name%22%20%3D%20%3F)
Sysdig-oss-prod-us-south| oss-prod | [Dallas](https://us-south.monitoring.cloud.ibm.com/#/overview/21412?scope=host.hostName%20as%20%22Host%20Name%22%20%3D%20%3F)|

<br><br>

>At the time of the creation of this runbook Sysdig monitors the following services; MongoDB, RabbitMQ, Redis and PostgresQL, however, MongoDB will be replaced by other database engine in the near future.

The follow table list the current alerts set by region and service. Alerts were focused on memory and disk percentages and in cases where apply such as PostgresQL, connections and CPU alerts were created. MongoDB, RabbitMQ and Redis `don't have dedicated cores, reason why CPU cannot be monitored by Sysdig`.


## Pre-requirement to create/edit an alert
- Only Cloud admin users can create/edit alerts. If you are not admin for the at least the Sysdig service, you will need to contact an admin to continue.
- Need to define the thresholds for each service/environment.
- Have communication channels ready such as Slack, {{doctor-alert-system-name}}. [Need to create new channels](#how-to-manage-channels).

## Services thresholds

The following table describe the current thresholds for each service/environment.

Service|Type|%|Severity|Enviroment|Notifications|Time
------ | ------|------|---|--|
MongoDB|Disk|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
MongoDB|Disk|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
MongoDB|Memory|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
MongoDB|Memory|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
RabbitMQ|Disk|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
RabbitMQ|Disk|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
RabbitMQ|Memory|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
RabbitMQ|Memory|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
Redis|Disk|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
Redis|Disk|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
Redis|Memory|90%|High|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
Redis|Memory|80%|Medium|Prod/Stg|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Connections|85%|High|Production|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Connections|85%|Medium|Staging|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|CPU|85%|High|Production|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|CPU|85%|Medium|Staging|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Disk|85%|High|Production|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Disk|85%|Medium|Staging|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Memory|80%|High|Production|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.
PostgreSQL|Memory|80%|Medium|Staging|[{{doctor-alert-system-name}}]({{doctor-alert-system-link}})<br>[{{slack-oss-icd-sysdig-alerts-name}}]({{slack-oss-icd-sysdig-alerts-link}})| For at least 10  min.

## Adding/Edditing alerts

Select the region where do you want to edit/add an alert. Each reagion hold production, staging and development services, even though the monitor name can be confused. 

- [Sysdig-oss-pord-us-south](https://us-south.monitoring.cloud.ibm.com/#/alerts)
>Even though the monitor name is labeled as prod (production); it monitors both  production and test/staging services.
- [Sysdig-oss-staging-us-east](https://us-east.monitoring.cloud.ibm.com/#/alerts)
> Even though the monitor name is labeled as staging; it monitors both  production and test/staging services.
- [Sysdig-oss-dev-eu-de](https://eu-de.monitoring.cloud.ibm.com/#/alerts)
> Even though the monitor name is labeled as dev (development); it monitors both  production and test/staging services.


## How to manage channels

Currently Sysdig will use Slack and {{doctor-alert-system-name}} to notify of an alert. To manage each notification channel follow the next steps:

### Slack
- From slack create a new channel, the channel can be public or private. [Click here](https://slack.com/help/articles/201402297-Create-a-channel) if you need help to create a new channel in Slack
- Go to [Slack API](https://api.slack.com/apps/A0137HWJE2H/general)
- Only listed members at the **Collaborators** can add/update Incoming Webhooks
  * Current collaborators:
    - {% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}
    - {% include contact.html slack=oss-auth-slack name=oss-auth-name userid=oss-auth-userid notesid=oss-auth-notesid %}
    - {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}
    - {% include contact.html slack=oss-security-focal-slack name=oss-security-focal-name userid=oss-security-focal-userid notesid=oss-security-focal-notesid %}
    - {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}
    - {% include contact.html slack=doctor-backend-3-slack name=doctor-backend-3-name userid=doctor-backend-3-userid notesid=doctor-backend-3-notesid %}
- From the feature menu select **Incoming Webhooks**.
- You can delete or add new channels.
- To add a new one channel to Webhooks, the channels needs to exist already.
  - Click on **Add New Webhooks to Workspace**.
  - Search for the previously created channel , you would like to use.
  - Click **Allow**
  - Now, you will see the channel listed.
  - Use the **Copy** button from the **Webhooks URL** column, to copy the URL to be use in Sysdig notification.

### {{doctor-alert-system-name}}
- OSS already have a Webhooks setup in {{doctor-alert-system-name}} to get the information about it.
  - Login to [{{doctor-alert-system-name}}]({{doctor-alert-system-link}}).
  - From the menu a the top select **Services**
  - Click on **OSS Platform Main Service**.
  - Form the Service menu, select **Integrations**.
  - Use the **Copy** button to copy the **Integration Key** to be use in Sysdig notification.

## Adding Notification Channels.
- Once you get the channel information select the monitor to add a notification channel
  - [Sysdig-oss-prod-us-south](https://us-south.monitoring.cloud.ibm.com/#/settings/notifications)
  - [Sysdig-oss-staging-us-east](https://us-east.monitoring.cloud.ibm.com/#ettings/notifications)
  - [Sysdig-oss-dev-eu-de](https://eu-de.monitoring.cloud.ibm.com/#ettings/notifications)
- For the list select **Slack/{{doctor-alert-system-name}}**.
    - For **Slack**:
      - Paste the **Webhooks URL** from Slack into the **URL** field.
      - Add the Slack channel name.
      - Enable at least the first time **Test notification** to make sure it is working as expected.
      - Click on **Save**
      - Make sure you get the notification test.
    - For **{{doctor-alert-system-name}}**:
      - If you get a popup window "Auto-fetch PagerDuty Channel Configuration", click on **Manual** since we already got a Key in the previous steps
      - Paste the **Integration Key** from {{doctor-alert-system-name}} into the **Service** Key field.
      - Fill out the other field with a relevant information to the channel.
      - Enable at least the first time **Test notification** to make sure it is working as expected.
      - Click on **Save**
      - Make sure you get the notification test.

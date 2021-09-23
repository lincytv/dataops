---
layout: default
title: Sysdig services alerts
type: Alert
runbook-name: "Sysdig services alerts"
description: Describe how to response to a service alert triggered by Sysdig for ICD services such as Redis, RabbitMQ ...
service: tip-api-platform
tags: Sysdig, slack, PD
link: /apiplatform/sysdig_services_alerts.html
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}


## Purpose

Sysdig will trigger an alert to Slack/PagerDuty or both if an alert meet the specified condition such as 90% of memory usage. Sysdig will only monitor the follow condition: Memory, Disk for MongoDB, RabbitMQ, Redis and PostgreSQL. Only PostgreSQL additionally check for CPU and connections. To find out more about the Sysdig alert configuration check [Sysdig alerts management]({{site.baseurl}}/docs//apiplatform/How_To/sysdig_alerts_management.html)

## Technical Details

The reason for this alert could be one of the following:

  1. Disk usage per service reached a thresholds of 80/90% for at least 10 min.
  2. Memory usage per service reached a thresholds of 80/90% for at least 10 min.
  3. CPU usage per service reached a thresholds of 80/90% only PostgreSQL for at least 10 min.
  4. The number of connection in PostgreSQL has reached 85% of total connections allowed for at least 10 min.

## User Impact

Users who are using the functionality provided by this service(s) will be affected.

## Instructions to Fix

>If you are not part of the OSS cloud administrator group, you will need to scale this alert to any of the current cloud administrator or contact OSS manager to get help.

### For a MongoDB/RabbitMQ/Redis alert

1. Log to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
2. Click the person icon in the top right corner. Select **{{oss-account-full-name}}** under accounts.
3. From the resource list, select **Services** and filter out using **mongodb**
4. Select the service posted in the alert. See an [example](#for-a-postgresql-alert)
5. Base on condition take appropriate action:

  - CPU/Memory/Disk usage:
    - If a configuration resource needs to be updated see,[Scaling up your installation](https://cloud.ibm.com/docs/databases-for-postgresql?topic=databases-for-postgresql-resources-scaling),for more information.

Related runbooks:

- [MongoDB](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.edb-mongodb.down.html)
- [RabbitMQ]( https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/ibm/Contact_RabbitMQ_team.html)
- [Redis](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/api.edb-redis.down.html)

### For a PostgreSQL alert

1. Log to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
2. Click the person icon in the top right corner. Select **{{oss-account-full-name}}** under accounts.
3. From the resource list, select **Services** and filter out using **postgresql**
4. Select the service posted in the alert
    * ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/sysdig/sysdig_alert_example.png){:width="600px"}
5. In the example above the service is `Triggered for databases-for-postgresql at us-south databases-for-postgresql with ID 49c476de-4f6c-4918-8e67-97fa44369a5c`
6. Base on condition take appropriate action:
    - Connections:
        - Reaching maximum number of connections
            - **OPTION 1** (*Recomended in PRD to restore services quckly*)
                - Open Postgrest service of deployment with the problem
                - Select **Setting** from the left side menu
                - ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pgSQL/PostgresSQL-Settings.png){:width="600px"}
                - Scroll down until you see **End Connections - Caution**
                - ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/pgSQL/PostgresSQL-EndConnections.png){:width="600px"}
                - A popup message will appear, click on **Continue**
                - Wait for about 20 seconds, services will restore after this action.
            - **OPTION 2**
                - Open [pgAdmin](https://www.pgadmin.org/download/) or any other PG admin tool to check the number of connections.
                - Restart pods starting from  `api-pnp_status` to release any stocked connections. If you need to release more connections try `api-pnp-nq2ds`
                    - `kubectl oss pod delete -l app=api-pnp_status -n api`
                - Once the number of connection gets down Sysdig will send a signal of resolve to any channel set. If a {{doctor-alert-system-name}} is created, it will be auto resolved once the alert is cleared.
        - PG lost connections, this alert means PG DB lost connections and will cause and error: `Error:  sql: database is closed `
            - Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
            - Select **PNP**
            - Search for `database is closed` you may focus on `api-pnp-nq2ds` and `api-pnp-susbcription-consumer`
            - Restart any pod that shows the `database is closed`
                - `kubectl oss pod delete -l app=api-pnp_status -n api` for example

    - CPU/Memory/Disk usage:
        - If a configuration resource needs to be updated see,[Scaling up your installation](https://cloud.ibm.com/docs/speech-to-text-data?topic=speech-to-text-data-speech-scaling-12),for more information.

Related runbooks:
 [OSS IBM Cloud Databases for PostgreSQL Monitoring runbook](https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/apiplatform/Runbook-icd-postgres-monitoring.html)

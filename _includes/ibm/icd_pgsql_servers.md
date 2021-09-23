{% include {{site.target}}/load_icd_pgsql_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

The following is a list of PostgreSQL instances created under the `OSS Account {{oss-account-account}}` on [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}/)


| Name               | Hostname             | Port            | Location             | Region            | Environment     | Notes
| -----------        | ---------            | --------------  | -------------------  | ------            | --------------- | ------
| {{ossprod-name}}   | {{ossprod-hostname}} | {{ossprod-port}}| {{ossprod-location}} | {{ossprod-region}}| {{ossprod-env}} | {{ossprod-notes}} |
| {{ossstg-name}}    | {{ossstg-hostname}} | {{ossstg-port}}  | {{ossstg-location}} | {{ossstg-region}}  | {{ossstgenv}}     {{ossstg-notes}} |
| {{ossprodreplica-name}}   | {{ossprodreplica-hostname}} | {{ossprodreplica-port}}| {{ossprodreplica-location}} | {{ossprodreplica-region}}| {{ossprodreplica-env}} | {{ossprodreplica-notes}} |

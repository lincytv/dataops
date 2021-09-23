{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_palente_constants.md %}
{% include {{site.target}}/load_oss_apiplatform_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}

  - Look at the `{{ include.name }}` widget in the [Pa'lente Metrics - DataStore](https://one.newrelic.com/launcher/dashboards.launcher?pane=eyJuZXJkbGV0SWQiOiJkYXNoYm9hcmRzLmRhc2hib2FyZCIsImVudGl0eUlkIjoiTVRreU5qZzVOM3hXU1ZwOFJFRlRTRUpQUVZKRWZHUmhPamcyT0RFNCIsInVzZURlZmF1bHRUaW1lUmFuZ2UiOmZhbHNlLCJpc1RlbXBsYXRlRW1wdHkiOmZhbHNlLCJzZWxlY3RlZFBhZ2UiOiJNVGt5TmpnNU4zeFdTVnA4UkVGVFNFSlBRVkpFZkRFMk1qRTNPVGsiLCJlZGl0TW9kZSI6ZmFsc2UsImlzU2F2aW5nRWRpdENoYW5nZXMiOmZhbHNlfQ==&platform[accountId]=1926897&platform[$isFallbackTimeRange]=false) dashboard to see what errors are occurring with Elasticsearch
  - Look in LogDNA: Go to [{{logDNA-name}}]({{logDNA-link}}), See [{{logDNA-docName}}]({{logDNA-docRepo}}) for information on how to access and view logs on LogDNA.
    - Select the **PALANTE**, then **OSS-CSD(Palante)**
    - Filter out the region
    - Search for `Errors`
    - ![]({{site.baseurl}}/docs/runbooks/palente/images/logDNA/set_err_levels.png){:width="600px"}
  - Use the `Kubernetes dashboard` for the appropriate cluster in the [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}) console
    >Need help to access `Kubernetes dashboard` [here]({{site.baseurl}}/docs/runbooks/palente/Palente_Tips_and_Techniques.html#how-to-access-kubernetes-dashboards)
  - Use the `kubectl logs` command to view the logs of the api-oss-csd pod in the appropriate environment
      - examples:
       ```
         kubectl -napi logs api-oss-csd-<id> -c api-oss-csd -f
         kubectl -napi logs api-oss-csd-<id> -c api-oss-csd |grep Err
       ```

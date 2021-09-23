---
layout: default
description: This Runbook is for how to create a case to Armada team.
title: How to create a case to Armada team
service: IKS
runbook-name: How to create a case to Armada team
tags: Armada, cluster, IKS
link: /doctor/Runbook-How-To-Create-Case-To-Armada-Team.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}
__

## Apply access to create case

To create a case on IBM Cloud, you need to get `Editor` access of `Support Center` service. Please contact OSS admin help to grant the access to your account.

**OSS admin:** Ken(kparzygn@us.ibm.com), Shane(shanec@ca.ibm.com), Irma(irma@ca.ibm.com), Amit(joglekar@us.ibm.com), Jing(youjing@cn.ibm.com), Jim(yujunjie@cn.ibm.com)

**Steps to grant access(for OSS admin)**
* Logon [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
* Switch to `{{oss-account-full-name}}` account.
* Click `Manage users` on the bottom of the page.
* From the row for the user that you want to assign access, select the Actions menu, and then click `Assign access`.
* Select `Assign access to account management services`.
* Select service `Support Center`.
* Select `Editor` role.
* Click `Assign` button.

## How to create a case
* Logon [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}}).
* Switch to `{{oss-account-account}}` account.
* Click `Support` on the top of the page.
* On 'Find Answers' tab, click `Create a case`.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/support-case-create.png){:width="640px"}

* Choose a type of the case `Technical`.
* Choose a category: `Containers`.
* Choose an offering: choose the cluster which problem occurred on, for example `oss-stage-wdc06`.

![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/support-case-category.png){:width="640px"}

* Input the case summary in Subject field.
* Input the region, cluster id, and details of the issue in Description field, you can also paste error logs here or attach log files to the case.
* Add the person who want to watch the updates of this case in `Add another person to this case` field.
* Click `Submit` button.
* After you submit the case, you can find it in `Manage cases` tab.

## Reference
For all OSS developers who will use IKS environment, it is recommended of reading the IKS troubleshooting document as following. For any quick question of IKS, you can post it to Slack channel `#armada-users` for seeking help.

* [Troubleshooting clusters and worker nodes](https://cloud.ibm.com/docs/containers?topic=containers-cs_troubleshoot_clusters).
* [Troubleshooting cluster storage](https://cloud.ibm.com/docs/containers?topic=containers-cs_troubleshoot_storage).
* [Troubleshooting logging and monitoring](https://cloud.ibm.com/docs/containers?topic=containers-cs_troubleshoot_health).
* [Debugging Ingress](https://cloud.ibm.com/docs/containers?topic=containers-cs_troubleshoot_debug_ingress).
* [Troubleshooting cluster networking](https://cloud.ibm.com/docs/containers?topic=containers-cs_troubleshoot_network).

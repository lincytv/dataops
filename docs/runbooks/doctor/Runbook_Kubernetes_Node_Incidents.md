---
layout: default
description: Kubernetes Node Incidents Alert
title: Kubernetes Node Incidents
service: kubernetes
runbook-name: Runbook Kubernetes Node Incidents
tags: oss, bluemix, doctor, kubernetes
link: /doctor/Runbook_Kubernetes_Node_Incidents.html
type: Alert
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


# oss_kube_[prod|stage|dev]_[cpu|memory|filesys|syspod|pulse|network] incidents

## Purpose
Several Kubernetes production and staging clusters are being monitored by {{new-relic-portal-name}}. The alert indicates that a cluster or a node requires attention. Although in many cases the Kebernetes cluster may still be able to operate, the issue at the reported node should be resolved to prevent further deterioration.

## Technical Details
Each Kubernetes node is monitored for its CPU, memory, file system usage, network issues and Node response. Each Kubernetes cluster is monitored for its system pod status, and presence of monitoring metrics.

Each cluster is associated with its own monitoring conditions, therefore monitoring conditions can be adjusted for each cluster independently.

There are four alert policies:
  * All production clusters.
  * All staging clusters.
  * All Development cluster.
  * Host/Node Not responding

Each policy is associated with its own notification channels; therefore, all production clusters have the same notification setup; as well as all staging clusters.

Special access privilege may be required for the Ops support to view the performance and to work with the Kubernetes cluster.

## User Impact
Depending on the nature of the alert, a Kubernetes node or cluster may or may not be operating. Even when it's still operating, its performance may be impacted.

## Instructions to Fix

{% include {{site.target}}/oss_bastion_guide.html %}

### Do not mark {{doctor-alert-system-name}} incident _resolved_
Once the underline issue is fixed, {{new-relic-porta-name}} will recognize the violation no longer exists, and send a _resolved_ signal to TIP, and the ServiceNow and {{doctor-alert-system-name}} incidents will become resolved on their own.

### Identify reported Kubernetes cluster and node
The incident name and details include the region {% if site.target == 'ibm' %}(us-south, us-east, `eu-de` {% else %}<<cloud regions here>>{% endif %}, the cluster (production or staging) and the node (named by its IP address) being reported. The incident name includes the nature of the concern: cpu, memory, disk, etc.

### {{new-relic-portal-name}} basics
{{new-relic-portal-name}} official document on [Monitoring Integration](https://docs.newrelic.com/docs/integrations/host-integrations/host-integrations-list/kubernetes-monitoring-integration). To see current and past CPU, memory, disk usage, and network stats of a node:

  * Go to [{{new-relic-portal-name}} Infrastructure]({{new-relic-portal-link-infra}}).
  * Another way to view the details is by using the [Kubernetes Cluster Explorer](https://one.newrelic.com/launcher/k8s-cluster-explorer-nerdlet.cluster-explorer-launcher?pane=eyJuZXJkbGV0SWQiOiJrOHMtY2x1c3Rlci1leHBsb3Jlci1uZXJkbGV0Lms4cy1jbHVzdGVyLWxpc3QifQ==)
  * Click on **FILTER HOSTS** in the left.
  * Enter the Kubenetes node IP found in the incident description.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/infra/filter_host.png)
  * For CPU and memory.
    - Use the _Hosts_ tab from the second banner at the top.
    - Filter as shown before.
  * For memory.
    - Use the _Storage_ tab.
    - Filter as shown before.
  * For network.
    - Use the _Network_ tab.
    - Filter as shown before.
* A few widgets are shown on the panel by default, usually including _CPU %_, _Memory Used %_, _Disk Used %_ etc. If the data you are interested in is not one of those shown, use the drop-down of the any widget to select another data series
![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/infra/change_data_series.png)
* By default, only data from the last hour is shown. To see older data.
  * Click on the three dots at the top right corner of the widget.
  * Invoke _View query_.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/infra/3_dots_view_qry.png)
  * Then _View in Insights_.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/infra/chart_qry.png)
  * In the new window opened with {{new-relic-portal-name}} Insights.
  * Modify the query.
  * Click the _run_ button.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/insights/query.png)

    - In many {{new-relic-portal-name}} pages, there is a _time picker_ or select the range metrics based on time.
    - In {{new-relic-portal-name}} queries, clauses like _SINCE_ and _UNTIL_ can be used to select the time span.

### Kubernetes access and command line basics
* [Access]({{repos-cloud-sre-tools-platform-link}}/wiki/How-to-Access-OSS-Armada-Cluster) Armada OSS [kubernetes clusters]( https://cloud.ibm.com/kubernetes/clusters)
* Get started with [IBM Cloud CLI](https://cloud.ibm.com/docs/cli?topic=cli-getting-started)
* Kubernetes command line [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/)
* Kubenetest pods can be deleted, and Kubenetes will recreate them. By deleting and having Kubernetes to recreate pods, some resource might be freed.

#### Using kubernetes commands
To start working in a specific cluster, do the following:
In the [IBM Cloud webpage](https://cloud.ibm.com/kubernetes/clusters), click the cluster, from top right, click "Actions ..." then you can use either "Web terminal" or "connect via CLI...".

### Verify the issue
Access privilege may be required for the Ops support to view the Kubernetes system performance information in {{new-relic-portal-name}}.

Follow the incident link to confirm the {{new-relic-portal-name}} alert condition violated, or start from [{{new-relic-portal-name}} Insights]({{new-relic-portal-link-insights}}), to view the overall system performance.

 A Newrelic Dashboard have been created to assist you with the investigating. Access the [Kubernetes Integration - Infrastructure](https://insights.newrelic.com/accounts/1926897/dashboards/546408) and view each Panel based on the incident reported.


### Resolving the issue

<div class="alert alert-warning" role="alert">

Access privilege may be required for the Ops support to manage the Kubernetes clusters.
If you do not have the required access, assign this alert to a Seconadry on-call.

</div>

#### How to delete pods

The find out the pods with high resource usage and delete them
* Go to [{{ibm-cloud-dashboard-name}}]({{ibm-cloud-dashboard-link}})
* Log into **OSS account**
> Switch to account `{{oss-account-account}}`
* Click on the cluster being reported
> The PD title will have the cluster name e.g. INC0519440:ESC0988190:**Staging cluster** memory usage high, click on **OSSStage**<br>
Location is also provided on the PD oss_kube_stage_memory_high.2.**us-east** in this case it is referring to **Washington DC**

* Click on **Kubernetes Dashboard** on the top right
![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/kube_dashboard.png){:width="640px"}
* Click on **Nodes** in the left banner under **Cluster**
* Click on the node being reported
> Details: oss_kube_stage_memory_high.2.us-east.SLD2: Critical on 10.188.27.141. The node will be  **10.188.27.141**

![]({{site.baseurl}}/docs/runbooks/doctor/images/ibm_cloud/find_nodes.png){:width="640px"}
* In the page for the node, click on the Namespace dropdown to select "All namespaces" (unless you know a specific namespace in which a pod is causing the problem)
* Scan through the tables to see resource usage by each pod. For "memory usage high" incidents, pick those with a high memory usage to delete.
* To delete a pod, remember the namespace and name of the pod, click on the button with three dots, then press Delete.
* After deleting a pod, make sure a new pod is created, and is using less resource.
* The newly created pod will have the same name (ignore the suffix) and in the same namespace. It may or may not be running on the same node, but it will be in the cluster.
* The Kubernetes command to see node or pod with top CPU/memory usage are `kubectl oss top nodes` and `kubectl oss top pods --all-namespaces`
* The Kubernetes command to delete a pod is `kubectl oss pod delete [pod name] -n [pod namespace]`
> If you get a message like the follow: `Error from server (Forbidden): pods.metrics.k8s.io is forbidden:` <br> `User "IAM#wyue@ca.ibm.com" cannot list resource "pods" in API group "metrics.k8s.io" at the cluster scope` contact a Kubernetes admin in the Doctor team ({% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} or {% include contact.html slack=bluemix-dev-slack name=bluemix-dev-name userid=bluemix-dev-userid notesid=bluemix-dev-notesid %} to request access to the namespaces.


### 1. `oss_kube_[prod|stage|dev]_cpu_high`
### 2. `oss_kube_[prod|stage|dev]_memory_high`
Check if there is any Kubernetes pod can be removed.
Delete and re-create pods which may be a significant resource consumer.
At docker level, try to free up some resources by deleting older docker images, restart docker containers, etc.

Here are a few runbooks with some useful procedures, related to checking disk space, usage and stopping and restarting a docker container using ```docker rm``` and ```{{doctor-compose-cmd}}```, etc.
* [Doctor disk usage runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Disk_Usage_is_High.html)
* [Doctor blink runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_Doctor_Blink_ibm_allenvs_network_doctor_blink.html)
* [BBO runbook]({{site.baseurl}}/docs/runbooks/doctor/Runbook_BBO_Agent_Down.html)

### 3. `oss_kube_[prod|stage|dev]_disk_high`
This rarely happens, however there isn't much the on-call agent can do.
Contact an admin ({% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} ) and provide the incident information.

### 4. `oss_kube_[prod|stage|dev]_syspod_down`
This incident indicates that, for an extended period of time, there is at least one pod in the Kubernetes `kube-system` namespace not in _Running_ state. The names of the pods in the unexpected state over the time are usually different but with the same prefix.

During the upgrade or maintenance of certain apps, it is normal for Kubernetes to restart their pods one at a time: system pods from several work nodes in each affected cluster take turn to go into _Pending_ state, and eventually will return to _Running_ state when the upgrade or maintenance is completed.

It is only of concern if the same pod gets stuck in the _Pending_ state for an extended time (over an hour?). You may consider to ask in the ([{{oss-kube-work-name}}]({{oss-kube-work-link}}))  Slack channel if there is any work being done on the cluster which affects pods of that name, and snooze the alert for an hour to see if it goes away.

To find out the name of the _Pending_ pod:
  * Click the [{{new-relic-portal-name}} Incident]({{new-relic-portal-link-alert}}) link.
  * Click the **k8sPodSample** query_ overview link.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/new_relic/alerts/k8sPodSample_qry.png)
  * To see historic pending pod count:
    - Copy-paste the query to [{{new-relic-portal-name}} Insights]({{new-relic-portal-link-insights}}).
    - Modify the _SINCE_ time.
    - To see the name of the pending pod:
      * In [{{new-relic-portal-name}} Insights]({{new-relic-portal-link-insights}}).
      * Modify with the query to, e.g.:
      ```
      SELECT podName from K8sPodSample where namespace='kube-system' and status='Pending' and clusterName='[the cluster name in the original query]' SINCE '[the timestamp in the original query]'
      ```

In a command prompt, login and setup `KUBECONFIG` as described above, then run `kubectl get pods -n kube-system | grep kube-state-metrics` to see if Kubernetes metrics is running, if not, restart by doing the following in command line:
* `git clone git@github.com:kubernetes/kube-state-metrics.git` to download kube metrics to a folder
* `kubectl delete -f kube-state-metrics/kubernetes/` to delete the current metrics
* `kubectl create -f kube-state-metrics/kubernetes/` to deploy new metrics
A Pager Duty alert as result of `kube-state-metrics` pod-not-running would not resolve itself after the metrics pod is fixed.  Run `kubectl get pods -n kube-system | grep kube-state-metrics` again, if the state is `Running`, manually resolve the Pager Duty alert.

Due to New Relic limitation, after an extedned period of downtime, even if all system pods are back to normal, such New Relic incident may not get resolved by itself, therefore the Pager Duty alert stays on.
After confirm all system pods are indeed running, click the New Relic incident link in the Pager Duty incident descrption to get to the New Relic alert. Find the "Manually close violation" link and click to close it in New Relic. The corresponding Pager Duty incident will go away afterwards.

If it is confirmed that Kubernetes is having difficulty creating a pod, contact a Kubernetes admin in the Doctor team ({% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} or {% include contact.html slack=bluemix-dev-slack name=bluemix-dev-name userid=bluemix-dev-userid notesid=bluemix-dev-notesid %} or {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}).

### 5. `oss_kube_[prod|stage|dev]_no_metrics`
Either the Kubenetest agent is not working properly on a Kubernetes node, or there is a network problem preventing the metrics to be received by {{new-relic-portal-name}}.

Find the state of the node using `https://cloud.ibm.com/resources`. Click on the corresponding cluster, then click on the "Worker Nodes" tab.
If there is the problematic node is not in "Normal" state, select the node, then try the "Reload" action; if reload doesn't fix the problem, try "Reboot".
If you do not have the authority to reload or reboot the node, contact one of the Kubernetes admin listed below.

If all nodes are in "Normal" state, but there is no metrics, investigate if there is any network and connection issue.

To see agent connection events:
  * Go to [{{new-relic-portal-name}} Incident]({{new-relic-portal-link-alert}})
  * Click the _Go to [node IP] overview_ hyperlink.

  * In [{{new-relic-portal-name}} Infrastructure]({{new-relic-portal-link-infra}}) page.
  * Click the _Events_ tab.
  * There should be _Agent disconnected_ and _Agent connected_ events matching the incident.
  * Contact a Kubernetes admin in the Doctor team ({% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} or {% include contact.html slack=bluemix-dev-slack name=bluemix-dev-name userid=bluemix-dev-userid notesid=bluemix-dev-notesid %} or {% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %}) to fix the {{site.data[site.target].oss-doctor.links.new-relic-portal.name}} agent on the Kubernetes node.

### 6. `oss_kube_[prod|stage|dev]_network_err`
This is an aggregation of four metrics data series (_receiveDroppedPerSecond_, _receiveErrorsPerSecond_, _transmitDroppedPerSecond_, and _transmitErrorsPerSecond_), over all nodes in the cluster.

Follow the {{new-relic-portal-name}} incident link to note all the node IPs in the cluster.
  * Go to [{{new-relic-portal-name}} Infrastructure]({{new-relic-portal-link-infra}}).
  * Use the _Network_ tab.
  * Filter on one or more nodes, and see the data of for the four series.
  * Try different queries to narrow down the issue to one node or one data series.
  * If all irregularities are from one work node, try reboot or reload the work node (this can be done from IBM Cloud portal).
  * If a network problem is confirmed and still exists
    - Contact the Doctor team ([{{oss-doctor-name}}]({{oss-doctor-link}})) to resolve the problem with Armada and the network team.

## Notes and Special Considerations
This runbook is still being developed, and {{new-relic-portal-name}} monitoring of Kubernetes is still being tested. When in doubt, contact a Doctor team member ({% include contact.html slack=doctor-backend-2-slack name=doctor-backend-2-name userid=doctor-backend-2-userid notesid=doctor-backend-2-notesid %} or {% include contact.html slack=doctor-backend-slack name=doctor-backend-name userid=doctor-backend-userid notesid=doctor-backend-notesid %} ) and resolve the {{doctor-alert-system-name}} incident.

{% include {{site.target}}/tips_and_techniques.html %}

---
layout: default
title: "API Platform - Worker node NotReady state"
type: Alert
runbook-name: kubernetes node not ready
description: "This alert will be triggered when a kubernetes worker node is in NotReady state"
service: kubernetes
tags: kubernetes, worker node, not ready, NotReady
link: /apiplatform/kubernetes_node_notready.html
---
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


## Purpose
To notify users of the state of Kubernetes worker nodes. On occasion, a worker node cannot recover from the state `Node NotReady`. Newrelic monitors the state of worker nodes and reports on the condition `Node NotReady`.

## Technical Details
Our kubernetes clusters contain several worker nodes responsible for running our applications. When a worker node cannot recover from the `NotReady` state it prevents any pods from running their tasks.
If Newrelic detects this condition it issues an alert for the violation period.

## User Impact
Applications cannot start until a worker node is ready.  


## Instructions to Fix


<div class="alert alert-warning" role="alert">

Operators require the role <strong>Operator platform</strong> to manage the Kubernetes clusters.
If you do not have the required access, assign this alert to a Secondary on-call.

</div>

### Identify reported Kubernetes cluster and node
The incident name and details include the region {% if site.target == 'ibm' %}(us-south, us-east, eu-de){% else %}<<cloud regions here>>{% endif %}, the cluster (production or staging), 
and the node (named by its IP address) being reported. The incident name includes the nature of the concern: `Node <IP_ADDRESS> status is now: NodeNotReady`.

 - Access the [{{ibm_cloud-name}}]({{ibm_cloud-link}}) using your W3 credentials.
 - The IBM Cloud page opens:
 Navigate to the cluster link as per below screen capture

 ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/kubernetes/k8s_wns_cloud_acct_and_cluster_link.png){:width="880px" height="500px"}

 - The cluster listing page opens:
  Select the desired cluster by clicking on its link; see enclosed capture:

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/kubernetes/k8s_wns_cluster_listing.png){:width="980px" height="400px"}

 - The selected cluster page opens:
   1. Navigate to `Worker Nodes`
   2. Click on the `checkbox` besides the worker node name, taking care it corresponds to the same IP address
      which triggered the `Pager Duty` alert.
   3. If your permission and role allows, you will see a set of actions on the menu bar right above the
      list of worker nodes. Select `reload`

An example follows:

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/kubernetes/k8s_wns_wnode_actions_page.png){:width="980px" height="200px"}

### Do not manually resolve the {{doctor-alert-system-name}} alert
Once the worker node reloads properly, {{new-relic-portal-name}} will recognize the violation no longer exists, and send a _resolved_ signal to TIP which will, in turn, allow ServiceNow and {{doctor-alert-system-name}} to resolve the incidents automatically.


### Notes and special considerations
Should the instructions in this runbook fail to address the problem or if you have found
an error with or have a suggestion/comment regarding this runbook, please contact the appropriate person:

#### For kubernetes specific problems (e.g. error messages while executing `reload` action):  

{% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}  
{% include contact.html slack=tip-api-platform-1-slack name=tip-api-platform-1-name userid=tip-api-platform-1-userid notesid=tip-api-platform-1-notesid %}  

#### For runbook errors/suggestions:  

{% include contact.html slack=sosat-netcool-alt-slack name=sosat-netcool-alt-name userid=sosat-netcool-alt-userid notesid=sosat-netcool-alt-notesid %}

---
layout: default
description: How to setup cross-region replication for a Cloudant database
title: How to setup cross-region replication for a Cloudant database
service: tip-api-platform
runbook-name: How to setup cross-region replication for a Cloudant database
tags: oss, pnp, runbook, secrets, vault, password, credentials, rotation
link: /apiplatform/How_To/Setup_Cloudant_Replication.html
type: Informational
---

## Purpose
This runbook illustrates the necessary steps to setup cross-region replication for a Cloudant database.

See [this diagram](https://cloud.ibm.com/docs/Cloudant?topic=Cloudant-configuring-ibm-cloudant-for-cross-region-disaster-recovery#configuring-ibm-cloudant-for-cross-region-disaster-recovery) to see the cross-region redundancy for disaster recovery setup.

## Setup IBM Cloud Cloudant Database Replication 

Follow these instructions to setup cross-region replication for active-active mode:

Navigate to [IBM Cloud Console Resources](https://cloud.ibm.com/resources), search for Cloudant within the list of available services. You can use the search bar under the name property to find the entries related to Cloudant.

1. Search for Cloudant service.
2. Select the appropriate Cloudant instance(s).
3. Navigate to `Service credentials`. Take note of the manager IAM api key for each instance.
4. Navigate to `Manage`. Click on the `Launch Dashboard` button to go to the respective instance's Cloudant console UI.
5. Go to the `Replication` page. Click on the `New Replication` button on the top right of the table.

    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cloudant/cloudant_replication_page.png){: width="700" }

6. Fill in the fields as shown. The source should be the current instance and the target is the instance that you would like to replicate to. The URL for the remote database should be following the pattern `<CLOUDANT_URL>/<DBNAME>` (e.g. `https://227ff1b3-8453-43be-9d44-84ddae668eed-bluemix.cloudant.com/edb-rolling-metrics`). 

    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cloudant/cloudant_replication_existing_remote_db.png){: width="700" }

    If the database does not exist on the target instance, select `new remote database`.

    ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cloudant/cloudant_replication_new_remote_db.png){: width="700" }

    Click on the `Start replication` button to complete the creation step.

7. Ensure that on the `Replication` page for the replication that you have just created, the value of the `Type` is `Continuous` and the value of the `State` is `Running` with no errors.

8. Repeat steps 5 - 7 on the other Cloudant instance, making sure that the source and target are switched.


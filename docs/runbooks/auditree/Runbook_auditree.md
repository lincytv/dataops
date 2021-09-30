---
layout: default
description: Auditree 
title: Auditree Runbook
service: auditree
runbook-name: auditree
tags: auditree, sos, vulnarabilities
link: /auditree/Runbook_auditree.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}


## Settingup Auditree : 

Auditree provides automated checking and reporting for compliance and security controls, to reduce the number of audit findings across IBM.

- Here is the starting document to help setup Auditree [https://pages.github.ibm.com/auditree/user_docs/user_docs.html](https://pages.github.ibm.com/auditree/user_docs/user_docs.html)

**Access:** owner privileges to the GitHub organisation is required in order to setup Auditree.
The seed command (discussed in the link above) can be used to setup Auditee repos. The command creates an auditree config and evidence locker private repo’s 

- If we encounter below error while setting up Auditree using seed make sure the following git configuration is setup with your values. 

**Eg:** priyavegiraju:~/seed$ git config -l
user.name=xxxx
user.email=xxxx@ca.ibm.com

![SeedInstallationError1]({{site.baseurl}}/assets/images/SeedInstallationError1.png){:width="380px" height="388px"}

![SeedInstallationError2]({{site.baseurl}}/assets/images/SeedInstallationError2.png){:width="380px" height="388px"}

[https://github.ibm.com/dataops/evidence_locker](https://github.ibm.com/dataops/evidence_locker)
[https://github.ibm.com/dataops/auditree_config](https://github.ibm.com/dataops/auditree_config)

- The next step is to configure the fetchers/checks to execute. Each provider provides a README to indicate how to use and configure their fetchers/checks. These are defined in the auditree-central repo:[https://github.ibm.com/auditree/auditree-central](https://github.ibm.com/auditree/auditree-central)


- A current summary list of Provider fetchers and checks that have been developed can be found in the below link and the detail behind each is available at Auditree-Central Repo

[https://gist.github.ibm.com/simonmetson/d7252ad6b352286ddfc2c72614477d10](https://gist.github.ibm.com/simonmetson/d7252ad6b352286ddfc2c72614477d10)

- Auditree uses a set of fetchers to retrieve evidence from evidence providers, this evidence is stored in an evidence locker. Auditree then runs checkers against the evidence to validate that a control, or part of a control, is compliant. The outcome of this check is stored in the evidence locker as a report, and if the outcome is negative, a notifier is used to alert the service that remediation is required.

## settingup travis job :

After Auditree is setup configure the Auditree_config repo into the Travis. 
[https://travis.ibm.com/dataops/auditree_config/branches](https://travis.ibm.com/dataops/auditree_config/branches)

If something fails in the Travis job, make sure that the environment variables which you are providing is correct.

![TravisEnvironmentalVariables]({{site.baseurl}}/assets/images/TravisEnvironmentalVariables.png){:width="380px" height="288px"}

![TravisEnvironmentalVariables2]({{site.baseurl}}/assets/images/TravisEnvironmentalVariables2.png){:width="380px" height="288px"}


Account API key( prod &test -midtier, datatier) should have access to the following
Viewer, Reader - Kubernetes services
Viewer, Reader - Container services
Viewer - applicable resource groups


For `SOS_INVENTORY_API KEY & EMAIL` follow  [https://w3.sos.ibm.com/inventory.nsf/profile.xsp](https://w3.sos.ibm.com/inventory.nsf/profile.xsp)
For   `SOS-REPORTS-API-KEY` follow [https://pages.github.ibm.com/SOSTeam/SOS-Docs/api_platform_service/SOS-API-Service/](https://pages.github.ibm.com/SOSTeam/SOS-Docs/api_platform_service/SOS-API-Service/)
For `SLACK-WEBHOOK` follow [https://complianceascode.github.io/auditree-framework/notifiers.html#](https://complianceascode.github.io/auditree-framework/notifiers.html#)

After adding all the required fetchers and checks we can see the cluster reports here. 
[https://github.ibm.com/dataops/evidence_locker/tree/master/reports/registry](https://github.ibm.com/dataops/evidence_locker/tree/master/reports/registry)

If few clusters has to be excluded follow [https://github.ibm.com/auditree/auditree-central/blob/master/auditree_central/provider/registry/README.md#vulnerability-advisor-scan-results](https://github.ibm.com/auditree/auditree-central/blob/master/auditree_central/provider/registry/README.md#vulnerability-advisor-scan-results)

Rest all other Env variables will come by default when we configure Travis job 

•	If something fails because of a fetcher, make sure that the fetcher is added correctly inside controls.Json file in Auditree-config repo 
•	If something fails because of checks make sure that the path of the check added is correct inside controls.json file.

Eg: "auditree_central.provider.sos.checks.test_qradar.QRadarLogsLastSeenCheck": {
    "auditree_evidence": {
      "auditree_control": ["provider..auditree"]
    }
  }

Sos/checks is the folder path. Test_qradar is the name of the file. And, QRadarLogsLastSeenCheck is the class name (inside Auditree-central repo)

## Notifications :

For setting up notifications: Follow [https://complianceascode.github.io/auditree-framework/notifiers.html#](https://complianceascode.github.io/auditree-framework/notifiers.html#)


**slack:** #cpux-auditree-notifications (it’s a private channel where we can find all our Auditree notifications)

**gitissues:** To track the git issues [https://github.ibm.com/dataops/SOS_auditree-issues/issues](https://github.ibm.com/dataops/SOS_auditree-issues/issues)


If it fails to notify(slack/gitissues) make sure that the below line is there in run.sh file in travis folder 

![Notification]({{site.baseurl}}/assets/images/Notification.png){:width="680px" height="288px"}


## links :

- For, Gitissues [https://github.ibm.com/dataops/SOS_auditree-issues/issues](https://github.ibm.com/dataops/SOS_auditree-issues/issues)

- For, Cluster Reports [https://github.ibm.com/dataops/evidence_locker/tree/master/reports/registry](https://github.ibm.com/dataops/evidence_locker/tree/master/reports/registry)

- For, sos reports [https://github.ibm.com/dataops/evidence_locker/tree/master/reports/sos](https://github.ibm.com/dataops/evidence_locker/tree/master/reports/sos)


**Notes:** Kindly, post in #auditree-adaptors channel if any help needed. 
































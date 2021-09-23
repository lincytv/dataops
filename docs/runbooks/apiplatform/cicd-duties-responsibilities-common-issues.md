---
layout: default
title: CICD duties, responsibilities and common issues
type: Informational
runbook-name: cicd-duties-responsibilities-common-issues
description: "CICD duties, responsibilities and common issues"
service: tip-api-platform
tags: cicd
link: /apiplatform/cicd-duties-responsibilities-common-issues.html
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

## Overview

The OSS Platform CI/CD process is intended to follow [Cloud and Watson System Architecture DEVOPS](https://pages.github.ibm.com/CloudEngineering/system_architecture/guardrails_standards/devops.html) guidelines

- Continuous Integration and Continuous Deployment pipeline automation should be treated as code; check into source control, build, publish and deploy
- Clean separation between Continuous Integration and Continuous Deployment automations implemented as independent pipelines

For all OSS Platform components which are deployed as containers on Armada, we have a single [shared](https://jenkins.io/doc/book/pipeline/shared-libraries/) Jenkins CI pipeline hosted in the [oss-common-pipeline](https://github.ibm.com/cloud-sre/oss-common-pipeline/blob/master/vars/buildPublishComponent.txt) repository. There is a single Jenkins CD pipeline in the [oss-charts](https://github.ibm.com/cloud-sre/oss-charts/blob/staging/Jenkinsfile.cd) repository which handles deployments of helm charts to Armada

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_tip_platform.png){:width="640px"}

## Resources

- [OSS-TIP-Platform-CI-CD-Process Wiki page](https://github.ibm.com/cloud-sre/ToolsPlatform/wiki/OSS-TIP-Platform-CI-CD-Process-for-containers)
- [CICD Pipeline](https://ibm.ent.box.com/folder/40384786513) Box folder. Includes recordings, demos and presentations
- [OSS Team Education and Architecture](https://ibm.ent.box.com/folder/94173249018) Box folder. Includes recordings and presentations from Ken Parzygnat call. If you require access, please contact {% include contact.html slack=oss-platform-architecture-slack name=oss-platform-architecture-name userid=oss-platform-architecture-userid notesid=oss-platform-architecture-notesid %}- [Declarative deployment tools](https://github.ibm.com/cloud-sre/declarative-deployment-tools) repository that serves as a common collection of binaries that are needed for development and deployment to Kubernetes



## Request access to Jenkins

- [Jenkins Main Page](https://wcp-cto-sre-jenkins.swg-devops.com)
- Access is controlled by [BlueGroup](https://w3-03.ibm.com/tools/groups/protect/groupsgui.wss?task=Administrators&gName=jaas%2Dwcp%2Dcto%2Dsre%2Ddev). `Use your W3 credentials to login`
- Contact {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %} to add you

## Monitor Slack channels for Jenkins job status

**NOTE: If you are deploying code, it is your responsibility to keep a lookout for the jenkins job to ensure it's complete**

- [{{oss-slack-oss-charts-cd-name}}]({{oss-slack-oss-charts-cd-link}}) used for Jenkins CD pipeline status for OSS charts
- [{{oss-slack-oss-api-ci-name}}]({{oss-slack-oss-api-ci-link}}) used for Jenkins job status for tip api platform components
- [{{oss-slack-oss-tip-ci-name}}]({{oss-slack-oss-tip-ci-link}}) used for Jenkins job status for oss tip components
- [{{oss-slack-oss-cicd-name}}]({{oss-slack-oss-cicd-link}}) used for CICD Q&A
- [{{oss-slack-cto-sre-product-ci-name}}]({{oss-slack-cto-sre-product-ci-link}}) used for Travis CI job status for CTO SRE Productization team
- [{{oss-slack-oss-ciebot-ci-name}}]({{oss-slack-oss-ciebot-ci-link}}) used for Jenkins job status for ciebot

Example of Job status:

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_slack_msg.png){:width="640px"}

## View Job logs

- If the job fails, you can review the output log for errors that might give you indication of the issue using one of these options:

- Under the `Build History` section from the Branch [Stage View](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/oss-charts/job/production/), clcik on the failed build number, then select `View as plain text` from the navigation menu

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_viewastext.png){:width="400px"}

- Under the `Build History` section from the Branch [Stage View](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/oss-charts/job/production/), clcik on the failed build number, then select `View as plain text` from the dropdown menu

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_failedbuildInfo.png){:width="400px"}

## Validate helm charts

- Validate new or updated helm charts before merging your component updates to master. You can validate/dry-run a deployment manually calling [kdep](https://wcp-cto-sre-jenkins.swg-devops.com/job/Pipeline/job/oss-charts/job/PR-11167/2/display/redirect) using the -d and/or -v options.

## Be aware of components that trigger other job builds

- Components that have a `config-jenkins.yaml` file in their repo will have a list of other components for which a build will also get triggered. Search [Github](https://github.ibm.com/search?q=org%3Acloud-sre+%22%2FPipeline%2Fapi%22+extension%3Ayaml&type=Code) to view the list
- We must monitor the slack channels above and make sure all jobs are successful
- Reach out for help in [{{oss-slack-cto-oss-tip-internal-name}}]({{oss-slack-cto-oss-tip-internal-link}}) channel if you required assistance

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_component_trigger_other_job_builds.png){:width="640px"}

- Even though the component build was successful, the [Blue Ocean](https://wcp-cto-sre-jenkins.swg-devops.com/blue/organizations/jenkins/Pipeline%2Fapi-osscatalog/detail/master/29/pipeline) view of the build pipeline which triggers other builds will show the status of those triggered builds separately at the bottom of the page. For example:

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_blue_ocean_triggered_jobs.png){:width="640px"}

## Install Detect Secrets Developer Tool

- The Detect Secrets developer tool allows developers to detect secrets in their code before they push to GitHub. By detecting and stopping secrets before they find their way onto GitHub, you avoid remediation processes and make life easier for yourself, as well as your colleagues. The developer tool is a simple Python package that checks each local commit for secrets and then flags what it finds. This process allows you to remove the secrets from your code before you push your code to GitHub
- Installation instructions can be found on the [Detect Secrets](https://w3.ibm.com/w3publisher/detect-secrets/developer-tool) W3 page
- Additional information and troubleshooting topics are available on the [FAQ](https://github.ibm.com/Whitewater/whitewater-detect-secrets/wiki/Developer-Tool-FAQs) page
- You can also reach out to the team on their slack channel [#guild-detect-secrets](https://ibm-cloudplatform.slack.com/archives/CDMGJ9QG2)

* Example of the local commit:

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_dev_tool_verify.jpg){:width="640px"}

## Production deployment

- Normal schedule is once a day except during freezes
- Merge is handled on a rotational basis by the following contacts:

    * {% include contact.html slack=tip-api-platform-2-slack name=tip-api-platform-2-name userid=tip-api-platform-2-userid notesid=tip-api-platform-2-notesid %}
    * {% include contact.html slack=sosat-tools-slack name=sosat-tools-name userid=sosat-tools-userid notesid=sosat-tools-notesid %}
    * {% include contact.html slack=sosat-deploy-slack name=sosat-deploy-name userid=sosat-deploy-userid notesid=sosat-deploy-notesid %}
    * {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %}

- Approval is sought via [{{oss-slack-cto-oss-tip-internal-name}}]({{oss-slack-cto-oss-tip-internal-link}}) slack channel so please monitor for updates

## Common problems

**Current branch is behind**

![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_git_push_common_problem.jpg){:width="640px"}

- The other case appears when a previous push to the staging release branch in the oss-charts repository resulted in a failed deployment that was not taken care of. View the release-staging branch in question in oss-charts repository to find the failing PR and associated Jenkins job.  View the console log to find the failure reason, fix and re-run
- If a PR is manually closed with unmerged commits to the `release-staging-xx-xx` that needs to be resolved. If this was done in error, we can open the PR back up and it should kick off the CICD on it again

**Failed staging deployments**

- If there is a problem with the staging chart values causing deployment to fail, it is possible to make an update to the associated release-staging branch PR, which will trigger the Jenkins job to run again

**Manually Generated PR's**

- PR's to staging branch not generated through CICD pipeline need to be manually merged

**Failed production deployment**

- If there are problems with production values in the charts, _ie. missing values_, incorrect vault values, these are not tested during the staging deployment.  We must be extra careful with these
- If the production deployments fails because of this, we cannot simply update the charts and re-run the jenkins job as it points to the already merged branch
- We would need to force an update of all the charts that did not get deployed because of the failure and run through the whole CD process again
- Failed integration tests during production deployment can also block the job from completing and require everything to run through the whole CD process again
- More information on vault can be found in [k8s fast track](https://ibm.ent.box.com/notes/286033630512?s=8jad9em1wmd2d6tkvomxci49jkl5b39r) boxnote

**520: Web server is returning an unknown error**

- If the review the log (see View Job logs section) and you encounter a 520 error, this could be due to connection issue between Cloudflare and the origin web server or possible containers issue

- We could just try to re-run the job using the `Replay` or `Rebuild` options from Jenkins as described in the below section. The issue presisted, please reach out for help in [{{oss-slack-cto-oss-tip-internal-name}}]({{oss-slack-cto-oss-tip-internal-link}}) channel

**cf_slave down**

- If you see a large number of failed Jenkins jobs, it's possible that the docker slaves are offline. This can be caused by an intermittent Jenkins issue
- Check the job log ((see View Job logs section) and look for this type of error

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_cf_slave.jpg){:width="600px"}

- Check the [{{oss-slack-taas-jenkins-help-name}}]({{oss-slack-taas-jenkins-help-link}}) channel for any reported issues
- We could just try to re-run the job using the `Replay` or `Rebuild` options from Jenkins as described in the below section
- If jobs still fail with the same error, reach out to [{{oss-slack-taas-jenkins-help-name}}]({{oss-slack-taas-jenkins-help-link}}) channel for assistance

**Unit test failures**

- At times, changes to a component will cause unit test failures in upstream pipelines
- Check the job log ((see View Job logs section) and look for an error that begins with `--- FAIL` like the below screenshot

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_integtest_FAIL.jpg){:width="600px"}

- The PR author will need to review the changes and try to re-run the job using the `Replay` or `Rebuild` options from Jenkins as described in the below section
- A successful unit test will look like the following screenshot

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_integtest_success.jpg){:width="600px"}

**Rebuilding failed jobs**

- From within the Blue Ocean UI, do not use the `Restart` link. Use the rerun icon in top toolbar:

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_failed_pipleline.png){:width="600px"}

- From within the classic UI, use the `Rebuild` menu option and the not _Restart from stage_

  ![]({{site.baseurl}}/docs/runbooks/apiplatform/images/cicd_jenkins_classic_ui.png){:width="600px"}

## Using Go Modules with CICD

**GO Modules Resources**

- Go modules are supported for Go versions 1.11 and up, all of which are supported by CICD<br>
- To use Go modules with CICD:

  - Commit `go.mod` and `go.sum` files to the component repo
  - Verify any local `Makefile` does not contain cicd-full target

- For an in-depth introduction to Go Modules, reference the official Go [documentation](https://blog.golang.org/using-go-modules)
- The golang [Github WIKI](https://github.com/golang/go/wiki/Modules) Modules page is an another excellent resource. On the page, there is an [FAQ](https://github.com/golang/go/wiki/Modules#faqs) section that provides answers and further details on common functions of Go Modules

**Developer Responsibilities when using Go Modules**

- As we migrate/transition to using Go Modules, it's the indiviual developer responsibility to maintain the versions of external packages and updating `go.mod` accordingly in their repository
- Maintain the correct import paths in your code

**CICD automatically updates private Go Modules**

- The CICD pipeline have been modified to automatically update the private (github.ibm.com) Go Modules to the latest version.

**Git Tagging with CICD**
Tagging will work as follows:

- Each component repo has a file called `metadata.json`. A field will need to be added in the file to specify the major and minor versions of the component. Ex: `"version": "1.3"`.  If it does not exist this will default to 1.0.
- This value must be updated by component developers for new major or minor releases. By default, CICD will just increment the patch version from the last version tagged. If the `major.minor` is updated to a value lower than the latest tagged version in git, the pipeline will fail.

## Runbook Owners

- {% include contact.html slack=ss-security-focal-slack name=ss-security-focal-name userid=ss-security-focal-userid notesid=ss-security-focal-notesid %}
- {% include contact.html slack=edb-admin-slack name=edb-admin-name userid=edb-admin-userid notesid=edb-admin-notesid %}

## Notes and Special Considerations

{% include {{site.target}}/api-platform-notes.html %}

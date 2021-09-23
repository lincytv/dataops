---
layout: default
title: OSS DevOps Platform Runbooks Workflow
description: New description
---

## Background

We need to have a single location for publishing runbooks so they can be searched, navigated and have a common look and feel.

To support these requirements for a single Wanda runbooks environment, runbooks will be migrated into new forked repositories that generate static sites via GitHub Pages and Jekyll.  We don't want to maintain several copies of the runbooks.

The plan is to fork the [https://github.ibm.com/Bluemix/runbooks](https://github.ibm.com/Bluemix/runbooks) repository _(which represents the single Wanda runbooks environment)_ in each of the organizations where we host our runbooks today and provide automated pipeline scripts to validate the runbooks on pull requests and merge to the remote master.
Currently we have:
- [https://github.ibm.com/cloud-sre/runbooks](https://github.ibm.com/cloud-sre/runbooks) with published runbooks at [https://pages.github.ibm.com/cloud-sre/runbooks](https://pages.github.ibm.com/cloud-sre/runbooks)
- [https://github.ibm.com/sosat/runbooks](https://github.ibm.com/sosat/runbooks) with published runbooks at [https://pages.github.ibm.com/sosat/runbooks](https://pages.github.ibm.com/sosat/runbooks)

Each of the components will have a separate directory to hold their respective runbooks and we should not run into any merge conflicts with other components.

## Contributions
Contributions are welcome! Please follow the process below to contribute.

## Issues
For any issues, we would prefer having an issue created in the [ToolsPlatform repo](https://github.ibm.com/cloud-sre/ToolsPlatform/issues) and labelled against *Productization*.


## Runbooks Feature Development

Simple text changes may be made directly by editing via GitHub on the web, but more complex updates, content references for example, should be made and tested using the workflow, guide and steps below. 

If you make an edit directly via Github to the master branch, it will take a few minutes to see your updates on the generated site. A Travis job will run to first validate and then generate the new static page. If the Travis job fails the site will fail to build. Travis job status can be found on the [#cto-sre-product-ci](https://ibm-cloudplatform.slack.com/messages/G873ERW9M) slack channel.  Any issues causing builds to fail need to be rectified immediately.

--------------

We subscribe to the [Git Feature Branch workflow](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow).

Follow the guide on [Adding Runbook documentation]({{ site.baseurl }}/docs/doc_updates/runbook_updates.html) for information on adding new runbooks,
templates and how to include conditional content based on target audience, e.g. IBM or Wanda.

### Steps to Follow:
1. Start with an updated local master branch by checking out the master branch and pulling changes:\\
`git checkout master`\\
`git pull origin master`

2. Create and checkout a feature branch:\\
`git checkout -b username-issueid-fancy-branch-name`
*Note: Include username, issue id and short description as part of the branch name.  When committing code for a GitHub issue, use the issue number in the commit comment.*

3. Do work in your feature branch, committing early and often:\\
`git commit -m "Comment about the commit"`

4. Rebase frequently to incorporate upstream changes:

    `git fetch origin master`\\
    `git rebase origin/master`

     -- or --

    `git checkout master`\\
    `git pull`\\
    `git checkout username-issueid-fancy-branch-name`\\
    `git rebase master`

5. Optional: Perform an interactive rebase (squash) of your commits before pushing the branch:\\
`git fetch origin master`\\
`git rebase -i origin/master`

6. Once you have reviewed your changes, and verified formatting and intention, push your changes upstream to origin:\\
`git push -u origin username-issueid-fancy-branch-name`

### Get Your Runbooks Validated
Your runbook markdown must pass validation checks, in order to be eligible for Merge.

1. Run `make -f OSSMakefile` in your workspace to validate changes made.  Running this script may update or generate json files for each component, which will be used for searching runbooks and generating navigation. Json files generated are placed under the directory: `/assets/json/`, with names in the format: `component_name-runbook-list.json`.  Include any affected json files within your pull request.
2. Open a pull request from `origin/username-issueid-fancy-branch-name` to `origin/master` in GitHub.
3. Standards for Runbook templates can be found [here]({{ site.baseurl }}/docs/doc_updates/runbook_updates.html#follow-the-runbook-templates).
4. After your changes pass validation, you can have your pull request reviewed and then merge to master.  *Note* you should wait for the travis job to complete succesfully on the PR before a merge is submitted.

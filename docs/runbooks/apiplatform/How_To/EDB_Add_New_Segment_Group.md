---
layout: default
title: How to add new segment access group for EDB
type: Informational
runbook-name: How to add new segment access group for EDB
description: How to add new segment access group for EDB when a new segment is onboarded
service: edb-api-oss
tags: edb, add, segment
link: /apiplatform/How_To/EDB_Add_New_Segment_Group.html   
---

## Purpose
This runbook should be used when a new segment has been onboarded to OSS Resources and we need to support it in EDB by creating a new access group for the new segment.

## How to create a new access group and assign it with correct permissions

You will have to perform this procedure twice: once for staging and once for production. The person performing these steps must have Admin privileges in the PNPServe IBM Cloud account.

1. Go to the IAM Groups page: [Staging](https://test.cloud.ibm.com/iam/groups) OR [Production](https://cloud.ibm.com/iam/groups). Make sure that you are in the correct IBM Cloud account (see table below):

    | Environment | Account Name             | Account ID                       |
    |-------------|--------------------------|----------------------------------|
    | Staging     | PNP TEST                 | 685c179b19614ba68b923f49e4f284bd |
    | Production  | 2310704 - IBM - PNPServe | 16629eea1f9b4c74bbf5e6b3e6f4fee8 |

2. Create a new access group by clicking the `Create` button at the top right of the table. \
   Get the proper name of the segment via the `Segments` tab of the [OSS Resources page](https://cloud.ibm.com/scorecard/resources?env=production). \
   Name of the access group should not contain spaces and instead be hyphenated (e.g. IBM-RegTech). \
   Description of the access group should follow the template: `EDB access group for segment <INSERT proper name of segment>` (e.g. EDB access group for segment IBM RegTech). \
   Click the Create button to submit and finish creating the new access group.
3. Click on the newly created access group to go to its details page. Record the ID of the access group by clicking the Details button at the top right of the page. \ 
   The ID should be a long alphanumeric string that begins with `AccessGroupId-`.
4. Record the segment ID of the segment by going back to the `Segments` tab of the [OSS Resources page](https://cloud.ibm.com/scorecard/resources?env=production) and clicking on the segment of interest to go to its details page. \
   Click the down arrow to the right of the title of the page (e.g. Segment: IBM RegTech) to reveal more information. Record down the segment ID value.
5. Download the [iam-utility-scripts](https://github.ibm.com/cloud-sre/iam-utility-scripts). Allow the shell (.sh) scripts to be executable by running command `chmod +x *.sh` inside the directory.
6. There are 3 scripts that we will be using: `getToken.sh`, `setAccessGroupPolicyResourceAttr.sh`, and `getPolicies.sh`. \ 
   Edit `getToken.sh` by filling in the value for `ADMIN_API_KEY` variable and uncommenting the correct (and commenting the incorrect) environment (STAGING or PRODUCTION) of IBM Cloud. \
   Run `./getToken.sh` and a `token.txt` file should be generated with its contents being a very long alphanumeric string.
7. Edit `getPolicies.sh` by filling in the value for `ACCOUNT_ID` variable (see table in step 1 for valid values) and uncommenting the correct (and commenting the incorrect) environment (STAGING or PRODUCTION) of IBM Cloud. \
   Run command `./getPolicies.sh > policiesBefore.txt` to record down all policies before we add a new policy.
8. Edit `setAccessGroupPolicyResourceAttr.sh` by filling in the values for variables (see table below):

    | Variable Name   | Description                                                                                                                                    | Example Value                                      |
    |-----------------|------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------|
    | ACCOUNT_ID      | Target IBM Cloud account ID (see table in step 1 for valid values)                                                                             | 685c179b19614ba68b923f49e4f284bd                   |
    | SERVICE_NAME    | For EDB, should always be edb-api-oss                                                                                                          | edb-api-oss                                        |
    | ACCESS_GROUP_ID | The ID of the access group created in step 3 (begins with AccessGroupId-)                                                                      | AccessGroupId-a351e09c-e755-4ab3-aaa6-18d0c08e2b18 |
    | RESOURCE        | Should be a hyphenated concatenation of the access group name (from step 2) and the segment ID (from step 4). `<ACCESS-GROUP-NAME>-<SEGMENT-ID>` | IBM-RegTech-60f6f6c3d9e0e8dd734b07ca               |
  
   Don't forget to uncomment the correct (and comment the incorrect) environment (STAGING or PRODUCTION) of IBM Cloud at the end of the script. \
   Run `./setAccessGroupPolicyResourceAttr.sh` and if successful, you should get a 201 Created response code along with the new policy JSON in the response body.
9. To verify the policy has been created, you can run command (similar to like you did in step 7) `./getPolicies.sh > policiesAfter.txt` and search for the new access group name or ID.

## How to modify EDB documentation and code to accept new access group
1. Create a PR against [auth.go](https://github.ibm.com/cloud-sre/edb-adapter-abstract/blob/master/common/auth.go) by adding a new element into the `SegmentsMapping` map. \ 
   The key should be the lowercase version of the `RESOURCE` variable value in step 8 of the previous section and the value is the same as the `RESOURCE` variable value in step 8 of the previous section.
2. Create a PR against [edb-api-map.yaml](https://github.ibm.com/cloud-sre/edb-mapping-api/blob/master/swagger/edb-api-map.yaml) by adding the value of the lowercase version of the `RESOURCE` variable value in step 8 of the previous section to the list of segment values under the POST and PUT descriptions.
3. Create a PR against [getting-started.md](https://github.ibm.com/cloud-docs-internal/dev-event-data-broker/blob/draft/getting-started.md) by adding the value of the lowercase version of the `RESOURCE` variable value in step 8 of the previous section to the list of segment values at the bottom of the document.
---
layout: default
title: OSS DevOps Platform Alert Incident Runbook Template
type: Informational
runbook-name: "Info on OSS DevOps Platform Runbook template for Runbook of Type 'Alert'"
description: "Info on OSS DevOps Platform Runbook template for Runbook of Type 'Alert'"
service: Conductors
tags: oss, template, runbook
link: /doc_updates/oss_alert_runbook_template.html
---

#### Required Metadata
```yaml
---
layout: default
title: <Replace with a title to be displayed on the runbook page (surrounded by double quotes)>
type: Alert
runbook-name: <Replace with runbook-name>
description: <Replace with description>
service: <Replace with service, e.g. Containers>
tags: <replace with comma separated list of relevant tags>
link: <relative link under runbooks folder to Runbook - replace .md with .html>
---
```

# [Alert ID] Alert Name

## Purpose
Describe purpose and cause of the alert.

## Technical Details
Describe the technical details of how the alert checks for the condition being alerted. Include any relevant details.

### Detail 1
When there are several technical details and it makes sense to categorize them.

### Detail 2
When there are several technical details and it makes sense to categorize them.

## User Impact
Describe the implications of the problem in terms of impact to users, ongoing risks, and impact to the SLA/SLO/SLI's. Include the severity and urgency of this problem.

## Instructions to Fix
1. Step by step instructions for fixing the problem.
2. If applicable include the following:
    - How to restore the service to normal operations from an end-user perspective.
    - How to do root cause analysis.
    - How to repair the service to a normal configuration, if needed.
3. Conclude with the expected outcome of the instructions.

## Notes and Special Considerations
Include the contacts for escalation when applicable.

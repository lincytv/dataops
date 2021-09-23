---
layout: default
description: When creating a runbook, you should include all important information related to the error received.
title: bluemix-ops - Creating Runbooks
service: doctor
runbook-name: "Creating Runbooks"
tags: oss, bluemix, runbook
link: /doctor/Runbook-Guidelines.html
type: Informational
---

## Overview

When creating a runbook, you should include all important information related to the error received. The runbook template was created to ensure that our team creates comprehensive complete guides that enable our operators to troubleshoot an alert. The template also ensures consistency through our entire runbook catalogue.

[Template]({{ site.baseurl }}/docs/doc_updates/oss_alert_runbook_template.html)

## Template Explained

**[Alert ID] Alert Name**
Each alert has a meaningful name to ensure immediate problem identification. Runbook title references the alert.

**Purpose**
Describe the purpose and cause of the alert.

**Technical Details**
Describe the technical details of how the alert checks for the condition being alerted.

**User Impact**
Describe the implications of the problem in terms of impact to users, ongoing risks, and impact to the SLA/SLO/SLI’s. Include the severity and urgency of this problem.

**Instructions to Fix**
Provide step-by-step instructions for fixing the problem. In priority order:

1. How to restore the service to normal operations from an end-user perspective (include code).

2. How to do root cause analysis.

3. How to repair the service to a normal configuration, if needed.

**Notes and Special Considerations**
Include contacts for escalation when applicable.

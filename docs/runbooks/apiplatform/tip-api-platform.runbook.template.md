---
layout: default
title: "Replace template title"
type: Alert
runbook-name: tip-api-platform.runbook.template
description: "Replace with description.  Surround with quotes."
service: tip-api-platform
tags: <replace with a list of relevant tags>
link: /apiplatform/tip-api-platform.runbook.template.html
---

{% capture sosat-netcool-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.slack }}{% endcapture %}
{% capture sosat-netcool-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.name }}{% endcapture %}
{% capture sosat-netcool-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.userid }}{% endcapture %}
{% capture sosat-netcool-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.notesid }}{% endcapture %}

# [Alert ID] Alert Name  (only if different from title in front matter above)

## Purpose

Describe purpose and cause of the alert.  
## Technical Details

Describe the technical details of how the alert checks for the condition being alerted. Include any relevant details.
### Detail 1

When there are several technical details and it makes sense to categorize them.
### Detail 2

Helpful tools for creating Markdown documents:  
 - [Mastering Markdown](https://guides.github.com/features/mastering-markdown/)  
 - [Markdown Table generator](https://www.tablesgenerator.com/markdown_tables)

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

## Contacts
{% capture sc %}{% include {{site.target}}/sosat-contacts.md %}{% endcapture %}
{{ sc | markdownify }}

**Runbook Owners**
* {% include contact.html slack=sosat-netcool-slack name=sosat-netcool-name userid=sosat-netcool-userid notesid=sosat-netcool-notesid %}

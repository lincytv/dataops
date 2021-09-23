---
layout: default
title: PagerDuty
---
# PagerDuty #

## Turning off specific PagerDuty incidents
You may want to prevent specific events from triggering PagerDuty incidents.  This is useful obviously if there is a specific known problem that you do not want to be woken up for.  To do this:

1.  Logon to [https://bluemix.pagerduty.com/](https://bluemix.pagerduty.com/).
2.  Click "Services" and search for "iot" and click "IOT Ops".
3.  Click the cog icon top right and select "Edit".
4.  Use your own judgement for 5 and 6 below but for example...
4.  Select the email filter "Accept email only if it matches ALL of the rules below".
5.  Create a rule "The email subject does not match the regex" and supply a regex that will match the subject of the email you wish to prevent from triggering an incident, eg. ".\*monagent-cloudant on host monagent-0 restarted automatically.\*".
6.  DON'T FORGET TO RESTORE THE ORIGINAL BEHAVIOUR 
---
layout: default
title: On Duty
---
## PagerDuty ##
PagerDuty is responsible for paging out the person holding the Ops phone.  It does this by:

* A phone call - a talking voice will detail the event that has been created and offer the option of interacting with the event via the keypad on the phone.
* An SMS - a TXT message will be sent to the phone detail the event.  Interaction with the event is possible by replying to the TXT.
* Email - an email is sent to iotf@uk.ibm.com with the details of the event.  The event CANNOT be interacted with via email.  The Notes mail database for IoT Foundation/UK/Contr/IBM forwards PagerDuty emails to all those on the Rota via a rule in the mail database.

You can log in to PagerDuty using the following username and interact with the event, view history and event detail.

PagerDuty: [https://bluemix.pagerduty.com/dashboard](https://bluemix.pagerduty.com/dashboard)
User Name: `iotf@uk.ibm.com`

## Being on call ##
On change over day you will get a laptop and phone.  **You** must check that the phone is not forwarded to some other number.  Just ring it if in doubt.

The phone contract is with Vodafone.  If you do not have good signal at your house or some place you wish to go whilst on call you can forward the phone to another number.  Just make sure you forward it to the right number and that number has signal/is plugged in!  SMS txt messages are obviously NOT forwarded.

## What to do in the event of a page out ##
*For compliance, any time you need to use the production SoftLayer account you must do so using the laptop provided.*

In the event of a page out, the operations person should "acknowledge" the event using either the keypad during the phone call or reply to the SMS to prevent escalation.  Escalation will be to notify the person holding the service nursery phone, who will most likely not know much about IoTF or be able to do anything meaningful.  They will simply attempt to get hold of someone from Ops.

The monitor component may trigger multiple times for the same problem.  If the event is not acknowledge then the new detail is simply appended to the existing event.  Otherwise a new event is created and page out will occur again.  Events are identified by the subject in the email.  Obviously multiple events may occur in a single instant.  

If you have acknowledged the event and are getting spammed, PagerDuty can simply be turned off *temporarily* by removing the `pagerduty/email` K/V from consul.  Monitoring will continue to function, but no events will be raised.  Logging in the monitoring scripts details any new events that are occurring.

Currently, the only monitoring that will result in a page out is done in the `monagent-e2e` container running on `monagent-0`.  It logs to stdout so the logs are not in Kibana and can only be seen via `docker logs monagent-e2e`.

**DO NOT FORGET** to add the K/V back in once the problem is resolved otherwise PagerDuty will not function!  The value needs to be `iot-ops@bluemix.pagerduty.com`.

The event will provide basic details (including time in UTC) of why it was raised.  Currently these are:

* The e2e container starts (or restarts!).  This lets us know that the e2e conatiner started ok after a deploy, but also importantly that it may have restarted.  The script is designed to ensure that in any exceptional event it panics and exits, thus restarting.  This is a page out either because there is something wrong with the system or the monitoring is not working.  A side effect of this is that you may see information in the PagerDuty event for e2e starting interleaved with information as to why it is restarting.   
* E2E application/device is unable to connect to the broker.  Python exception included in details of the event.
* Some or all MQTT messages were not received by the E2E subscribers.  % message loss will be included in the details of the event.
* 10% or more Historian messages not found 30 seconds after being published.  % message loss will be included in the details of the event.

Once the problem is resolved, the event can be "resolved".

Currently, the incident reporting focuses on the availability of messaging and historian, from a customer perspective.  If the monagent scripts for running an end-to-end flow aren't able to work successfully, an event is raised.

Here is the link to the Notes Task ID:  [`IoT Foundation/UK/Contr/IBM` (`iotf@uk.ibm.com`)](/iotf-task-id.ndl)

## Engaging Support for Technology Used by IoTF ##
Sometimes a problem will be in a component which we do not support.  There are many, each with their own means of engaging support if support is available.

A [page in the wiki](https://w3-connections.ibm.com/wikis/home?lang=en-gb#!/wiki/Wbaca767aac15_4918_91ec_7d5014efde02/page/Dependency%20table%2C%20contact%20links) details support for our components with invocation procedures.

For certain components like MessageSight, you may need to supply must gather as well as traces/dumps etc.  See [Gathering diagnostics](/docs/ops/dumps.html)

## Infrastructure Problems Preventing you from Working on a Problem Out of Hours ##
In the event that an infrastructure problem is preventing you from resolving a problem out of hours (for example RTC is down), you can contact the Duty Manager directly on `07711 228586`.  They can invoke devops in Hursley.

## What if a PagerDuty Event is not Acknowledged - Escalation ##
In the #unlikely# event that a PagerDuty event is not acknowledged, the event will escalate after 30 minutes.  Therefore it is important to acknowledge the event within 30 minutes of being alerted.  The escalation is to page out the what is called a nursery phone.  The person holding that phone will typically not have production access and may not know anything about IoTF.  The only thing they will normally attempt to do is get hold of the person on duty for IoTF Ops and failing that, someone else from the rota.

PagerDuty is also in place for IoTF Support.  Paying customers can open tickets to get support.  In the event that a sev 1 support ticket is not acknowledged, the PagerDuty event will escalate to IoTF Ops.  Typically someone from IoTF Ops will not have access to the tools required to answer the customer's ticket and so, as with the inverse, you should attempt to get hold of the person holding the nursery phone, or someone else from that rota.

The nursery phone number is `07764 666553`.  The personal details of the people from that rota are [here](Notes://D06DBL065/8025715E005813BA/4B87A6F6EAEAADD385256A2D006A582C/33BE213CF047BC4CC125764A005AAC1A).  Anyone working the WL3BKT queue needs to be contacted.
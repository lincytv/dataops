---
layout: default
description: Steps to regenerate bot OAuth tokens
title: Guide to generate OAuth tokens
service: ciebot
runbook-name: BOT OAuth Guide
tags: oss,ciebot,gobot
link: /ciebot/BOT_OAuth_Guide.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}
{% include {{site.target}}/load_cloud_constants.md %}


## Purpose
A Bot runs many micro-services communicating using *Bot OAuth Access Token* and *Bot User Oath Access Token*.
As required by Service Framework, the two tokens must be kept in vault and be updated yearly.
This guide describe the steps.

## Vault
The tokens of the OSS owned bots are stored at the following vault path
(The "app tokens" shown in column "User OAuth token vault path" are no longer needed after slack-consumer upgrade to event APIs.)


bot        | workspace       | Bot OAuth token vault path                                        | User OAuth token vault path                                         
---------- | --------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- 
gobot | Watson Data Platform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_gobot_in_watsondataplatform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_gobot_in_watsondataplatform 
gobot | IBM Cloud Platform   | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_gobot_in_ibmcloud | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_gobot_in_ibmcloud 
gobot | Data and AI (Anlytics) | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_gobot_in_ibmanalytics | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_gobot_in_ibmanalytics 
gobot | Compose              | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_gobot_in_compose | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_gobot_in_compose 
ciebot | Watson Data Platform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebot_in_watsondataplatform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebot_in_watsondataplatform 
ciebot | Cloud Incident Manager | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebot_in_cim | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebot_in_cim |
ciebot | IBM Cloud Platform   | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebot_in_ibmcloud | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebot_in_ibmcloud 
ciebotwdp | Watson Data Platform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebotwdp_in_watsondataplatform | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebotwdp_in_watsondataplatform 
ciebotdpw | Cloud Incident Manager | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebotwdp_in_cim | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebotwdp_in_cim 
ciebotwdp | IBM Cloud Platform   | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciebotwdp_in_ibmcloud | generic/crn/v1/internal/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciebotwdp_in_ibmcloud 
cietest | IBM Cloud Platform  | generic/crn/v1/staging/local/tip-oss-flow/global/ciebot/slack_bot_token_for_cietest_in_ibmcloud | generic/crn/v1/staging/local/tip-oss-flow/global/ciebot/slack_app_token_for_cietest_in_ibmcloud 
cietest1| IBM Cloud Platform  | generic/crn/v1/staging/local/tip-oss-flow/global/ciebot/slack_bot_token_for_cietest1_in_ibmcloud | generic/crn/v1/staging/local/tip-oss-flow/global/ciebot/slack_app_token_for_cietest1_in_ibmcloud 
ciedev1 | IBM Cloud Platform  | generic/crn/v1/dev/local/tip-oss-flow/global/ciebot/slack_bot_token_for_ciedev1_in_ibmcloud | generic/crn/v1/dev/local/tip-oss-flow/global/ciebot/slack_app_token_for_ciedev1_in_ibmcloud 



## Steps to change tokens
- Go to [slack apps](https://api.slack.com/apps/), click the slack app name (e.g. the bot name). Login with your IBM slack credential if asked.
- On top left dropdown, make sure select the app whose tokens are to be changed
- On the left banner, click on *OAuth & Permissions* under *Features*, and see *OAuth Access Token* and *Bot User OAuth Access Token*.
- Click on the button *Request to Reinstall*, and follow the prompt. **Note: this step may take a few hours or days.**
- Once the reinstall is approved, notify bot users and bot service owners, and schedule a time for the reinstallation.
- Store the new tokens to vault.
- Click on the *Reinstall* button. Follow the prompts to reinstall the app in the **Watson Data Platform** workspace. Use *slack-app-installer* to reinstall in other supported workspaces. **Note: this step may take one or more hours, during which the bot is unavailable to users**.
- Update the environment variables for the tokens in all micro-services related to the bot. Restart theseservices. **Note: this should take less than one hour, and during which the bot is unavailable to users**.
- Annouce bots are available again.

## Contact
For any questions, contact
- {% include contact.html slack=oss-ciebot-slack name=oss-ciebot-name userid=oss-ciebot-userid notesid=oss-ciebot-notesid%} 
- {% include contact.html slack=oss-ciebot-2-slack name=oss-ciebot-2-name userid=oss-ciebot-2-userid notesid=oss-ciebot-2-notesid%} 
 

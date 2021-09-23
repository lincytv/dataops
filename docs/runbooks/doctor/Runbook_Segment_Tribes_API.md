---
layout: default
description: Instructions for the Scorecard API.
title: Segments Tribes API
service: doctor
runbook-name: Segments Tribes API
tags: oss, bluemix, doctor, scorecard
link: /doctor/Runbook_Segment_Tribes_API.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__


#### The new Scorecard API is now named Segments and Tribes API on API platform. Any valid API platform users can get/update segments, tribes, services and service compliance information via API approach.

# API definition
- You can get the API definition from [{{api-catalog-name}}]({{api-catalog-link}}).
- You can also directly open the swagger definition from the [Segments and Tribes API]({{api-catalog-link}}/swagger-ui/dist/index.html?url=/specs/segmentsTribes.yaml&no-proxy).

If you have any questions or issues regarding the design of the API, or have problems accessing the Swagger document, please contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=cloud-platform-dev-3-slack name=cloud-platform-dev-3-name userid=cloud-platform-dev-3-userid notesid=cloud-platform-dev-3-notesid %}.

# How to use the API
- You should follow the [guidance]({{repos-cloud-sre-tools-platform-link}}/wiki/API-Platform-Overview) of the API platform to use the Scorecard API.
- The API is secured by an Authorization token. You can get the token (API Key) on your profile setting after you log in to IBM Cloud Ops Platform (Doctor).

# API runbook
## HTTP Error code
* **400 Bad Request**

  Check with the Swagger document that the URL is correct (eg. _ limit, _ offset value are within range, other parameters are in correct format).

* **401 Unauthorized**

  Check if you provided the correct API key.

* **404 Not Found**

  Make sure the URL is correct, with no typos or mis-spellings.

  If the URL contains segment/tribe/service ids, make sure the id is correct.

* **500 Internal Server Error**

  Go to the Scorecard APIs section below.

## Scorecard APIs

1. Try the API Info URL `{{doctor-rest-apis-link}}/scorecard/api/info`.

   If yes, move to step 2.

   If no, go to the KONG problem section to verify if it is a KONG problem. If not, continue with the next step.

2. Try any failed API (KONG URL)

   If yes, the problem has been resolved.

   If no, move to step 3.

3. Try the Doctor URL directly.
   Use your local environment (within bluezone) to try doctor API directly  
   `{{doctor-portal-link}}/taishan_api/router/scorecard/api/segmenttribe/v1/segments`
    (tribes/services/production_readiness)  

   If yes, it is a KONG problem.

   If no, move to step 4.

4. Check the Scorecard Logs. (You need to have the authority to access Wukong for this section.)  

   * Login to [{{wukong-portal-name}}]({{wukong-portal-link}}).

   * Go to **CI&CD**.

   * In **Continuous Deployment**, type in **doctor_scorecard**.

   * Make sure all instances of __doctor_scorecard__ on the different environments are "Up".  

   * If the status of any instance is down:
     - Click on the 'Restart Service' icon on the 'Action' column to restart the service.   
     - If the status of the service instances are back to "Up", try the API again.   
     - If the service can't be restarted, report any error to {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=scorecard-2-slack name=scorecard-2-name userid=scorecard-2-userid notesid=scorecard-2-notesid %}.

     - Click on one of the environments
     - The scorecard logs are under: /opt/taishan_logs/scorecard/scorecard  
       - Scorecard has a dependency on servicedb, so you may also need to check logs under:
         /opt/taishan_logs/scorecard/servicedb  
       - Report any log error to {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %} or {% include contact.html slack=scorecard-2-slack name=scorecard-2-name userid=scorecard-2-userid notesid=scorecard-2-notesid %}.

### KONG problem:
(You must have access to Wukong for this section.)

1. Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
  - Select **API Management**.
  - Click on **API Catalog** tab.
  - Check that Scorecard is registered.

   Is Scorecard on the list?

   If yes, proceed to Step 2.

   If no, contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}.

   To manually register scorecard, click on "Add a client" and fill in the form with the following information:

   ```
   Client ID: scorecard

   Category: segmenttribe

   Source Info: {{doctor-rest-apis-link}}/scorecard/api/info
   ```

2. Check the Scorecard APIs exist
   - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   - Select **API Management**.
   - Click on **API** tab.
   - Search for Segments/Tribes/Services/ProductionReadiness and make sure these APIs are there.

   - URI should be _/scorecard/api/segmenttribe/v1/segments_ etc.

   - Upstream URL should be _https://api_scorecard_service/router/scorecard/api/segmenttribe/v1/segments_ etc.

   - If any of the four APIs are missing, contact {% include contact.html slack=scorecard-1-slack name=scorecard-1-name userid=scorecard-1-userid notesid=scorecard-1-notesid %}.

   - You can add the API if you've verified the doctor URL works in Scorecard section 3.

3. Check virtual host (HA).

   - Go to [{{wukong-portal-name}}]({{wukong-portal-link}}).
   - Select **CI&CD**.
   - In **Continuous Deployment** type in "doctor_scorecard".
   - It should list out multiple environments. Write down the IPs.
   - Go to **API management**.
   - Click on **API** tab.
   - Click on manage virtual hosts.
     - Check _api_scorecard_service_ is listed.
     - Check that the targets are the same as previous IPs and the port should be 4677.

4. Contact {% include contact.html slack=kong-support-slack name=kong-support-name userid=kong-support-userid notesid=kong-support-notesid %} for KONG support.


## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

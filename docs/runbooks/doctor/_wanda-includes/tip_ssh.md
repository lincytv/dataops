{% include_relative _ibm-includes/load_oss_doctor_constants.md %}
{% include_relative _ibm-includes/load_oss_contacts_constants.md %}

>  **TIP** If SSH does not open in a different tab, try to use a different browser, like Firefox.

>  **TIP** If SSH opens, but your SSO user is not set up for the VM use _Remote Command_ as an alternative.
  * From [{{wukong-portal-name}}]({{wukong-portal-link}}).
  * Select **Remote Command** from the left side menu.
  * Search for the Environment.
  * Using the text box, input a command.
  * Click **Run**.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/remote_command/remote_cmd_1.png)
  * Report the SSO problem to {% include contact.html slack=bluemix-admin-slack name=bluemix-admin-name userid=bluemix-admin-userid notesid=bluemix-admin-notesid%}

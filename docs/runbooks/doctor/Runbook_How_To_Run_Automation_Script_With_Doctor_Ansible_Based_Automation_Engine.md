---
layout: default
description: How to run automation script with Doctor ansible-based automation engine.
title: How to run automation script with Doctor ansible-based automation engine
service: doctor
runbook-name: How to run automation script with Doctor ansible-based automation engine
tags: oss, bluemix, doctor, ansible, script
link: /doctor/Runbook_How_To_Run_Automation_Script_With_Doctor_Ansible_Based_Automation_Engine.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md%}

1. Deliver the scripts you would like to run to the target environment to the Doctor Agent Virtual Machine, under _/opt/ansible/scripts/_ directory.    

   * Push your scripts to the git repository then the CI/CD part of Doctor will automatically sync the scripts to the Doctor Agent Virtual Machine if the scripts can be shared.

   * Or upload the scripts to the Doctor Agent Virtual Machine _/opt/ansible/scripts_ directory by yourself.   

2. Log in to the  [{{doctor-portal-name}}]({{doctor-portal-link}}).

3. Select **Diagnose**.

4. **Script Execution**.

5. Search an environment and Virtual Machines, as target to execute a script.
![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/script_execution/set_env_vm.png){:width="640px"}

6. Click on the check box.

7. Click **Run Script** button, a popup will be shown:

   * **Script:** Click the **Select** button.
   * Input the script name in the **Search script by keyword** field filter.
   * Select a script.
   * **Libraries:** Click **+** icon.
      - Input the relative path of other scripts which the script depends on.
   * **Parameters:** Click **+** icon.
      - Input the parameter name and select the parameter which is referenced by the script.
    > Doctor also provides some common variables listed in the dropdown list.

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/script_execution/run_script.png){:width="640px"}  

8. Click **Submit**.

## Notes and Special Considerations

{% include {{site.target}}/tips_and_techniques.html %}

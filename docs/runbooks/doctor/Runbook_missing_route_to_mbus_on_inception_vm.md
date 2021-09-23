---
layout: default
description: How to handle missing route to mbus on inception VM.
title: Handle missing route to mbus on inception VM
service: doctor
runbook-name: "Handle missing route to mbus on inception VM"
tags: oss, bluemix, doctor
link: /doctor/Runbook_missing_route_to_mbus_on_inception_vm.html
type: Informational
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
__

## Purpose


## Technical Details
In general, there are two inception VMs for a single environment. When doctor operator check inception VMs on `Doctor Keeper` from [{{wukong-portal-name}}]({{wukong-portal-link}}) portal, sometimes one of the inception VM is in `Inactive` status and another one is `Active`. However, you can reach the inactive inception VM from the active VM using ssh with your SSO - `ssh <ssoid>@<ipOfInactiveVM>`. One of the reasons of this issue is caused by some missing route records to mbus when recreating the inception VM.

## User Impact
The doctor agent does not working properly because of the route problem.

## Instructions to Fix

* Login to the inception VM in `Inactive` (e.g. using the bridge of the other InceptionVM) using your SSO id and switch to root user. let's call it InactiveInceptionVM.
* You might need to run

  ```supervisorctl restart doctor_keeper```

  and check if the VM has been recovered on [{{wukong-portal-name}}]({{wukong-portal-link}})->DoctorKeeper. If it does not recover, please continue to next step.

* Restart the doctor_backend:

  ```docker restart doctor_backend```

* Check logs of the docker instance `doctor_backend`:

	```docker logs -f --200 docker_backend```

  If it shows some logs like this, for example:

  ```cannot connect to {{doctor-mbus1-ip-private}}```

  Then follow the next steps, otherwise the situation would not be covered by this runbook.

* Login from another inception VM, check the '{{doctor-compose-path}}' to check which endpoint is used, for example:

  ```
    services:
    ...
        doctor_backend:
            ...
            https://{{doctor-mbus3-ip-public}}:4568
  ```

  - Refer to the Doctor mbus Domain-IP table:

    Domain | IP
    -------|-------
    {{doctor-mbus1-domain}} | {{doctor-mbus1-ip-private}}/{{doctor-mbus1-ip-public}}
    {{doctor-mbus2-domain}} | {{doctor-mbus2-ip-private}}/{{doctor-mbus2-ip-public}}
    {{doctor-mbus3-domain}} | {{doctor-mbus3-ip-private}}/{{doctor-mbus3-ip-public}}
    {{doctor-mbus4-domain}} | {{doctor-mbus4-ip-private}}/{{doctor-mbus4-ip-public}}

<br>
<br>

  > **Note:** Double check the IP addresses from the table above, they may had changed, at the time of the edition those were the current values. If the values are not current, please update them at `_data/ibm/oss-doctor.yml` file.

  - You will know the doctor agent is trying to connect to {{doctor-mbus1-domain}}

* Then back to InactiveInceptionVM and check route info with cmd "route":

	```$  route```

	check whether from the output if doctormbus1/2/3/4.bluemix.net is in the table.

	if not, try to PING the IP address of doctor mbus machine from the table.

  if not package lost, run following command to add the route info

	`route add -net {{doctor-mbus3-ip-private}} netmask 255.255.255.255 gw 192.168.1.1`

* Check **keeper.yml** file

  - Open a Web SSH session of the environment from [{{doctor-portal-name}}]({{doctor-portal-link}})
  - ![]({{site.baseurl}}/docs/runbooks/doctor/images/doctor/cloud/SSH_console.png){:width="640px" height="230px"}
  - User your SSO or funtional ID to connect.
  - `sudo -i`
  - Change to `cd /opt/doctor-keeper/config`.
  - Review `keeper.yml` file using `cat` or any editor of your choice.
  - Make sure the file contains the correct endpoint information base on the doctor_backend service
    * Example if doctor_backend is using mbus3 the keeper file should look like the follow:
      ```

          root@doctor1-wdc:/opt/doctor-keeper/config# cat keeper.yml
          # IBM Confidential OCO Source Materials
          # (C) Copyright and Licensed by IBM Corp. 2017
          #
          # The source code for this program is not published or otherwise
          # divested of its trade secrets  irrespective of what has
          # been deposited with the U.S. Copyright Office.
          env_name: YP_WASHINGTON
          log_level: info
          registry:
            - endpoint: https://169.44.75.235:4568
            - endpoint: https://169.60.135.236:4568
          redis_client:
              host: public
          ssh_hub:
              - ip: 169.44.75.235
              - ip: 169.60.135.236
          sshhub_key:
              enabled: true
          docker-registry: {{doctor-mbus3-domain}}:5000

      ```

    >**Note:** If you make any changes to the **keeper.yml** file you must restart doctor keeper via `supervisorctl restart doctor_keeper`.

* Check the `doctor_backend` logs and see if the connection is recovered.
  - The VM Status should become active(color in GREEN) in [{{wukong-portal-name}}]({{wukong-portal-link}}) as well.
  - Otherwise try to restart doctor keeper via `supervisorctl restart doctor_keeper`.


## Notes and Special Considerations
{% include {{site.target}}/tips_and_techniques.html %}

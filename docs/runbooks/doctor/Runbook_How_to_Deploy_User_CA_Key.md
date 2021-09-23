---
layout: default
description: How to deploy a user CA Key
title: How to Deploy User CA Key
service: doctor
runbook-name: How to Deploy User CA Key
tags: oss, bluemix, doctor
link: /doctor/Runbook_How_to_Deploy_User_CA_Key.html
type: Informational
---

{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/load_oss_slack_constants.md %}


## If all or most of the BBO tasks of an environment are failed, there maybe something wrong with the SSH CA.

### First, we should confirm it is the SSH CA's problem.

{% include_relative _{{site.target}}-includes/doctor_kepper_ssh.md %}

```
ls /opt/ansible

ls /opt/bbo/data
```

There should be a taishan_key in `/opt/ansible`. If not, contact the Doctor team at [{{oss-doctor-name}}]({{oss-doctor-link}})

Check whether the _doctor_key & doctor_key-cert.pub_ and _taishan_key & taishan_key-cert.pub_ exist. If the doctor_key  doesn't exist, copy one from `/opt/ansible`.

### If _doctor_key-cert.pub_ or _taishan_key-cert.pub_ do not exist.

* Call the following API to generate them.

  ```
  curl https://cloud-oss-metadata.bluemix.net/cert-function-key/doctor/${env} -d '{"publicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoXqxRhUC1g9h0bP0jMb0jUx1zC4heQNXCTHzBV0BfqaHewmkpdSvo/m0CWbKK7mfzffvYjUiyCVSF/Ni0XZR6u4NMwWgMaMFbp9JHs7n+6+E9yGiB/hQkymUjJvujjLt55QdQJsRdZmOgbswTvCh9iD7hPyyt7+HlOhd93w/iJ+BphAiHnlxNcNYLOS7I6Dk8t0hBW4fyB89jg/tGCJu1Dk6WvcCw15t2Uv9h18E065yaQ0yCTdwNoRBeTO7/lAJIdn7dIJmzeNSmlHGdj5UMg93L/0vss7G6PhR6ed6QTuD9FREPRjrf8v8oU2Wgz3F4JBw+ohgWu2u4/6WtZyix"}'
  ```

  ```
  curl https://cloud-oss-metadata.bluemix.net/cert-function-key/taishan/${env} -d '{"publicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCoXqxRhUC1g9h0bP0jMb0jUx1zC4heQNXCTHzBV0BfqaHewmkpdSvo/m0CWbKK7mfzffvYjUiyCVSF/Ni0XZR6u4NMwWgMaMFbp9JHs7n+6+E9yGiB/hQkymUjJvujjLt55QdQJsRdZmOgbswTvCh9iD7hPyyt7+HlOhd93w/iJ+BphAiHnlxNcNYLOS7I6Dk8t0hBW4fyB89jg/tGCJu1Dk6WvcCw15t2Uv9h18E065yaQ0yCTdwNoRBeTO7/lAJIdn7dIJmzeNSmlHGdj5UMg93L/0vss7G6PhR6ed6QTuD9FREPRjrf8v8oU2Wgz3F4JBw+ohgWu2u4/6WtZyix"}'
  ```

  ```
  curl https://cloud-oss-metadata.bluemix.net/cert-function-key/doctor/${env} > /opt/ansible/doctor_key-cert.pub
  ```

   ```curl https://cloud-oss-metadata.bluemix.net/cert-function-key/taishan/${env} > /opt/ansible/taishan_key-cert.pub
   ```

* `copy /opt/ansible/doctor_key* /opt/bbo/data/`
* `copy /opt/ansible/taishan_key* /opt/bbo/data/`


* Print all the VM info by executing this command:

  `docker exec -it doctor_security cat /etc/ansible/hosts`

* There will be a list of VM info printed in the console.

* Try to login to some VMs:

  ```
  ssh -i /opt/bbo/data/taishan_key -i /opt/bbo/data/taishan_key-cert.pub taishan@ip
  ```

* If you can login successfully, it is not the SSH CA key's issue.
  - You can ping the [{{oss-doctor-name}}]({{oss-doctor-link}}) Slack channel.

* If you cannot login, it is the SSH CA key's problem. Execute the following command:

  ```
  curl localhost:4693/security/firecall/cert/check -d '{"email": "<your email address>", "regenerateca": "true"}'
  ```

## Notes and Special Considerations

For any other issues about SSH CA, contact {% include contact.html slack=oss-developer-slack name=oss-developer-name userid=oss-developer-userid notesid=oss-developer-notesid %}.

{% include {{site.target}}/tips_and_techniques.html %}

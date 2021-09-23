> **Note:** Not all Doctor backend agents use port **4569**.
To check the port, two option:
  * **Option** 1 from [{{site.data[site.target].oss-doctor.links.wukong-portal.name}}]({{site.data[site.target].oss-doctor.links.wukong-portal.link}}).
  * Select **Register**.
  * Search for an environment.
  * Get the port from the cloud field, e.g. _{"cloud":["10.183.191.168:4569"]}_.
![cloud port]({{site.baseurl}}/docs/runbooks/doctor/images/wukong/register/cloud_port.png){:width=700}
  * **Option 2** from  [{{site.data[site.target].oss-doctor.links.doctor-config-repo.name}}]({{site.data[site.target].oss-doctor.links.doctor-config-repo.link}}/tree/master/config) repo.
  * Search for an environment `taishan_[local/public/dedicated]_[env].yml` e.g. _taishan_dedicated_aa2.yml_
  * Get the port from the port field, e.g. _port: 4569_.
  ![]({{site.baseurl}}/docs/runbooks/doctor/images/ghe/doctor-configuration/doctor_conf_taishan_env_get_port.png){:width=640}

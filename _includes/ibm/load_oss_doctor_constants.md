{% capture pim-console-name %}{{site.data[site.target].oss-doctor.links.pim-console.name}}{% endcapture %}
{% capture pim-console-link %}{{site.data[site.target].oss-doctor.links.pim-console.link}}{% endcapture %}

{% capture access-hub-name %}{{site.data[site.target].oss-doctor.links.access-hub.name}}{% endcapture %}
{% capture access-hub-link %}{{site.data[site.target].oss-doctor.links.access-hub.link}}{% endcapture %}

{% capture logmet-name %}{{site.data[site.target].oss-doctor.links.logmet.name}}{% endcapture %}
{% capture logmet-link %}{{site.data[site.target].oss-doctor.links.logmet.link}}{% endcapture %}

{% capture oss-dev-console-name %}{{site.data[site.target].oss-doctor.links.oss-dev-console.name}}{% endcapture %}
{% capture oss-dev-console-link %}{{site.data[site.target].oss-doctor.links.oss-dev-console.link}}{% endcapture %}

{% capture tip-api-platform-policy-name %}{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}{% endcapture %}
{% capture tip-api-platform-policy-link %}{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}{% endcapture %}

{% capture ibm-wiki-name %}{{site.data[site.target].oss-doctor.links.ibm-wiki.name}}{% endcapture %}
{% capture ibm-wiki-link %}{{site.data[site.target].oss-doctor.links.ibm-wiki.link}}{% endcapture %}

{% capture doctor-rest-apis-link %}{{site.data[site.target].oss-doctor.links.doctor-rest-apis.link}}{% endcapture %}
{% capture doctor-rest-apis-name %}{{site.data[site.target].oss-doctor.links.doctor-rest-apis.name}}{% endcapture %}

{% capture api-catalog-link %}{{site.data[site.target].oss-doctor.links.api-catalog.link}}{% endcapture %}
{% capture api-catalog-name %}{{site.data[site.target].oss-doctor.links.api-catalog.name}}{% endcapture %}

{% capture ibm-blue-zone-name %}{{site.data[site.target].oss-doctor.links.ibm-blue-zone.name}}{% endcapture %}
{% capture ibm-blue-zone-link %}{{site.data[site.target].oss-doctor.links.ibm-blue-zone.link}}{% endcapture %}

{% capture doctor-hub-name %} {{site.data[site.target].oss-doctor.links.doctor-hub.name}} {% endcapture %}
{% capture doctor-hub-ip %} {{site.data[site.target].oss-doctor.links.doctor-hub.ip}} {% endcapture %}

{% capture grafana-dashboard-name %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.name}}{% endcapture %}
{% capture grafana-dashboard-link %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.link}}{% endcapture %}
{% capture dashboard-bluemix-alerts-name %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.bluemix-alerts-name}}{% endcapture %}
{% capture dashboard-bluemix-alerts-link %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.bluemix-alerts-link}}{% endcapture %}

{% capture netcat-ip-local %} {{site.data[site.target].oss-doctor.links.netcat.ip-local}} {% endcapture %}
{% capture netcat-ip-dedicated %} {{site.data[site.target].oss-doctor.links.netcat.ip-dedicated}} {% endcapture %}
{% capture netcat-ip-public %} {{site.data[site.target].oss-doctor.links.netcat.ip-public}} {% endcapture %}

{% capture netcat-port-local %} {{site.data[site.target].oss-doctor.links.netcat.port-local}} {% endcapture %}
{% capture netcat-port-dedicated %} {{site.data[site.target].oss-doctor.links.netcat.port-dedicated}} {% endcapture %}
{% capture netcat-port-public %}{{site.data[site.target].oss-doctor.links.netcat.port-public}} {% endcapture %}

{% capture doctor-ucd-name-A0215 %} {{site.data[site.target].oss-doctor.links.doctor-ucd.name-A0215}} {% endcapture %}
{% capture doctor-ucd-link %} {{site.data[site.target].oss-doctor.links.doctor-ucd.link}} {% endcapture %}

{% capture doctor-alert-system-name %}{{site.data[site.target].oss-doctor.links.doctor-alert-system.name}}{% endcapture %}
{% capture doctor-alert-system-link %}{{site.data[site.target].oss-doctor.links.doctor-alert-system.link}}{% endcapture %}

{% capture ucd-portal-name %}{{site.data[site.target].oss-doctor.links.ucd-portal.name}}{% endcapture %}
{% capture ucd-portal-link %}{{site.data[site.target].oss-doctor.links.ucd-portal.link}}{% endcapture %}
{% capture ucd-portal-short %}{{site.data[site.target].oss-doctor.links.ucd-portal.short}}{% endcapture %}

{% capture new-relic-portal-name %}{{site.data[site.target].oss-doctor.links.new-relic-portal.name}}{% endcapture %}
{% capture new-relic-portal-link-alert %}{{site.data[site.target].oss-doctor.links.new-relic-portal.link-alert}}{% endcapture %}
{% capture new-relic-portal-link-infra %}{{site.data[site.target].oss-doctor.links.new-relic-portal.link-infra}}{% endcapture %}
{% capture new-relic-portal-link-insights %}{{site.data[site.target].oss-doctor.links.new-relic-portal.link-insights}}{% endcapture %}
{% capture new-relic-portal-link-polices %}{{site.data[site.target].oss-doctor.links.new-relic-portal.link-polices}}{% endcapture %}

{% capture bluegroups-portal-name %}{{site.data[site.target].oss-doctor.links.blue-groups.name}}{% endcapture %}
{% capture bluegroups-portal-link %}{{site.data[site.target].oss-doctor.links.blue-groups.link}}{% endcapture %}

{% capture doctor-service1-name %}{{site.data[site.target].oss-doctor.links.doctor-service1.name}}{% endcapture %}
{% capture doctor-service1-ip %}{{site.data[site.target].oss-doctor.links.doctor-service1.ip}}{% endcapture %}

{% capture doctor-service2-name %}{{site.data[site.target].oss-doctor.links.doctor-service2.name}}{% endcapture %}
{% capture doctor-service2-ip %}{{site.data[site.target].oss-doctor.links.doctor-service2.ip}}{% endcapture %}

{% capture doctor-service2-rtp-name %}{{site.data[site.target].oss-doctor.links.doctor-service2-rtp.name}}{% endcapture %}
{% capture doctor-service2-rtp-ip %}{{site.data[site.target].oss-doctor.links.doctor-service2-rtp.ip}}{% endcapture %}

{% capture onestatus-name %}{{site.data[site.target].oss-doctor.links.onestatus.name}}{% endcapture %}
{% capture onestatus-link %}{{site.data[site.target].oss-doctor.links.onestatus.link}}{% endcapture %}

{% capture ibm_cloud-name%} {{site.data[site.target].oss-doctor.links.ibm_cloud.name}} {% endcapture %}
{% capture ibm_cloud-link %} {{site.data[site.target].oss-doctor.links.ibm_cloud.link}} {% endcapture %}

{% capture doctor-ssh-domain %} {{site.data[site.target].oss-doctor.links.doctor-ssh.domain}} {% endcapture %}
{% capture doctor-ssh-ip-private %} {{site.data[site.target].oss-doctor.links.doctor-ssh.ip-private}} {% endcapture %}
{% capture doctor-ssh-ip-public %} {{site.data[site.target].oss-doctor.links.doctor-ssh.ip-public}} {% endcapture %}

{% capture doctor-ssh2-domain %} {{site.data[site.target].oss-doctor.links.doctor-ssh2.domain}} {% endcapture %}
{% capture doctor-ssh2-ip-private %} {{site.data[site.target].oss-doctor.links.doctor-ssh2.ip-private}} {% endcapture %}
{% capture doctor-ssh2-ip-public %} {{site.data[site.target].oss-doctor.links.doctor-ssh2.ip-public}} {% endcapture %}

{% capture doctor-blink-ha-proxy-config-name %} {{site.data[site.target].oss-doctor.links.doctor-blink-ha-proxy-config.name}} {% endcapture %}
{% capture doctor-blink-ha-proxy-config-link %} {{site.data[site.target].oss-doctor.links.doctor-blink-ha-proxy-config.link}} {% endcapture %}

{% capture doctor-blink-ports-config-name %} {{site.data[site.target].oss-doctor.links.doctor-blink-ports-config.name}} {% endcapture %}
{% capture doctor-blink-ports-config-link %} {{site.data[site.target].oss-doctor.links.doctor-blink-ports-config.link}} {% endcapture %}

{% capture marmot-portal-name %} {{site.data[site.target].oss-doctor.links.marmot-portal.name}} {% endcapture %}
{% capture marmot-portal-link %} {{site.data[site.target].oss-doctor.links.marmot-portal.link}} {% endcapture %}

{% capture kibana-portal-name %} {{site.data[site.target].oss-doctor.links.kibana-portal.name}} {% endcapture %}
{% capture kibana-portal-link %} {{site.data[site.target].oss-doctor.links.kibana-portal.link}} {% endcapture %}

{% capture doctor-dev-env-proxy-ip %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.proxy-ip}} {% endcapture %}
{% capture doctor-dev-env-02-port %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.02-port}} {% endcapture %}
{% capture doctor-dev-env-03-port %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.03-port}} {% endcapture %}
{% capture doctor-dev-env-04-port %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.04-port}} {% endcapture %}
{% capture doctor-dev-env-05-port %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.05-port}} {% endcapture %}
{% capture doctor-dev-env-06-port %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.06-port}} {% endcapture %}
{% capture doctor-dev-env-portal-link %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.portal-link}} {% endcapture %}
{% capture doctor-dev-env-portal-name %} {{site.data[site.target].oss-doctor.links.doctor-dev-env.portal-name}} {% endcapture %}

{% capture watson-env-onboarding-name %} {{site.data[site.target].oss-doctor.links.watson-env-onboarding.name}} {% endcapture %}
{% capture watson-env-onboarding-link %} {{site.data[site.target].oss-doctor.links.watson-env-onboarding.link}} {% endcapture %}

{% capture monit-name %} {{site.data[site.target].oss-doctor.links.monit.name}} {% endcapture %}
{% capture monit-link %} {{site.data[site.target].oss-doctor.links.monit.link}} {% endcapture %}

{% capture compass-portal-name %}{{site.data[site.target].oss-doctor.links.compass-portal.name}}{% endcapture %}
{% capture compass-portal-link %}{{site.data[site.target].oss-doctor.links.compass-portal.link}}{% endcapture %}

{% capture doctor-portal-name %}
{{site.data[site.target].oss-doctor.links.doctor-portal.name}}
{% endcapture %}
{% capture doctor-portal-link %}{{site.data[site.target].oss-doctor.links.doctor-portal.link}}{% endcapture %}

{% capture wukong-portal-name %}{{site.data[site.target].oss-doctor.links.wukong-portal.name}}{% endcapture %}
{% capture wukong-portal-link %}{{site.data[site.target].oss-doctor.links.wukong-portal.link}}{% endcapture %}

{% capture doctor-config-repo-name %}{{site.data[site.target].oss-doctor.links.doctor-config-repo.name}}{% endcapture %}
{% capture doctor-config-repo-link %}{{site.data[site.target].oss-doctor.links.doctor-config-repo.link}}{% endcapture %}

{% capture doctor-ops-infra-tools-repo-name %}{{site.data[site.target].oss-doctor.links.doctor-ops-infra-tools-repo.name}}{% endcapture %}
{% capture doctor-ops-infra-tools-repo-link %}{{site.data[site.target].oss-doctor.links.octor-ops-infra-tools-repo.link}}{% endcapture %}

{% capture doctor-alert-system-name %}
{{site.data[site.target].oss-doctor.links.doctor-alert-system.name}}
{% endcapture %}
{% capture doctor-alert-system-links %}
{{site.data[site.target].oss-doctor.links.doctor-alert-system.link}}
{% endcapture %}

{% capture doctor-config-repo-name %}{{site.data[site.target].oss-doctor.links.doctor-config-repo.name}}{% endcapture %}
{% capture doctor-config-repo-link %}{{site.data[site.target].oss-doctor.links.doctor-config-repo.link}}{% endcapture %}

{% capture doctor-blink-proxy-name %}
{{site.data[site.target].oss-doctor.links.doctor-blink-proxy.name}}
{% endcapture %}
{% capture doctor-blink-proxy-link %}
{{site.data[site.target].oss-doctor.links.doctor-blink-proxy.link}}
{% endcapture %}
{% capture doctor-blink-proxy-port %}
{{site.data[site.target].oss-doctor.links.doctor-blink-proxy.port}}
{% endcapture %}

{% capture doctor-dset-pac-name %}{{site.data[site.target].oss-doctor.links.doctor-dset-pac.name}}
{% endcapture %}
{% capture doctor-dset-pac-link %}{{site.data[site.target].oss-doctor.links.doctor-dset-pac.link}}
{% endcapture %}

{% capture grafana-dashboard-name %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.name}}{% endcapture %}
{% capture grafana-dashboard-link %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.link}}{% endcapture %}

{% capture dashboard-bluemix-alerts-name %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.bluemix-alerts-name}}{% endcapture %}
{% capture dashboard-bluemix-alerts-link %}{{site.data[site.target].oss-doctor.links.grafana-dashboard.bluemix-alerts-link}}{% endcapture %}

{% capture new-relic-portal-name %}
{{site.data[site.target].oss-doctor.links.new-relic-portal.name}}
{% endcapture %}
{% capture dnew-relic-portal-link %}{{site.data[site.target].oss-doctor.links.new-relic-portal.link}}{% endcapture %}

{% capture usam-name %}
{{site.data[site.target].oss-doctor.links.usam.name}}
{% endcapture %}
{% capture usam-link %}
{{site.data[site.target].oss-doctor.links.usam.link}}
{% endcapture %}
{% capture usam-short %}
{{site.data[site.target].oss-doctor.links.usam.short}}
{% endcapture %}
{% capture usam-system-cli %}
{{site.data[site.target].oss-doctor.links.usam.system-cli}}
{% endcapture %}
{% capture usam-id-example %}
{{site.data[site.target].oss-doctor.links.usam.id-example}}
{% endcapture %}
{% capture usam-cli-privilege-l1 %}
{{site.data[site.target].oss-doctor.links.usam.cli-privilege-l1}}
{% endcapture %}
{% capture usam-cli-privilege-l2 %}
{{site.data[site.target].oss-doctor.links.usam.cli-privilege-l2}}
{% endcapture %}
{% capture usam-group-cli %}
{{site.data[site.target].oss-doctor.links.usam.group-cli}}
{% endcapture %}
{% capture usam-oss-system %}
{{site.data[site.target].oss-doctor.links.usam.oss-system}}
{% endcapture %}
{% capture usam-oss-privilege %}
{{site.data[site.target].oss-doctor.links.usam.oss-privilege}}
{% endcapture %}
{% capture usam-bluemix-envs-table %}
{{site.data[site.target].oss-doctor.links.usam.bluemix-envs-table}}
{% endcapture %}
{% capture usam-doctor-stage-dev-ops %}
{{site.data[site.target].oss-doctor.links.usam.doctor-stage-dev-ops}}
{% endcapture %}
{% capture usam-doctor-prod-dev-ops %}
{{site.data[site.target].oss-doctor.links.usam.doctor-prod-dev-ops}}
{% endcapture %}
{% capture usam-doctor-prod-dev-ops-l %}
{{site.data[site.target].oss-doctor.links.usam.doctor-prod-dev-ops-l}}
{% endcapture %}
{% capture usam-chg-pwd %}
{{site.data[site.target].oss-doctor.links.usam.chg-pwd}}
{% endcapture %}



{% capture bluegroups-portal-name %}
{{site.data[site.target].oss-doctor.links.blue-groups.name}}
{% endcapture %}
{% capture bluegroups-portal-link %}{{site.data[site.target].oss-doctor.links.blue-groups.link}}{% endcapture %}

{% capture ucd-portal-name %}
{{site.data[site.target].oss-doctor.links.ucd-portal.name}}
{% endcapture %}
{% capture ucd-portal-link %}{{site.data[site.target].oss-doctor.links.ucd-portal.link}}{% endcapture %}
{% capture ucd-portal-short %}{{site.data[site.target].oss-doctor.links.ucd-portal.short}}{% endcapture %}

{% capture doctor-critical-alerts-name %}
{{site.data[site.target].oss-doctor.links.doctor-critical-alerts.name}}
{% endcapture %}
{% capture doctor-critical-alerts-link %}{{site.data[site.target].oss-doctor.links.doctor-critical-alerts.link}}{% endcapture %}

{% capture doctor-critical-alerts-l2-name %}
{{site.data[site.target].oss-doctor.links.doctor-critical-alerts-l2.name}}
{% endcapture %}
{% capture doctor-critical-alerts-l2-link %}{{site.data[site.target].oss-doctor.links.doctor-critical-alerts-l2.link}}{% endcapture %}

{% capture doctor-status-name %}{{site.data[site.target].oss-doctor.links.doctor-status.name}}{% endcapture %}
{% capture doctor-status-link %}{{site.data[site.target].oss-doctor.links.doctor-status.link}}{% endcapture %}

{% capture prometheus-name %}{{site.data[site.target].oss-doctor.links.prometheus.name}}{% endcapture %}
{% capture prometheus-link %}{{site.data[site.target].oss-doctor.links.prometheus.link}}{% endcapture %}
{% capture prometheus-io-link %}{{site.data[site.target].oss-doctor.links.prometheus.io-link}}{% endcapture %}

{% capture tip-api-platform-policy-name %}
{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.name}}
{% endcapture %}
{% capture tip-api-platform-policy-link %}{{site.data[site.target].oss-doctor.links.tip-api-platform-policy.link}}{% endcapture %}

{% capture l-bnpp-green-window %}
https://tenx1.rtp.raleigh.ibm.com/rtcproxy/sync/regioncal?token=7afe6bde76731dfe8644901727098771bd130ad7f1ebf40914b2ca9f32dd9f2928085365db7027119e3b31a56cf7c6ffe72ff76b5ae928e0b5f7f3b96b6ebc1b3930dc7e5ce77e30dec12f1ded2ae84d0c0d6f8a536539e77c565b75fa93d1a1
{% endcapture %}

{% capture l-bnpp02-green-window %}
https://tenx1.rtp.raleigh.ibm.com/rtcproxy/sync/regioncal?token=7afe6bde76731dfe8644901727098771bd130ad7f1ebf40914b2ca9f32dd9f2928085365db7027119e3b31a56cf7c6ffe72ff76b5ae928e0b5f7f3b96b6ebc1b3930dc7e5ce77e30dec12f1ded2ae84d0c0d6f8a536539e77c565b75fa93d1a1
{% endcapture %}

{% capture ibm-blue-zone-name %}{{site.data[site.target].oss-doctor.links.ibm-blue-zone.name}}{% endcapture %}
{% capture ibm-blue-zone-link %}{{site.data[site.target].oss-doctor.links.ibm-blue-zone.link}}{% endcapture %}

{% capture bosh-cli-name %}
{{site.data[site.target].oss-doctor.links.bosh-cli.name}}
{% endcapture %}
{% capture bosh-cli-link %}{{site.data[site.target].oss-doctor.links.bosh-cli.link}}{% endcapture %}

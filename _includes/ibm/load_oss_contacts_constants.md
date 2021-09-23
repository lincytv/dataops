{% capture admin-console-slack %}{{ site.data[site.target].oss-contacts.contacts.admin-console.slack }}{% endcapture %}
{% capture admin-console-name %}{{ site.data[site.target].oss-contacts.contacts.admin-console.name }}{% endcapture %}
{% capture admin-console-userid %}{{ site.data[site.target].oss-contacts.contacts.admin-console.userid }}{% endcapture %}
{% capture admin-console-notesid %}{{ site.data[site.target].oss-contacts.contacts.admin-console.notesid }}{% endcapture %}

{% capture admin-console-2-slack %}{{ site.data[site.target].oss-contacts.contacts.admin-console-2.slack }}{% endcapture %}
{% capture admin-console-2-name %}{{ site.data[site.target].oss-contacts.contacts.admin-console-2.name }}{% endcapture %}
{% capture admin-console-2-userid %}{{ site.data[site.target].oss-contacts.contacts.admin-console-2.userid }}{% endcapture %}
{% capture admin-console-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.admin-console-2.notesid }}{% endcapture %}

{% capture jumpbox-sso-id-slack %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-sso-id.slack }}{% endcapture %}
{% capture jumpbox-sso-id-name %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-sso-id.name }}{% endcapture %}
{% capture jumpbox-sso-id-userid %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-sso-id.userid }}{% endcapture %}
{% capture jumpbox-sso-id-notesid %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-sso-id.notesid }}{% endcapture %}

{% capture jumpbox-root-slack %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-root.slack }}{% endcapture %}
{% capture jumpbox-root-name %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-root.name }}{% endcapture %}
{% capture jumpbox-root-userid %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-root.userid }}{% endcapture %}
{% capture jumpbox-root-notesid %}{{ site.data[site.target].oss-contacts.contacts.jumpbox-root.notesid }}{% endcapture %}

{% capture checkin-failure-slack%}{{ site.data[site.target].oss-contacts.contacts.checkin-failure.slack}}{% endcapture %}
{% capture checkin-failure-name %}{{ site.data[site.target].oss-contacts.contacts.checkin-failure.name}}{% endcapture %}
{% capture checkin-failure-userid %}{{ site.data[site.target].oss-contacts.contacts.checkin-failure.userid}}{% endcapture %}
{% capture checkin-failure-notesid %}{{ site.data[site.target].oss-contacts.contacts.checkin-failure.notesid }}{% endcapture %}

{% capture doctor-backend-slack%}{{ site.data[site.target].oss-contacts.contacts.doctor-backend.slack}}{% endcapture %}
{% capture doctor-backend-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend.name}}{% endcapture %}
{% capture doctor-backend-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend.userid}}{% endcapture %}
{% capture doctor-backend-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend.notesid }}{% endcapture %}

{% capture doctor-backend-2-slack%}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-2.slack}}{% endcapture %}
{% capture doctor-backend-2-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-2.name}}{% endcapture %}
{% capture doctor-backend-2-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-2.userid}}{% endcapture %}
{% capture doctor-backend-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-2.notesid }}{% endcapture %}

{% capture doctor-backend-3-slack%}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-3.slack}}{% endcapture %}
{% capture doctor-backend-3-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-3.name}}{% endcapture %}
{% capture doctor-backend-3-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-3.userid}}{% endcapture %}
{% capture doctor-backend-3-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-3.notesid }}{% endcapture %}

{% capture doctor-backend-4-slack %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-4.slack }}{% endcapture %}
{% capture doctor-backend-4-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-4.name }}{% endcapture %}
{% capture doctor-backend-4-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-4.userid }}{% endcapture %}
{% capture doctor-backend-4-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-4.notesid }}{% endcapture %}

{% capture doctor-backend-6-slack %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-6.slack }}{% endcapture %}
{% capture doctor-backend-6-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-6.name }}{% endcapture %}
{% capture doctor-backend-6-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-6.userid }}{% endcapture %}
{% capture doctor-backend-6-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-6.notesid }}{% endcapture %}

{% capture doctor-backend-7-slack %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-7.slack }}{% endcapture %}
{% capture doctor-backend-7-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-7.name }}{% endcapture %}
{% capture doctor-backend-7-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-7.userid }}{% endcapture %}
{% capture doctor-backend-7-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-backend-7.notesid }}{% endcapture %}

{% capture bosh-director-slack %}{{ site.data[site.target].oss-contacts.contacts.bosh-director.slack }}{% endcapture %}
{% capture bosh-director-name %}{{ site.data[site.target].oss-contacts.contacts.bosh-director.name }}{% endcapture %}
{% capture bosh-director-userid %}{{ site.data[site.target].oss-contacts.contacts.bosh-director.userid }}{% endcapture %}
{% capture bosh-director-notesid %}{{ site.data[site.target].oss-contacts.contacts.bosh-director.notesid }}{% endcapture %}

{% capture cloud-resource-api-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api.slack}}{% endcapture %}
{% capture cloud-resource-api-name %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api.name}}{% endcapture %}
{% capture cloud-resource-api-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api.userid}}{% endcapture %}
{% capture cloud-resource-api-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api.notesid}}{% endcapture %}

{% capture cloud-resource-api-2-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api-2.slack}}{% endcapture %}
{% capture cloud-resource-api-2-name %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api-2.name}}{% endcapture %}
{% capture cloud-resource-api-2-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api-2.userid}}{% endcapture %}
{% capture cloud-resource-api-2-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-api-2.notesid}}{% endcapture %}

{% capture cloud-resource-bbo-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-bbo.slack}}{% endcapture %}
{% capture cloud-resource-bbo-name %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-bbo.name}}{% endcapture %}
{% capture cloud-resource-bbo-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-bbo.userid}}{% endcapture %}
{% capture cloud-resource-bbo-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-resource-bbo.notesid}}{% endcapture %}

{% capture cloud-platform-dev-1-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.slack}}{% endcapture %}
{% capture cloud-platform-dev-1-name %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.name}}{% endcapture %}
{% capture cloud-platform-dev-1-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.userid}}{% endcapture %}
{% capture cloud-platform-dev-1-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-1.notesid}}{% endcapture %}

{% capture cloud-platform-dev-2-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.slack}}{% endcapture %}
{% capture cloud-platform-dev-2-name %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.name}}{% endcapture %}
{% capture cloud-platform-dev-2-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.userid}}{% endcapture %}
{% capture cloud-platform-dev-2-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-2.notesid}}{% endcapture %}

{% capture cloud-platform-dev-3-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-3.slack}}{% endcapture %}
{% capture cloud-platform-dev-3-name %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-3.name}}{% endcapture %}
{% capture cloud-platform-dev-3-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-3.userid}}{% endcapture %}
{% capture cloud-platform-dev-3-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-dev-3.notesid}}{% endcapture %}

{% capture cloud-platform-sre-slack %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-sre.slack}}{% endcapture %}
{% capture cloud-platform-sre-name %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-sre.name}}{% endcapture %}
{% capture cloud-platform-sre-userid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-sre.userid}}{% endcapture %}
{% capture cloud-platform-sre-notesid %}{{site.data[site.target].oss-contacts.contacts.cloud-platform-sre.notesid}}{% endcapture %}

{% capture datapower-config-slack%}{{ site.data[site.target].oss-contacts.contacts.datapower-config.slack}}{% endcapture %}
{% capture datapower-config-name %}{{ site.data[site.target].oss-contacts.contacts.datapower-config.name}}{% endcapture %}
{% capture datapower-config-userid %}{{ site.data[site.target].oss-contacts.contacts.datapower-config.userid}}{% endcapture %}
{% capture datapower-config-notesid %}{{ site.data[site.target].oss-contacts.contacts.datapower-config.notesid }}{% endcapture %}

{% capture ansible-self-healing-slack%}{{ site.data[site.target].oss-contacts.contacts.ansible-self-healing.slack}}{% endcapture %}
{% capture ansible-self-healing-name %}{{ site.data[site.target].oss-contacts.contacts.ansible-self-healing.name}}{% endcapture %}
{% capture ansible-self-healing-userid %}{{ site.data[site.target].oss-contacts.contacts.ansible-self-healing.userid}}{% endcapture %}
{% capture ansible-self-healing-notesid %}{{ site.data[site.target].oss-contacts.contacts.ansible-self-healing.notesid }}{% endcapture %}

{% capture monitoring-apis-slack %}{{ site.data[site.target].oss-contacts.contacts.monitoring-apis.slack }}{% endcapture %}
{% capture monitoring-apis-name %}{{ site.data[site.target].oss-contacts.contacts.monitoring-apis.name }}{% endcapture %}
{% capture monitoring-apis-userid %}{{ site.data[site.target].oss-contacts.contacts.monitoring-apis.userid }}{% endcapture %}
{% capture monitoring-apis-notesid %}{{ site.data[site.target].oss-contacts.contacts.monitoring-apis.notesid }}{% endcapture %}

{% capture cloud-newrelic-monitoring-slack %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.slack }}{% endcapture %}
{% capture cloud-newrelic-monitoring-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.name }}{% endcapture %}
{% capture cloud-newrelic-monitoring-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.userid }}{% endcapture %}
{% capture cloud-newrelic-monitoring-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-newrelic-monitoring.notesid }}{% endcapture %}

{% capture tip-api-platform-manager-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-managerg.slack }}{% endcapture %}
{% capture tip-api-platform-manager-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-manager.name }}{% endcapture %}
{% capture tip-api-platform-manager-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-manager.userid }}{% endcapture %}
{% capture tip-api-platform-manager-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-manager.notesid }}{% endcapture %}

{% capture tip-api-platform-1-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.slack }}{% endcapture %}
{% capture tip-api-platform-1-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.name }}{% endcapture %}
{% capture tip-api-platform-1-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.userid }}{% endcapture %}
{% capture tip-api-platform-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-1.notesid }}{% endcapture %}

{% capture tip-api-platform-2-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.slack }}{% endcapture %}
{% capture tip-api-platform-2-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.name }}{% endcapture %}
{% capture tip-api-platform-2-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.userid }}{% endcapture %}
{% capture tip-api-platform-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-2.notesid }}{% endcapture %}

{% capture tip-api-platform-3-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-3.slack }}{% endcapture %}
{% capture tip-api-platform-3-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-3.name }}{% endcapture %}
{% capture tip-api-platform-3-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-3.userid }}{% endcapture %}
{% capture tip-api-platform-3-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-3.notesid }}{% endcapture %}

{% capture tip-api-platform-4-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-4.slack }}{% endcapture %}
{% capture tip-api-platform-4-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-4.name }}{% endcapture %}
{% capture tip-api-platform-4-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-4.userid }}{% endcapture %}
{% capture tip-api-platform-4-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-4.notesid }}{% endcapture %}

{% capture tip-api-platform-5-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-5.slack }}{% endcapture %}
{% capture tip-api-platform-5-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-5.name }}{% endcapture %}
{% capture tip-api-platform-5-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-5.userid }}{% endcapture %}
{% capture tip-api-platform-5-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-5.notesid }}{% endcapture %}

{% capture tip-api-platform-6-slack %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-6.slack }}{% endcapture %}
{% capture tip-api-platform-6-name %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-6.name }}{% endcapture %}
{% capture tip-api-platform-6-userid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-6.userid }}{% endcapture %}
{% capture tip-api-platform-6-notesid %}{{ site.data[site.target].oss-contacts.contacts.tip-api-platform-6.notesid }}{% endcapture %}

{% capture sosat-lead-eng-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-lead-eng.slack }}{% endcapture %}
{% capture sosat-lead-eng-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-lead-eng.name }}{% endcapture %}
{% capture sosat-lead-eng-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-lead-eng.userid }}{% endcapture %}
{% capture sosat-lead-eng-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-lead-eng.notesid }}{% endcapture %}

{% capture sosat-netcool-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.slack }}{% endcapture %}
{% capture sosat-netcool-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.name }}{% endcapture %}
{% capture sosat-netcool-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.userid }}{% endcapture %}
{% capture sosat-netcool-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool.notesid }}{% endcapture %}

{% capture sosat-netcool-alt-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool-alt.slack }}{% endcapture %}
{% capture sosat-netcool-alt-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool-alt.name }}{% endcapture %}
{% capture sosat-netcool-alt-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool-alt.userid }}{% endcapture %}
{% capture sosat-netcool-alt-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-netcool-alt.notesid }}{% endcapture %}

{% capture sosat-deploy-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-deploy.slack }}{% endcapture %}
{% capture sosat-deploy-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-deploy.name }}{% endcapture %}
{% capture sosat-deploy-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-deploy.userid }}{% endcapture %}
{% capture sosat-deploy-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-deploy.notesid }}{% endcapture %}

{% capture sosat-compliance-dev-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-compliance-dev.slack }}{% endcapture %}
{% capture sosat-compliance-dev-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-compliance-dev.name }}{% endcapture %}
{% capture sosat-compliance-dev-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-compliance-dev.userid }}{% endcapture %}
{% capture sosat-compliance-dev-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-compliance-dev.notesid }}{% endcapture %}

{% capture scorecard-1-slack %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.slack }}{% endcapture %}
{% capture scorecard-1-name %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.name }}{% endcapture %}
{% capture scorecard-1-userid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.userid }}{% endcapture %}
{% capture scorecard-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-1.notesid }}{% endcapture %}

{% capture scorecard-2-slack %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.slack }}{% endcapture %}
{% capture scorecard-2-name %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.name }}{% endcapture %}
{% capture scorecard-2-userid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.userid }}{% endcapture %}
{% capture scorecard-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.scorecard-2.notesid }}{% endcapture %}

{% capture sosat-eventing-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-eventing.slack }}{% endcapture %}
{% capture sosat-eventing-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-eventing.name }}{% endcapture %}
{% capture sosat-eventing-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-eventing.userid }}{% endcapture %}
{% capture sosat-eventing-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-eventing.notesid }}{% endcapture %}

{% capture sosat-tools-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.slack }}{% endcapture %}
{% capture sosat-tools-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.name }}{% endcapture %}
{% capture sosat-tools-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.userid }}{% endcapture %}
{% capture sosat-tools-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-tools.notesid }}{% endcapture %}

{% capture sosat-productization-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-productization.slack }}{% endcapture %}
{% capture sosat-productization-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-productization.name }}{% endcapture %}
{% capture sosat-productization-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-productization.userid }}{% endcapture %}
{% capture sosat-productization-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-productization.notesid }}{% endcapture %}

{% capture sosat-availability-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.slack }}{% endcapture %}
{% capture sosat-availability-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.name }}{% endcapture %}
{% capture sosat-availability-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.userid }}{% endcapture %}
{% capture sosat-availability-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-availability.notesid }}{% endcapture %}

{% capture sosat-devops-1-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-1.slack }}{% endcapture %}
{% capture sosat-devops-1-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-1.name }}{% endcapture %}
{% capture sosat-devops-1-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-1.userid }}{% endcapture %}
{% capture sosat-devops-1-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-1.notesid }}{% endcapture %}

{% capture sosat-devops-2-slack %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-2.slack }}{% endcapture %}
{% capture sosat-devops-2-name %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-2.name }}{% endcapture %}
{% capture sosat-devops-2-userid %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-2.userid }}{% endcapture %}
{% capture sosat-devops-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.sosat-devops-2.notesid }}{% endcapture %}

{% capture sre-platform-chief-architect-slack %}{{ site.data[site.target].oss-contacts.contacts.sre-platform-chief-architect.slack }}{% endcapture %}
{% capture sre-platform-chief-architect-name %}{{ site.data[site.target].oss-contacts.contacts.sre-platform-chief-architect.name }}{% endcapture %}
{% capture sre-platform-chief-architect-userid %}{{ site.data[site.target].oss-contacts.contacts.sre-platform-chief-architect.userid }}{% endcapture %}
{% capture sre-platform-chief-architect-notesid %}{{ site.data[site.target].oss-contacts.contacts.sre-platform-chief-architect.notesid }}{% endcapture %}

{% capture toc-tooling-manager-slack %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling-manager.slack }}{% endcapture %}
{% capture toc-tooling-manager-name %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling-manager.name }}{% endcapture %}
{% capture toc-tooling-manager-userid %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling-manager.userid }}{% endcapture %}
{% capture toc-tooling-manager-notesid %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling-manager.notesid }}{% endcapture %}

{% capture toc-tooling-slack %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling.slack }}{% endcapture %}
{% capture toc-tooling-name %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling.name }}{% endcapture %}
{% capture toc-tooling-userid %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling.userid }}{% endcapture %}
{% capture toc-tooling-notesid %}{{ site.data[site.target].oss-contacts.contacts.toc-tooling.notesid }}{% endcapture %}

{% capture jsonnote-slack %}{{ site.data[site.target].oss-contacts.contacts.jsonnote.slack }}{% endcapture %}
{% capture jsonnote-name %}{{ site.data[site.target].oss-contacts.contacts.jsonnote.name }}{% endcapture %}
{% capture jsonnote-userid %}{{ site.data[site.target].oss-contacts.contacts.jsonnote.userid }}{% endcapture %}
{% capture jsonnote-notesid %}{{ site.data[site.target].oss-contacts.contacts.jsonnote.notesid }}{% endcapture %}

{% capture oss-developer-slack %}{{site.data[site.target].oss-contacts.contacts.oss-developer.slack}}{% endcapture %}
{% capture oss-developer-name %}{{site.data[site.target].oss-contacts.contacts.oss-developer.name}}{% endcapture %}
{% capture oss-developer-userid %}{{site.data[site.target].oss-contacts.contacts.oss-developer.userid}}{% endcapture %}
{% capture oss-developer-notesid %}{{site.data[site.target].oss-contacts.contacts.oss-developer.notesid}}{% endcapture %}

{% capture kong-support-slack %}{{ site.data[site.target].oss-contacts.contacts.kong-support.slack }}{% endcapture %}
{% capture kong-support-name %}{{ site.data[site.target].oss-contacts.contacts.kong-support.name }}{% endcapture %}
{% capture kong-support-userid %}{{ site.data[site.target].oss-contacts.contacts.kong-support.userid }}{% endcapture %}
{% capture kong-support-notesid %}{{ site.data[site.target].oss-contacts.contacts.kong-support.notesid }}{% endcapture %}

{% capture bluemix-automation-slack %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation.slack }}{% endcapture %}
{% capture bluemix-automation-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation.name }}{% endcapture %}
{% capture bluemix-automation-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation.userid }}{% endcapture %}
{% capture bluemix-automation-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation.notesid }}{% endcapture %}

{% capture bluemix-automation-2-slack %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation-2.slack }}{% endcapture %}
{% capture bluemix-automation-2-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation-2.name }}{% endcapture %}
{% capture bluemix-automation-2-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation-2.userid }}{% endcapture %}
{% capture bluemix-automation-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-automation-2.notesid }}{% endcapture %}

{% capture bluemix-dev-slack%}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev.slack}}{% endcapture %}
{% capture bluemix-dev-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev.name}}{% endcapture %}
{% capture bluemix-dev-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev.userid}}{% endcapture %}
{% capture bluemix-dev-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev.notesid }}{% endcapture %}

{% capture bluemix-dev-lodgment-slack%}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-lodgment.slack}}{% endcapture %}
{% capture bluemix-dev-lodgment-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-lodgment.name}}{% endcapture %}
{% capture bluemix-dev-lodgment-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-lodgment.userid}}{% endcapture %}
{% capture bluemix-dev-lodgment-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-lodgment.notesid }}{% endcapture %}

{% capture usam-bluemix-envs-slack%}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs.slack}}{% endcapture %}
{% capture usam-bluemix-envs-name %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs.name}}{% endcapture %}
{% capture usam-bluemix-envs-userid %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs.userid}}{% endcapture %}
{% capture usam-bluemix-envs-notesid %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs.notesid }}{% endcapture %}

{% capture usam-bluemix-envs-alt-slack%}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs-alt.slack}}{% endcapture %}
{% capture usam-bluemix-envs-alt-name %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs-alt.name}}{% endcapture %}
{% capture usam-bluemix-envs-alt-userid %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs-alt.userid}}{% endcapture %}
{% capture usam-bluemix-envs-alt-notesid %}{{ site.data[site.target].oss-contacts.contacts.usam-bluemix-envs-alt.notesid }}{% endcapture %}

{% capture bluemix-admin-slack%}{{ site.data[site.target].oss-contacts.contacts.bluemix-admin.slack}}{% endcapture %}
{% capture bluemix-admin-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-admin.name}}{% endcapture %}
{% capture bluemix-admin-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-admin.userid}}{% endcapture %}
{% capture bluemix-admin-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-admin.notesid }}{% endcapture %}

{% capture cloud-software-dev-slack%}{{ site.data[site.target].oss-contacts.contacts.cloud-software-dev.slack}}{% endcapture %}
{% capture cloud-software-dev-name %}{{ site.data[site.target].oss-contacts.contacts.cloud-software-dev.name}}{% endcapture %}
{% capture cloud-software-dev-userid %}{{ site.data[site.target].oss-contacts.contacts.cloud-software-dev.userid}}{% endcapture %}
{% capture cloud-software-dev-notesid %}{{ site.data[site.target].oss-contacts.contacts.cloud-software-dev.notesid }}{% endcapture %}

{% capture auto-scaling-slack%}{{ site.data[site.target].oss-contacts.contacts.auto-scaling-dev.slack}}{% endcapture %}
{% capture auto-scaling-name %}{{ site.data[site.target].oss-contacts.contacts.auto-scaling-dev.name}}{% endcapture %}
{% capture auto-scaling-userid %}{{ site.data[site.target].oss-contacts.contacts.auto-scaling-dev.userid}}{% endcapture %}
{% capture auto-scaling-notesid %}{{ site.data[site.target].oss-contacts.contacts.auto-scaling-dev.notesid }}{% endcapture %}

{% capture bluemix-dev-manager-slack%}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-manager.slack}}{% endcapture %}
{% capture bluemix-dev-manager-name %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-manager.name}}{% endcapture %}
{% capture bluemix-dev-manager-userid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-manager.userid}}{% endcapture %}
{% capture bluemix-dev-manager-notesid %}{{ site.data[site.target].oss-contacts.contacts.bluemix-dev-manager.notesid }}{% endcapture %}

{% capture gre-ucd-a7500-tester-slack %}{{ site.data[site.target].gre-contacts.contacts.gre-ucd-a7500-tester.slack }}{% endcapture %}
{% capture gre-ucd-a7500-tester-name %}{{ site.data[site.target].gre-contacts.contacts.gre-ucd-a7500-tester.name }}{% endcapture %}
{% capture gre-ucd-a7500-tester-userid %}{{ site.data[site.target].gre-contacts.contacts.gre-ucd-a7500-tester.userid }}{% endcapture %}
{% capture gre-ucd-a7500-tester-notesid %}{{ site.data[site.target].gre-contacts.contacts.gre-ucd-a7500-tester.notesid }}{% endcapture %}

{% capture doctor-blink-slack %}{{ site.data[site.target].oss-contacts.contacts.doctor-blink.slack }}{% endcapture %}
{% capture doctor-blink-name %}{{ site.data[site.target].oss-contacts.contacts.doctor-blink.name }}{% endcapture %}
{% capture doctor-blink-userid %}{{ site.data[site.target].oss-contacts.contacts.doctor-blink.userid }}{% endcapture %}
{% capture doctor-blink-notesid %}{{ site.data[site.target].oss-contacts.contacts.doctor-blink.notesid }}{% endcapture %}

{% capture watson-foundation-slack %}{{ site.data[site.target].oss-contacts.contacts.watson-foundation.slack }}{% endcapture %}
{% capture watson-foundation-name %}{{ site.data[site.target].oss-contacts.contacts.watson-foundation.name }}{% endcapture %}
{% capture watson-foundation-userid %}{{ site.data[site.target].oss-contacts.contacts.watson-foundation.userid }}{% endcapture %}
{% capture watson-foundation-notesid %}{{ site.data[site.target].oss-contacts.contacts.watson-foundation.notesid }}{% endcapture %}

{% capture edb-admin-slack %}{{ site.data[site.target].oss-contacts.contacts.edb-admin.slack }}{% endcapture %}
{% capture edb-admin-name %}{{ site.data[site.target].oss-contacts.contacts.edb-admin.name }}{% endcapture %}
{% capture edb-admin-userid %}{{ site.data[site.target].oss-contacts.contacts.edb-admin.userid }}{% endcapture %}
{% capture edb-admin-notesid %}{{ site.data[site.target].oss-contacts.contacts.edb-admin.notesid }}{% endcapture %}

{% capture oss-ciebot-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot.slack }}{% endcapture %}
{% capture oss-ciebot-name %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot.name }}{% endcapture %}
{% capture oss-ciebot-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot.userid }}{% endcapture %}
{% capture oss-ciebot-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot.notesid }}{% endcapture %}

{% capture oss-ciebot-2-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot-2.slack }}{% endcapture %}
{% capture oss-ciebot-2-name %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot-2.name }}{% endcapture %}
{% capture oss-ciebot-2-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot-2.userid }}{% endcapture %}
{% capture oss-ciebot-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-ciebot-2.notesid }}{% endcapture %}

{% capture oss-program-director-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-program-director.slack }}{% endcapture %}
{% capture oss-program-director-name %}{{ site.data[site.target].oss-contacts.contacts.oss-program-director.name }}{% endcapture %}
{% capture oss-program-director-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-program-director.userid }}{% endcapture %}
{% capture oss-program-director-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-program-director.notesid }}{% endcapture %}

{% capture oss-auth-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-auth.slack }}{% endcapture %}
{% capture oss-auth-name %}{{ site.data[site.target].oss-contacts.contacts.oss-auth.name }}{% endcapture %}
{% capture oss-auth-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-auth.userid }}{% endcapture %}
{% capture oss-auth-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-auth.notesid }}{% endcapture %}

{% capture oss-auth_2-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-auth_2.slack }}{% endcapture %}
{% capture oss-auth_2-name %}{{ site.data[site.target].oss-contacts.contacts.oss-auth_2.name }}{% endcapture %}
{% capture oss-auth_2-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-auth_2.userid }}{% endcapture %}
{% capture oss-auth_2-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-auth_2.notesid }}{% endcapture %}

{% capture oss-platform-architecture-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-platform-architecture.slack }}{% endcapture %}
{% capture oss-platform-architecture-name %}{{ site.data[site.target].oss-contacts.contacts.oss-platform-architecture.name }}{% endcapture %}
{% capture oss-platform-architecture-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-platform-architecture.userid }}{% endcapture %}
{% capture oss-platform-architecture-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-platform-architecture.notesid }}{% endcapture %}

{% capture oss-security-focal-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal.slack }}{% endcapture %}
{% capture oss-security-focal-name %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal.name }}{% endcapture %}
{% capture oss-security-focal-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal.userid }}{% endcapture %}
{% capture oss-security-focal-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal.notesid }}{% endcapture %}

{% capture oss-security-focal-2-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal-2.slack }}{% endcapture %}
{% capture oss-security-focal-2-name %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal-2.name }}{% endcapture %}
{% capture oss-security-focal-2-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal-2.userid }}{% endcapture %}
{% capture oss-security-focal-2-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-security-focal-2.notesid }}{% endcapture %}

{% capture oss-bastion-admin-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-bastion-admin.slack }}{% endcapture %}
{% capture oss-bastion-admin-name %}{{ site.data[site.target].oss-contacts.contacts.oss-bastion-admin.name }}{% endcapture %}
{% capture oss-bastion-admin-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-bastion-admin.userid }}{% endcapture %}
{% capture oss-bastion-admin-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-bastion-admin.notesid }}{% endcapture %}

{% capture oss-team-alex-torres-rojas-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-alex-torres-rojas.slack }}{% endcapture %}
{% capture oss-team-alex-torres-rojas-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-alex-torres-rojas.name }}{% endcapture %}
{% capture oss-team-alex-torres-rojas-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-alex-torres-rojas.userid }}{% endcapture %}
{% capture oss-team-alex-torres-rojas-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-alex-torres-rojas.notesid }}{% endcapture %}

{% capture oss-team-ali-hussain-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ali-hussain.slack }}{% endcapture %}
{% capture oss-team-ali-hussain-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ali-hussain.name }}{% endcapture %}
{% capture oss-team-ali-hussain-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ali-hussain.userid }}{% endcapture %}
{% capture oss-team-ali-hussain-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ali-hussain.notesid }}{% endcapture %}

{% capture oss-team-amit-anand-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-amit-anand.slack }}{% endcapture %}
{% capture oss-team-amit-anand-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-amit-anand.name }}{% endcapture %}
{% capture oss-team-amit-anand-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-amit-anand.userid }}{% endcapture %}
{% capture oss-team-amit-anand-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-amit-anand.notesid }}{% endcapture %}

{% capture oss-team-bob-mckenna-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-bob-mckenna.slack }}{% endcapture %}
{% capture oss-team-bob-mckenna-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-bob-mckenna.name }}{% endcapture %}
{% capture oss-team-bob-mckenna-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-bob-mckenna.userid }}{% endcapture %}
{% capture oss-team-bob-mckenna-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-bob-mckenna.notesid }}{% endcapture %}

{% capture oss-team-chris-gambrell-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-chris-gambrell.slack }}{% endcapture %}
{% capture oss-team-chris-gambrell-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-chris-gambrell.name }}{% endcapture %}
{% capture oss-team-chris-gambrell-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-chris-gambrell.userid }}{% endcapture %}
{% capture oss-team-chris-gambrell-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-chris-gambrell.notesid }}{% endcapture %}

{% capture oss-team-crystal-su-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-crystal-su.slack }}{% endcapture %}
{% capture oss-team-crystal-su-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-crystal-su.name }}{% endcapture %}
{% capture oss-team-crystal-su-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-crystal-su.userid }}{% endcapture %}
{% capture oss-team-crystal-su-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-crystal-su.notesid }}{% endcapture %}

{% capture oss-team-dong-li-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-dong-li.slack }}{% endcapture %}
{% capture oss-team-dong-li-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-dong-li.name }}{% endcapture %}
{% capture oss-team-dong-li-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-dong-li.userid }}{% endcapture %}
{% capture oss-team-dong-li-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-dong-li.notesid }}{% endcapture %}

{% capture oss-team-emma-zhang-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-emma-zhang.slack }}{% endcapture %}
{% capture oss-team-emma-zhang-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-emma-zhang.name }}{% endcapture %}
{% capture oss-team-emma-zhang-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-emma-zhang.userid }}{% endcapture %}
{% capture oss-team-emma-zhang-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-emma-zhang.notesid }}{% endcapture %}

{% capture oss-team-gabriel-avila-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-gabriel-avila.slack }}{% endcapture %}
{% capture oss-team-gabriel-avila-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-gabriel-avila.name }}{% endcapture %}
{% capture oss-team-gabriel-avila-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-gabriel-avila.userid }}{% endcapture %}
{% capture oss-team-gabriel-avila-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-gabriel-avila.notesid }}{% endcapture %}

{% capture oss-team-hui-wang-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-hui-wang.slack }}{% endcapture %}
{% capture oss-team-hui-wang-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-hui-wang.name }}{% endcapture %}
{% capture oss-team-hui-wang-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-hui-wang.userid }}{% endcapture %}
{% capture oss-team-hui-wang-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-hui-wang.notesid }}{% endcapture %}

{% capture oss-team-irma-sheriff-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-irma-sheriff.slack }}{% endcapture %}
{% capture oss-team-irma-sheriff-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-irma-sheriff.name }}{% endcapture %}
{% capture oss-team-irma-sheriff-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-irma-sheriff.userid }}{% endcapture %}
{% capture oss-team-irma-sheriff-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-irma-sheriff.notesid }}{% endcapture %}

{% capture oss-team-izhak-jakov-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-izhak-jakov.slack }}{% endcapture %}
{% capture oss-team-izhak-jakov-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-izhak-jakov.name }}{% endcapture %}
{% capture oss-team-izhak-jakov-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-izhak-jakov.userid }}{% endcapture %}
{% capture oss-team-izhak-jakov-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-izhak-jakov.notesid }}{% endcapture %}

{% capture oss-team-jason-geer-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-geer.slack }}{% endcapture %}
{% capture oss-team-jason-geer-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-geer.name }}{% endcapture %}
{% capture oss-team-jason-geer-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-geer.userid }}{% endcapture %}
{% capture oss-team-jason-geer-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-geer.notesid }}{% endcapture %}

{% capture oss-team-jason-koo-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-koo.slack }}{% endcapture %}
{% capture oss-team-jason-koo-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-koo.name }}{% endcapture %}
{% capture oss-team-jason-koo-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-koo.userid }}{% endcapture %}
{% capture oss-team-jason-koo-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-koo.notesid }}{% endcapture %}

{% capture oss-team-jason-wang-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-wang.slack }}{% endcapture %}
{% capture oss-team-jason-wang-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-wang.name }}{% endcapture %}
{% capture oss-team-jason-wang-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-wang.userid }}{% endcapture %}
{% capture oss-team-jason-wang-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jason-wang.notesid }}{% endcapture %}

{% capture oss-team-jing-you-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jing-you.slack }}{% endcapture %}
{% capture oss-team-jing-you-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jing-you.name }}{% endcapture %}
{% capture oss-team-jing-you-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jing-you.userid }}{% endcapture %}
{% capture oss-team-jing-you-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jing-you.notesid }}{% endcapture %}

{% capture oss-team-jonas-stein-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jonas-stein.slack }}{% endcapture %}
{% capture oss-team-jonas-stein-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jonas-stein.name }}{% endcapture %}
{% capture oss-team-jonas-stein-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jonas-stein.userid }}{% endcapture %}
{% capture oss-team-jonas-stein-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jonas-stein.notesid }}{% endcapture %}

{% capture oss-team-jun-jie-yu-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jun-jie-yu.slack }}{% endcapture %}
{% capture oss-team-jun-jie-yu-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jun-jie-yu.name }}{% endcapture %}
{% capture oss-team-jun-jie-yu-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jun-jie-yu.userid }}{% endcapture %}
{% capture oss-team-jun-jie-yu-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-jun-jie-yu.notesid }}{% endcapture %}

{% capture oss-team-ken-parzygnat-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ken-parzygnat.slack }}{% endcapture %}
{% capture oss-team-ken-parzygnat-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ken-parzygnat.name }}{% endcapture %}
{% capture oss-team-ken-parzygnat-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ken-parzygnat.userid }}{% endcapture %}
{% capture oss-team-ken-parzygnat-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-ken-parzygnat.notesid }}{% endcapture %}

{% capture oss-team-khushboo-singh-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-khushboo-singh.slack }}{% endcapture %}
{% capture oss-team-khushboo-singh-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-khushboo-singh.name }}{% endcapture %}
{% capture oss-team-khushboo-singh-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-khushboo-singh.userid }}{% endcapture %}
{% capture oss-team-khushboo-singh-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-khushboo-singh.notesid }}{% endcapture %}

{% capture oss-team-kumari-muktta-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kumari-muktta.slack }}{% endcapture %}
{% capture oss-team-kumari-muktta-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kumari-muktta.name }}{% endcapture %}
{% capture oss-team-kumari-muktta-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kumari-muktta.userid }}{% endcapture %}
{% capture oss-team-kumari-muktta-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kumari-muktta.notesid }}{% endcapture %}

{% capture oss-team-kun-yang-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kun-yang.slack }}{% endcapture %}
{% capture oss-team-kun-yang-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kun-yang.name }}{% endcapture %}
{% capture oss-team-kun-yang-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kun-yang.userid }}{% endcapture %}
{% capture oss-team-kun-yang-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-kun-yang.notesid }}{% endcapture %}

{% capture oss-team-michelle-zeitlin-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-michelle-zeitlin.slack }}{% endcapture %}
{% capture oss-team-michelle-zeitlin-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-michelle-zeitlin.name }}{% endcapture %}
{% capture oss-team-michelle-zeitlin-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-michelle-zeitlin.userid }}{% endcapture %}
{% capture oss-team-michelle-zeitlin-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-michelle-zeitlin.notesid }}{% endcapture %}

{% capture oss-team-niharika-sahoo-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-niharika-sahoo.slack }}{% endcapture %}
{% capture oss-team-niharika-sahoo-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-niharika-sahoo.name }}{% endcapture %}
{% capture oss-team-niharika-sahoo-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-niharika-sahoo.userid }}{% endcapture %}
{% capture oss-team-niharika-sahoo-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-niharika-sahoo.notesid }}{% endcapture %}

{% capture oss-team-qi-guo-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-qi-guo.slack }}{% endcapture %}
{% capture oss-team-qi-guo-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-qi-guo.name }}{% endcapture %}
{% capture oss-team-qi-guo-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-qi-guo.userid }}{% endcapture %}
{% capture oss-team-qi-guo-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-qi-guo.notesid }}{% endcapture %}

{% capture oss-team-quin-du-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-quin-du.slack }}{% endcapture %}
{% capture oss-team-quin-du-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-quin-du.name }}{% endcapture %}
{% capture oss-team-quin-du-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-quin-du.userid }}{% endcapture %}
{% capture oss-team-quin-du-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-quin-du.notesid }}{% endcapture %}

{% capture oss-team-rohit-basu-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rohit-basu.slack }}{% endcapture %}
{% capture oss-team-rohit-basu-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rohit-basu.name }}{% endcapture %}
{% capture oss-team-rohit-basu-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rohit-basu.userid }}{% endcapture %}
{% capture oss-team-rohit-basu-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rohit-basu.notesid }}{% endcapture %}

{% capture oss-team-rui-sun-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rui-sun.slack }}{% endcapture %}
{% capture oss-team-rui-sun-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rui-sun.name }}{% endcapture %}
{% capture oss-team-rui-sun-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rui-sun.userid }}{% endcapture %}
{% capture oss-team-rui-sun-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-rui-sun.notesid }}{% endcapture %}

{% capture oss-team-sean-power-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sean-power.slack }}{% endcapture %}
{% capture oss-team-sean-power-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sean-power.name }}{% endcapture %}
{% capture oss-team-sean-power-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sean-power.userid }}{% endcapture %}
{% capture oss-team-sean-power-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sean-power.notesid }}{% endcapture %}

{% capture oss-team-shane-cartledge-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shane-cartledge.slack }}{% endcapture %}
{% capture oss-team-shane-cartledge-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shane-cartledge.name }}{% endcapture %}
{% capture oss-team-shane-cartledge-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shane-cartledge.userid }}{% endcapture %}
{% capture oss-team-shane-cartledge-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shane-cartledge.notesid }}{% endcapture %}

{% capture oss-team-shawn-bramblett-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shawn-bramblett.slack }}{% endcapture %}
{% capture oss-team-shawn-bramblett-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shawn-bramblett.name }}{% endcapture %}
{% capture oss-team-shawn-bramblett-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shawn-bramblett.userid }}{% endcapture %}
{% capture oss-team-shawn-bramblett-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-shawn-bramblett.notesid }}{% endcapture %}

{% capture oss-team-sushma-hiremath-slack %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sushma-hiremath.slack }}{% endcapture %}
{% capture oss-team-sushma-hiremath-name %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sushma-hiremath.name }}{% endcapture %}
{% capture oss-team-sushma-hiremath-userid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sushma-hiremath.userid }}{% endcapture %}
{% capture oss-team-sushma-hiremath-notesid %}{{ site.data[site.target].oss-contacts.contacts.oss-team-sushma-hiremath.notesid }}{% endcapture %}

{% capture slack-home-name %}{{site.data[site.target].oss-slack.channels.home.name}}{% endcapture %}
{% capture slack-home-link %}{{site.data[site.target].oss-slack.channels.home.link}}{% endcapture %}

{% capture sre-platform-onshift-name %}{{site.data[site.target].oss-slack.channels.sre-platform-onshift.name}}{% endcapture %}
{% capture sre-platform-onshift-link %}{{site.data[site.target].oss-slack.channels.sre-platform-onshift.link}}{% endcapture %}

{% capture oss-doctor-name %}{{site.data[site.target].oss-slack.channels.oss-doctor.name}}{% endcapture %}
{% capture oss-doctor-link %}{{site.data[site.target].oss-slack.channels.oss-doctor.link}}{% endcapture %}

{% capture slack-vault-name %}{{site.data[site.target].oss-slack.channels.vault.name}}
{% endcapture %}{% capture slack-vault-link %}{{site.data[site.target].oss-slack.channels.vault.link}}{% endcapture %}

{% capture doctor-on-call-shift-name %}{{site.data[site.target].oss-slack.channels.doctor-on-call-shift.name}}{% endcapture %}
{% capture doctor-on-call-shift-link %}{{site.data[site.target].oss-slack.channels.doctor-on-call-shift.link}}{% endcapture %}

{% capture eu-emerg-approvers-name %}{{site.data[site.target].oss-slack.channels.eu-emerg-approvers.name}}{% endcapture %}
{% capture eu-emerg-approvers-link %}{{site.data[site.target].oss-slack.channels.eu-emerg-approvers.link}}{% endcapture %}

{% capture sosat-monitor-prod-name %}{{site.data[site.target].oss-slack.channels.sosat-monitor-prod.name}}{% endcapture %}
{% capture sosat-monitor-prod-link %}{{site.data[site.target].oss-slack.channels.sosat-monitor-prod.link}}{% endcapture %}

{% capture oss-kube-work-name %}{{site.data[site.target].oss-slack.channels.oss-kube-work.name}}{% endcapture %}
{% capture oss-kube-work-link %}{{site.data[site.target].oss-slack.channels.oss-kube-work.link}}{% endcapture %}

{% capture oss-slack-api-platform-prd-name %}{{site.data[site.target].oss-slack.channels.api-platform-prd.name}}{% endcapture %}
{% capture oss-slack-api-platform-prd-link %}{{site.data[site.target].oss-slack.channels.api-platform-prd.link}}{% endcapture %}

{% capture oss-slack-api-platform-stg-name %}{{site.data[site.target].oss-slack.channels.api-platform-stg.name}}{% endcapture %}
{% capture oss-slack-api-platform-stg-link %}{{site.data[site.target].oss-slack.channels.api-platform-stg.link}}{% endcapture %}

{% capture oss-slack-api-platform-dev-name %}{{site.data[site.target].oss-slack.channels.api-platform-dev.name}}{% endcapture %}
{% capture oss-slack-api-platform-dev-link %}{{site.data[site.target].oss-slack.channels.api-platform-dev.link}}{% endcapture %}

{% capture oss-slack-oss-charts-cd-name %}{{site.data[site.target].oss-slack.channels.oss-charts-cd.name}}{% endcapture %}
{% capture oss-slack-oss-charts-cd-link %}{{site.data[site.target].oss-slack.channels.oss-charts-cd.link}}{% endcapture %}

{% capture oss-slack-oss-ciebot-ci-name %}{{site.data[site.target].oss-slack.channels.oss-ciebot-ci.name}}{% endcapture %}
{% capture oss-slack-oss-ciebot-ci-link %}{{site.data[site.target].oss-slack.channels.oss-ciebot-ci.link}}{% endcapture %}

{% capture oss-slack-oss-api-ci-name %}{{site.data[site.target].oss-slack.channels.oss-api-ci.name}}{% endcapture %}
{% capture oss-slack-oss-api-ci-link %}{{site.data[site.target].oss-slack.channels.oss-api-ci.link}}{% endcapture %}

{% capture oss-slack-oss-tip-ci-name %}{{site.data[site.target].oss-slack.channels.oss-tip-ci.name}}{% endcapture %}
{% capture oss-slack-oss-tip-ci-link %}{{site.data[site.target].oss-slack.channels.oss-tip-ci.link}}{% endcapture %}

{% capture oss-slack-oss-cicd-name %}{{site.data[site.target].oss-slack.channels.oss-cicd.name}}{% endcapture %}
{% capture oss-slack-oss-cicd-link %}{{site.data[site.target].oss-slack.channels.oss-cicd.link}}{% endcapture %}

{% capture oss-slack-cto-sre-product-ci-name %}{{site.data[site.target].oss-slack.channels.cto-sre-product-ci.name}}{% endcapture %}
{% capture oss-slack-cto-sre-product-ci-link %}{{site.data[site.target].oss-slack.channels.cto-sre-product-ci.link}}{% endcapture %}

{% capture oss-slack-cto-oss-tip-internal-name %}{{site.data[site.target].oss-slack.channels.cto-oss-tip-internal.name}}{% endcapture %}
{% capture oss-slack-cto-oss-tip-internal-link %}{{site.data[site.target].oss-slack.channels.cto-oss-tip-internal.link}}{% endcapture %}

{% capture oss-slack-taas-jenkins-help-name %}{{site.data[site.target].oss-slack.channels.taas-jenkins-help.name}}{% endcapture %}
{% capture oss-slack-taas-jenkins-help-link %}{{site.data[site.target].oss-slack.channels.taas-jenkins-help.link}}{% endcapture %}

{% capture oss-slack-oss-onboarding-name %}{{site.data[site.target].oss-slack.channels.oss-onboarding.name}}{% endcapture %}
{% capture oss-slack-oss-onboarding-link %}{{site.data[site.target].oss-slack.channels.oss-onboarding.link}}{% endcapture %}

{% capture oss-slack-oss-postgres-sysdig-name %}{{site.data[site.target].oss-slack.channels.oss-postgres-sysdig.name}}{% endcapture %}
{% capture oss-slack-oss-postgres-sysdig-link %}{{site.data[site.target].oss-slack.channels.oss-postgres-sysdig.link}}{% endcapture %}

{% capture oss-slack-palente-operations-name %}{{site.data[site.target].oss-slack.channels.palente-operations.name}}{% endcapture %}
{% capture oss-slack-palente-operations-link %}{{site.data[site.target].oss-slack.channels.palente-operations.link}}{% endcapture %}

{% capture oss-slack-palente-support-name %}{{site.data[site.target].oss-slack.channels.palente-support.name}}{% endcapture %}
{% capture oss-slack-palente-support-link %}{{site.data[site.target].oss-slack.channels.palente-support.link}}{% endcapture %}

{% capture slack-toc-avm-name %}{{site.data[site.target].oss-slack.channels.toc-avm.name}}{% endcapture %}
{% capture slack-toc-avm-link %}{{site.data[site.target].oss-slack.channels.toc-avm.link}}{% endcapture %}

{% capture slack-palante-pcie-automation-name %}{{site.data[site.target].oss-slack.channels.palante-pcie-automation.name}}{% endcapture %}
{% capture slack-palante-pcie-automation-link %}{{site.data[site.target].oss-slack.channels.palante-pcie-automation.link}}{% endcapture %}

{% capture slack-oss-bastion-users-name %}{{site.data[site.target].oss-slack.channels.oss-bastion-users.name}}{% endcapture %}
{% capture slack-oss-bastion-users-link %}{{site.data[site.target].oss-slack.channels.oss-bastion-users.link}}{% endcapture %}

{% capture slack-oss-icd-sysdig-alerts-name %}{{site.data[site.target].oss-slack.channels.oss-icd-sysdig-alerts.name}}{% endcapture %}
{% capture slack-oss-icd-sysdig-alerts-link %}{{site.data[site.target].oss-slack.channels.oss-icd-sysdig-alerts.link}}{% endcapture %}

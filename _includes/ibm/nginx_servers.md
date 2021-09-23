{% include {{site.target}}/load_api_constants.md %}
{% include {{site.target}}/load_ghe_constants.md %}

{% capture doctorbus-nginx-conf-name %}{{doctorbus-short_name}}_{{doctorbus-private-ip}}_nginx.conf{% endcapture %}
{% capture doctorbus-nginx-conf-url %}{{api-platform-general-nginx-link}}{{doctorbus-nginx-conf-name}}{% endcapture %}

{% capture doctorapigw-nginx-conf-name %}{{doctorapigw-short_name}}_{{doctorapigw-private-ip}}_nginx.conf{% endcapture %}
{% capture doctorapigw-nginx-conf-url %}{{api-platform-general-nginx-link}}{{doctorapigw-nginx-conf-name}}{% endcapture %}

{% capture doctorapigw2-nginx-conf-name %}{{doctorapigw2-short_name}}_{{doctorapigw2-private-ip}}_nginx.conf{% endcapture %}
{% capture doctorapigw2-nginx-conf-url %}{{api-platform-general-nginx-link}}{{doctorapigw2-nginx-conf-name}}{% endcapture %}


{% capture doctorapitest-nginx-conf-name %}{{doctorapitest-short_name}}_{{doctorapitest-private-ip}}_nginx.conf{% endcapture %}
{% capture doctorapitest-nginx-conf-url %}{{api-platform-general-nginx-link}}{{doctorapitest-nginx-conf-name}}{% endcapture %}

{% capture OSSLBStage3-nginx-conf-name %}{{OSSLBStage3-short_name}}_{{OSSLBStage3-private-ip}}_nginx.conf{% endcapture %}
{% capture OSSLBStage3-nginx-conf-url %}{{api-platform-general-nginx-link}}{{OSSLBStage3-nginx-conf-name}}{% endcapture %}

{% capture OSSLBStage2-nginx-conf-name %}{{OSSLBStage2-short_name}}_{{OSSLBStage2-private-ip}}_nginx.conf{% endcapture %}
{% capture OSSLBStage2-nginx-conf-url %}{{api-platform-general-nginx-link}}{{OSSLBStage2-nginx-conf-name}}{% endcapture %}

{% capture doctorapitestgw-nginx-conf-name %}{{doctorapitestgw-short_name}}_{{doctorapitestgw-private-ip}}_nginx.conf{% endcapture %}
{% capture doctorapitestgw-nginx-conf-url %}{{api-platform-general-nginx-link}}{{doctorapitestgw-nginx-conf-name}}{% endcapture %}


| Environment | Region    | Domain Name                 | Internal IP    | External IP     | Nginx Conf*                        |
| ----------- | --------- | --------------------------- | -------------- | --------------- | -----------------------------------|
|{{doctorbus-environment}}|{{doctorbus-region}}|{{doctorbus-domain}}|{{doctorbus-private-ip}}|{{doctorbus-public-ip}}|[{{doctorbus-nginx-conf-name}}]({{doctorbus-nginx-conf-url}})|
|{{doctorapigw-environment}}|{{doctorapigw-region}}|{{doctorapigw-domain}}|{{doctorapigw-private-ip}}|{{doctorapigw-public-ip}}|[{{doctorapigw-nginx-conf-name}}]({{doctorapigw-nginx-conf-url}})|
|{{doctorapigw2-environment}}|{{doctorapigw2-region}}|{{doctorapigw2-domain}}|{{doctorapigw2-private-ip}}|{{doctorapigw2-public-ip}}|[{{doctorapigw2-nginx-conf-name}}]({{doctorapigw2-nginx-conf-url}}) |
| {{doctorapitest-environment}} | {{doctorapitest-region}} | {{doctorapitest-domain}} | {{doctorapitest-private-ip}} | {{doctorapitest-public-ip}} | [{{doctorapitest-nginx-conf-name}}]({{doctorapitest-nginx-conf-url}}) |
| {{OSSLBStage3-environment}} | {{OSSLBStage3-region}} | {{OSSLBStage3-domain}} | {{OSSLBStage3-private-ip}} | {{OSSLBStage3-public-ip}} | [{{OSSLBStage3-nginx-conf-name}}]({{OSSLBStage3-nginx-conf-url}}) |
| {{OSSLBStage2-environment}} | {{OSSLBStage2-region}} | {{OSSLBStage2-domain}} | {{OSSLBStage2-private-ip}} | {{OSSLBStage2-public-ip}} | [{{OSSLBStage2-nginx-conf-name}}]({{OSSLBStage2-nginx-conf-url}}) |
| {{doctorapitestgw-environment}} | {{doctorapitestgw-region}} | {{doctorapitestgw-domain}} | {{doctorapitestgw-private-ip}} | {{doctorapitestgw-public-ip}} | [{{doctorapitestgw-nginx-conf-name}}]({{doctorapitestgw-nginx-conf-url}}) |

<br>
All the above external addresses are internet facing. Dev does not have an external IP but has a 9.66.246.38 address.

**(*) Backup of the configuration files are available in the [{{api-platform-general-nginx-name}}]({{api-platform-general-nginx-link}}) repository or use the hyperlink from the table.**
> As best practice, if a configuration file is update, upload the older version
<br><br>

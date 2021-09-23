---
layout: default
title: Sources of information
---
## User interfaces

There are several key sources of information which are useful for operations:

| Information source | Description | How to access |
|-
| Grafana | Graphs of historical statistics.  Useful for spotting trends and anomalous behaviour | Any `stats` server, port 8002 |
| Kibana | Searchable logs | Any `logs` server, port 9292 |
| Consul | Current status of each registered service | Any server, port 8500 |
| ElasticHQ | Detailed information on the ElasticSearch cluster | `logs-0:9200/_plugin/HQ` (works on any logs server) |
| MessageSight | Detailed information on messaging | MessageSight server, port 9087.  User ID is `sysadmin`.  Password can be found on the `seed` machine, under the `/home/iot-deploy/.ssh/` directory. |
| DataPower | Detailed information on HTTP/HTTPS routing and single signon | DataPower server, port 9090.  User ID is `admin`.  Password can be found on the `seed` machine, under the `/home/iot-deploy/.ssh/` directory. |
{:.table .table-bordered .table-striped .table-responsive}

See the [Production dashboard](https://iot-dash-prod.hursley.ibm.com/) to access these consoles for the production service, without needing to log onto the VPN.

## Bluemix troubleshooting
[Bluemix troubleshooting guide](https://w3-connections.ibm.com/wikis/home?lang=en-us#!/wiki/Wfba9e56cc40c_4bb2_8805_e05bdeb2105f/page/Troubleshooting)

## SoftLayer links

* [SoftLayer customer portal](https://control.softlayer.com/)
* [Old SoftLayer customer portal](https://manage.softlayer.com/)

## People

### On-call operations team

* David J Parker/UK/IBM
* Graham J Eames/UK/IBM
* Ben Bakowski/UK/IBM
* Benjamin Alton2/UK/IBM
* Sam Danbury/UK/IBM

### IoT Service Team

* Paul Slater1/UK/IBM
* Valerie Lampkin/Alpharetta/IBM
* Uzma Siddiqui/Sunnyvale/IBM
* Maya Anilson/India/IBM
* Simon Gormley/UK/IBM

### Cloudant Support Contact

* support@cloudant.com
* Technical Account Manager - Claudius Li/Boston/IBM

### Informix Support Team

* Lauri Ojantakanen/Finland/IBM
* Mark Singleton/Santa Teresa/IBM
* Ryan Mayor/Toronto/IBM
* Paul Van Run/Toronto/IBM
* Peng LP Li/China/IBM

### Subject matter experts

| Subject area | Contact |
|-
| Service architecture | Stuart Hayton, Peter Niblett |
| Infrastructure architecture | Arthur Barr, Graham Eames |
| DataPower / single-sign on / IBM ID | Tom Klapiscak |
| Security | Andrew Johnson, Graham Eames |
| Billing | Stuart Hayton, Tim Daniel-Jacobi |
| Metering | David Clayton |
| Load balancers | Jon Levell, Ian Edwards |
| MessageSight configuration | Andrew Johnson, Ian Edwards |
| MS Proxy | Ken Borgendale |
| MS Proxy Java connector | David Clayton |
| Portal UI | Tim Daniel-Jacobi, David Clayton |
| Cloudant | Dave Parker, Ben Alton |
| Historian | Ben Alton, Dave Parker |
| Deployment code | Tom Klapiscak, Andrew Johnson |
| Logging | Arthur Barr, Graham Eames |
| Statistics | Arthur Barr, Graham Eames |
| Monagent scripts | Ben Alton, Dave Parker |
| Device recipes | Amit Mangalvedkar |
| Support (inc. PagerDuty) | Paul Slater |
| Engineering/operations manager | Michael Bradley |
| Anything else | Dave Parker, Graham Eames |
{:.table .table-bordered .table-striped .table-responsive}

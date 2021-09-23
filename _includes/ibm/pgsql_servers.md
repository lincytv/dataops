{% include {{site.target}}/load_pgsql_constants.md %}

### PostgresSQL and HAProxy servers


| Hostname               | Type                 | Location                 | Region                 | Public IP                 | Private IP                 | Environment | Notes
| -----------            | ---------                   | ------------------------ | ------                 | --------------            | ---------------            | ---------   | ------
| {{osspgproxy1-domain}} | {{osspgproxy1-device-type}} | {{osspgproxy1-location}} | {{osspgproxy1-region}} | {{osspgproxy1-public-ip}} | {{osspgproxy1-private-ip}} | {{osspgproxy1-env}} | {{osspgproxy1-notes}} |
| {{osspgproxy2-domain}} | {{osspgproxy1-device-type}} | {{osspgproxy2-location}} | {{osspgproxy2-region}} | {{osspgproxy2-public-ip}} | {{osspgproxy2-private-ip}} | {{osspgproxy2-env}} | {{osspgproxy2-notes}} |
| {{osspg1-domain}}      | {{osspg1-device-type}}      | {{osspg1-location}}      | {{osspg1-region}}  | {{osspg1-public-ip}}   | {{osspg1-private-ip}} | {{osspg1-env}} | {{osspg1-notes}} |
| {{osspg2-domain}}      | {{osspg2-device-type}}      | {{osspg2-location}}      | {{osspg2-region}} | {{osspg2-public-ip}}   | {{osspg2-private-ip}} | {{osspg2-env}} | {{osspg2-notes}} |
| {{doctorapitestgw-domain}} | {{doctorapitestgw-device-type}} | {{doctorapitestgw-location}} | {{doctorapitestgw-region}} | {{doctorapitestgw-public-ip}} | {{doctorapitestgw-private-ip}} | {{doctorapitestgw-env}} | {{doctorapitestgw-notes}} |


#### Additional information:

* Virtual Machine (VM), Intel(R) Xeon(R) CPU E5-2683 v3 @ 2.00GHz (4 cores), 8 GB RAM
* Baremetal (BM), Intel(R) Xeon(R) Silver 4110 CPU @ 2.10GHz (32 cores), 62 GB RAM
* Clients do not talk to the production and staging Postgres servers directly, but go through the HAProxy instances which allows for failover (clients connect to the pg.oss.cloud.ibm.com hostname)
* Clients do talke directly to the dev Postgres server

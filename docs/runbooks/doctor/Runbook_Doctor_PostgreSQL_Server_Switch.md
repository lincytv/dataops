---
layout: default
description: RETIRED - This Runbook is for PostgreSQL server is down.
title: RETIRED - Runbook Doctor PostgreSQL server is down
service: PostgreSQL
runbook-name: RETIRED - Runbook Doctor PostgreSQL server is down
tags: oss, bluemix, doctor, PostgreSQL, pg
link: /doctor/Runbook_Doctor_PostgreSQL_Server_Switch.html
type: Alert
---

{% include {{site.target}}/load_oss_doctor_constants.md %}
{% include {{site.target}}/load_oss_contacts_constants.md %}
{% include {{site.target}}/new_relic_tip.html%}
{% include {{site.target}}/load_pgsql_constants.md %}
---

**PostgreSQL has been migrated to IBM Cloud Databases (ICD).  Please use the following [runbook]({{site.baseurl}}/docs/runbooks//apiplatform/Runbook-icd-postgres-monitoring.html). Please DO NOT update it here**

## Purpose

This runbook is used to switch master and slave node of PostgreSQL clusters, when PostgreSQL node is down, please follow these steps to switch master and slave node.



## User Impact
If PostgreSQL master server is down, doctor db can't be accessed any more.

## Instructions to Fix
Currently we have two servers of PostgreSQL.

{% include {{site.target}}/pgsql_servers.md %}

### Recover PostgreSQL server

#### Step 1 Promote slave server to master.
  - Logon slave node (10.177.49.59).
  - Run following commands to promote slave node to master.

  ```
  su – postgres
  ```

  ```
  source ./.bashrc
  ```

  ```
  pg_ctl promote -D /var/lib/postgresql/9.6/main
  ```

  - Verify if current database is promoted to master node.

    Run **pg_controldata**, verify the **Database cluster state** of the output, it should be **in production**.

  - Verify if the database is writable, run following commands.

  ```
  psql -U doctor -h 10.177.49.59 -d postgres
  ```

  ```
  CREATE DATABASE testdb;
  ```

  ```
  CREATE TABLE public.employee (id character(50) NOT NULL,name text NOT NULL,age integer NOT NULL,sex character(50),email text,loginname text,password text);
  ```

  ```
  INSERT INTO employee (id, name, age, sex, email, loginname, password)VALUES('53c68ee7', 'hello', 10, 'f', 'hello@cn.ibm.com', 'hello', 'hello');
  ```

#### Step 2 Change the IP of domain name on CIS.
  - Logon cloud.ibm.com with your w3id.
  - Switch account to **{{oss-account-account}}**.
  - Click **Services** on dashboard Resource Summary part.

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/services.jpg){:width="640px"}

  - Input **CIS** under Name column to filter the result,then click **CIS-OSS-Prod**.

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/choose-service-CIS-OSS.png){:width="640px"}

  - If you can't find **CIS-OSS-Prod** under **Services**, please contact Jim(yujunjie@cn.ibm.com) to apply access to **CIS-OSS-Prod** service.

  - Click **DNS Records**.

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/click-DNS-Records.png){:width="640px"}

  - Under DNS Records, search **pg-doctor**, then click three dots beside pg-doctor, click Edit.

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/edit-pg-domain.png){:width="640px"}

  - Change the IP of **pg-doctor**, to 10.x.x.x of new master node (10.177.49.59).

    ![]({{site.baseurl}}/docs/runbooks/doctor/images/update-pg-domain.png){:width="400px"}

  - Under DNS Records, search **pg-doctor-nat**, then click three dots beside pg-doctor-nat, click Edit, these steps are the same as steps of changing **pg-doctor**.

  - Change IP of **pg-doctor-nat** to 9.x.x.x of new master node (9.66.242.218).

### Setup master-slave replication
After 10.188.27.161 is recovered, please follow these steps to setup master-slave replication.

#### Step 1 Demote master node to slave.
  - Logon master node (10.188.27.161).
  - Run following commands.

  ```
  su – postgres
  ```

  ```
  source ./.bashrc
  ```

  - Backup recovery.conf file.

  ```
  cp /var/lib/postgresql/9.6/main/recovery.conf /var/lib/postgresql/9.6/
  ```

  - Backup main folder.

  ```
  mv /var/lib/postgresql/9.6/main /var/lib/postgresql/9.6/main_bak
  ```

  - Stop PostgreSQL.

  ```
  pg_ctl -D $PGDATA -l pgsqllog.log stop
  ```

  - Create replica database folder, replace **Master-IP** with the IP of new master node (10.177.49.59).

  ```
  pg_basebackup -D $PGDATA -Fp -Xs -v -P -h Master-IP -p 5432 -U repuser
  ```

  - Copy recovery.conf to main folder.

  ```
  cp /var/lib/postgresql/9.6/recovery.conf /var/lib/postgresql/9.6/main/
  ```

  ```
  rm /var/lib/postgresql/9.6/main/recovery.done
  ```

  - Start PostgreSQL.

  ```
  pg_ctl -D $PGDATA -l pgsqllog.log start
  ```

  - Verify if current database is demoted to slave node.

    Run **pg_controldata**, verify the **Database cluster state** of the output, it should be **in archive recovery**.

#### Step 2 Verify the Streaming Replication.
  - Logon new master node (10.177.49.59).

  ```
  psql -U doctor -h 10.177.49.59 -d testdb
  ```

  - Insert a record to testdb on master node.

  ```
  INSERT INTO employee (id, name, age, sex, email, loginname, password)VALUES('53c68ee11', 'hello', 10, 'f', 'hello_new@cn.ibm.com', 'hello', 'hello');
  ```

  - Logon new slave node (10.188.27.161).

  ```
  psql -U doctor -h 10.188.27.161 -d testdb
  ```

  - Verify if there is same record on slave node.

  ```
  SELECT * from employee;
  ```

**If any questions, please contact {% include contact.html slack=doctor-backend-5-slack name=doctor-backend-5-name userid=doctor-backend-5-userid notesid=doctor-backend-5-notesid %} or {% include contact.html slack=cloud-software-dev-slack name=cloud-software-dev-name userid=cloud-software-dev-userid notesid=cloud-software-dev-notesid %}.**

---
layout: default
title: Changing versions of software
---
## Software in Docker containers
Software in Docker containers is usually installed via `apt`, from the [Hursley mirror](http://ubuntu.hursley.ibm.com/ubuntu/) of the official Ubuntu repositories.

If the official repositories don't contain a particular package, it is downloaded from a [Hursley FTP server](http://iot-test-01.hursley.ibm.com/dependencies/) at build time.

The contents of this can be updated using the iotbld user account on iot-test-01 and updating the contents of `/artifacts/dependencies/` 

See Graham Eames or Dave Parker if you need to update this.

## Base image template
An IoT-specific base image is used for all nodes, as the default SoftLayer images are insecure.
There is an Ubuntu 14.04 template used for virtual servers and a CentOS 6 template used for Bare Metal servers (eg loadbalancer)

Most updates to these templates are performed by deploying the existing template onto a new hourly system before making the required changes.
Once the changes have been completed, the system then needs to be captured as an image template for use elsewhere
See Graham or Jon if you need further information to update these templates.

Once a new template has been created, you need to reference it from the environment's blueprint JSON file.

## MessageSight
This requires access to mar145.test.austin.ibm.com to carry out
See Ian if you need to update this
TBD

## DataPower
TBD

## MSProxy
This requires access to mar145.test.austin.ibm.com to carry out
TBD

## Apt Repository
The seed machine in every environment provides a minimal apt repository containing packages which are not available in the official Ubuntu repositories
(such as IBM Java and internal IBM security tooling)
This repository can be updated using the iotbld account on iot-test-01.
To add additional files to this repository they should be placed in `/artifacts/staging/repos/apt/pool/main/`
Once the necessary changes have been made you should run `cd  /artifacts/staging/repos/apt/ && ./rebuild_apt.sh` to regenerate the metadata about the packages.
To replicate the changes to Soft Layer you should then run the *IoTC Sync Dependencies [Development]* build.

## Yum Repository
The seed machine in every environment provides a minimal apt repository containing packages which are not available in the official CentOS/RedHat repositories
(such as IBM Java and internal IBM security tooling)
This repository can be updated using the iotbld account on iot-test-01.
To add additional files to this repository they should be placed in `/artifacts/staging/yum/repo/iotcloud/`
To replicate the changes to Soft Layer you should then run the *IoTC Sync Dependencies [Development]* build.

## Security patches
IBM security policy (ITCS 104) requires the following:

> 1.5.5 - Security advisory patch management
>
> Requirement 6: A process must be in place to install security advisory patches within the time limits outlined below.
>
> Table 2 Security advisory patch time limits
>
> | Group | System Type/Operating System | High severity | Medium severity | Low severity |
> |--
> | Any group | Internet systems that populate IES security zones | 3 days | 7 days | 30 days |
> {:.table .table-bordered}

Patches and their deadlines are published via the [IBM Securities Advisory Database](https://advisories.secintel.ibm.com/adv_database.php)

It is recommended that multiple members of the operations team subscribes to the mailing lists for the products in use - Ubuntu, CentOS and IBM Other (covers Java) - to ensure that the the dates can be met.

To enable updates to be applied a build definition has been created to allow updates to be applied to any environment (IoTC Update Environment) by setting the environment as a build property.

When patches are released, they should be tested by running this build against either an integration stand or the Staging environment. If you are happy that the environment continues to operate as expected, the build should then be run against Staging (if not already done) and Production.

To update these latter two environments, it will be necessary to override the build engine used such that it runs on one of the iot-prod-1.1/2/3 build engines.
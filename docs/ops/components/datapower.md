---
layout: default
title: DataPower
---
# DataPower #

DataPower XI52 virtual appliance runs as a guest on an ESXi host.

## Recovering DataPower ##

There is no state in DataPower, so a reinstall will recover DataPower function.
Deploy reload or reset will reinstall DataPower.
An ordinary deploy will reconfigure DataPower.

### Logging onto DataPower ###

The GUI is available at:
[link](https://datapower-0.dal06-1.management.test.internetofthings.ibmcloud.com:9090 "DataPower dal06-1 GUI")
or:
[link](https://datapower-0.dal06.management.dal06-1.test.internetofthings.ibmcloud.com:9087 "DataPower dal06.dal06-1 GUI)

The GUI password for DataPower is available on the seed machine in that deployment unit in:
`/home/iot-deploy/.ssh/datapower-0.admin.password`

The GUI userid is `admin`

This password gets regenerated on each deploy. 

If the deploy has not happened and the password has been lost due to a SoftLayer OS image reload then also try looking at the iSCSI which is preserved by an OS reload.
`/mnt/iscsi/datapower/datapower-0.admin.password`

If the initial configuration hasn't completed then the default userid/password is `admin/admin`.


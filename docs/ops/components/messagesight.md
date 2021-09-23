---
layout: default
title: MessageSight
---
# MessageSight #

## Recovering MessageSight ##
In the event of a MessageSight failure, where it will not come up in production mode we can take a backup of the persistent data on the machine. This might be usable to restore the machine after it has been wiped, or to retrieve data for customers.

### MessageSight In Maintenance Mode ###
If MessageSight is available, but in maintenance mode we can use the backup command to make a backup of the data.

To determine if MessageSight is in maintenance mode, connect into it from the seed machine (by su to root and then `ssh admin@messagesight-0`). Then issue the command:

`imaserver status`

This will show a status of:

`Status = Running (maintenance)  
ServerUpTime = ...`

If the server is running, but in production, and you want to make a backup it first needs to be put into maintenance mode, by following this procedure:

`imaserver runmode maintenance`  
`imaserver stop`  
`imaserver start`  

Following this, `imaserver status` should now show `Running (maintenance)`.

Once in maintenance mode, the configuration and store can be backed up with the command:

You will need to be running an SSH server on a machine that is also connected to the Softlayer VPN (e.g. the duty laptop or seed)

`imaserver backup "Password=<PASSWORD>" "StoreDestinationURL=scp://<SSH_SERVER>:<PATH>/imaStoreBackup" "StoreDestinationUserID=<SSH_USERID>" "StoreDestinationPassword=<SSH_PASSWORD>"`

This will place a file named STOREBACKUP in the <PATH> directory on the SSH server. In addition, a configuration backup will be taken and written to a file (whose name is displayed in the response to the imaserver backup command). The file name will be of the form imaBackup.<TIMESTAMP>.

For completeness it is probably worth taking a copy of this configuration backup (although, our configuration is fixed). To do that, scp the file off with:

`file put imaBackup.<TIMESTAMP> scp://<SSH_USERID>@<SSH_SERVER>:<PATH>/imaBackup.<TIMESTAMP>`

When prompted, enter the SSH_PASSWORD.

To put MessageSight into production mode, use:

`imaserver runmode production`  
`imaserver stop`  
`imaserver start`  

## MessageSight Stopped ##
If MessageSight is not running in maintenance mode, so is stopped, and cannot be restarted in maintenance mode, we will need to take a manual backup of the store. This cannot be done from within the standard shell available to administrators in MessageSight, it requires the use of an undocumented 'advanced-pd-options' command (_enableshell) to get to a unix shell from which the store can be manually accessed.

To enable the shell, a key must be generated based on the serial number of the MessageSight machine. The serial number can be accessed by running the command:

`show version`

This displays information similar to the following:

`Installation date: Oct 10, 2014 5:43:47 AM`  
`Platform version: 6.0.0.7`  
`Platform build ID: bsdk6-20141003-1040`  
`Platform build date: 2014-10-03 16:00:58+00:00`  
`Machine type/model: VMware`  
`Serial number: 8b1b3d06`  
`Entitlement: 8b1b3d06`  
`Firmware type: Release`  

The key generator is maintained by the MessageSight service team. To get a key you will need to provide the serial number above the key has a time limit (maximum is 99 hours).

Once you have a key, you can get to a Unix shell using the command:

`advanced-pd-options _enableshell <KEY>`

After entering the key the 1st time, to re-enter the unix shell, you should just use `advanced-pd-options _enableshell`.

Once into the shell, the persistent store is located in `/store`.

You can copy the entire store by making a zipped tar of it and then sending it to an SSH server with:

`tar --exclude '*.tgz' -czf /store/imaManualStoreBackup.tgz /store`  
`scp /store/imaManualStoreBackup.tgz <SSH_USERID>@<SSH_SERVER>:<PATH>/imaManualStoreBackup.tgz`

### Logging onto MessageSight ###

The GUI is available at:
[link](https://messagesight-0.dal06-1.management.test.internetofthings.ibmcloud.com:9087 "MessageSight dal06-1 GUI")
or:
[link](https://messagesight-0.dal06.management.dal06-1.test.internetofthings.ibmcloud.com:9087 "MessageSight dal06.dal06-1 GUI")

The GUI password for MessageSight is available on the seed machine in that deployment unit in:

`/home/iot-deploy/.ssh/messagesight-0.sysadmin.password`

The GUI userid is `sysadmin`

This password gets regenerated on each deploy. If the deploy has not happened and the password has been
lost due to a SoftLayer OS image reload then log onto MessageSight using the admin/<SSH key: iot-deploy>.

`ssh admin@messagesight-0.dal06-1.management.test.internetofthings.ibmcloud.com`
or
`ssh admin@messagesight-0.dal06.managementdal06-1.test.internetofthings.ibmcloud.com`

Then reset the password using:

`imaserver user edit UserID=sysadmin Type=WebUI password=********`

If MessageSight has not been fully configured then the password might still be `admin/admin`, though the 
SSH key should be set up as part of the deploy.

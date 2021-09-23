---
layout: default
title: Loadbalancer
---
# Load Balancers #

## What are they running? ##
The load balancers are a pair of Linux boxes. They are a highly-available pair in an active/passive 
configuration. The load balancing on the active machine is performed by a kernel module called 'ipvs' 
(IP Virtual Server). IPVS is controlled by a service called keepalived. Keepalived monitors the connectivity 
of the proxies and the partner in the HA pair and configures IPVS appropriately.

### Which one is MASTER ###
The syslog from the loadbalancers contains lines from keepalived saying when it transistions from BACKUP to 
MASTER and vice-versa. This log is uploaded to logstash

### Can I confirm which is MASTER ###
If you're logged into a machine issue:
`ip addr list`
If you can see the external IP address that corresponds to messaging.internetofthings.ibmcloud.com then the 
machine is currently trying to be master.

### How can I see the current routes ###
Issue the command:
`sudo service ipvsadm status`

Output looks like (from a test system with a single proxy:

iot-deploy@loadbalancer-0:~$ sudo service ipvsadm status
IP Virtual Server version 1.2.1 (size=4096)
Prot LocalAddress:Port Scheduler Flags
  -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
TCP  158.85.7.2:443 lc
  -> 10.108.6.52:443              Route   1      0          0
TCP  158.85.7.2:1883 lc
  -> 10.108.6.52:1883             Route   1      0          0
TCP  158.85.7.2:8883 lc
  -> 10.108.6.52:8883             Route   1      0          0

### How do I restart it ###
Issue the command:
`sudo service keepalived restart`
(This will usually cause the paired machine to take over if issued on the current master)

### How do I stop it ###
If the loadbalancer is malfunctioning, we can rely on a single loadbalancer in extremis. Stop the "bad" one:
`sudo service keepalived stop`
(and to undo this: `sudo service keepalived start` )

### Where are the config files ###
To aid understanding of an issues, it's possible to look at the config files under /etc/keepalived



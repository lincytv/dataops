---
layout: default
title: Known issues & workarounds
---
## Node and Service status appears to "flap" within Consul

### Description

When viewing the service status in Consul, particular nodes appear to be constantly changing between available and failed.

When viewing the consul-server logs you see something similar to the following with nodes joining and being marked as failed over a short interval:

~~~
2014/09/29 14:39:31 [INFO] serf: EventMemberFailed: loadbalancer-1 10.104.46.209
2014/09/29 14:39:31 [INFO] consul: member 'loadbalancer-1' failed, marking health critical
2014/09/29 14:39:31 [INFO] serf: EventMemberJoin: msproxy-0 10.104.46.200
2014/09/29 14:39:31 [INFO] consul: member 'msproxy-0' joined, marking health alive
2014/09/29 14:39:31 [INFO] serf: EventMemberJoin: loadbalancer-1 10.104.46.209
2014/09/29 14:39:31 [INFO] consul: member 'loadbalancer-1' joined, marking health alive
2014/09/29 14:39:34 [INFO] memberlist: Suspect msproxy-0 has failed, no acks received
2014/09/29 14:39:36 [INFO] memberlist: Marking msproxy-quickstart-0 as failed, suspect timeout reached
2014/09/29 14:39:36 [INFO] serf: EventMemberFailed: msproxy-quickstart-0 10.104.46.201
2014/09/29 14:39:36 [INFO] consul: member 'msproxy-quickstart-0' failed, marking health critical
2014/09/29 14:39:37 [INFO] memberlist: Marking msproxy-1 as failed, suspect timeout reached
2014/09/29 14:39:37 [INFO] serf: EventMemberFailed: msproxy-1 10.104.46.208
2014/09/29 14:39:37 [INFO] consul: member 'msproxy-1' failed, marking health critical
~~~
 

### Solution
1. Login to the affected node and stop consul and the other running docker containers
2. Wait for around 5 minutes to ensure it's removal has propogated to the rest of the cluster
3. Start consul-server
4. Start the remaining containers


## MessageSight Proxy segfault
The MSProxy has been known to crash completely.  The Docker daemon should restart it automatically.

Look for messages containing "segfault" in the syslog for the MSProxy servers.  You may also see a [core dump](dumps.html).

## ElasticSearch errors
In the event of a failure, ElasticSearch's logs inherently don't appear in ElasticSearch.  The best way to see errors in ElasticSearch is by running `docker logs elasticsearch` on a `logs` node.

## Docker registry is full
The disk on the Docker registry sometimes gets full and needs to be manually purged.

The automated method for addressing this is to run the *IoTC Deploy Infrastructure* build with a recent continuous build passed in as the build label.

This will clean the registries in all datacenters. If you only want to touch a single registry, you can login to that server and manually remove files. Run `docker inspect registry`
to identify the real location of the volume where the files are stored, remove all files from this directory and restart the container.

The first deployment to a datacenter after this has been performed will take longer as the images need to be uploaded from Hursley. 
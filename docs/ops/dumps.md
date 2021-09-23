---
layout: default
title: Gathering diagnostics
---
Diagnostic dumps are configured to be placed in the `/var/dump` directory on each node.  Docker containers which can generate dumps bind mount a sub-directory into `/var/dump` inside the container.

## Native core dumps
Linux core dumps for native processes are turned off on most servers (run `ulimit -c` to check the maximum core dump file size, which is usually zero).  This is because you can usually only use the core dump if you are familiar with, and have access to, the original source code.

Core dumps are enabled for MSProxy nodes.

Native core dumps are configured to re-use the same file name every time, so that multiple dumps do not fill the disk.

## Java dumps
Java core dumps and heap dumps are disabled for non-IBM Java processes (such as ElasticSearch), via an environment variable setting.

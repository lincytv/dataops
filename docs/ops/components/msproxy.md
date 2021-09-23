---
layout: default
title: MessageSight Proxy
---
# MSProxy #

## Manually generating dumps from MSProxy ##
If the MSProxy is misbehaving in some way but not dying, it should be possible to get a dump from it for later analysis before restarting it.  This is particularly useful when you just want to get diagnostics that we don't already have.

To do this follow these steps:

1. Log on to the msproxy host.
2. Execute `2docker.sh` as root (this script auto enters the `msproxy` container, so you may need to use `2docker.sh msproxy-quickstart` to get to the msproxy quickstart container.  This is much like `docker exec -ti ... bash` but gdb works.
3. From the container execute `gdb -p 1`.
4. From gdb, execute `generate-core /var/dump/core`. Exit gdb with `quit` and then `y`.
5. Optional - If you want to analyse the JVM running in the proxy process:
   * Change to the `/opt/ibm/msproxy` directory and execute `export PATH=$PATH:/opt/ibm/java/jre/bin`.
   * Execute `jextract /var/dump/core`.  There should be no warnings.
7. Gather the resulting `/var/dump/core(.zip if its been jextracted - the zip includes the original core)` (which will be at `/var/dump/msproxy/` on the host).  Don't forget to clean up the core once you've got it.
8. Optional - If the problem is an apparent hang you may want to get a number of core files (like 3 in 1 minute) to check to see if threads are progressing or not.

## Diagnosing MSProxy JVM problems Using a core file ##
`jextract` adds all the goodies that JVM diagnostic tools needs (using the same Java build level from a core).

The IDDE tool can be used to interrogate the JVM running in the MSProxy process:

[http://www.ibm.com/developerworks/java/jdk/tools/idde/](http://www.ibm.com/developerworks/java/jdk/tools/idde/)

There are docs about how to use this tool, but as a hint you could try `!javathreads` Ctrl-Enter to get the Java threads from the time of the core.

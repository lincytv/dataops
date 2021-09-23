#!/bin/bash
# Use to cleanup container logs ($containerName) such as
# BBBO logs from  /opt/bbo/bluemix_best_operator/logs
# and /opt/bbo/bluemix_best_operator_agent/logs.
# If any log file in the locations ($pathLogs), is > $maxSizeFile then the
# file(s) will be truncated to only keep $maxSizeFile of log information
# This script will run as crontrab job weekly.
# This action and the rolling logs previusly implemented,
# should be enoug to avoid more disk usage alerts
# https://github.ibm.com/cloud-sre/ToolsPlatform/issues/7401
#
# Alejandro Torres Rojas 10-Jun-2019

me=$(basename "$0")
# Set default values
containerName="bbo_agent"
pathLogs="/opt/bbo/bluemix_best_operator/logs"
maxSizeFile="50M"
helpMessage="\
Usage: $me -c container_name -p logs_path -s maxFileSize [<options>]
       $me -c bbo_agent -p /opt/bbo/bluemix_best_operator/logs -s 50M
Truncate log files to keep a healthy disk usage.

  -h, --help               Show this help information.
  -c                       Docker container name to truncate logs.
                           default: bbo_agent
  -p                       Path where the logs to be truncated are located.
                           default: /opt/bbo/bluemix_best_operator/logs
  -s                       Maximum size of the files to be allow,
                           sizing is the same value use by the truncate bash utility
                           more info at
                           http://www.gnu.org/software/coreutils/manual/html_node/truncate-invocation.html
                           defaul: 50M"

 parse_args() {
     # Parse arg flags
     while : ; do
       if [[ ( $1 = "-c" ) && -n $2  ]]; then
         containerName=$2
         shift 2
       elif [[  $1 = "-p"  && -n $2 ]]; then
         pathLogs=$2
         shift 2
       elif [[ ( $1 = "-s" ) && -n $2 ]]; then
         maxSizeFile=$2
         shift 2
       elif [[ $1 = "-h" || $1 = "--help"  ]]; then
         echo "$helpMessage"
         exit 0
     else
         break
     fi
   done
 }


truncate_logs() {
# Checks if bbo_agent container is running in this VM
exist_container=$(docker ps --format '{{.Names}}' |grep $containerName)
if [ "$exist_container" ]; then
  # truncate all log files that are > maxSizeFile in size reducing them to maxSizeFile
  docker exec -it $exist_container find $pathLogs -type f -size +$maxSizeFile -exec truncate -s $maxSizeFile {} \;
fi
}


cleanup_bbo_tasks() {

  if [ "$exits_bbo_agent" ]; then
    docker exec -it $exits_bbo_agent find /opt/bbo/tasks -type d -mtime +1 -exec rm -r {} \; &> /dev/null
  fi
}

cleanup_ansible_old_logs(){
  exist_doctor_backend=$(docker ps --format '{{.Names}}' |grep doctor_backend)
  exist_doctor_cloud=$(docker ps --format '{{.Names}}' |grep doctor_cloud)
  if [ "$exist_doctor_backend" ]; then
    docker exec -it $exist_doctor_backend find /opt/ansible/logs -type f -mtime +1  -exec rm -r {} \; &> /dev/null
  elif [ "$exist_doctor_cloud" ]; then
    docker exec -it $exist_doctor_cloud find /opt/ansible/logs -type f -mtime +1  -exec rm -r {} \; &> /dev/null
  fi

}

checks_logrotate(){
  count=0
  if [ "$exits_bbo_agent" ]; then
    count=$(docker exec -it $exits_bbo_agent ls  /etc/logrotate.d/bbo|wc -l)
    # Checks if the logrotation configuration file for bbo exist
    if [ $count -eq 1 ]; then
       docker exec -it bbo_agent logrotate /etc/logrotate.conf
    elif [ -f /opt/bbo_logs_rot_cnf ]; then
      docker cp /opt/bbo_logs_rot_cnf bbo_agent:/etc/logrotate.d/bbo
      docker exec -it bbo_agent logrotate /etc/logrotate.conf
    fi
  fi
}

main() {
  exits_bbo_agent=$(docker ps --format '{{.Names}}' |grep bbo_agent)
  parse_args "$@"
  truncate_logs
  checks_logrotate
  cleanup_bbo_tasks
  cleanup_ansible_old_logs
}
[[ $1 = --source-only ]] || main "$@"

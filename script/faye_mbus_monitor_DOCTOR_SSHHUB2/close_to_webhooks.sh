#!/bin/bash
########################################################### {COPYRIGHT-TOP} ####
# Licensed Materials - Property of IBM
# CloudOE
#
# (C) Copyright IBM Corp. 2014,2019
#
# US Government Users Restricted Rights - Use, duplication, or
# disclosure restricted by GSA ADP Schedule Contract with IBM Corp.
########################################################### {COPYRIGHT-END} ####
#
# Variables
#
#set -o errexit #abort if any command fails
me=$(basename "$0")
helpMessage="\
Usage: $me -e event_name -m (prd|test) [<options>]
       $me -e mhub_faye_is_down -m test  -v
Post a message to webhooks to create a PagerDuty incident.
TIP Integration infromation can be found here: https://github.ibm.com/cloud-sre/tip-api
Options:
  -h, --help               Show this help information.
  -c, --tip_console        Possible values 'toc'/'analytics'
                           default is 'toc'. Indicates how the alert will be handled.
  -d, --debug_mode         Will generated a log file.
  -e, --event_name         Event name having an issue Mandatory
                           -e mhub_faye_is_down.
  -f, --json-file PATH     Contains a JSON  file with the ticket detail
                           If empty will use a template and fill with data.
  -m, --send_mode          Use 'prd' for production 'test' for testing defaul is test
                           If -w or --webhook is passed, will use the URL passed.
  -n, --tribe_name         The name of the tribe where the alert was generated
                           defaul is 'CTO SRE Development'.
  -s, --service_name       Part of the CRN object default is 'ibm-cloud-ops-platform'.
  -t, --tip_token          TIP token https://github.ibm.com/cloud-sre/tip-api#request-access-token.
  -v, --verbose            Increase verbosity. Useful for debugging.
  -w, --webhook            Webhooks URL to send messages https://<domain>/hooks/tip-alert."
tipToken=82ed279f9da77aed5a4df4a65237d151 #doctor token
webHookUrlTest="https://tip-oss-flow.test.cloud.ibm.com/hooks/tip-alert"
webHookUrlPrd="https://tip-oss-flow.cloud.ibm.com/hooks/tip-alert"
webHookUrl=""
tribeName="CTO SRE Development"
pwdLocation=`pwd`
sendMode="test"
tipAlertUiUrl=""
tipCrnVersion="v1"
tipCrnCname="internal"
tipCrnCtype="private"
tipCrnServiceName="ibm-cloud-ops-platform"
hostName=`hostname -s`
tipSeverity=1
tipSource="monit"
tipSituation="mhub_faye_is_down"
tipCrnLocation="us-south"
tipCrnScope=""
tipCrnServiceInstance=""
tipCrnResourceType=""
tipCrnResource=""
tipConsole="toc"
tipCustomerImpacting="true"
tipDisablePager="false"
tipRunbookTocEnabled="false"
tipRunbookUrl="https://pages.github.ibm.com/cloud-sre/runbooks/docs/runbooks/doctor/ibm-only/Doctor_how_to_restart_BBO_Mbus_agents.html"
tipVersion="1.0"
templateJSONFile=""
logFileName=/etc/monit/log/$(basename "$me" | cut -d. -f1).log
debugMode=false
verbose_flag=false
CREATE_NOTICE="create.notice"
UPDATE_NOTICE="update.notice"
CLOSE_NOTICE="close.notice"
tipTipMsgType=$CLOSE_NOTICE
inputJSONFile=""
parse_args() {
    # Parse arg flags
    # If something is exposed as an environment variable, set/overwrite it
    # here. Otherwise, set/overwrite the internal variable instead.
    while : ; do
      if [[ ( $1 = "-c" || $1 = "--tip_console" ) && -n $2 ]]; then
        tipConsole=$2
        shift 2
      elif [[  $1 = "-d" || $1 = "--debug_mode"  ]]; then
        debugMode=true
        shift 1
      elif [[ ( $1 = "-e" || $1 = "--event_name" ) && -n $2 ]]; then
        eventName=$2
        shift 2
      elif [[ ( $1 = "-f" || $1 = "--json-file" ) && -n $2 ]]; then
        inputJSONFile=$2
        shift 2
      elif [[ $1 = "-h" || $1 = "--help"  ]]; then
        echo "$helpMessage"
        exit 0
      elif [[ ( $1 = "-m" || $1 = "--send_mode" ) && -n $2 ]]; then
        sendMode=$2
        shift 2
      elif [[ ( $1 = "-n" || $1 = "--tribe_name" ) && -n $2 ]]; then
        tribeName=$2
        shift 2
      elif [[ ( $1 = "-s" || $1 = "--service_name" ) && -n $2 ]]; then
        tipCrnServiceName=$2
        shift 2
      elif [[ ( $1 = "-t" || $1 = "--tip_token" ) && -n $2 ]]; then
        tipToken=$2
        shift 2
      elif [[ $1 = "-v" || $1 = "--verbose" ]]; then
        verbose_flag=true
        shift
    elif [[ ( $1 = "-w" || $1 = "--webhook" ) && -n $2 ]]; then
        webHookUrl=$2
        shift 2
    else
        break
    fi
  done
}
set_webhooks_url(){
  logger ">>> set_webhooks_url"
  # If webhoo URL is passed will use the user one otherwise will check the send mode
  # and select the URL base on the mode selecet prd or test
  if [ -z "$webHookUrl" ]; then
    if [ $sendMode = "prd" ]; then
      webHookUrl=${webHookUrlPrd}
    else
      webHookUrl=${webHookUrlTest}
    fi
    logger "Using Webhook URL: $webHookUrl to send messages."
  else
     if ! [[ $webHookUrl =~ https?://.*\tip-alert ]]; then
       echo "Invalid Webhook URL: $webHookUrl expecting https://<domain>/hooks/tip-alert"
       logger "Invalid Webhook URL: $webHookUrl."
       exit 1
     fi
  fi
  logger "<<< set_webhooks_url"
}
detect_and_verify(){
  # Verify critical values are set
  logger ">>> detect_and_verify"
  if [ -z "$eventName" ]; then
    echo "Missing event name it is a mandatory value."
    logger "Missing event name it is a mandatory value" "$(date)"
    echo echo "$helpMessage"
    exit 1
  fi
  logger "Event name: ${eventName}."
  set_webhooks_url
  if [ -z "$webHookUrl" ]; then
    echo "Failed to trigger event: you must set/provide the webHookUrl variable."
    logger "Failed to trigger event: you must set/provide the webHookUrl variable."
    exit 1
  elif [ -z "$tipToken" ]; then
    echo "Failed to trigger event: you must set/provide the tipToken variable."
    logger "Failed to trigger event: you must set/provide the tipToken variable."
    exit 1
  elif [ ! -x "/usr/bin/python" ]; then
    echo "Failed to trigger event; python is required, please install python and try again."
    logger "Failed to trigger event; python is required, please install python and try again."
    exit 1
  fi
  logger "Using TIP TOKEN: ${tipToken}."
  logger "<<< detect_and_verify"
}
get_json_file(){
  logger ">>> get_json_file"
  #incidentKey=`echo "$hostName:$eventName" | md5 | cut -f 1 -d ' '` # For MacOS
  incidentKey=`echo "$hostName:$eventName" | md5sum | cut -f 1 -d ' '` # For Ubuntu
  templateJSONFile="/tmp/tip_alert_webhooks-"$incidentKey
  hostIP=`curl ifconfig.me`
  if [ ! -z "$inputJSONFile" ]; then
    if [ -f "$inputJSONFile" ]; then
      is_valid_json $inputJSONFile
      logger "Using input JSONfile $inputJSONFile"
      cp $inputJSONFile $templateJSONFile
    fi
  elif [ -f "$templateJSONFile" ]; then
    create_json_template $templateJSONFile
    is_valid_json $templateJSONFile
    logger "No JSON file provided. Using template JSON file $templateJSONFile"
  else
    logger "No open alert exist for ${hostName}:${eventName}, missing file $templateJSONFile Aborting operation :("
    exit 0
  fi
  logger "<<< get_json_file"
}
#echo expanded commands as they are executed (for debugging)
enable_expanded_output() {
                set -o xtrace
                set +o verbose
}
#this is used to avoid outputting the repo URL, which may contain a secret token
disable_expanded_output() {
                set +o xtrace
                set -o verbose
}
create_json_template(){
  logger ">>> create_json_template"
  tipShortDescription=$(echo ${tipSituation}:${hostName}:${tipCrnCname}:${tipCrnCtype}:${tipCrnLocation} alert - $eventName )
  tipLongDescription=$(echo Faye message bus is down for serivce: ${tipSituation}:${hostName}:${tipCrnCname}:${tipCrnCtype}:${tipCrnLocation}:${hostIP} alert - $eventName  Datails: runbook: ${tipRunbookUrl})
  tipTimestamp=`date +"%Y-%m-%d %H:%M:%S %z"`
  echo "{ \
   \"alert_id\": \"${incidentKey}\",  \
   \"alert_ui_url\": \"${tipAlertUiUrl}\", \
   \"crn\": {
    \"version\": \"${tipCrnVersion}\", \
    \"cname\": \"${tipCrnCname}\", \
    \"ctype\": \"${tipCrnCtype}\", \
    \"service_name\": \"${tipCrnServiceName}\", \
    \"location\": \"${tipCrnLocation}\", \
    \"scope\": \"${tipCrnScope}\", \
    \"service_instance\": \"${tipCrnServiceInstance}\", \
    \"resource_type\": \"${tipCrnResourceType}\", \
    \"resource\": \"${tipCrnResource}\" \
   }, \
    \"extras\": [\
      {\
        \"name\":\"disable_incident_management\",\
         \"value\":\"false\"\
      }\
    ],\
   \"console\": \"${tipConsole}\", \
   \"customer_impacting\": \"${tipCustomerImpacting}\", \
   \"disable_pager\": \"${tipDisablePager}\", \
   \"hostname\": \"${hostName}\", \
   \"ip\": \"${hostIP}\", \
   \"severity\": ${tipSeverity}, \
   \"source\": \"${tipSource}\", \
   \"situation\": \"${tipSituation}\", \
   \"short_description\": \"${tipShortDescription}\", \
   \"long_description\": \"${tipLongDescription}\", \
   \"runbook_toc_enabled\": \"${tipRunbookTocEnabled}\", \
   \"runbook_url\": \"${tipRunbookUrl}\", \
   \"timestamp\": \"${tipTimestamp}\", \
   \"tip_msg_type\": \"${tipTipMsgType}\", \
   \"tribe_name\": \"${tribeName}\", \
   \"version\": \"${tipVersion}\" \
 }" > $templateJSONFile
 logger "JSON template file : $templateJSONFile"
 logger "<<< create_json_template"
}
send_message_to_webhooks(){
  logger ">>> sending_to_webhook"
  echo  "(curl -s -o /dev/null -w '%{http_code}' -H "X-Auth-Token: ${1}" -H "Content-Type: application/json" -X POST -d @$2 $3)"
  logger "(curl -s -o /dev/null -w '%{http_code}' -H "X-Auth-Token: ${1}" -H "Content-Type: application/json" -X POST -d @$2 $3)" "$(date)"
  STATUS=$(curl -s -o /dev/null -w '%{http_code}' -H "X-Auth-Token: $1" -H "Content-Type: application/json" -X POST -d @$2 $3)
  if  [ $STATUS -eq 200 ]; then
    echo "Event: '$eventName' with type $tipTipMsgType was sent successfully. :)"
    logger "Event: '$eventName' with type $tipTipMsgType was sent successfully. :)"
    if [  $tipTipMsgType = $CLOSE_NOTICE ]; then
      rm -f $templateJSONFile
    fi
  else
    echo "Failed to sent '$eventName' with type $tipTipMsgType status: $STATUS :("
    echo "Use -d and/or -v options to debug the problem"
    logger "Failed to sent '$eventName' with type $tipTipMsgType status: $STATUS :("
    exit 1
  fi
  logger "<<< sending_to_webhook"
}
is_valid_json() {
  # validate json file.
  logger ">>> is_valid_json"
  python -mjson.tool $1 > /dev/null
  if [[ $? -gt 0 ]];then
    echo "JSON validation failed. Check payload ${1} and try again :("
    logger "JSON validation failed. Check payload ${1} and try again :("
    exit 1
  fi
  logger "${1} is valid JSON file"
  logger "<<< is_valid_json"
}
function logger {
  if $debugMode ; then
      for var in "$@"; do
            echo -e "${var}"
            echo -e "${var}" >> $logFileName
          done
  fi
}
main() {
  parse_args "$@"
  if $verbose_flag ; then
    enable_expanded_output
  else
    disable_expanded_output
  fi
  logger "------------ Starting ${me} -----------------------" "$(date)"
  detect_and_verify
  get_json_file
  send_message_to_webhooks $tipToken $templateJSONFile $webHookUrl
  logger "------------ Ended ${me} --------------------------" "$(date)"
}
[[ $1 = --source-only ]] || main "$@"

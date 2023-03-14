#!/bin/bash

# exit on error
set -e

# declare an array of variable names
var_names=("BUCKET_NAME" "BUCKET_PREFIX")

# loop over the array and check each variable
for var_name in "${var_names[@]}"; do
  if [[ -v $var_name ]]; then
    # echo "$var_name found"
    echo ""
  else
    echo "$var_name does not exist"
    exit -1
  fi
done

# fetch logs from file and store in /elb-log-analyzer/logs/latest
## NOTE: DATE_SUFFIX can create issues
/usr/local/bin/python -m elb_log_analyzer.s3_log -b ${BUCKET_NAME} -p '${BUCKET_PREFIX}${DATE_SUFFIX}' -m ${LOG_ANALYSIS_INTERVAL} -o /elb-log-analyzer/logs/latest

# analyze logs
if [[ -v "REQUESTS_THRESHOLD" && -n ${REQUESTS_THRESHOLD} && -v "IP_ABUSE_DB_API_KEY" && -n ${IP_ABUSE_DB_API_KEY} ]]; then
    echo -e "[*] REQUESTS_THRESHOLD and API key found\n"
    /usr/local/bin/python -m elb_log_analyzer -i /elb-log-analyzer/logs/latest -o /elb-log-analyzer/analyzed_logs/log.json -t ${REQUESTS_THRESHOLD} -k ${IP_ABUSE_DB_API_KEY}
else
    echo -e "[!] REQUESTS_THRESHOLD and API key not found\n"
    /usr/local/bin/python -m elb_log_analyzer -i /elb-log-analyzer/logs/latest -o /elb-log-analyzer/analyzed_logs/log.json
fi

# send alert
if [[ -v "SLACK_WEBHOOK" && -n ${SLACK_WEBHOOK} ]]; then
    "[*] Sending IP details to slack"
    /usr/local/bin/python -m elb_log_analyzer.alerts -w ${SLACK_WEBHOOK} -f log.json
else
    echo -e "[!] SLACK_WEBHOOK var not found. Skipping Alert.\n"
fi

# move analyzed log files
mv /elb-log-analyzer/logs/latest/* /elb-log-analyzr/logs/

# mv analyzed file 
mv /elb-log-analyzer/analyzed_logs/log.json /elb-log-analyzer/analyzed_logs/log-$(date +%Y-%m-%d-%H_%M_%S).json
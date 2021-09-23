# Delete ansible logs older than two weeks
find "/opt/ansible/logs/" -name "*.stderr" -type f -mtime +14 -exec rm -r {} \; &
find "/opt/ansible/logs/" -name "*.stdout" -type f -mtime +14 -exec rm -r {} \; &
find "/opt/ansible/logs/" -name "*.log" -type f -mtime +14 -exec rm -r {} \; &

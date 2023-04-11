#!/bin/bash
# Issue: https://access.redhat.com/solutions/4620671
proxy="http://proxy.ar:8080"
slackurl="https://hooks.slack.com/services/TM2JFRK5F/B01JGJ2SFA5/ASLJKWJelvAksdO3Df"
crontablog="/home/openshift/crontab.log"
send_slack ()
{
  image_error="http://i.imgur.com/LUveOg7.gif"
  svg="https://github.com/odb/official-bash-logo/blob/master/assets/Logos/Icons/SVG/BASH_logo-transparent-bg-bw-02.svg"
  hostname="$(hostname)"
  logs="$(tail $crontablog)"
  payload="{\"text\": \"Cronjob: Argument list too long failed at $(hostname)\\nLast 15 lines of log: \", \"attachments\":[{\"text\": \"${logs}\"}]}"
  curl -X POST -H 'Content-type: application/json' --data "${payload}" ${slackurl} -x ${proxy}
}

main ()
{
  for i in infras workers ; do
    timeout 60 ansible ${i} -m shell -a "sudo systemctl list-units --all | wc -l;sudo systemctl daemon-reload; sudo systemctl list-units --all |wc -l" >> $crontablog
    if [ $? -gt 0  ] ; then
      send_slack
    else
      echo "" > $crontablog
    fi
  done
}
main $@
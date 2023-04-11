#!/bin/bash
STATUS=Success
EXIT=0
EMOJI=✅
CODEPIPELINE_URL="https://us-east-2.console.aws.amazon.com/codesuite/codepipeline/pipelines/$ORGANIZATION-$STAGE-$REPOSITORY_NAME/view?region=us-east-2"
ELASTIC_DNS="deploy.elastic-cloud.com"

if [ -z "$TAG" ] || [ -z "$STAGE" ]; then
  echo "[ERROR] Required enviroment variables at missing"
  exit 1
else
  echo "Deploying $REPOSITORY_NAME to $STAGE..."
fi

helm upgrade $REPOSITORY_NAME --install --create-namespace --values=values.yaml \
--namespace $REPOSITORY_NAME-$STAGE \
--set escloud.url=$ELASTIC_URL --set escloud.token=$ELASTIC_TOKEN \
--set app.name=$REPOSITORY_NAME --set app.image.repository=$REPOSITORY_URI --set app.version=$TAG --set app.env=$STAGE \
--set op.group=$OP_GROUP \
--wait --timeout 10m $ORGANIZATION-ms-prod/

if [ "$?" -ne "0" ]
then
  POD=$(kubectl get pods -n $REPOSITORY_NAME-$STAGE --sort-by=.status.startTime | tail -1 | awk '{print $1}')
  if [ ${#POD} -gt 1 ]
  then
    printf "\nMaybe this would help...\n"
    echo "Copy & Paste Elasticsearch link: https://$ELASTIC_DNS:9243/app/discover#/?_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-15m,to:now))&_a=(columns:!(),filters:!(),index:'logs-*',interval:auto,query:(language:kuery,query:'kubernetes.pod.name%20:%20%22$POD%22%20'),sort:!(!('@timestamp',desc)))"
    printf "\n****************** Kubernetes Last Pod Logs \"--tail=50\" ******************\n"
    kubectl -n $REPOSITORY_NAME-$STAGE logs $POD --tail=50
  fi
  STATUS=Failed
  EXIT=1
  EMOJI=❌
fi

if [ ${#WEBHOOK_URL} -ge 1 ]
then
  curl -s -X POST -H 'Content-type: application/json' \
  --data '{"cards":[{"header":{"title":"Devops Bot","subtitle":"devops@organization.com","imageUrl":"https://www.clipartmax.com/png/small/195-1955059_what-is-aws-cloud-practitioner-certification-amazon-web-services-icon.png"},"sections":[{"widgets":[{"keyValue":{"topLabel":"Deployment","content":"'$TAG'"}},{"keyValue":{"topLabel":"Status","content":"'$EMOJI' '$STATUS'"}}]},{"widgets":[{"buttons":[{"textButton":{"text":"OPEN CODEPIPELINE","onClick":{"openLink":{"url":"'$CODEPIPELINE_URL'"}}}}]}]}]}]}' \
  $WEBHOOK_URL &>/dev/null
  printf "\nNotification sended"
fi

exit $EXIT
#!/bin/bash

set -e

prefix=${1:-some-prefix}

pipelines=$(aws codepipeline list-pipelines --query "pipelines[?starts_with(name, '${prefix}')].name" --output text)

echo "Starting pipelines with prefix '${prefix}':"

echo "$pipelines" | while read -r pipeline; do
  echo "Starting pipeline ${pipeline}..."
  if aws codepipeline start-pipeline-execution --name "${pipeline}"; then
    echo "Pipeline ${pipeline} started successfully."
  else
    echo "Failed to start pipeline ${pipeline}."
  fi
done

echo "All pipelines with prefix '${prefix}' started."

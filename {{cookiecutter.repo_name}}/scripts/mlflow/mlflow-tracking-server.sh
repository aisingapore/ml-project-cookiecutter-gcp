#!/bin/bash -x

if [[ -z "${ARTIFACT_URL}" ]]; then
    export ARTIFACT_URL="mlruns"
fi

if [[ -z "${DATABASE_URL}" ]]; then
    export DATABASE_URL="./mlruns"
fi

exec mlflow server --backend-store-uri=$DATABASE_URL --default-artifact-root=$ARTIFACT_URL

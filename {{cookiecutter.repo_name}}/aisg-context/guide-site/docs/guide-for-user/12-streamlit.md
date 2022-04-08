<!-- omit in toc -->
# Streamlit

There are 4 main ways we recommend when spinning up a Streamlit
application for quick dashboarding:

- [Local Execution](#local-execution)
- [Docker Container](#docker-container)
- [Integration with Polyaxon](#integration-with-polyaxon)
- [Native Kubernetes Deployment (GKE)](#native-kubernetes-deployment-gke)

The Streamlit demo created in this guide will accept a string as an
input, and the dashboard will provide an output as to whether the
sentiment is "positive" or "negative", following the
[guide's problem statement](02-preface.md#guides-problem-statement).

This guide will be similar to that of ["Deployment"](08-deployment.md)
and ["Batch Inferencing"](09-batch-inferencing.md), with the difference
mainly being the use of Streamlit as an interface
to get your inputs and show your outputs from.

While it is possible for Streamlit to interact with the FastAPI
deployment backend as a frontend engine/interface,
we would only focus on interacting with the model
directly after downloading from GCS for simplicities' sake. For small
scale infrastructure, this would be better in terms of simplicity and
efficiency. Otherwise, if big scalability is a factor, then consider
the other method.

This template provides:

- a Python script (`src/streamlit.py`)
- a Dockerfile for containerised executions
  (`docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile`)
- a Polyaxon config file for spinning up a Streamlit service
  (`aisg-context/polyaxon/polyaxonfiles/streamlit.yml`)

## Local Execution

To run the Streamlit app locally, one of course has to download a
predictive model into the local machine:

=== "Linux/macOS"

    ```bash
    $ export PRED_MODEL_UUID="<MLFLOW_EXPERIMENT_UUID>"
    $ export PRED_MODEL_GCS_URI="gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/$PRED_MODEL_UUID"
    $ gsutil cp -r $PRED_MODEL_GCS_URI ./models
    ```

=== "Windows PowerShell"

    ```powershell
    $ $Env:PRED_MODEL_UUID='<MLFLOW_EXPERIMENT_UUID>'
    $ $PRED_MODEL_GCS_URI="gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/$Env:PRED_MODEL_UUID"
    $ gsutil cp -r $PRED_MODEL_GCS_URI .\models
    ```

`PRED_MODEL_UUID` is the unique ID associated with the MLFLow run
that generated the predictive model to be used for dashboarding.

Spin up the Streamlit application locally:

=== "Linux/macOS"

    ```bash
    $ export PRED_MODEL_PATH="$PWD/models/$PRED_MODEL_UUID/artifacts/model/data/model"
    $ streamlit run src/streamlit.py -- \
        hydra.run.dir=. hydra.output_subdir=null hydra/job_logging=disabled \
        inference.model_path=$PRED_MODEL_PATH
    ```

=== "Windows PowerShell"

    ```powershell
    $ $Env:PRED_MODEL_PATH="$(Get-Location)\models\$Env:PRED_MODEL_UUID\artifacts\model\data\model"
    $ streamlit run src/streamlit.py -- `
        hydra.run.dir=. hydra.output_subdir=null hydra/job_logging=disabled `
        inference.model_path=$Env:PRED_MODEL_PATH
    ```

__Reference(s):__

- [Streamlit Docs - Run Streamlit apps](https://docs.streamlit.io/library/advanced-features/configuration#run-streamlit-apps)

## Docker Container

To use the Docker image, first build it:

=== "Linux/macOS"

    ```bash
    $ docker build \
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0 \
        --build-arg PRED_MODEL_UUID="$PRED_MODEL_UUID" \
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile \
        --platform linux/amd64.
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker build `
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0 `
        --build-arg PRED_MODEL_UUID="$Env:PRED_MODEL_UUID" `
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile .
    ```

After building the image, you can run the container like so:

=== "Linux/macOS"

    ```bash
    $ chgrp -R 2222 outputs
    $ docker run --rm -p 8501:8501 \
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json \
        -v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json \
        -v $PWD/models:/home/aisg/from-gcs \
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker run --rm -p 8501:8501 `
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json `
        -v "<PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json" `
        -v "$(Get-Location)\models:/home/aisg/from-gcs" `
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
    ```

- `GOOGLE_APPLICATION_CREDENTIALS` allows the container's entrypoint to
  download the predictive model specified during build time from GCS.
- `-v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json`
  attaches the JSON file for the service account credentials to the
  Docker container.
- `-v $PWD/models:/home/aisg/from-gcs` allows the models downloaded to
  the host machine to be used by the container after being mounted to
  `/home/aisg/from-gcs`.

## Integration with Polyaxon

From the Docker build section, push the Docker image to GCR:

```bash
$ docker push asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
```

Then, push the configurations to the Polyaxon server to start up the
Streamlit dashboard:

```bash
$ polyaxon run \
  -f aisg-context/polyaxon/polyaxonfiles/streamlit-service.yml \
  -P DOCKER_IMAGE="asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0" \
  -P WORKING_DIR="/polyaxon-v1-data" \
  -p {{cookiecutter.repo_name}}-<YOUR_NAME>
```

__Reference(s):__

- [Polyaxon - Integrations](https://polyaxon.com/integrations/streamlit/)

## Native Kubernetes Deployment (GKE)

Similar to deploying [the FastAPI server](08-deployment.md#deploy-to-gke),
to deploy the Streamlit dashboard on GKE, you can make use of the
sample Kubernetes manifest files provided with this template:

```bash
$ kubectl apply \
  -f aisg-context/k8s/dashboard/streamlit-deployment.yml \
  --namespace=polyaxon-v1
$ kubectl apply \
  -f aisg-context/k8s/dashboard/streamlit-service.yml \
  --namespace=polyaxon-v1
```

To access the server, you can port-forward the service to a local port
like such:

```bash
$ kubectl port-forward service/streamlit-svc 8501:8501 --namespace=polyaxon-v1
Forwarding from 127.0.0.1:8501 -> 8501
Forwarding from [::1]:8501 -> 8501
```

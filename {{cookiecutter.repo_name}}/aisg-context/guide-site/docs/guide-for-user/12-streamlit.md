<!-- omit in toc -->
# Streamlit

There are 4 main ways we recommend to spin up Streamlit
applications for quick dashboarding:

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
for simplicities' sake,
we will only dealing with the use case where
Streamlit application directly loads the predictive model downloaded
from GCS. For small scale infrastructure or prototyping,
this would be sufficient in terms of simplicity and efficiency.

This template provides:

- a Python script (`src/streamlit.py`)
- a Dockerfile for containerised executions
  (`docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile`)
- a Polyaxon config file for spinning up a Streamlit service
  (`aisg-context/polyaxon/polyaxonfiles/streamlit.yml`)

## Local Execution

To run the Streamlit app locally, one of course has to download a
predictive model into the local machine:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
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
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    $ export PRED_MODEL_UUID="<MLFLOW_EXPERIMENT_UUID>"
    $ export PRED_MODEL_GCS_URI="gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/{{cookiecutter.author_name}}/$PRED_MODEL_UUID"
    $ gsutil cp -r $PRED_MODEL_GCS_URI ./models
    ```

=== "Windows PowerShell"

    ```powershell
    $ $Env:PRED_MODEL_UUID='<MLFLOW_EXPERIMENT_UUID>'
    $ $PRED_MODEL_GCS_URI="gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/{{cookiecutter.author_name}}/$Env:PRED_MODEL_UUID"
    $ gsutil cp -r $PRED_MODEL_GCS_URI .\models
    ```
{% endif %}
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

The application would look like the screenshot below:

![Streamlit App - Local Execution](../assets/screenshots/streamlit-app-local-exec.png)

__Reference(s):__

- [Streamlit Docs - Run Streamlit apps](https://docs.streamlit.io/library/advanced-features/configuration#run-streamlit-apps)

## Docker Container

To use the Docker image, first build it:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Linux/macOS"

    ```bash
    $ docker build \
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0 \
        --build-arg PRED_MODEL_UUID="$PRED_MODEL_UUID" \
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker build `
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0 `
        --build-arg PRED_MODEL_UUID="$Env:PRED_MODEL_UUID" `
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile `
        --platform linux/amd64 .
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    $ docker build \
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0 \
        --build-arg PRED_MODEL_UUID="$PRED_MODEL_UUID" \
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker build `
        -t asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0 `
        --build-arg PRED_MODEL_UUID="$Env:PRED_MODEL_UUID" `
        -f docker/{{cookiecutter.repo_name}}-streamlit.Dockerfile `
        --platform linux/amd64 .
    ```
{% endif %}
After building the image, you can run the container like so:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Linux/macOS"

    ```bash
    $ sudo chgrp -R 2222 outputs
    $ docker run --rm -p 8501:8501 \
        --name streamlit-app \
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json \
        -v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json \
        -v $PWD/models:/home/aisg/from-gcs \
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker run --rm -p 8501:8501 `
        --name streamlit-app `
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json `
        -v "<PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json" `
        -v "$(Get-Location)\models:/home/aisg/from-gcs" `
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    $ sudo chgrp -R 2222 outputs
    $ docker run --rm -p 8501:8501 \
        --name streamlit-app \
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json \
        -v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json \
        -v $PWD/models:/home/aisg/from-gcs \
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker run --rm -p 8501:8501 `
        --name streamlit-app `
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json `
        -v "<PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json" `
        -v "$(Get-Location)\models:/home/aisg/from-gcs" `
        asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0
    ```
{% endif %}
- `GOOGLE_APPLICATION_CREDENTIALS` allows the container's entrypoint to
  download the predictive model specified during build time from GCS.
- `-v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json`
  attaches the JSON file for the service account credentials to the
  Docker container.
- `-v $PWD/models:/home/aisg/from-gcs` allows the models downloaded to
  the host machine to be used by the container after being mounted to
  `/home/aisg/from-gcs`.

To stop the container:

```bash
$ docker container stop streamlit-app
```

## Integration with Polyaxon

!!! attention

    As this mode of deployment would take up resources in a
    long-running manner, please tear the service down through
    the dashboard once you've gone through this part of the guide.

From the Docker build section, push the Docker image to GCR:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
```bash
$ docker push asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0
```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
```bash
$ docker push asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0
```
{% endif %}
Then, push the configurations to the Polyaxon server to start up the
Streamlit dashboard:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Linux/macOS"

    ```bash
    $ polyaxon run \
      -f aisg-context/polyaxon/polyaxonfiles/streamlit-service.yml \
      -P DOCKER_IMAGE="asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0" \
      -p {{cookiecutter.repo_name}}-<YOUR_NAME>
    ```

=== "Windows PowerShell"

    ```powershell
    $ polyaxon run `
      -f aisg-context/polyaxon/polyaxonfiles/streamlit-service.yml `
      -P DOCKER_IMAGE="asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit:0.1.0" `
      -p {{cookiecutter.repo_name}}-<YOUR_NAME>
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    $ polyaxon run \
      -f aisg-context/polyaxon/polyaxonfiles/streamlit-service.yml \
      -P DOCKER_IMAGE="asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0" \
      -p {{cookiecutter.repo_name}}-<YOUR_NAME>
    ```

=== "Windows PowerShell"

    ```powershell
    $ polyaxon run `
      -f aisg-context/polyaxon/polyaxonfiles/streamlit-service.yml `
      -P DOCKER_IMAGE="asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit:0.1.0" `
      -p {{cookiecutter.repo_name}}-<YOUR_NAME>
    ```
{% endif %}
Just like with the VSCode or JupyterLab services, you can access
the Streamlit service you've just spun up through the Polyaxon
dashboard:

![Streamlit App - Polyaxon Service](../assets/screenshots/streamlit-app-poly-service.png)

__Reference(s):__

- [Polyaxon - Integrations](https://polyaxon.com/integrations/streamlit/)

## Native Kubernetes Deployment (GKE)

!!! attention

    As this mode of deployment would take up resources in a
    long-running manner, please tear it down once you've
    gone through this part of the guide. If you do not have the right
    permissions, please request assistance from your team lead or the
    administrators.

Similar to deploying [the FastAPI server](08-deployment.md#deploy-to-gke),
to deploy the Streamlit dashboard on GKE, you can make use of the
sample Kubernetes manifest files provided with this template:

```bash
$ kubectl apply -f aisg-context/k8s/dashboard/streamlit-deployment.yml --namespace=polyaxon-v1
$ kubectl apply -f aisg-context/k8s/dashboard/streamlit-service.yml --namespace=polyaxon-v1
```

To access the server, you can port-forward the service to a local port
like such:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Local Machine"

    ```bash
    $ kubectl port-forward service/streamlit-svc 8501:8501 --namespace=polyaxon-v1
    Forwarding from 127.0.0.1:8501 -> 8501
    Forwarding from [::1]:8501 -> 8501
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Local Machine"

    ```bash
    $ kubectl port-forward service/streamlit-{{cookiecutter.author_name.replace('_', '-')}}-svc 8501:8501 --namespace=polyaxon-v1
    Forwarding from 127.0.0.1:8501 -> 8501
    Forwarding from [::1]:8501 -> 8501
    ```
{% endif %}
!!! attention

    Please tear down the deployment and service objects once they are
    not required.
    {% if cookiecutter.gcr_personal_subdir == 'No' %}
    === "Local Machine"

        ```bash
        $ kubectl delete streamlit-deployment --namespace=polyaxon-v1
        $ kubectl delete streamlit-svc --namespace=polyaxon-v1
        ```
    {% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
    === "Local Machine"

        ```bash
        $ kubectl delete streamlit-{{cookiecutter.author_name.replace('_', '-')}}-deployment --namespace=polyaxon-v1
        $ kubectl delete streamlit-{{cookiecutter.author_name.replace('_', '-')}}-svc --namespace=polyaxon-v1
        ```
    {% endif %}
    If you do not have the right
    permissions, please request assistance from your team lead or the
    administrators.

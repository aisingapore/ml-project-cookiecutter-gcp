# Deployment

Assuming we have a predictive model that we are satisfied with, we can
serve it within a REST API service with which requests can be made to
and predictions are returned.

Python has plenty of web frameworks that we can leverage on to build
our REST API. Popular examples include
[Flask](https://flask.palletsprojects.com/en/2.0.x/),
[Django](https://www.djangoproject.com/) and
[Starlette](https://www.starlette.io/). For this guide however, we will
resort to the well-known [FastAPI](https://fastapi.tiangolo.com/)
(which is based on Starlette itself).

__Reference(s):__

- [IBM Technology - What is a REST API? (Video)](https://www.youtube.com/watch?v=lsMQRaeKNDk)

## Model Artifacts

Seen in
["Model Training"](./07-job-orchestration.md#model-training)
, we have the trained models
uploaded to GCS through the MLflow Tracking server (done through
autolog). With that, we have the following pointers to take note of:

- By default, each MLflow experiment run is given a unique ID.
- When artifacts are uploaded to GCS through MLflow,
  the artifacts are located within directories named after the
  unique IDs of the runs.
{% if cookiecutter.gcr_personal_subdir == 'No' %}
- This guide by default uploads your artifacts to the following
  directory on GCS:
  `gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server`.
- Artifacts for specific runs will be uploaded to a directory with a
  convention similar to the following:
  `gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/<MLFLOW_EXPERIMENT_UUID>`.
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
- This guide by default uploads your artifacts to the following
  directory on GCS:
  `gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/{{cookiecutter.author_name}}`.
- Artifacts for specific runs will be uploaded to a directory with a
  convention similar to the following:
  `gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/{{cookiecutter.author_name}}/<MLFLOW_EXPERIMENT_UUID>`.
{% endif %}
- With this path/URI, we can use
  [`gsutil`](https://cloud.google.com/storage/docs/gsutil)
  to download the predictive model from GCS into a mounted volume when
  we run the Docker image for the REST APIs.

Now that we have established on how we are to obtain the models for the
API server, let's look into the servers themselves.

## Model Serving (FastAPI)

FastAPI is a web framework that has garnered much popularity in recent
years due to ease of adoption with its comprehensive tutorials, type
and schema validation, being async capable and having automated docs,
among other things. These factors have made it a popular framework
within AI Singapore across many projects.

If you were to inspect the `src` folder, you would notice that there
exist more than one package:

- `{{cookiecutter.src_package_name}}`
- `{{cookiecutter.src_package_name}}_fastapi`

The former contains the modules for
executing pipelines like data preparation and model training while
the latter is dedicated to modules meant for the REST API. Regardless,
the packages can be imported by each other.


!!! note
    It is recommended that you grasp some basics of the FastAPI
    framework, up till the
    [beginner tutorials](https://fastapi.tiangolo.com/tutorial/) for
    better understanding of this section.

Let's try running the boilerplate API server on a local machine.
Before doing that, identify from the MLflow dashboard the unique ID
of the experiment run that resulted in the predictive model that you
would like to serve.

![MLflow - Dashboard Run View](../assets/screenshots/mlflow-dashboard-run-view.png)

With reference to the example screenshot above, the UUID for
the experiment run is `7251ac3655934299aad4cfebf5ffddbe`.
Once the ID of the MLflow run has been obtained,
let's download the model that we intend to serve.
Assuming you're in the root of this template's repository, execute the
following commands:
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
Executing the commands above will download the artifacts related to the
experiment run `<MLFLOW_EXPERIMENT_UUID>` to this repository's
subdirectory `models`.
However, the specific subdirectory that is relevant for TensorFlow
to load will be
`./models/<MLFLOW_EXPERIMENT_UUID>/artifacts/model/data/model`.
Let's export this path to an environment variable:

!!! note
    See
    [here](https://www.tensorflow.org/tutorials/keras/save_and_load#savedmodel_format)
    for more information on the `SavedModel` format that TensorFlow
    uses for exporting trained models through the function call
    `model.save`.

=== "Linux/macOS"

    ```bash
    $ export PRED_MODEL_PATH="$PWD/models/$PRED_MODEL_UUID/artifacts/model/data/model"
    ```

=== "Windows PowerShell"

    ```powershell
    $ $Env:PRED_MODEL_PATH="$(Get-Location)\models\$Env:PRED_MODEL_UUID\artifacts\model\data\model"
    ```
### Local Server

Run the FastAPI server using [Gunicorn](https://gunicorn.org)
(for Linux/macOS) or [`uvicorn`](https://www.uvicorn.org/)
(for Windows):

!!! attention
    Gunicorn is only executable on UNIX-based or UNIX-like systems,
    this method would not be possible/applicable for
    Windows machine.

=== "Linux/macOS"

    ```bash
    $ conda activate {{cookiecutter.repo_name}}
    $ cd src
    $ gunicorn {{cookiecutter.src_package_name}}_fastapi.main:APP -b 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornWorker
    ```

    See
    [here](https://fastapi.tiangolo.com/deployment/server-workers/) as to
    why Gunicorn is to be used instead of just
    [Uvicorn](https://www.uvicorn.org/). TLDR: Gunicorn is needed to spin
    up multiple processes/workers to handle more requests i.e. better for
    the sake of production needs.

=== "Windows PowerShell"

    ```powershell
    $ conda activate {{cookiecutter.repo_name}}
    $ cd src
    $ uvicorn {{cookiecutter.src_package_name}}_fastapi.main:APP
    ```

In another terminal, use the `curl` command to submit a request to the API:

=== "Linux/macOS"

    ```bash
    $ curl -H 'Content-Type: application/json' -H 'accept: application/json' \
        -X POST -d '{"reviews": [{"id": 9176, "text": "This movie is quite boring."}, {"id": 71, "text": "This movie is awesome."}]}' \
      localhost:8080/api/v1/model/predict
    ```

=== "Windows PowerShell"

    ```powershell
    $ curl.exe '-H', 'Content-Type: application/json', '-H', 'accept: application/json', `
        '-X', 'POST', '-d', `
        '{\"reviews\": [{\"id\": 9176, \"text\": \"This movie is quite boring.\"}, {\"id\": 71, \"text\": \"This movie is awesome.\"}]}', `
        'localhost:8000/api/v1/model/predict'
    ```

With the returned JSON object, we have successfully submitted a request
to the FastAPI server and it returned predictions as part of the
response.

### Pydantic Settings

Now you might be wondering, how does the FastAPI server knows the path
to the model for it to load? FastAPI utilises
[Pydantic](https://pydantic-docs.helpmanual.io/), a library for data
and schema validation, as well as
[settings management](https://fastapi.tiangolo.com/advanced/settings/?h=env#pydantic-settings).
There's a class
called `Settings` under the module
`src/{{cookiecutter.src_package_name}}_fastapi/config.py`. This class contains
several fields: some are defined and some others not. The fields
`PRED_MODEL_UUID` and `PRED_MODEL_PATH` inherit their values from
the environment variables.

`src/{{cookiecutter.src_package_name}}_fastapi/config.py`:
```python
...
class Settings(pydantic.BaseSettings):

    API_NAME: str = "{{cookiecutter.src_package_name}}_fastapi"
    API_V1_STR: str = "/api/v1"
    LOGGER_CONFIG_PATH: str = "../conf/base/logging.yml"

    PRED_MODEL_UUID: str
    PRED_MODEL_PATH: str
...
```

FastAPI automatically generates interactive API documentation for
easy viewing of all the routers/endpoints you have made available for
the server. You can view the documentation through
`<API_SERVER_URL>:<PORT>/docs`. In our case here, it is viewable through
[`localhost:8080/docs`](http://localhost:8080/docs). It will look like
such:

![FastAPI - OpenAPI Docs](../assets/screenshots/fastapi-openapi-docs.png)

### Docker Container

We now look into packaging the server within a Docker image. This
process of containerising the server isn't just for the sake of
reproducibility but it makes it easier for the server to be deployed
on any server/infrastructure that can run a Docker container.
A boilerplate
Dockerfile is provided to containerise the FastAPI server:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Linux/macOS"

    ```bash
    $ export GCP_PROJECT_ID={{cookiecutter.gcp_project_id}}
    # Ensure that you are in the root of the repository
    $ docker build \
        -t asia.gcr.io/$GCP_PROJECT_ID/fastapi-server:0.1.0 \
        --build-arg PRED_MODEL_UUID="$PRED_MODEL_UUID" \
        -f docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    $ $GCP_PROJECT_ID='{{cookiecutter.gcp_project_id}}'
    # Ensure that you are in the root of the repository
    $ docker build `
        -t asia.gcr.io/$GCP_PROJECT_ID/fastapi-server:0.1.0 `
        --build-arg PRED_MODEL_UUID="$Env:PRED_MODEL_UUID" `
        -f docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile `
        --platform linux/amd64 .
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    $ export GCP_PROJECT_ID={{cookiecutter.gcp_project_id}}
    # Ensure that you are in the root of the repository
    $ docker build \
        -t asia.gcr.io/$GCP_PROJECT_ID/{{cookiecutter.author_name}}/fastapi-server:0.1.0 \
        --build-arg PRED_MODEL_UUID="$PRED_MODEL_UUID" \
        -f docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile \
        --platform linux/amd64 .
    ```

=== "Windows PowerShell"

    ```powershell
    $ $GCP_PROJECT_ID='{{cookiecutter.gcp_project_id}}'
    # Ensure that you are in the root of the repository
    $ docker build `
        -t asia.gcr.io/$GCP_PROJECT_ID/{{cookiecutter.author_name}}/fastapi-server:0.1.0 `
        --build-arg PRED_MODEL_UUID="$Env:PRED_MODEL_UUID" `
        -f docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile `
        --platform linux/amd64 .
    ```
{% endif %}
The Docker build command above requires an argument to be passed and it
is basically the same unique MLflow run ID that was used above.
The ID would then be used to create environment variables that would
persist beyond the build time. When the container is being run,
these environment variables would be
used by the entrypoint script
(`scripts/fastapi/api-entrypoint.sh`)
to download the relevant predictive model
into the mounted volumes and be referred to by the FastAPI Pydantic
models.

Let's try running the Docker container now:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Linux/macOS"

    ```bash
    # First make the `models` folder accessible to user within Docker container
    $ sudo chgrp -R 2222 models
    $ docker run --rm -p 8080:8080 \
        --name fastapi-server \
        -v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json \
        -v $PWD/models:/home/aisg/from-gcs \
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json \
        asia.gcr.io/$GCP_PROJECT_ID/fastapi-server:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker run --rm -p 8080:8080 `
        --name fastapi-server `
        -v "<PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json" `
        -v "$(Get-Location)\models:/home/aisg/from-gcs" `
        --env GOOGLE_APPLICATION_CREDENTIALS="/var/secret/cloud.google.com/gcp-service-account.json" `
        asia.gcr.io/$GCP_PROJECT_ID/fastapi-server:0.1.0
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Linux/macOS"

    ```bash
    # First make the `models` folder accessible to user within Docker container
    $ sudo chgrp -R 2222 models
    $ docker run --rm -p 8080:8080 \
        --name fastapi-server \
        -v <PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json \
        -v $PWD/models:/home/aisg/from-gcs \
        --env GOOGLE_APPLICATION_CREDENTIALS=/var/secret/cloud.google.com/gcp-service-account.json \
        asia.gcr.io/$GCP_PROJECT_ID/{{cookiecutter.author_name}}/fastapi-server:0.1.0
    ```

=== "Windows PowerShell"

    ```powershell
    $ docker run --rm -p 8080:8080 `
        --name fastapi-server `
        -v "<PATH_TO_SA_JSON_FILE>:/var/secret/cloud.google.com/gcp-service-account.json" `
        -v "$(Get-Location)\models:/home/aisg/from-gcs" `
        --env GOOGLE_APPLICATION_CREDENTIALS="/var/secret/cloud.google.com/gcp-service-account.json" `
        asia.gcr.io/$GCP_PROJECT_ID/{{cookiecutter.author_name}}/fastapi-server:0.1.0
    ```
{% endif %}
Let's go through a couple of the flags used above:

- `--rm`: Automatically stops the container when it exits or when you
  stop it.
- `-p`: This binds port `8080` of the container to port `8080` of the
  host machine.
- `-v`: Bind mounts files or directories from the host machine to the
  container. In this case, we are mounting the SA file and the `models`
  folder to the container. The SA file is needed for `gsutil`
  to download the model from GCS and the `models` folder will persist
  the downloaded models.
- `--env`: This sets environment variables within the container.

Use the same `curl` command for the server spun up by the container:

=== "Linux/macOS"

    ```bash
    $ curl -H 'Content-Type: application/json' -H 'accept: application/json' \
        -X POST -d '{"reviews": [{"id": 9176, "text": "This movie is quite boring."}, {"id": 71, "text": "This movie is awesome."}]}' \
        localhost:8080/api/v1/model/predict
    ```

=== "Windows PowerShell"

    ```powershell
    $ curl.exe '-H', 'Content-Type: application/json', '-H', 'accept: application/json', `
        '-X', 'POST', '-d', `
        '{\"reviews\": [{\"id\": 9176, \"text\": \"This movie is quite boring.\"}, {\"id\": 71, \"text\": \"This movie is awesome.\"}]}', `
        'localhost:8080/api/v1/model/predict'
    ```

To stop the container:

```bash
$ docker container stop fastapi-server
```

Push the Docker image to the GCR:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
```bash
$ docker push asia.gcr.io/$GCP_PROJECT_ID/fastapi-server:0.1.0
```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
```bash
$ docker push asia.gcr.io/$GCP_PROJECT_ID/{{cookiecutter.author_name}}/fastapi-server:0.1.0
```
{% endif %}
With this Docker image, you can spin up a VM (Compute Engine instance)
that has Docker installed and run the container on it for deployment.
You can also deploy the image within a Kubernetes cluster for ease of
scaling.

### Deploy to GKE

!!! warning

    As this mode of deployment would take up resources in a
    long-running manner, please tear it down once you've
    gone through this part of the guide. If you do not have the right
    permissions, please request assistance from your team lead or the
    administrators.

To deploy the FastAPI server on GKE, you can make use of the sample
Kubernetes manifest files provided with this template:

=== "Local Machine"

    ```bash
    $ kubectl apply -f aisg-context/k8s/model-serving-api/fastapi-server-deployment.yml --namespace=polyaxon-v1
    $ kubectl apply -f aisg-context/k8s/model-serving-api/fastapi-server-service.yml --namespace=polyaxon-v1
    ```

To access the server, you can port-forward the service to a local port
like such:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "Local Machine"

    ```bash
    $ kubectl port-forward service/fastapi-server-svc 8080:8080 --namespace=polyaxon-v1
    Forwarding from 127.0.0.1:8080 -> 8080
    Forwarding from [::1]:8080 -> 8080
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "Local Machine"

    ```bash
    $ kubectl port-forward service/fastapi-server-{{cookiecutter.author_name.replace('_', '-')}}-svc 8080:8080 --namespace=polyaxon-v1
    Forwarding from 127.0.0.1:8080 -> 8080
    Forwarding from [::1]:8080 -> 8080
    ```
{% endif %}
You can view the documentation for the API at
[`http://localhost:8080/docs`](http://localhost:8080/docs). You can also
make a request to the API like so:

=== "Linux/macOS"

    ```bash
    $ curl -H 'Content-Type: application/json' -H 'accept: application/json' \
        -X POST -d '{"reviews": [{"id": 9176, "text": "This movie is quite boring."}, {"id": 71, "text": "This movie is awesome."}]}' \
        localhost:8080/api/v1/model/predict
    ```

=== "Windows PowerShell"

    ```powershell
    $ curl.exe '-H', 'Content-Type: application/json', '-H', 'accept: application/json', `
        '-X', 'POST', '-d', `
        '{\"reviews\": [{\"id\": 9176, \"text\": \"This movie is quite boring.\"}, {\"id\": 71, \"text\": \"This movie is awesome.\"}]}', `
        'localhost:8080/api/v1/model/predict'
    ```

!!! attention

    Please tear down the deployment and service objects once they are
    not required.
    {% if cookiecutter.gcr_personal_subdir == 'No' %}
    === "Local Machine"

        ```bash
        $ kubectl delete fastapi-server-deployment --namespace=polyaxon-v1
        $ kubectl delete fastapi-server-svc --namespace=polyaxon-v1
        ```
    {% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
    === "Local Machine"

        ```bash
        $ kubectl delete fastapi-server-{{cookiecutter.author_name.replace('_', '-')}}-deployment --namespace=polyaxon-v1
        $ kubectl delete fastapi-server-{{cookiecutter.author_name.replace('_', '-')}}-svc --namespace=polyaxon-v1
        ```
    {% endif %}
    If you do not have the right
    permissions, please request assistance from your team lead or the
    administrators.

__Reference(s):__

- [FastAPI Docs](https://fastapi.tiangolo.com)
- [Pydantic Docs - Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/)
- [TensorFlow Docs - `tf.keras.models.load_model`](https://www.tensorflow.org/api_docs/python/tf/keras/models/load_model)
- [`curl` tutorial](https://curl.se/docs/manual.html)
- [`docker run` Reference](https://docs.docker.com/engine/reference/commandline/run/)

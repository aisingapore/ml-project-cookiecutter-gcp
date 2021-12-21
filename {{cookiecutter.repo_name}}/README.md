# End-to-end Project Template (GCP)

Customised for {{cookiecutter.project_name}}.

{{cookiecutter.description}}

## Table of Contents

- [End-to-end Project Template (GCP)](#end-to-end-project-template-gcp)
  - [Table of Contents](#table-of-contents)
  - [Project Repo Tree](#project-repo-tree)
  - [Prerequisites](#prerequisites)
    - [NUS VPN](#nus-vpn)
  - [Preface](#preface)
    - [Repository Setup](#repository-setup)
    - [Guide's Problem Statement](#guides-problem-statement)
    - [Google Cloud Platform (GCP) Projects](#google-cloud-platform-gcp-projects)
      - [Authorisation](#authorisation)
  - [MLOps Components & Platform](#mlops-components--platform)
    - [Polyaxon](#polyaxon)
      - [Dashboard](#dashboard)
    - [Relevant Concepts](#relevant-concepts)
      - [Polyaxonfiles](#polyaxonfiles)
      - [Components](#components)
      - [Jobs](#jobs)
      - [Services](#services)
    - [Secrets & Credentials on Kubernetes](#secrets--credentials-on-kubernetes)
  - [Development Environment](#development-environment)
    - [VSCode](#vscode)
    - [Jupyter Lab](#jupyter-lab)
  - [Git Repository](#git-repository)
  - [Cloud SDK for Development Environment](#cloud-sdk-for-development-environment)
  - [Virtual Environment](#virtual-environment)
  - [Data Versioning](#data-versioning)
  - [Job Orchestration](#job-orchestration)
    - [Data Preparation](#data-preparation)
      - [Pulling Raw Data](#pulling-raw-data)
      - [Processing Data](#processing-data)
    - [Model Training](#model-training)
      - [Hyperparameter Tuning](#hyperparameter-tuning)
  - [Deployment](#deployment)
  - [Batch Inferencing](#batch-inferencing)
  - [Continuous Integration & Deployment](#continuous-integration--deployment)

## Project Repo Tree

```
{{cookiecutter.repo_name}}
    ├── {{cookiecutter.repo_name}}-conda-env.yml
    │                   ^-  The `conda` environment file for reproducing
    │                       the project's development environment.
    ├── LICENSE         <-  The license this repository is to be
    │                       respected under. Can be absent due to
    │                       omission upon generation of repository.
    ├── README.md       <-  The top-level README containing the basic
    │                       guide for using the repository.
    ├── .gitlab-ci.yml  <-  YAML file for configuring instructions for
    │                       GitLab CI/CD.
    ├── .dockerignore   <-  File for specifying files or directories
    │                       to be ignored by Docker contexts.
    ├── .pylintrc       <-  Configurations for `pylint`.
    ├── .gitignore      <-  File for specifying files or directories
    │                       to be ignored by Git.
    ├── aisg-context    <-  Folders containing files and assets relevant
    │   │                   for works within the context of AISG's
    │   │                   development environments.
    │   ├── code-server <-  Directory containing the entry point script
    │   │                   for the VSCode server's Docker image.
    │   │
    │   │
    │   └── polyaxon    <-  Specification files for services and jobs
    │                       to be executed by the Polyaxon server.
    ├── assets          <-  Screenshots and images.
    ├── conf            <-  Configuration files associated with the
    │                       various pipelines as well as for logging.
    ├── data            <-  The folder that is to contain the DVC files
    │                       of the project. Contents of folder will be
    │                       ignored except for `.dvc` and `.gitignore`
    │                       files.
    ├── docker          <-  Dockerfiles associated with the various
    │                       stages of the pipeline.
    ├── docs            <-  A default Sphinx project; see sphinx-doc.org
    │                       for details.
    ├── helm-charts     <-  Helm charts for the deployment to the
    │                       Kubernetes cluster.
    ├── models          <-  DVC files of trained and serialised models.
    ├── notebooks       <-  Jupyter notebooks. Naming convention is a
    │                       number (for ordering), the creator's
    │                       initials, and a short `-` delimited
    │                       description, e.g.
    │                       `1.0-jqp-initial-data-exploration`.
    ├── scripts         <-  Bash scripts for any parts of the pipelines.
    └── src             <-  Directory containing the source code and
        |                   packages for the project repository.
        |── {{cookiecutter.src_package_name}}
        |               ^-  Package containing modules for all pipelines
        |                   except deployment.
        |── {{cookiecutter.src_package_name}}_api
        |               ^-  Files associated with the deployment of
        |                   models as API.
        └── tests       <-  Directory containing tests for the
                            repository's packages.
```

Reference(s):

- [Dockerfile reference - `.dockerignore`](https://docs.docker.com/engine/reference/builder/#dockerignore-file)
- [Atlassian's Tutorial on `.gitignore`](https://www.atlassian.com/git/tutorials/saving-changes/gitignore)
- [GitLab CI/CD Quickstart](https://docs.gitlab.com/ee/ci/quick_start/)
- [`pylint` Docs - Command-line Arguments and Configuration Files](https://pylint.pycqa.org/en/latest/user_guide/ide-integration.html?highlight=pylintrc#command-line-arguments-and-configuration-files)

## Prerequisites

Aside from an internet connection, you would need the following to
follow through with the guide:

- NUS Staff/Student account
- Google account with `@aisingapore.org`/`@aiap.sg` domains provisioned
  by AI Singapore
- PC with the following installed:
  - Pulse Secure
    - Refer to [NUS IT eGuides](https://nusit.nus.edu.sg/eguides/)
      for installation guides.
  - Web browser
  - Terminal
  - Docker Engine
    - [System requirements for Windows](https://docs.docker.com/desktop/windows/install/)
  - [miniconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
    (recommended) or [Anaconda](https://docs.anaconda.com/anaconda/install/index.html)
  - [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
  - [kubectl](https://kubernetes.io/docs/tasks/tools/),
    CLI for Kubernetes
  - [Helm](https://helm.sh/docs/intro/install/),
    CLI for Kubernetes' package manager
  - [yq](https://github.com/mikefarah/yq), command-line YAML processor
- Access to a project on
  [Google Cloud Platform](https://console.cloud.google.com)

### NUS VPN

Your credentials for your NUS Staff/Student account is needed to
login to NUS' VPN for access to the following:

- AI Singapore's GitLab instance
- NUS resources

In order to interact with remote Git repositories situated on
AI Singapore's GitLab instance (clone, push, fetch, etc.)
outside of NUS' network or GCP (for regions `asia-southeast1` and
`us-central1`), you would need to login to NUS' VPN.

## Preface

### Repository Setup

This repository provides an end-to-end template for AI
Singapore's AI engineers to onboard their AI projects. This repository
was created using AI Singapore's
[`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/)
template located
[here](https://github.com/aimakerspace/ml-project-cookiecutter-gcp).

While this repository provides users with a set of boilerplates,
with this `README.md` document, you are presented with a linear guide on
how to use the boilerplates that are rendered when you generated this
repository using `cookiecutter`.
You can follow along the guide but it will be tackling a simple problem
statement.

Since we will be making use of this repository and the files
contained within it, __ensure that this repository is pushed to a
remote repository__. Refer to
[here](https://docs.gitlab.com/ee/user/project/working_with_projects.html#create-a-project)
on creating a blank remote repository (or project in GitLab's term).

```bash
$ git init
$ git remote add origin <REMOTE_URL>
$ git push -u origin
```

### Guide's Problem Statement

For this guide, we will work towards building a predictive model that is
able to conduct sentiment classification for movie reviews.
The model is then to be deployed through a REST API and used for batch
inferencing as well.
The raw dataset to be used is made available for you to download;
instructions are detailed [here](#data-preparation), to be referred
to later on.

### Google Cloud Platform (GCP) Projects

Each project in AI Singapore that requires the usage of GCP resources
would be provided with a
[GCP project](https://cloud.google.com/docs/overview#projects). Such
projects would be accessible through the
[GCP console](https://console.cloud.google.com/home) once you've logged
into your AI Singapore Google account. Projects are managed and
provisioned by AI Singapore's MLOps team. If you'd like to request for a
project to be created (or for any other enquiries as well), please
contact `mlops@aisingapore.org`.

#### Authorisation

You can use GCP's [Cloud SDK](https://cloud.google.com/sdk) to interact
with the varying GCP services.
When you're using the SDK for the first time,
you are to provide authorisation using a user or service account. In AI
Singapore's context, unless your use case concerns some automation or
CI/CD pipelines, you will probably be using your user account
(i.e. Google accounts with AI Singapore domains such as
`@aisingapore.org` or `@aiap.sg`).
See [here](https://cloud.google.com/sdk/docs/authorizing) for more
information on authorising your SDK.

A simple command to authorise access:

```bash
$ gcloud auth login
```

To register `gcloud` for Docker so you can push to
Google Container Registry:

```bash
$ gcloud auth configure-docker
```

With your user account, you should have access to the following GCP
products/services:

- [Kubernetes Engine (GKE)](https://cloud.google.com/kubernetes-engine)
- [Cloud Storage (GCS)](https://cloud.google.com/storage)
- [Container Registry (GCR)](https://cloud.google.com/container-registry)

## MLOps Components & Platform

A number of services and applications that you will be interacting with
(or deploying) are deployed (to be deployed) within a GKE cluster
environment. A GKE cluster should be set up upon creation of your GCP
project, viewable
[here](https://console.cloud.google.com/kubernetes/list/overview).
If this is not the case, please notify the MLOps team at
`mlops@aisingapore.org`.

Some of the MLOps components for which the GKE environment will be
relevant for are:

- Developer Workspace
- Model Experimentation
- Experiment Tracking
- Data/Artefact Storage
- Model Serving
- Model Monitoring

What this means is that AI engineers would need to be able to access the
GKE cluster. Documentation for obtaining a cluster's configuration can
be found
[here](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl#generate_kubeconfig_entry).

The following command can be executed to configure `kubectl` command
line access:

```bash
$ gcloud container clusters get-credentials <CLUSTER_NAME> --zone asia-southeast1-c --project <GCP_PROJECT_ID>
```

After obtaining the credentials and configurations for the GKE cluster,
you can start to interact with the main MLOps platforms tool that you
will be leveraging on for a development workspace, data preparation as
well as model training.

### Polyaxon

[Polyaxon](https://polyaxon.com) is an MLOps platform that provides a
suite of features for AI engineers to facilitate their end-to-end
machine learning workflows. The platform is to be deployed on a GKE
cluster; the Platforms and MLOps team would have set the platform up for
your team upon creation of the GCP project. AI engineers need not worry
about having to administer the platform as end-consumers of the
platform.

To verify if Polyaxon has been deployed on your GKE cluster, run the
following command:

```bash
$ helm list --namespace polyaxon-v1
NAME            NAMESPACE       REVISION        UPDATED                       STATUS          CHART           APP VERSION
polyaxon        polyaxon-v1     X               2021-XX-XX XX:XX:XX +0800 +08 deployed        polyaxon-1.11.3 1.11.3
```

An output similar to the one above should be returned.

#### Dashboard

Now, let's access the dashboard for Polyaxon. Before we can interact
with the platform, we have to install the Polyaxon CLI. This should
ideally be done within a virtual Python environment. You can
conveniently get the relevant libraries for this guide by executing the
following command:

```bash
$ conda env create -f {{cookiecutter.repo_name}}-conda-env.yml
```

At any point of time you would like __to interact with the Polyaxon
server, you would need port forwarding of the Polyaxon Kubernetes
service to your localhost__.
You can do port forwarding to a port on the localhost with
the Polyaxon CLI (we'll go ahead with the port `8888`):

```bash
$ polyaxon port-forward --port=8888 --namespace=polyaxon-v1 &
```

Open up a browser and head over to `localhost:8888`. You should see an
interface as such:

![Polyaxon v1 - Projects Dashboard](./assets/screenshots/polyaxon-v1-projects-dashboard.png)

Before we can create any services or run jobs on the platform, we have
to configure the host for the CLI and create a project within the
platform:

```bash
$ polyaxon config set --host=http://localhost:8888
$ polyaxon project create --name {{cookiecutter.repo_name}}-<YOUR_NAME>
```

After the command above, you should see a project with the name you've
specified above in the
[projects dashboard](http://localhost:8888/ui/orgs/default/projects).

__Reference(s):__

- [Ampersands & on the command line](https://bashitout.com/2013/05/18/Ampersands-on-the-command-line.html)

### Relevant Concepts

Before we proceed further, let's cover some basic concepts that one
should know when getting started with Polyaxon.

#### Polyaxonfiles

To submit jobs or spin up services on the Polyaxon platform, users would
have to make use of both the CLI as well as Polyaxon-specific config
files known as Polyaxonfiles. The CLI establishes communications and
connections with the Polyaxon server while Polyaxonfiles provide
specification to the server for the kind of request you are making.
Polyaxonfiles can be written and defined in several formats
(YAML, JSON, Python, and some other languages) but in
AI Singapore's context, we will be sticking with YAML.

Head over [here](https://polyaxon.com/docs/core/specification/) for the
official documentation on Polyaxonfiles.

#### Components

Before you can define a job or service for Polyaxon, you would have to
call upon and define a component. Hence, in every Polyaxonfile that is
provided as an example, you see the following lines
at the very beginning:

```yaml
version: 1.1
kind: component
...
```

From the official documentation:

> Component is a discrete, repeatable, and self-contained action that
> defines an environment and a runtime.

Essentially, a "component" is to represent a discrete aspect of your
end-to-end workflow. You can have a component for your development
environment, one for your data preparation pipeline, and another for
your model training workflow. You can also have different components for
different variations of your pipelines. However these workflows are to
be defined, they all start with specifying a component.
Shown [here](https://polyaxon.com/docs/intro/concepts/runtime-concepts/),
you can specify various runtimes
(experimentation tools) you would like to spin up through the Polyaxon
server.

__Reference(s):__

- [Polyaxon Docs - Component Specification](https://polyaxon.com/docs/intro/quick-start/components/)
- [Polyaxon Docs - Polyaxon experimentation tools](https://polyaxon.com/docs/experimentation/)

#### Jobs

One example of such components is "jobs". You can run jobs for training
models, data preprocessing or any generic tasks that are executable
within Docker images. Whenever you need to execute a pipeline or a
one-off task, "jobs" is the right runtime to go for.

__Reference(s):__

- [Polyaxon Docs - Jobs Introduction](https://polyaxon.com/docs/experimentation/jobs/)

#### Services

The "services" runtime is used for spinning up applications or
interfaces that are to remain running until you stop the service
(or an error is faced on the server's end).
You can spin up services the likes of a VSCode editor that would
be accessible via a browser, a Jupyter Lab server or a REST API server.

__Reference(s):__

- [Polyaxon Docs - Services Introduction](https://polyaxon.com/docs/experimentation/)

We will dive deeper into these concepts and the usage of each one of
them in later sections.

### Secrets & Credentials on Kubernetes

When executing jobs on Polyaxon, credentials are needed to access
various services like GCR or GCS. To provide your container jobs with
access to these credentials, you need to carry out the following:

1. Download a service account key to your local machine (or obtain it
   from the lead engineer/MLOps team) and rename it to
   `gcp-service-account.json`. Take note of the client email detailed
   in the JSON file. The client email should be of the following
   convention: `aisg-100e-sa@<PROJECT_ID>.iam.gserviceaccount.com`.
2. Create a Kubernetes secret on your Kubernetes (GKE) cluster,
   within the same namespace where Polyaxon is deployed: `polyaxon-v1`.
3. Configure Polyaxonfiles to refer to these secrets.

Here are the commands to be executed for creating the secrets:

```bash
$ export SA_CLIENT_EMAIL=<SA_CLIENT_EMAIL>
$ export PATH_TO_SA_JSON_FILE=<PATH_TO_SA_JSON_FILE>
$ kubectl create secret docker-registry gcp-imagepullsecrets \
  --docker-server=https://asia.gcr.io \
  --docker-username=_json_key \
  --docker-email=$SA_CLIENT_EMAIL \
  --docker-password="$(cat $PATH_TO_SA_JSON_FILE)" \
  --namespace=polyaxon-v1
$ kubectl create secret generic gcp-sa-credentials \
  --from-file $PATH_TO_SA_JSON_FILE \
  --namespace=polyaxon-v1
```

Make sure that the Polyaxonfiles for the jobs and services that requires
your service account credentials have the following configurations:

```yaml
...
inputs:
  - name: SA_CRED_PATH
    description: Path to credential file for GCP service account.
    isOptional: true
    type: str
    value: /var/secret/cloud.google.com/gcp-service-account.json
    toEnv: GOOGLE_APPLICATION_CREDENTIALS
run:
  kind: job
  environment:
    imagePullSecrets: ["gcp-imagepullsecrets"]
  volumes:
    - name: gcp-service-account
      secret:
        secretName: "gcp-sa-credentials"
  container:
    volumeMounts:
      - name: gcp-service-account
        mountPath: /var/secret/cloud.google.com
...
```

__Reference(s):__

- [Kubernetes Docs - Namespaces](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)

## Development Environment

An advantage presented by the Polyaxon platform is that you can utilise
the GKE cluster's resources for your development and engineering works
instead of your own resources. We can make use of
[Polyaxon services](https://polyaxon.com/docs/experimentation/services/#specification)
to spin up VSCode or Jupyter Lab servers with which cluster resources
can be dedicated (except for GPUs);
all you need on your end is a machine with WebSockets,
a browser and a terminal.

A caveat: since these development environments are essentially pods
deployed within a Kubernetes cluster, using Docker within the pods
themselves is not feasible or recommended. We will explore alternatives
later on for building Docker images outside of your local machine's
context.

### VSCode

The VSCode service to be created will be using a Docker image. You
can use the Dockerfile that is provided out-of-the-box
`docker/{{cookiecutter.repo_name}}-poly-vscode.Dockerfile` to build a
Docker image to be pushed to your project's container registry (GCR) or
you can customise that same Dockerfile to your liking. Either way, you
are to specify the image to be used for the service.

```bash
$ export GCP_PROJECT_ID={{cookiecutter.gcp_project_id}}
$ docker build \
  -t asia.gcr.io/$GCP_PROJECT_ID/vscode-server:0.1.0 \
  -f docker/{{cookiecutter.repo_name}}-poly-vscode.Dockerfile .
$ docker push asia.gcr.io/$GCP_PROJECT_ID/vscode-server:0.1.0
```

Once that is done, change the value of `.run.container.image` for the
file `aisg-context/polyaxon/polyaxonfiles/vscode-service.yml` to the
name and tag of the Docker image you've just pushed:

```bash
$ yq e ".run.container.image = \"asia.gcr.io/$GCP_PROJECT_ID/vscode-server:0.1.0\"" -i aisg-context/polyaxon/polyaxonfiles/vscode-service.yml
```

Push the configurations to the Polyaxon server to start up the VSCode
service:

```bash
$ polyaxon run -f aisg-context/polyaxon/polyaxonfiles/vscode-service.yml -p {{cookiecutter.repo_name}}-<YOUR_NAME>
```

Now head over to the services dashboard under your project. The link to
your services would be as such -
`http://localhost:8888/ui/default/{{cookiecutter.repo_name}}-<YOUR_NAME>/services`
. The interface should look something like the following:

![Polyaxon v1 - Services Dashboard](./assets/screenshots/polyaxon-v1-services-dashboard.png)

To access the VSCode service, expand the service and click on the
`Service` tab:

![Polyaxon v1 - VSCode Service Run View](./assets/screenshots/polyaxon-v1-vscode-service-run-view.png)

The service you see here is embed within Polyaxon's dashboard. You can
click on the `Fullscreen` button to have a single browser tab be
dedicated to this service.

![Polyaxon v1- VSCode Service Interface](./assets/screenshots/polyaxon-v1-vscode-service-interface.png)

To open up the integrated terminal within the VSCode environment, you
can use the keyboard shortcut <code>Ctrl + Shift + `</code>.

### Jupyter Lab

> Coming soon...

## Git Repository

Now that we have a development environment, we can clone this repository
into the environment's persistent storage. As the persistent storage
would be accessible by the rest of your project team members, __you
should only use the `HTTPS` protocol to clone the repository__
as opposed to using an `SSH` key.

The path to persistent storage on Polyaxon is located at
`/polyaxon-v1-data`. You can create your own workspace folder under
`/polyaxon-v1-data/workspaces/<YOUR_NAME>`:

```bash
$ sudo mkdir -p /polyaxon-v1-data/workspaces/<YOUR_NAME>
$ sudo chown -R 2222:2222 /polyaxon-v1-data/workspaces
$ cd /polyaxon-v1-data/workspaces/<YOUR_NAME>
$ git clone <REMOTE_URL_HTTPS>
$ cd {{cookiecutter.repo_name}}
```

## Cloud SDK for Development Environment

As mentioned [here](#secrets--credentials-on-kubernetes),
credentials or secrets can be attached to Polyaxon services or jobs
when configured properly. In doing so, you can make use of Google
service accounts to interact with GCP services or resources.

If you used the provided Dockerfile to build the image for the VSCode
service on Polyaxon, the VSCode environment would have the Cloud SDK
installed. You can configure the `gcloud` CLI to make use of the
service account attached to the VSCode service:

```bash
$ gcloud auth activate-service-account --key-file /var/secret/cloud.google.com/gcp-service-account.json
```

Once the service account has been configured, examples of actions you
can carry out consists of the following:

- list objects within GCS buckets
- create objects within GCS buckets
- list deployed pods within a GKE cluster

Do note that the service account has limited permissions.

## Virtual Environment

While the Docker images you will be using to run experiments on Polyaxon
would contain the conda environments you would need, you can also create
these virtual environments within your development environment, and have
it be persisted. The following set of commands allows you to create the
conda environment and store the packages within your own workspace
directory:

```bash
$ conda init bash
$ conda env create -f {{cookiecutter.repo_name}}-conda-env.yml -p /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
$ alias {{cookiecutter.repo_name}}-conda-env="conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env"
$ {{cookiecutter.repo_name}}-conda-env
```

## Data Versioning

Now that we have our development environment set up, we can clone the
repository containing the metadata and cache information for the problem
statement's raw data.
(Please refer to the UDP guide for usage of the UDP portal for uploading
raw data for your own project's problem statement.)

> More content to be included for uploading of project data
> through UDP...

For this guide's problem statement,
we will use the following repository:
https://github.com/aimakerspace/e2e-project-template-gcp-data

```bash
$ cd /polyaxon-v1-data/workspaces/<YOUR_NAME>
$ git clone https://github.com/aimakerspace/e2e-project-template-gcp-data
$ cd e2e-project-template-gcp-data
$ ls -la
drwxr-sr-x 5 coder 2222 xxxx xxx xx xx:xx .dvc
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx .dvcignore
drwxr-sr-x 8 coder 2222 xxxx xxx xx xx:xx .git
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx .gitignore
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx raw.dvc
```

Projects' data repositories contains base configurations for the remote
DVC cache which stores versions of your project's data. In our context
here, the remote cache is situated within a GCS bucket
(a publicly accessible one). For you to be able to navigate between the
different versions of your project's data, you need the cache.

To pull from the remote cache, you need to execute a job that
pulls (or push) data from (or to) it. The next section covers on how you
can execute jobs on Polyaxon.

__Reference(s):__

- [DVC - Storing & Sharing](https://dvc.org/doc/start/data-and-model-versioning#storing-and-sharing)

## Job Orchestration

Jobs are submitted to the Polyaxon server and executed within Docker
containers. These images are either pulled from a registry or built upon
a job's submission. The names and definitions of images are specified in
Polyaxonfiles. Using these images, Kubernetes pods are spun up to
execute the entry points or commands defined, tapping on to the
Kubernetes cluster's available resources.

Any jobs that are submitted to the Polyaxon server can be tracked and
monitored through Polyaxon's dashboard. See [this section](#dashboard)
on how to access the dashboard for Polyaxon and create a project.

### Data Preparation

#### Pulling Raw Data

If you have yet to pull in data from the remote DVC cache to the
persistent storage on Polyaxon, this section will cover on how to do so.

First, let's build the Docker image to be used for the data preparation
pipelines and push it to your GCP project's image registry:

```bash
$ docker build \
  -t asia.gcr.io/$GCP_PROJECT_ID/data-prep:0.1.0 \
  -f docker/{{cookiecutter.repo_name}}-data-prep.Dockerfile .
$ docker push asia.gcr.io/$GCP_PROJECT_ID/data-prep:0.1.0
```

Replace the name of the Docker image for the value
`.run.container.image` in the Polyaxonfile
`aisg-context/polyaxon/polyaxonfiles/update-raw-data.yml`:

```bash
$ yq e ".run.container.image = \"asia.gcr.io/$GCP_PROJECT_ID/data-prep:0.1.0\"" -i aisg-context/polyaxon/polyaxonfiles/update-raw-data.yml
```

Assuming you're still connected to the Polyaxon server through
port-forwarding, submit a job to the server like such:

```bash
$ polyaxon run -f aisg-context/polyaxon/polyaxonfiles/update-raw-data.yml -p {{cookiecutter.repo_name}}-<YOUR_NAME> -P WORKING_DIR="/polyaxon-v1-data/workspaces/<YOUR_NAME>/e2e-project-template-gcp-data"
Creating a new run...
A new run `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` was created
You can view this run on Polyaxon UI: http://localhost:8888/ui/default/<YOUR_PROJECT_NAME>/runs/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/
```

__Note:__ The `-P` flag is for overriding or specifying parameters that
can be set for the Polyaxon component.
See [here](https://polyaxon.com/docs/core/specification/io/)
for more information on how to specify input parameters.

Now, you can head over to the dashboard through the localhost URL
`localhost:8888` and switch over to the jobs tab:

![Polyaxon v1 - Project Overview Hover Jobs](./assets/screenshots/polyaxon-v1-project-overview-hover-jobs.png)

![Polyaxon v1 - Project](./assets/screenshots/polyaxon-v1-jobs-dashboard.png)

Refer to
[this page](https://polyaxon.com/docs/management/runs-dashboard/) on
how to navigate the interface listing the job runs you have submitted.

To inspect the contents of the pulled data, head back over to the VSCode
interface.

```bash
$ cd /polyaxon-v1-data/workspaces/<YOUR_NAME>/e2e-project-template-gcp-data
$ ls -la
drwxr-sr-x 5 coder 2222 xxxx xxx xx xx:xx .dvc
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx .dvcignore
drwxr-sr-x 8 coder 2222 xxxx xxx xx xx:xx .git
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx .gitignore
drwxr-xr-x 3 coder 2222 xxxx xxx xx xx:xx raw
-rw-r--r-- 1 coder 2222 xxxx xxx xx xx:xx raw.dvc
```

__Note:__ Your output may differ from the above.

Notice that now, the project's data repository is populated with
subdirectories (corresponding with the names of files with the
`.dvc` extension) containing data files.

Now that we have the raw data, let's run a job to process the data to
make it suitable for model training. (If you are using the example data,
it will essentially be a removal of tags and punctuations.)

#### Processing Data

To process the raw data, we will be spinning up another separate job
while specifying the same Docker image used for pulling in the raw data.

```bash
$ yq e ".run.container.image = \"asia.gcr.io/$GCP_PROJECT_ID/data-prep:0.1.0\"" -i aisg-context/polyaxon/polyaxonfiles/process-data.yml
$ polyaxon run -f aisg-context/polyaxon/polyaxonfiles/process-data.yml -p {{cookiecutter.repo_name}}-<YOUR_NAME> \
  -P RAW_DATA_DIRS='["/polyaxon-v1-data/workspaces/<YOUR_NAME>/e2e-project-template-gcp-data/raw/aclImdb-aisg-set1"]' \
  -P PROCESSED_DATA_DIR="/polyaxon-v1-data/workspaces/<YOUR_NAME>/e2e-project-template-gcp-data/processed/aclImdb-aisg-combined" \
  -P WORKING_DIR="/home/aisg/{{cookiecutter.repo_name}}"
```

If you were to inspect
`aisg-context/polyaxon/polyaxonfiles/process-data.yml`,
the second command with `yq` overwrites the list of directories
specified in the config file `conf/base/pipelines.yml` for the key
`.data_prep.raw_dirs_paths`. You may specify a list of directory paths
with which you can process and combine the results into one single
directory.

__Note:__ The `yq` utility is used to overwrite the values in the YAML
config as
[Hydra currently doesn't support modification of list in YAML files](https://github.com/facebookresearch/hydra/issues/1547).

After some time, the data processing job should conclude and we can
proceed with training the predictive model.

### Model Training

Before we submit a job to Polyaxon to train our model,
we need to build the Docker image to be used for it:

```bash
$ docker build --network=host \
  -t asia.gcr.io/$GCP_PROJECT_ID/model-train:0.1.0 \
  -f docker/{{cookiecutter.repo_name}}-model-training-gpu.Dockerfile .
$ docker push asia.gcr.io/$GCP_PROJECT_ID/model-train:0.1.0
```

Now that we have the Docker image pushed to the registry,
we can run a job using it:

```bash
$ export MLFLOW_TRACKING_USERNAME=<MLFLOW_TRACKING_USERNAME>
$ export MLFLOW_TRACKING_PASSWORD=<MLFLOW_TRACKING_PASSWORD>
$ export CLUSTER_IP_OF_MLFLOW_SERVICE=$(kubectl get service/mlflow-nginx-server-svc -o jsonpath='{.spec.clusterIP}' --namespace=polyaxon-v1)
$ polyaxon run -f aisg-context/polyaxon/polyaxonfiles/train-model-gpu.yml -p {{cookiecutter.repo_name}}-<YOUR_NAME> \
  -P MLFLOW_TRACKING_USERNAME=$MLFLOW_TRACKING_USERNAME -P MLFLOW_TRACKING_PASSWORD=$MLFLOW_TRACKING_PASSWORD \
  -P SETUP_MLFLOW=true -P MLFLOW_AUTOLOG=true \
  -P MLFLOW_TRACKING_URI="http://$CLUSTER_IP_OF_MLFLOW_SERVICE:5005" -P MLFLOW_EXP_NAME=<MLFLOW_EXPERIMENT_NAME> \
  -P MLFLOW_ARTIFACT_LOCATION="gs://{{cookiecutter.repo_name}}/mlflow-tracking-server" \
  -P WORKING_DIR="/home/aisg/{{cookiecutter.repo_name}}" \
  -P INPUT_DATA_DIR="/polyaxon-v1-data/workspaces/<YOUR_NAME>/e2e-project-template-gcp-data/processed/aclImdb-aisg-combined"
```

#### Hyperparameter Tuning

> Coming soon...

## Deployment

> Coming soon...

## Batch Inferencing

> Coming soon...

## Continuous Integration & Deployment

> Coming soon...

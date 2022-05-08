# Continuous Integration & Deployment

This template presents users with a base configuration for a GitLab
CI/CD pipeline. In this section, the guide aims to provide readers
with some basic understanding of the pipeline defined in the
configuration file `.gitlab-ci.yml`.

That being said, readers would certainly benefit from reading up on
[introductory CI/CD concepts](https://docs.gitlab.com/ee/ci/introduction/)
as introduced by GitLab's Docs.

<div class="video-wrapper">
  <iframe width="1280" height="720" src="https://www.youtube.com/embed/l5705U8s_nQ?start=392" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## GitHub Flow

The defined pipeline assumes a GitHub flow which only relies on
feature branches and a `master`/`main` (default) branch.

![AISG's GitHub Flow Diagram](../assets/images/github-flow-aisg-diagram.png)

With reference to the diagram above, we have the following pointers:

- We make use of feature branches
  (`git checkout -b <NAME_OF_BRANCH>`) to introduce changes to the
  source.
- Merge requests are made when we intend to merge the commits made to a
  feature branch to `master`.
- While one works on a feature branch, it is recommended that changes
  pushed to the `master` are pulled to the feature branch itself on a
  consistent basis. This allows the feature branch to possess the
  latest changes pushed by other developers through their own feature
  branches. In the example above, commits from the `master` branch
  following a merge of the `add-hidden-layer` branch are pulled into
  the `change-training-image` branch while that branch still expects
  further changes.
- The command `git pull` can be used to pull and sync
  these changes. However, it's recommended that developers make use of
  `git fetch` and `git log` to observe incoming changes first rather
  than pulling in changes in an indiscriminate manner.
- While it's possible for commits to be made directly
  to the `master` branch, it's recommended that they are kept minimal,
  at least for GitHub flow _(other workflows might not heed such
  practices)_.

As we move along, we should be able to relate parts of the flow
described above with the stages defined by the default GitLab CI
pipeline.

## Environment Variables

Before we can make use of the GitLab CI pipeline, we would have to
define the following variables for the pipeline beforehand:

- `GCP_PROJECT_ID`: The ID of the GCP project for which container images
  are to be pushed to or where apps are to be deployed to.
- `GCP_SERVICE_ACCOUNT_KEY`: A service account's
  JSON key that is to be used for communicating with GCP services.
- `PRED_MODEL_UUID`: Unique ID of the MLflow run associated with a
  default model to be used for building the images of the following
  services: batch inferencing, FastAPI server and Streamlit app.
  Technically, this can be UUID for any baseline model or an arbitrary
  string as it can be overridden when the containers are being run.

To define CI/CD variables for a project (repository), follow the steps
listed
[here](https://docs.gitlab.com/ee/ci/variables/#add-a-cicd-variable-to-a-project).
For `GCP_PROJECT_ID` and `PRED_MODEL_UUID`, they are to be of `Variable`
type while `GCP_SERVICE_ACCOUNT_KEY` needs to be a `File` type.

__Reference(s):__

- [GitLab Docs - GitLab CI/CD variables](https://docs.gitlab.com/ee/ci/variables/)

## Stages & Jobs

In the default pipeline, we have 3 stages defined:

- `test`: For every push to certain branches, the source code residing
  in `src` will be tested.
- `build`: Assuming the automated tests are passed, the pipeline
  will build Docker images, making use of the latest source.
- `deploy-docs`: This stage is for the purpose of deploying a static
  site through
  [GitLab Pages](https://docs.gitlab.com/ee/user/project/pages/).
  More on this stage is covered in
  ["Documentation"](./11-documentation.md).

These stages are defined and listed like so:

=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    stages:
      - test
      - build
      - deploy-docs
    ...
    ```

The jobs for each of the stages are executed using Docker images defined
by users. For this, we have to specify in the pipeline the tag
associated with the GitLab Runner that has the
[Docker executor](https://docs.gitlab.com/runner/executors/docker.html).
In our case, the tag for the relevant runner is `dind`.

=== "`.gitlab-ci.yml`"

    ```yaml
    default:
      tags:
        - dind
    ...
    ```

## Automated Testing & Linting

Let's look at the job defined for the `test`stage first:

=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    test:pylint-pytest:
      stage: test
      image:
        name: continuumio/miniconda:4.7.12
      before_script:
        - conda env create -f {{cookiecutter.repo_name}}-conda-env.yml
        - source activate {{cookiecutter.repo_name}}
      script:
        - pylint src --fail-under=7.0 --ignore=tests --disable=W1202
        - pytest src/tests
      rules:
        - if: $CI_MERGE_REQUEST_IID
          changes:
            - src/**/*
            - conf/**/*
        - if: $CI_PIPELINE_SOURCE == "push"
        - if: $CI_COMMIT_TAG
          when: never
    ...
    ```

First of all, this `test:pylint-pytest` job will only execute on the
condition that the defined
[`rules`](https://docs.gitlab.com/ee/ci/yaml/#rules)
are met. In this case,
the job will only execute for the following cases:

- For any pushes to any branch.
- For pushes to branches which merge requests have been created,
  tests are executed only if there are changes made to any files within
  `src` or `conf` are detected. This is to prevent automated tests
  from running for pushes made to feature branches
  with merge requests when no
  changes have been made to files for which tests are relevant.
  Otherwise, tests will run in a redundant manner, slowing down the
  feedback loop.
- If the push action is associated with a tag
  (`git push <remote> <tag_name>`), the job will not run.

The job defined above fails
under any of the following conditions:

- The source code does not meet a linting score of at least 6.5.
- The source code fails whatever tests have been defined under
  `src/tests`.

The job would have to succeed before moving on to the `build` stage.
Otherwise, no Docker images will be built. This is so that source
code that fail tests would never be packaged.

__Reference(s):__

- [GitLab Docs - Predefined variables reference](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html)
- [Real Python - Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [VSCode Docs - Linting Python in Visual Studio Code](https://code.visualstudio.com/docs/python/linting)

## Automated Builds

The template has thus far introduced a couple of Docker images relevant
for the team. The tags for all the Docker images are listed below:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/vscode-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/jupyter-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/data-prep`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/model-train`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/fastapi-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/batch-inference`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/streamlit`
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/vscode-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/jupyter-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/data-prep`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/model-train`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/fastapi-server`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/batch-inference`
- `asia.gcr.io/{{cookiecutter.gcp_project_id}}/{{cookiecutter.author_name}}/streamlit`
{% endif %}
The `build` stage aims at automating the building of these Docker
images in a parallel manner. Let's look at a snippet for a single job
that builds a Docker image:
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    build:fastapi-server-image:
      stage: build
      image:
        name: gcr.io/kaniko-project/executor:debug
        entrypoint: [""]
      variables:
        GOOGLE_APPLICATION_CREDENTIALS: /kaniko/gcp-sa.json
      script:
        - mkdir -p /kaniko/.docker
        - cat $GCP_SERVICE_ACCOUNT_KEY > /kaniko/gcp-sa.json
        - >-
          /kaniko/executor
          --context "${CI_PROJECT_DIR}"
          --dockerfile "${CI_PROJECT_DIR}/docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile"
          --build-arg PRED_MODEL_UUID=${PRED_MODEL_UUID}
          --destination "asia.gcr.io/${GCP_PROJECT_ID}/fastapi-server:${CI_COMMIT_SHORT_SHA}"
      rules:
        - if: $CI_MERGE_REQUEST_IID
          changes:
            - docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile
            - src/**/*
            - conf/**/*
            - scripts/**/*
        - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    ...
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    build:fastapi-server-image:
      stage: build
      image:
        name: gcr.io/kaniko-project/executor:debug
        entrypoint: [""]
      variables:
        GOOGLE_APPLICATION_CREDENTIALS: /kaniko/gcp-sa.json
      script:
        - mkdir -p /kaniko/.docker
        - cat $GCP_SERVICE_ACCOUNT_KEY > /kaniko/gcp-sa.json
        - >-
          /kaniko/executor
          --context "${CI_PROJECT_DIR}"
          --dockerfile "${CI_PROJECT_DIR}/docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile"
          --build-arg PRED_MODEL_UUID=${PRED_MODEL_UUID}
          --destination "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/fastapi-server:${CI_COMMIT_SHORT_SHA}"
      rules:
        - if: $CI_MERGE_REQUEST_IID
          changes:
            - docker/{{cookiecutter.repo_name}}-fastapi.Dockerfile
            - src/**/*
            - conf/**/*
            - scripts/**/*
        - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    ...
    ```
{% endif %}
!!! note
    You would have noticed that the jobs for building images utilise the
    command `/kaniko/executor` as opposed to `docker build` which most
    users would be more familiar with. This is due to the usage of
    [`kaniko`](https://github.com/GoogleContainerTools/kaniko) within a
    runner with a Docker executor. Using Docker within Docker
    ([Docker-in-Docker](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker))
    requires privileged mode that poses several security concerns.
    Hence, the image `gcr.io/kaniko-project/executor:debug` is being
    used for all `build` jobs related to building of Docker images.
    That being said, the flags used for `kaniko` corresponds well with
    the flags usually used for `docker` commands.

Just like with the `test` job, the each of the jobs under `build`
will execute under certain conditions:

- If a push is being done to a branch which has a merge request opened,
  a check would be done to see if any changes were made to folders like
  `src`, `conf`, `scripts`, or the relevant Dockerfile itself. If there
  are changes, the job will be executed. An opened merge request is
  detected through the predefined variable `CI_MERGE_REQUEST_IID`.
- If a push is being made to the default branch (`CI_DEFAULT_BRANCH`)
  of the repo, which in
  most cases within our organisation would be `master`, the job would
  execute as well. Recalling the `test` stage, any pushes to the repo
  would trigger the automated tests and linting. If a push to the
  `master` branch passes the tests, all Docker images will be
  built, regardless of whether changes have been made to files
  relevant to the Docker images to be built themselves.

Images built through the pipeline will be tagged with the commit
hashes associated with the commits that triggered it. This is seen
through the usage of the predefined variable `CI_COMMIT_SHORT_SHA`.

__Reference(s):__

- [GitLab Docs - Use kaniko to build Docker images](https://docs.gitlab.com/ee/ci/docker/using_kaniko.html)
- [GitLab Docs - Use Docker to build Docker images](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html#use-docker-in-docker)

## Tagging

As mentioned, pushes to the default branch would trigger builds for
Docker images and they would be tagged with the commit hash.
However, such commit hashes aren't the best way to tag "finalised"
Docker images so the usage of tags would be more appropriate here.
Hence, for the job defined below, it would only trigger if a tag
is pushed to the default branch and only the default branch.
The tag pushed (say through a command like `git push <remote> <tag>`)
to the default branch on the remote would have the runner
__retag__ the Docker image that exists on GCR with the tag that is being
pushed. The relevant images to be retagged are originally tagged with
the short commit hash obtained from the commit that was pushed
to the default branch before this.
{% if cookiecutter.gcr_personal_subdir == 'No' %}
=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    build:retag-images:
      stage: build
      image:
        name: google/cloud-sdk:debian_component_based
      variables:
        GOOGLE_APPLICATION_CREDENTIALS: /gcp-sa.json
      script:
        - cat $GCP_SERVICE_ACCOUNT_KEY > /gcp-sa.json
        - gcloud auth activate-service-account --key-file=/gcp-sa.json
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/vscode-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/vscode-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/jupyter-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/jupyter-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/data-prep:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/data-prep:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/model-train:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/model-train:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/fastapi-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/fastapi-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/batch-inference:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/batch-inference:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/streamlit:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/streamlit:${CI_COMMIT_TAG}"
      rules:
        - if: $CI_COMMIT_TAG && $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    ...
    ```
{% elif cookiecutter.gcr_personal_subdir == 'Yes' %}
=== "`.gitlab-ci.yml`"

    ```yaml
    ...
    build:retag-images:
      stage: build
      image:
        name: google/cloud-sdk:debian_component_based
      variables:
        GOOGLE_APPLICATION_CREDENTIALS: /gcp-sa.json
      script:
        - cat $GCP_SERVICE_ACCOUNT_KEY > /gcp-sa.json
        - gcloud auth activate-service-account --key-file=/gcp-sa.json
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/vscode-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/vscode-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/jupyter-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/jupyter-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/data-prep:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/data-prep:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/model-train:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/model-train:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/fastapi-server:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/fastapi-server:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/batch-inference:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/batch-inference:${CI_COMMIT_TAG}"
        - gcloud container images add-tag --quiet "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/streamlit:${CI_COMMIT_SHORT_SHA}" "asia.gcr.io/${GCP_PROJECT_ID}/{{cookiecutter.author_name}}/streamlit:${CI_COMMIT_TAG}"
      rules:
        - if: $CI_COMMIT_TAG && $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    ...
    ```
{% endif %}
__Reference(S):__

- [GitHub Docs - GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow)
- [GitLab Docs - GitLab Flow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)

## Conclusion

The stages and jobs defined in this default pipeline is rudimentary at
best as there is much more that could be done with GitLab CI.
Some examples off the top:

- automatically generate reports for datasets that arrive in regular
  intervals
- submit model training jobs following triggers invoked by the same
  pipeline
- automate the deployment of the FastAPI servers to
  the GKE clusters that is accessible by the service account provided
  to the repository

There's much more that can be done but whatever has been shared thus far
is hopefully enough for one to get started with CI/CD.

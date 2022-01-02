FROM ubuntu:18.04

SHELL ["/bin/bash", "-c"]

ARG REPO_DIR="."
ARG CONDA_ENV_FILE="{{cookiecutter.repo_name}}-conda-env.yml"
ARG CONDA_ENV_NAME="{{cookiecutter.repo_name}}"
ARG PROJECT_USER="aisg"
ARG HOME_DIR="/home/$PROJECT_USER"

ARG CONDA_HOME="$HOME_DIR/miniconda3"
ARG CONDA_BIN="$CONDA_HOME/bin/conda"
ARG MINI_CONDA_SH="Miniconda3-latest-Linux-x86_64.sh"

ARG PRED_MODEL_UUID
RUN test -n "$PRED_MODEL_UUID"
ARG PRED_MODEL_GCS_URI="gs://{{cookiecutter.repo_name}}-artifacts/mlflow-tracking-server/$PRED_MODEL_UUID"

ARG PRED_MODEL_PATH="$HOME_DIR/from-gcs/$PRED_MODEL_UUID/artifacts/model/data/model"
ENV PRED_MODEL_UUID=$PRED_MODEL_UUID
ENV PRED_MODEL_GCS_URI=$PRED_MODEL_GCS_URI
ENV PRED_MODEL_PATH=$PRED_MODEL_PATH

WORKDIR $HOME_DIR

RUN groupadd -g 2222 $PROJECT_USER && useradd -u 2222 -g 2222 -m $PROJECT_USER

RUN touch "$HOME_DIR/.bashrc"

RUN apt-get update && \
    apt-get -y install bzip2 curl wget gcc rsync git vim locales \
    apt-transport-https ca-certificates gnupg && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean && \
    curl -O https://repo.anaconda.com/miniconda/$MINI_CONDA_SH && \
    chmod +x $MINI_CONDA_SH && \
    ./$MINI_CONDA_SH -b -p $CONDA_HOME && \
    rm $MINI_CONDA_SH

# From https://cloud.google.com/sdk/docs/install#installation_instructions
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && \
    apt-get update -y && apt-get install google-cloud-sdk -y

COPY $REPO_DIR {{cookiecutter.repo_name}}
RUN mkdir $HOME_DIR/from-gcs

RUN $CONDA_BIN env create -f {{cookiecutter.repo_name}}/$CONDA_ENV_FILE && \
    $CONDA_BIN init bash && \
    $CONDA_BIN clean -a -y && \
    echo "source activate $CONDA_ENV_NAME" >> "$HOME_DIR/.bashrc"

RUN chown -R 2222:2222 $HOME_DIR && \
    rm /bin/sh && ln -s /bin/bash /bin/sh

ENV PATH $CONDA_HOME/bin:$HOME_DIR/.local/bin:$PATH
ENV PYTHONIOENCODING utf8
ENV LANG "C.UTF-8"
ENV LC_ALL "C.UTF-8"

USER 2222

EXPOSE 8080

WORKDIR $HOME_DIR/{{cookiecutter.repo_name}}
RUN chmod -R +x scripts

ENTRYPOINT [ "/bin/bash", "./scripts/fastapi/api-entrypoint.sh" ]

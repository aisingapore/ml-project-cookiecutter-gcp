FROM nvidia/cuda:11.3.0-cudnn8-devel-ubuntu18.04

ARG REPO_DIR="."
ARG CONDA_ENV_FILE="{{cookiecutter.repo_name}}-conda-env.yml"
ARG CONDA_ENV_NAME="{{cookiecutter.repo_name}}"
ARG PROJECT_USER="aisg"
ARG HOME_DIR="/home/$PROJECT_USER"

ARG DVC_VERSION="2.8.3"
ARG DVC_BINARY_NAME="dvc_2.8.3_amd64.deb"

ARG CONDA_HOME="$HOME_DIR/miniconda3"
ARG CONDA_BIN="$CONDA_HOME/bin/conda"
ARG MINI_CONDA_SH="Miniconda3-latest-Linux-x86_64.sh"

WORKDIR $HOME_DIR

RUN groupadd -g 2222 $PROJECT_USER && useradd -u 2222 -g 2222 -m $PROJECT_USER

RUN touch "$HOME_DIR/.bashrc"

RUN apt-get update && \
    apt-get -y install bzip2 curl wget gcc rsync git vim locales && \
    sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8 && \
    apt-get clean && \
    curl -O https://repo.anaconda.com/miniconda/$MINI_CONDA_SH && \
    chmod +x $MINI_CONDA_SH && \
    ./$MINI_CONDA_SH -b -p $CONDA_HOME && \
    rm $MINI_CONDA_SH

RUN wget https://github.com/mikefarah/yq/releases/download/v4.16.1/yq_linux_amd64.tar.gz -O - |\
    tar xz && mv yq_linux_amd64 /usr/bin/yq

RUN wget "https://github.com/iterative/dvc/releases/download/$DVC_VERSION/$DVC_BINARY_NAME" && \
    apt install -y "./$DVC_BINARY_NAME" && \
    rm "./$DVC_BINARY_NAME"

COPY $REPO_DIR {{cookiecutter.repo_name}}

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
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility
ENV LD_LIBRARY_PATH /usr/local/cuda/lib64:$LD_LIBRARY_PATH

USER 2222

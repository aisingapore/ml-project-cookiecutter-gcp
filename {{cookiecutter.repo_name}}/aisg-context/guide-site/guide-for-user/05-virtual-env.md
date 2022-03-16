# Virtual Environment

While the Docker images you will be using to run experiments on Polyaxon
would contain the conda environments you would need, you can also create
these virtual environments within your development environment, and have
it be persisted. The following set of commands allows you to create the
conda environment and store the packages within your own workspace
directory:

```bash
$ /home/coder/miniconda3/bin/conda init bash
$ source ~/.bashrc
$ conda env create -f {{cookiecutter.repo_name}}-conda-env.yml \
    -p /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
$ alias {{cookiecutter.repo_name}}-conda-env="conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env"
$ {{cookiecutter.repo_name}}-conda-env
```

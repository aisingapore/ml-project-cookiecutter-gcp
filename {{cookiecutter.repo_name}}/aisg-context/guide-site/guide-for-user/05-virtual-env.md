# Virtual Environment

While the Docker images you will be using to run experiments on Polyaxon
would contain the conda environments you would need, you can also create
these virtual environments within your development environment, and have
it be persisted. The following set of commands allows you to create the
conda environment and store the packages within your own workspace
directory:

=== "Polyaxon VSCode Terminal"

    ```bash
    $ /miniconda3/bin/conda init bash
    $ source ~/.bashrc
    (base) $ conda env create -f {{cookiecutter.repo_name}}-conda-env.yml \
               -p /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
    (base) $ alias {{cookiecutter.repo_name}}-conda-env="conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}      -conda-env"
    (base) $ {{cookiecutter.repo_name}}-conda-env
    ({{cookiecutter.repo_name}}-conda-env) $ # conda environment has been activated
    ```

!!! tip
    If you encounter issues in trying to install Python libraries,
    do ensure that the amount of resources allocated to the VSCode
    service is sufficient. Installation of libraries from PyPI tends
    to fail when there's insufficient memory. For starters, dedicate
    4GB of memory to the service:

    ```yaml
    ...
        resources:
      requests:
        memory: "4Gi"
        cpu: "2.5"
      limits:
        memory: "4Gi"
        cpu: "2.5"
    ...
    ```

    Another way is to add the flag `--no-cache-dir` for your
    `pip install` executions. However, there's no similar flag for
    `conda` at the moment so the above is a blanket solution.

__Reference(s):__

- [`conda` Docs - Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file)
- [StackOverflow - "Pip install killed - out of memory - how to get around it?"](https://stackoverflow.com/questions/57058641/pip-install-killed-out-of-memory-how-to-get-around-it)

# Virtual Environment

While the Docker images you will be using to run experiments on Polyaxon
would contain the `conda` environments you would need, you can
also create
these virtual environments within your development environment, and have
it be persisted. The following set of commands allows you to create the
`conda` environment and store the packages within your own workspace
directory:

- First, have VSCode open the repository that you have cloned
  previously by heading over to the top left hand corner, selecting
  `File > Open Folder...`, and entering the path to the repository.
  In this case, you should be navigating to the folder
  `/polyaxon-v1-data/workspaces/<YOUR_NAME>/{{cookiecutter.repo_name}}`.

- Now, let's initialise `conda` for the bash shell, and create
  the virtual environment specified in
  `{{cookiecutter.repo_name}}-conda-env.yml`.

=== "Polyaxon VSCode Terminal"

```bash
$ /miniconda3/bin/conda init bash
$ source ~/.bashrc
(base) $ conda env create -f {{cookiecutter.repo_name}}-conda-env.yml \
            -p /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
```

- After creating the `conda` environment, let's create a permanent
  alias for easy activation.

=== "Polyaxon VSCode Terminal"

    ```bash
    (base) $ echo 'alias {{cookiecutter.repo_name}}-conda-env="conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env"' >> ~/.bashrc
    (base) $ source ~/.bashrc
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
- [phoenixNAP - Linux alias Command: How to Use It With Examples](https://phoenixnap.com/kb/linux-alias-command#:~:text=In%20Linux%2C%20an%20alias%20is,and%20avoiding%20potential%20spelling%20errors.)

## Jupyter Kernel for VSCode

While it is possible for VSCode to make use of different virtual Python
environments, some other additional steps are required for Polyaxon
VSCode service to detect the `conda` environments that you would have
created.

- Ensure that you are in a project folder which you intend to work
  on. You can open a folder through `File > Open Folder...`.
  In this case, you should be navigating to the folder
  `/polyaxon-v1-data/workspaces/<YOUR_NAME/{{cookiecutter.repo_name}}`.

- Install the VSCode extensions
  [`ms-python.python`](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
  and
  [`ms-toolsai.jupyter`](https://marketplace.visualstudio.com/items?itemName=ms-toolsai.jupyter).
  After installation of these extensions, restart VSCode by using
  the shortcut `Ctrl + Shift + P`, entering `Developer: Reload Window` in the
  prompt and pressing `Enter` following that.

- Ensure that you have
  [`ipykernel`](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
  installed in the `conda` environment that you intend to use.
  This template by default lists the library as a dependency under
  `{{cookiecutter.repo_name}}-conda-env.yml`. You can check for the
  library like so:

=== "Polyaxon VSCode Terminal"

    ```bash
    $ conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
    $ conda list | grep "ipykernel"
    ipykernel  6.9.2  pypi_0  pypi
    ```

- Now enter `Ctrl + Shift + P` again and execute `Python: Select Interpreter`.
  Provide the path to the Python executable within the `conda`
  environment that you intend to use, something like so:
  `path/to/conda_env/bin/python`.

- Open up any Jupyter notebook and click on the button that says
  `Select Kernel` on the top right hand corner. You will be presented
  with a selection of Python interpreters. Select the one that
  corresponds to the environment you intend to use.

- Test out the kernel by running the cells in the sample notebook
  provided under `notebooks/sample-tf-classification.ipynb`.

## Jupyter Kernel for JupyterLab

The same with the VSCode service, the JupyterLab service
would not by default detect `conda` environments. You would have to
specify to the JupyterLab installation the `ipython` kernel existing
within your `conda` environment.

- Open up a
  [terminal within JupyterLab](https://jupyterlab.readthedocs.io/en/stable/user/terminal.html).

- Activate the `conda` environment in question and ensure that you have
  [`ipykernel`](https://ipython.readthedocs.io/en/stable/install/kernel_install.html)
  installed in the `conda` environment that you intend to use.
  This template by default lists the library as a dependency under
  `{{cookiecutter.repo_name}}-conda-env.yml`. You can check for the
  library like so:

=== "JupyterLab Terminal"

    ```bash
    $ conda activate /polyaxon-v1-data/workspaces/<YOUR_NAME>/conda_envs/{{cookiecutter.repo_name}}-conda-env
    $ conda list | grep "ipykernel"
    ipykernel  6.9.2  pypi_0  pypi
    ```

- Within the `conda` environment, execute the following:

=== "JupyterLab Terminal"

    ```bash
    $ ipython kernel install --name "{{cookiecutter.repo_name}}-conda-env" --user
    ```

- Refresh the JupyterLab instance.

![Polyaxon v1- JupyterLab Service Interface Refresh](../assets/screenshots/polyaxon-v1-jupyter-service-refresh.png)

- Within each Jupyter notebook, you can select the kernel of
  specific `conda` environments that you intend to use by heading to
  the toolbar under
  `Kernel` -> `Change Kernel...`.

![Polyaxon v1- JupyterLab Service Interface Change Kernel](../assets/screenshots/polyaxon-v1-jupyter-service-change-kernel.png)

- Test out the kernel by running the cells in the sample notebook
  provided under `notebooks/sample-tf-classification.ipynb`.

__Reference(s):__

- [Jupyter Docs - Kernels (Programming Languages)](https://docs.jupyter.org/en/latest/projects/kernels.html)

# Prerequisites

## Software & Tooling Prerequisites

Aside from an internet connection, you would need the following to
follow through with the guide:

- NUS Staff/Student account
- Google account with `@aisingapore.org`/`@aiap.sg` domains provisioned
  by AI Singapore
- PC with the following installed:
    - If your machine is with a Windows OS, use
      [__PowerShell__](https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.2)
      instead of the default Command (`cmd.exe`) shell. Best if you
      resort to
      [Windows Terminal](https://docs.microsoft.com/en-us/windows/terminal/).
    - __Pulse Secure__
        - Refer to [NUS IT eGuides](https://nusit.nus.edu.sg/eguides/)
          for installation guides.
    - __Web browser__
    - __Terminal__
    - __[Git](https://git-scm.com/downloads)__
    - __[Docker Engine](https://docs.docker.com/engine/install):__
      Client-server application for containerising applications as well
      as interacting with the Docker daemon.
    - [__miniconda__](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
      (recommended) or
      [__Anaconda__](https://docs.anaconda.com/anaconda/install/index.html):
      Virtual environment manager. The former is the minimal installer.
    - __[`gcloud`](https://cloud.google.com/sdk/docs/install):__
      CLI for interacting with GCP resources.
    - __[`kubectl`](https://kubernetes.io/docs/tasks/tools/):__
      CLI for Kubernetes.
    - *(Optional)* __[`helm`](https://helm.sh/docs/intro/install/):__
      CLI for Kubernetes' package manager.
- Access to a project on
  [Google Cloud Platform](https://console.cloud.google.com).
  See [here](./02-preface.md#google-cloud-platform-gcp-projects)
  for more information on this.

!!! info
    Wherever relevant, you can toggle between the different commands
    that need to be executed
    for either Linux/macOS or the Windows environment (PowerShell).
    See below for an example:

    === "Linux/macOS"

        ```bash
        # Get a list of files/folders in current directory
        $ ls -la
        ```

    === "Windows PowerShell"

        ```powershell
        # Get a list of files/folders in current directory
        $ Get-ChildItem . -Force
        ```

    !!! caution
        If you are on Windows OS, you would need to ensure that the
        files you've cloned or written on your machine be with
        `LF` line endings. Otherwise, issues would arise when Docker
        containers are being built or run. See
        [here](https://stackoverflow.com/questions/48692741/how-can-i-make-all-line-endings-eols-in-all-files-in-visual-studio-code-unix)
        on how to configure consistent line endings for a whole folder
        or workspace using VSCode.

## NUS VPN

Your credentials for your NUS Staff/Student account is needed to
login to NUS' VPN for access to the following:

- AI Singapore's GitLab instance
- NUS resources

In order to interact with remote Git repositories situated on
AI Singapore's GitLab instance (clone, push, fetch, etc.)
outside of NUS' network or GCP (for regions `asia-southeast1` and
`us-central1`), you would need to login to NUS' VPN.

## GitLab

We at AI Singapore host
[our own GitLab server](https://gitlab.aisingapore.net/). You should
be provided with a set of credentials during onboarding for access to
the server.

If you would like to configure SSH access for it, you can add the
following lines to your SSH config file:

```config
Host gitlab.aisingapore.net
    Port 2222
    IdentityFile ~/.ssh/<path_to_key_file>
```

__Reference(s):__

- [GitLab Docs - Using SSH keys with GitLab CI/CD](https://docs.gitlab.com/ee/ci/ssh_keys/)

# Quickstart CLI Tool

## Overview
The Quickstart CLI Tool allows you to quickly initialize new projects based on predefined templates. It simplifies the process of setting up new project directories, including automatic GitLab initialization (for private GitLab instances). It has been inspired by the [kickstart project](https://github.com/Keats/kickstart.git) from Keats but the whole development was custom.

## Features

- Create a new project from a template.
- Automatically start a GitLab remote repository.
- Highly customizable templates stored as python files in the `.quickstart` directory. 
- Available templates :
    - `default` : redirect to the temp template.
    - `temp` : basic template for latex article (personal macros).
    - `beamer` : custom beamer template.
    - `boiler` : boilerplate template (only creating a text file) that can be used as the minimal code for a template to run (also contains some useful information). 

### Future features
 - [ ] fix (or remove) the ssh-agent (no need to repeat ssh-key) ; 
 - [ ] `python` template (automatic virtual environment creation threw a requirement.txt file) ; 
 - [ ] `manim` template (math visualization) ;
 - [ ] add a support for github synch (switch between profiles) ;
 - [ ] adding options to the `temp` and `beamer` template to automatically fill titles, author, etc ;

## Installation
### OS support

The python code is (not tested) OS agnostic but the installation script is only for Windows. If using another OS directly run the python script `quickstart.py` with the argument of the command (example: `python quickstart.py info`) but make sure that the click and requests libraries are available in the current environment (or do your own executing script). 

### Prerequisites
- **Python 3** must be installed on your system.
- **Git** and **GitLab account** (optional for version control, if not installed use the `-ng` flag when running `quickstart`). 

### Steps
1. Clone the repository:
    ```sh
    git clone https://github.com/lattes314/quickstart.git
    ```
2. Run the installation script:
    ```sh
    cd quickstart
    install.bat
    ```

3. Follow the on-screen prompts to complete the installation.

4. Set up a GitLab access and edit the `.quickstart/gitlabProfile_example.ini` :

    1. In your Gitlab account create an access token (in `Profile/Preferences/Access Tokens`) with at least `api` in the scope. Paste the token in the `api_token` field of the `.quickstart/gitlabProfile_example.ini` file.

    2. Create an ssh key on your machine (usually stored in `~/.shh`, if you don't know how to do it see [here](https://docs.gitlab.com/ee/user/ssh.html)) and register it on your gitlab account (in `Profile/Preferences/SSH Key`).

    3. Create an ssh profile by creating a `config` (no extension) file in the `.shh` directory such as 
    ```txt
    Host <choose a hostname>
        HostName gitlab.<your company gitlab domain>
        User git
        Preferredauthentications publickey
        IdentityFile <path to your ssh key, typically ~/.ssh/gitlab_key>
    ```

    4. Edit the `.quickstart/gitlabProfile_example.ini` file using the informations from the ssh config such as
    ```ini
    [DEFAULT]
    # Connection through a ssh access assuming an alias has been defined in the config file of the .ssh directory
    hostname=<the hostname you chose>
    # Username and API token are registered in your gitlab account
    username=<your gitlab username>
    api_token=<the access token>
    ```

    5. Rename the file in `gitlabProfile.ini`

### Troubleshooting
- **Python not found**: Ensure Python 3 is installed and added to your PATH.
- **Permission errors**: The script should not require admin rights; ensure you have sufficient user permissions.
- **Gitlab access**: if while using the application it does not manage to access your gitlab account check your ssh credentials manually, in the terminal run 
```sh
ssh -T <the hostname your chose>
```

## Usage
### Basic Commands
- **Create a New Project** with template `temp` (if -t not used use the default template):
    ```sh
    quickstart MyNewProject -t temp
    ```
- **List Available Templates**:
    ```sh
    quickstart info
    ```
- **Get the description of the template "temp"**:
    ```sh
    quickstart info -t temp
    ```

### Command Options
- **Avoid Git Initialization**:
    ```sh
    quickstart MyNewProject -t temp -ng
    ```
- **Use a different Gitlab profile**: You can register different Gitlab profile in the `gitlabProfile.ini` file and you can use them with the `-g` option (use the `DEFAULT` profile if not specified):
    ```sh
    quickstart MyNewProject -g profile2
    ``` 


## Customization
### Template Customization
Templates are stored in the `.quickstart/templates` directory. You can modify existing templates or add new ones. Refer to the `boiler` template for more details and basic requirements to build your template.

### Virtual Environment
A virtual environment is created during installation to ensure dependencies are isolated. If you need special libraries for your templates don't forget to install them in the environment.

### Git profiles
By simply adding an entry in the `gitlabProfile.ini` you can switch between profiles (WIP to add github support). For example :
```ini
[DEFAULT]
hostname=<the hostname you chose>
username=<your gitlab username>
api_token=<the access token>

[PROFILE2]
hostname=<other hostname>
username=<other username>
api_token=<new access token>
```

## Contributing
### Reporting Issues
Please report issues via the project’s GitLab issue tracker.

### Submitting Changes
Fork the repository, make your changes, and submit a pull request.

## License
This project is licensed under the MIT License.

## Additional Resources
- [Python Documentation](https://docs.python.org/3/)
- [GitLab ssh connection guide](https://docs.gitlab.com/ee/user/ssh.html)

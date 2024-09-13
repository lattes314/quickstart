"""
Class for handling gitlab -> associated to a config file in the .quickstart folder

SSHAgent not working but do not create any problems.
"""
import os
import configparser
import requests
import subprocess
import re

from lib.ssh_agent import SSH_agent

class GitLabClient:

    def __init__(self, config_path: os.PathLike, profile: str = 'DEFAULT'):
        # Config file parsing
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.profile = profile
        
        # data saving
        self.hostname = self.config[self.profile]['hostname']
        self.username = self.config[self.profile]['username']
        self.api_token = self.config[self.profile]['api_token']

        # Preparing data
        self.gitlab_url, self.ssh_key_name = self.get_from_ssh_config(self.hostname)
        self.headers = {
            "Authorization": f"Bearer {self.api_token}", 
            "Content-Type": "application/json"
        }
        self.ssh_agent = SSH_agent(self.ssh_key_name)

        # Testing connection
        try:
            self.check_connection()
        except Exception as e:
            raise e

    def check_connection(self):
        """
        Try to connect in ssh and through the API to the gitlab. 
        Raise PermissionError if does not match the profile.
        """
        # Using the ssh agent
        self.ssh_agent.add_ssh_key()
        # Requesting connection
        try: 
            result = subprocess.run(
                ["ssh","-T",self.hostname],
                check=True,
                stdout=subprocess.PIPE,         # Captures the output
                stderr=subprocess.PIPE,         # Captures any errors
                text=True,                      # Returns output as a string (Python 3.7+)
                input=None                      # Allows interactive passphrase entry in terminal
            )
        except Exception as e:
            raise ConnectionError(f"Error accessing GitLab : {e}")
        match_user = re.search(r'Welcome to GitLab, @(\w+)!', result.stdout)
        if match_user:
            self.git_username = match_user.group(1)
            if not self.git_username==self.username:
                raise PermissionError(f"Username not matching : config_file={self.username}, gitlab={self.git_username}")
        else:
            raise ConnectionError(f"Error accessing GitLab : ssh output={result.stdout}")

    def create_repo(self, project_name: str, visibility: str="private") -> str :
        """
        Create a repo of the project name and return its path on gitlab.
        """

        data = {
            'name': project_name,
            'visibility': visibility
        }
        try:
            response = requests.post(f"https://{self.gitlab_url}/api/v4/projects", headers=self.headers, json=data)

            if response.status_code == 201:
                repo_namespace = response.json()['path']
                return repo_namespace
            else:
                raise ConnectionError(f"Failed to create GitLab repository: {response.status_code} - {response.text}")
        except Exception as e:
                raise ConnectionError(f"Error accessing gitlab : {e}")
        
    def clone_repo(self, local_path: os.PathLike, project_name: str) -> None:
        """
        Clone the GitLab repository to a local directory using git CLI.

        :param local_path: Local directory for cloning the repo.
        :param project_name: Name of the GitLab repository to clone.
        """

        # Run the git clone command via subprocess
        source_path = f"{self.hostname}:{self.username}/{project_name}.git"
        destination_path = os.path.join(local_path, project_name)
        try:
            subprocess.run(
                ["git", "clone", source_path, destination_path],
                check=True,
                input=None
                )
        except Exception as e:
            raise ConnectionError(f"Error cloning repo : {e}")
        
    def sync_repo(self, local_path : os.PathLike, project_name: str):
        """
        Stage, commit, and push the files in the local repository using git CLI.
        :param project_name: Name of the repository to sync.
        """

        # Save current directory
        working_path = os.getcwd() 

        try:
            # Navigate to the local repository directory
            os.chdir(os.path.join(local_path, project_name))
            
            # Stage all changes
            subprocess.run(["git", "add", "."], check=True)
            
            # Commit the changes with a message
            subprocess.run(["git", "commit", "-m", "Initial commit according to template"], check=True)
            
            # Push the commit to the remote repository
            subprocess.run(["git", "push", "origin"], check=True)
        
        except Exception as e:
            raise ConnectionError(f"Error while syncing repository: {e}")
        finally:
            # Return to the original directory after the operation
            os.chdir(working_path)
            # Kill the ssh agent
            self.ssh_agent.stop_ssh_agent()

    @staticmethod
    def get_from_ssh_config(alias : str) -> str:
        """
        Retrieve from the .ssh/config file the Hostname of the alias Host.
        """
        # Define the path to the user's .ssh/config file
        ssh_config_path = os.path.expanduser('~/.ssh/config')
        
        # Check if the config file exists
        if not os.path.exists(ssh_config_path):
            raise FileNotFoundError(f"SSH config file not found at {ssh_config_path}")
        
        # Read the .ssh/config file
        with open(ssh_config_path, 'r') as file:
            lines = file.readlines()
        
        # Initialize variables to track host information
        found_alias = False
        hostname = None
        key_name = None
        
        # Parse the config file
        for line in lines:
            line = line.strip()
            
            # Check if the line starts with 'Host' followed by the alias
            if line.startswith('Host ') and alias in line:
                found_alias = True
            
            # If the alias is found, search for the HostName in subsequent lines
            if found_alias and line.startswith('HostName'):
                hostname = line.split()[1]  # Get the second word, which is the hostname

            if found_alias and line.startswith('IdentityFile'):
                key_name = line.split('/')[2]  # Get the third word, which is the key name
                break  # Exit after finding the infos
        
        if hostname and key_name:
            return (hostname, key_name)
        else:
            raise ValueError(f"HostName or Keyname not found for alias '{alias}' in {ssh_config_path}")
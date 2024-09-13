"""
Class for handling an ssh agent for the time of creating a repo.
"""

import os
import subprocess

class SSH_agent:

    def __init__(self, ssh_key_name : str) -> None:
        """Start the SSH agent and return its environment variables."""
        # Store the key name
        self.key_name = ssh_key_name

        # Run the agent
        result = subprocess.run(['ssh-agent', '-s'], capture_output=True, text=True)
        agent_output = result.stdout
        agent_info = {}

        # Parse the ssh-agent output to extract environment variables
        for line in agent_output.splitlines():
            if 'SSH_AUTH_SOCK' in line or 'SSH_AGENT_PID' in line:
                key, value = line.split(';')[0].split('=')
                agent_info[key] = value

        # Set environment variables for the SSH agent
        os.environ.update(agent_info)

    def add_ssh_key(self):
        """Add the SSH private key to the running SSH agent."""
        private_key_path = os.path.join(os.path.expanduser('~/.ssh'), self.key_name)
        try:
            # Run the ssh-add command and capture stdout/stderr
            result = subprocess.run(
                ['ssh-add', private_key_path], 
                check=True, 
                capture_output=True, 
                text=True
            )
            print(result.stdout)  # If successful, print any output

        except subprocess.CalledProcessError as e:
            # Print more detailed error information if the command fails
            print(f"Error: Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            print(f"Error Message: {e.stderr.strip()}")  # Display stderr
            raise  # Re-raise the exception if needed for further handling

    def stop_ssh_agent(self):
        """Kill the SSH agent."""
        agent_pid = os.environ.get('SSH_AGENT_PID')
        if agent_pid:
            subprocess.run(['ssh-agent', '-k'], check=True)
        else:
            print("SSH agent is not running.")
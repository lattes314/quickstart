import click
import os
import subprocess
import sys

from lib.gitlab_client import GitLabClient

# Base directory for templates
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
CONF_FILE = os.path.join(os.path.dirname(__file__), "gitlabProfile.ini")

# Utility function
def parse_directory(new_directory):
    """Check the directory and parse the project name"""
    path = os.path.normpath(new_directory)
    project_path, project_name = os.path.dirname(path), os.path.basename(path)
    return project_path, project_name

# click style messages
click_warning = lambda message : click.secho(f"WARNING - {message}", fg='yellow', bold=True)
click_error = lambda message : click.secho(f"ERROR - {message}", fg='red', bold=True, err=True)
click_info = lambda message : click.secho(f"INFO - {message}", fg='blue', bold=True)
click_valid = lambda message : click.secho(f"OK - {message}", fg='green', bold=True)

@click.group()
def cli():
    """CLI tool to initialize projects based on templates."""
    pass

@click.command()
@click.argument('new_directory')
@click.option('-t', '--template', default='default', help='Template name to use')
@click.option('-ng', '--no-git', is_flag=True, help='Deactivate git')
@click.option('-g', '--gitlab', default='DEFAULT', help='Activate gitlab account')
def init(new_directory, template, no_git, gitlab):
    """Create a new project in NEW_DIRECTORY based on the TEMPLATE."""
    # Check directory and parse the project name
    gitlab_profile = gitlab
    try:
        project_path, project_name = parse_directory(new_directory)
    except OSError as e:
        click_error(f"Could not create new project directory : {e}")
        sys.exit(1)
    
    # Check the template
    template_path = os.path.join(TEMPLATE_DIR, f"{template}.py")
    if not os.path.exists(template_path):
        click_error(f"Template '{template}' not found.")
        sys.exit(1)

    # Initialize git repository
    if not no_git:
        click_info("Initializing GitLab repository...")
        try:
            try:
                client = GitLabClient(CONF_FILE, gitlab_profile)
            except PermissionError as e:
                click_warning(e)
                if click.confirm("Do you want to use the gitlab username (if no project will no be created) ?"):
                    client.username = client.git_username
                else:
                    raise ConnectionError(f"{e}")
            git_path = client.create_repo(project_name)
            try:
                client.clone_repo(project_path, git_path)
            except Exception as e:
                click_warning(f"Repo has been created online but could not use it later")
                raise e 
        except ConnectionError as e:
            click_error(f"Could not use a GitLab repo : {e}")
            if click.confirm("Do you want to only use a local repo without git ?"):
                no_git = True
            else:
                click_error(f"Abort project creation")
                sys.exit(1)

        if not no_git:
            click_valid(f"GitLab repository {project_name} successfully created")

    # Prepare calling template
    if no_git:
        source_path = str(os.path.join(project_path, project_name))
        try:
            os.makedirs(source_path)
        except OSError as e:
            click_error(f"Could not create new project directory : {e}")
            sys.exit(1)
    else:
        source_path = str(os.path.join(project_path, git_path))

    # Create files
    click_info(f"Generating template {template}")
    try:
        subprocess.run(['python', str(template_path), source_path])
    except Exception as e:
        click_error(f"Something went wrong with the template : {e}")
        if not no_git:
            click_warning("The repo has been created online and locally")
        sys.exit(1)
    click_valid(f"Template successfully applied in {source_path}")

    # Push repo
    if not no_git:
        click_info("Pushing repository")
        try:
            client.sync_repo(project_path, git_path)
        except ConnectionError as e:
            click_error(f"Could not push repo (do it manually) : {e}")
            sys.exit(1)
    click_valid("Project successfully initialized")

@click.command()
@click.option('-t', '--template', default=None, help='Template name to get info on')
def info(template):
    """Provide information about the TEMPLATE."""
    if template:
        # Show description of specific template
        template_path = os.path.join(TEMPLATE_DIR, f"{template}.py")
        if not os.path.exists(template_path):
            click_error(f"Template '{template}' not found.")
            sys.exit(1)
        
        with open(template_path, 'r') as f:
            first_line = f.readline().strip()
            if first_line.startswith('"""'):
                newline = f.readline().strip()
                desc = ""
                while not newline.startswith('"""'):
                    desc += "\n"+newline
                    newline = f.readline().strip()
                click.echo(desc)
            else:
                click.echo(f"No description available for template '{template}'.")
    else:
        # List all available templates
        templates = [f[:-3] for f in os.listdir(TEMPLATE_DIR) if f.endswith('.py')]
        click.echo("Available templates:")
        for tmpl in templates:
            click.echo(f" - {tmpl}")
    sys.exit(0)

cli.add_command(init)
cli.add_command(info)

if __name__ == '__main__':
    cli()

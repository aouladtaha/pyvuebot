"""Project management commands for PyVueBot CLI."""
import click
import os
import shutil
from pathlib import Path
from ...core.project import Project
from ...core.template import TemplateManager
from ...core.wizard import SetupWizard


@click.command()
@click.argument("name", required=False)
@click.option("--template", help="Template to use")
@click.option("--description", help="Project description")
@click.option("--yes", "-y", is_flag=True, help="Skip interactive prompts and use defaults")
@click.option("--force", "-f", is_flag=True, help="Force project creation even if directory exists")
def init(name, template, description, yes, force):
    """Initialize a new Telegram Mini App project structure."""
    wizard = SetupWizard()

    if yes and name:
        # Non-interactive mode with provided name
        project = Project(
            name=name,
            template=template or "task_manager",
            description=description
        )
        config = {
            "name": name,
            "template": template or "task_manager",
            "description": description,
            "setup_env": False,
            "env_vars": {}
        }
    elif name and template and description:
        # All parameters provided, no need for wizard
        project = Project(name=name, template=template,
                          description=description)
        config = {
            "name": name,
            "template": template,
            "description": description,
            "setup_env": False,
            "env_vars": {}
        }
    else:
        # Interactive mode - run wizard
        config = wizard.run_wizard(name)
        project = Project(
            name=config["name"],
            template=config["template"],
            description=config["description"]
        )

    # Check if directory exists and handle it
    project_path = Path.cwd() / config["name"]
    if project_path.exists():
        if not force:
            click.echo(f"Error: Directory already exists: {project_path}")
            click.echo("Use --force or -f option to overwrite")
            return
        else:
            # Remove existing directory if --force is used
            click.echo(f"Removing existing directory: {project_path}")
            shutil.rmtree(project_path)

    # Create the project
    project.create_structure()

    # Handle environment files
    template_env_example = wizard.templates_dir / \
        config["template"] / ".env.example"

    # Create .env file if setup_env is True
    if config.get("setup_env") and config.get("env_vars"):
        env_content = []
        for key, value in config["env_vars"].items():
            env_content.append(f'{key}="{value}"')

        env_path = project_path / ".env"
        with open(env_path, "w") as f:
            f.write("\n".join(env_content))
        click.echo("Created .env file with your configurations")

    # Copy .env.example file if it exists in the template
    if template_env_example.exists():
        dest_env_example = project_path / ".env.example"
        if not dest_env_example.exists():
            shutil.copy(template_env_example, dest_env_example)
            click.echo("Created .env.example file")

    click.echo(f"✨ Project structure created: {project.name}")
    click.echo(f"📁 Use 'cd {project.name}' to go to the project directory")
    click.echo("🚀 Run 'pyvuebot install' to install dependencies")


@click.command()
def install():
    """Install project dependencies."""
    project = Project.load_current()
    project.install_dependencies()
    click.echo("✅ Dependencies installed successfully")


@click.command()
def dev():
    """Start development servers."""
    project = Project.load_current()
    project.start_dev()


@click.command()
def build():
    """Build project for production."""
    project = Project.load_current()
    project.build()


@click.command()
def deploy():
    """Deploy project to Vercel."""
    project = Project.load_current()
    project.deploy()

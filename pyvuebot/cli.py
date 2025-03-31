"""CLI entry point for PyVueBot."""
import click
from pathlib import Path
from .core.project import Project
from .core.template import TemplateManager


@click.group()
def cli():
    """PyVueBot CLI for Telegram Mini Apps."""
    pass


@cli.command()
@click.argument("name")
@click.option("--template", default="task_manager", help="Template to use")
@click.option("--description", help="Project description")
def init(name: str, template: str, description: str):
    """Initialize a new Telegram Mini App project structure."""
    project = Project(name=name, template=template, description=description)
    project.create_structure()
    click.echo(f"Project structure created: {name}")
    click.echo(f"Use 'cd {name}' to go to the project directory")
    click.echo("Run 'pyvuebot install' to install dependencies")
    click.echo("Congrats")


@cli.command()
def install():
    """Install project dependencies."""
    project = Project.load_current()
    project.install_dependencies()
    click.echo("Dependencies installed successfully")


@cli.command()
def dev():
    """Start development servers."""
    project = Project.load_current()
    project.start_dev()


@cli.command()
def build():
    """Build project for production."""
    project = Project.load_current()
    project.build()


@cli.command()
def deploy():
    """Deploy project to Vercel."""
    project = Project.load_current()
    project.deploy()


if __name__ == "__main__":
    cli()

"""CLI entry point for PyVueBot."""
import click
import os
from pathlib import Path
from .core.project import Project
from .core.template import TemplateManager
from .core.wizard import SetupWizard


@click.group()
def cli():
    """PyVueBot CLI for Telegram Mini Apps."""
    pass


@cli.command()
@click.argument("name", required=False)
@click.option("--template", help="Template to use")
@click.option("--description", help="Project description")
@click.option("--yes", "-y", is_flag=True, help="Skip interactive prompts and use defaults")
def init(name, template, description, yes):
    """Initialize a new Telegram Mini App project structure."""
    wizard = SetupWizard()

    if yes and name:
        # Non-interactive mode with provided name
        project = Project(
            name=name,
            template=template or "task_manager",
            description=description
        )
    elif name and template and description:
        # All parameters provided, no need for wizard
        project = Project(name=name, template=template,
                          description=description)
    else:
        # Interactive mode - run wizard
        config = wizard.run_wizard(name)
        project = Project(
            name=config["name"],
            template=config["template"],
            description=config["description"]
        )

        # Create .env file if bot token was provided
        if config.get("bot_token"):
            env_content = [
                "# Bot and webhook setup",
                f'TELEGRAM_BOT_TOKEN="{config["bot_token"]}"',
                'WEB_APP_URL=""',
                "",
                "# Environment mode 'development' OR 'production'",
                'NODE_ENV="development"',
                ""
            ]

            if config.get("setup_database"):
                env_content.extend([
                    "# Supabase configs",
                    'SUPABASE_URL=""',
                    'SUPABASE_KEY=""',
                    ""
                ])

            env_content.append(
                '# Bot Link to open when Back to bot main button clicked')
            env_content.append('VITE_TELEGRAM_BOT_LINK=""')

            env_path = Path.cwd() / config["name"] / ".env"
            os.makedirs(os.path.dirname(env_path), exist_ok=True)

    # Create the project
    project.create_structure()

    # Create .env file if it doesn't exist yet and we have a bot token
    if not yes and config.get("bot_token"):
        env_path = project.root_path / ".env"
        with open(env_path, "w") as f:
            f.write("\n".join(env_content))

    click.echo(f"✨ Project structure created: {project.name}")
    click.echo(f"📁 Use 'cd {project.name}' to go to the project directory")
    click.echo("🚀 Run 'pyvuebot install' to install dependencies")


@cli.command()
def install():
    """Install project dependencies."""
    project = Project.load_current()
    project.install_dependencies()
    click.echo("✅ Dependencies installed successfully")


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

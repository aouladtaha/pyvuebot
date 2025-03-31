"""Main CLI entry point for PyVueBot."""
import click
from .commands import project_commands, webhook_commands


@click.group()
def cli():
    """PyVueBot CLI for Telegram Mini Apps."""
    pass


# Register command groups
cli.add_command(project_commands.init)
cli.add_command(project_commands.install)
cli.add_command(project_commands.dev)
cli.add_command(project_commands.build)
cli.add_command(project_commands.deploy)
cli.add_command(webhook_commands.webhook)

if __name__ == "__main__":
    cli()

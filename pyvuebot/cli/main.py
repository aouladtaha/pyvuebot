"""Main CLI entry point for PyVueBot."""
import click
from .. import __version__
from .commands import project_commands, webhook_commands, version_commands


@click.group(invoke_without_command=True)
@click.option('--version', '-v', is_flag=True, help="Show version and exit")
@click.pass_context
def cli(ctx, version):
    """PyVueBot CLI for Telegram Mini Apps."""
    if version or (ctx.invoked_subcommand is None and ctx.args == []):
        click.echo(f"PyVueBot version {__version__}")
        return


# Register command groups
cli.add_command(project_commands.init)
cli.add_command(project_commands.install)
cli.add_command(project_commands.dev)
cli.add_command(project_commands.build)
cli.add_command(project_commands.deploy)
cli.add_command(webhook_commands.webhook)
cli.add_command(version_commands.version)

if __name__ == "__main__":
    cli()

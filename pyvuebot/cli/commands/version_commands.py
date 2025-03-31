"""Version command for PyVueBot CLI."""
import click
from ... import __version__


@click.command()
def version():
    """Show PyVueBot version."""
    click.echo(f"PyVueBot version {__version__}")

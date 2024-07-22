import click

from .util.version import version_msg


@click.command(short_help="Print version information.")
def version():
    """Print version information about the Jumpstarter CLI."""
    click.echo(version_msg())

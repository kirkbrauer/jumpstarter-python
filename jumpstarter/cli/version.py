import click

from .util.version import version_msg


@click.command(short_help="Print version information")
def version():
    """Get the current Jumpstarter version"""
    click.echo(version_msg())

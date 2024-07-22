import click

from .util.version import get_jmp_version
from .util.deps import check_kubectl, check_helm


@click.command(short_help="Check your system configuration.")
def doctor():
    """Checks your system configuration to make sure Jumpstarter will work."""
    click.echo(f"Jumpstarter Doctor v{get_jmp_version()}\n")
    click.echo(check_kubectl())
    click.echo(check_helm())

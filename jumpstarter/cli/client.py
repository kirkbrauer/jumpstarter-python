from typing import Optional
import click

from .util.alias import AliasedGroup


@click.group(cls=AliasedGroup, short_help="Manage and interact with clients.")
def client():
    pass


@click.command(short_help="Create a client configuration.")
@click.argument("name")
@click.option(
    "-o",
    "--out",
    type=click.Path(dir_okay=False),
    help="Specify an output file for the config.",
)
def create(name: str, out: Optional[str]):
    """Create a Jumpstarter client configuration."""
    pass


@click.command(short_help="Remove a client configuration.")
@click.argument("name", type=str)
def remove(name: str):
    """Remove a Jumpstarter client configuration."""
    pass


@click.command(short_help="List available client configurations.")
def list():
    pass


client.add_command(create)
client.add_command(remove)
client.add_command(list)

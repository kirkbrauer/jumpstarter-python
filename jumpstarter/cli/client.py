from typing import Optional

import click

from jumpstarter.config import ClientConfig
from jumpstarter.config.user import UserConfig

from .util import AliasedGroup, make_table


@click.group(cls=AliasedGroup, short_help="Manage and interact with clients.")
def client():
    pass


@click.command("create", short_help="Create a client configuration.")
@click.argument("name")
@click.option(
    "-o",
    "--out",
    type=click.Path(dir_okay=False),
    help="Specify an output file for the config.",
)
def create_client(name: str, out: Optional[str]):
    """Create a Jumpstarter client configuration."""
    pass


@click.command("delete", short_help="Delete a client configuration.")
@click.argument("name", type=str)
def delete_client(name: str):
    """Delete a Jumpstarter client configuration."""
    pass


@click.command("list", short_help="List available client configurations.")
def list_clients():
    current = UserConfig.load().current_client
    configs = ClientConfig.list()
   
    columns = ["CURRENT", "NAME", "ENDPOINT", "PATH"]

    def make_row(c: ClientConfig):
        return {
            "CURRENT": "*" if current.name == c.name else "",
            "NAME": current.name,
            "ENDPOINT": current.endpoint,
            "PATH": current.path
        }
    
    rows = list(map(make_row, configs))

    click.echo(make_table(columns, rows))


client.add_command(create_client)
client.add_command(delete_client)
client.add_command(list_clients)

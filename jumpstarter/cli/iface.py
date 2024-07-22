import click


from .util.alias import AliasedGroup


@click.group(cls=AliasedGroup, short_help="Manage available interfaces.")
def iface():
    """Manage interfaces provided by the installed drivers."""
    pass


@click.command()
@click.option("--driver", "-d", type=str, help="Filter interfaces by driver.")
@click.option("--type", "-t", type=str, help="Filter interfaces by type.")
def list(driver: str):
    """List available interfaces."""
    pass


@click.command(short_help="Bring up an interface.")
@click.argument("name", type=str, help="The name of the interface to bring up.")
def up(name: str):
    """
    Bring up an interface using the Jumpstarter driver initialization logic.

    This command allows driver developers to verify that the init logic is working correctly.
    """
    pass


@click.command(short_help="Bring down an interface.")
@click.argument("name", type=str, help="The name of the interface to bring down.")
def down(name: str):
    """
    Bring down an interface using the Jumpstarter driver destructor logic.

    This command allows driver developers to verify that the destructor logic is working correctly.
    """
    pass


iface.add_command(list)
iface.add_command(up)
iface.add_command(down)

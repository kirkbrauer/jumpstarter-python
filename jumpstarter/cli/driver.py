import click


from .util.alias import AliasedGroup


@click.group(cls=AliasedGroup, short_help="Manage interface drivers.")
def driver():
    """Manage the installed interface drivers."""
    pass


@click.command()
def list():
    """List installed drivers."""
    pass


driver.add_command(list)

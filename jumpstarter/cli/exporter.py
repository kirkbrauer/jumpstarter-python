import click

from .util.alias import AliasedGroup


@click.group(cls=AliasedGroup, short_help='Configure and interact with exporters')
def exporter():
    pass


@click.command(short_help='Create an exporter configuration.')
@click.argument('name')
@click.option('-o', '--out', type=click.Path(dir_okay=False))
def create(name, out):
    pass


@click.command(short_help='Remove an exporter configuration.')
@click.argument('name')
def remove(name):
    pass


@click.command(short_help='List available exporter configurations.')
def list():
    pass


exporter.add_command(create)
exporter.add_command(remove)
exporter.add_command(list)

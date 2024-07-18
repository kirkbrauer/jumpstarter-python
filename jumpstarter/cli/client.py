import click


@click.group(short_help='Configure and interact with clients')
def client():
    pass


@click.command(short_help='Create a client YAML configuration file')
@click.argument('name')
@click.option('-o', '--out', type=click.Path(dir_okay=False))
def create(name, out):
    click.echo(f'Writing file for client {name} to {out}')
    pass


client.add_command(create)

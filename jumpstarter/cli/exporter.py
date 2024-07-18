import click


@click.group(short_help='Configure and interact with exporters')
def exporter():
    pass


@click.command(short_help='Create an exporter YAML configuration file')
@click.argument('name')
@click.option('-o', '--out', type=click.Path(dir_okay=False))
def create(name, out):
    click.echo(f'Writing file for exporter {name} to {out}')


exporter.add_command(create)

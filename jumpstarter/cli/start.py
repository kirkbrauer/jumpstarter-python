import click


@click.command(short_help='Run tests with Jumpstarter')
def start():
    """
    Start a Jumpstarter test

    This command will start the exporter instance and execute any command passed to it.
    """
    click.echo('Zap!')

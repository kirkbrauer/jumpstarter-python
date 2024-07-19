import click


@click.command(short_help='Run local tests.')
@click.option('--venv', '-v', type=click.Path(exists=True), help='Use a specified Python venv.')
@click.option('--audit', '-a', is_flag=True, default=False, help='Print audit logs from the exporter session.')
@click.argument('args', nargs=-1)
def start(audit, venv, args):
    """
    Run local tests with Jumpstarter.

    This command runs a local exporter instance and executes the provided test
    command with the correct client configuration environment variables.
    """
    pass

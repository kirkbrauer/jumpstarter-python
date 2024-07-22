import click


@click.command(short_help="Install Jumpstater Helm chart.")
@click.option("--kube-context")
def install():
    """
    Install the a compatible version of the Jumpstarter Helm chart.
    """
    pass

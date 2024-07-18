"""Main Jumpstarter CLI"""
import click

from .start import start
from .client import client
from .exporter import exporter
from .version import version


@click.group(context_settings={"help_option_names": ['-h', '--help']}, no_args_is_help=True)
def main():
    """
    The Jumpstarter CLI tool.
    """
    pass


main.add_command(start)
main.add_command(client)
main.add_command(exporter)
main.add_command(version)


if __name__ == "__main__":
    main()

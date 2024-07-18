"""Main Jumpstarter CLI"""
import click

from .start import start
from .client import client
from .exporter import exporter
from .version import version


@click.command(short_help='Show this message and exit')
def help():
    """Display the Jumpstarter help information"""
    ctx = click.get_current_context()
    # Print out help information for root
    click.echo(ctx.parent.get_help())
    ctx.exit()


@click.group(no_args_is_help=True)
def jmp():
    """The Jumpstarter CLI tool."""
    pass


jmp.add_command(start)
jmp.add_command(client)
jmp.add_command(exporter)
jmp.add_command(version)
jmp.add_command(help)


if __name__ == "__main__":
    jmp()

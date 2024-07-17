"""Main Jumpstarter CLI"""
import click
import os
import sys

# from jumpstarter import __version__

__version__ = '0.1.0'


def version_msg():
    """Return the Jumpstarter version."""
    python_version = sys.version
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return f"Jumpstarter {__version__} from {location} (Python {python_version})"


@click.command(context_settings={"help_option_names": ['-h', '--help']}, no_args_is_help=True)
@click.version_option(__version__, '-V', '--version', message=version_msg())
def main():
    sys.exit(1)


if __name__ == "__main__":
    main()

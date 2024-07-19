import importlib.metadata
import os
import sys


def get_jmp_version():
    """Get the version of the Jumpstarter Python client/exporter."""
    return importlib.metadata.version("jumpstarter")


def get_cli_path():
    """Get the path of the current Jumpstarter binary."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def version_msg():
    """Generate a human-readable version message for Jumpstarter."""
    python_version = sys.version
    jumpstarter_version = get_jmp_version()
    location = get_cli_path()
    return (
        f"Jumpstarter v{jumpstarter_version} from {location}\n"
        f"Python {python_version}"
    )

import shutil
import subprocess
import json
from typing import Callable


def check_command(command: str, get_version: Callable[[], str]) -> str:
    """Checks if a dependency is installed"""
    path = shutil.which(command)
    if path is None:
        return f"🚨 {command} not installed"
    return f"✅ {command} {get_version()} ({path})"


def get_kubectl_version():
    """Get the installed kubectl client version."""
    result = subprocess.run(
        ["kubectl", "version", "--output", "json", "--client"],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        json_result = result.stdout.decode("utf-8")
        client_version = json.loads(json_result)["clientVersion"]
        return client_version["gitVersion"]
    return "[ERROR]"


def check_kubectl():
    return check_command("kubectl", get_kubectl_version)


def get_helm_version():
    """Get the installed Helm version."""
    result = subprocess.run(
        ["helm", "version", "--short"], capture_output=True, check=False
    )
    if result.returncode == 0:
        return result.stdout.decode("utf-8").replace("\n", "")
    return "[ERROR]"


def check_helm():
    return check_command("helm", get_helm_version)

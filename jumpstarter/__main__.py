"""Allow running Jumpstarter through `python -m jumpstarter`."""

from jumpstarter.cli import jmp

if __name__ == "__main__":
    jmp(prog_name="jmp")

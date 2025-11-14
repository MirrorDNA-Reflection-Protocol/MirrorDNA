"""
MirrorDNA CLI main entry point.
"""

import click
from .commands import init_vault, compute_hash, verify_log, reflect


@click.group()
@click.version_option(version="1.0.0", prog_name="mirrordna")
def cli():
    """
    MirrorDNA CLI - Command-line interface for the MirrorDNA protocol.

    A powerful local interface into core MirrorDNA concepts:
    - Vault scaffolding
    - Continuity hashing
    - Simple reflective logs
    """
    pass


# Register commands
cli.add_command(init_vault)
cli.add_command(compute_hash)
cli.add_command(verify_log)
cli.add_command(reflect)


if __name__ == "__main__":
    cli()

"""
init-vault command - Creates a minimal example vault structure.
"""

import click
import json
import yaml
from pathlib import Path
from datetime import datetime


@click.command(name="init-vault")
@click.argument("target_dir", type=click.Path(), default=".")
@click.option("--format", type=click.Choice(["yaml", "json"]), default="yaml",
              help="Config file format (yaml or json)")
def init_vault(target_dir, format):
    """
    Create a minimal example vault structure.

    Creates the following structure:
      vault/
        config/
        logs/
        docs/

    And includes:
      - Sample config file (YAML or JSON)
      - Sample continuity log file
      - README inside the vault
    """
    target_path = Path(target_dir)

    # Create directory structure
    vault_dir = target_path / "vault"
    config_dir = vault_dir / "config"
    logs_dir = vault_dir / "logs"
    docs_dir = vault_dir / "docs"

    try:
        # Create directories
        for directory in [vault_dir, config_dir, logs_dir, docs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
            click.echo(f"Created: {directory}")

        # Create sample config
        config_data = {
            "vault_id": "vault_example_001",
            "version": "1.0.0",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "storage": {
                "type": "filesystem",
                "base_path": "./vault"
            },
            "metadata": {
                "description": "Example MirrorDNA vault",
                "owner": "user@example.com"
            }
        }

        config_file = config_dir / f"vault_config.{format}"
        with open(config_file, "w") as f:
            if format == "yaml":
                yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(config_data, f, indent=2)
        click.echo(f"Created: {config_file}")

        # Create sample continuity log
        log_entries = [
            {
                "event_id": "evt_001",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event_type": "vault_created",
                "actor": "mirrordna_cli",
                "message": "Vault initialized via CLI",
                "metadata": {
                    "cli_version": "1.0.0"
                }
            },
            {
                "event_id": "evt_002",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "event_type": "session_start",
                "actor": "user",
                "message": "First session started",
                "metadata": {
                    "platform": "local"
                }
            }
        ]

        log_file = logs_dir / "continuity.json"
        with open(log_file, "w") as f:
            json.dump(log_entries, f, indent=2)
        click.echo(f"Created: {log_file}")

        # Create README
        readme_content = """# MirrorDNA Vault

This vault was created using the MirrorDNA CLI.

## Structure

- `config/` - Vault configuration files
- `logs/` - Continuity and event logs
- `docs/` - Documentation and notes

## Getting Started

1. Review the vault config in `config/vault_config.{}`
2. Check the continuity log in `logs/continuity.json`
3. Add your own entries and documents as needed

## Commands

```bash
# Compute vault state hash
mirrordna compute-hash ./vault

# Verify continuity log
mirrordna verify-log ./vault/logs/continuity.json

# Create a reflection
mirrordna reflect "Today's work on the vault was productive"
```

For more information, see the MirrorDNA documentation.
""".format(format)

        readme_file = vault_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        click.echo(f"Created: {readme_file}")

        click.echo()
        click.secho("✓ Vault structure created successfully!", fg="green", bold=True)
        click.echo(f"Location: {vault_dir.absolute()}")

    except Exception as e:
        click.secho(f"Error creating vault: {e}", fg="red", err=True)
        raise click.Abort()

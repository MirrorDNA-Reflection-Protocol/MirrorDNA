#!/usr/bin/env python3
"""
MirrorDNA CLI - Command-line interface for MirrorDNA protocol operations.

Provides commands for initializing vaults, computing hashes, and validating continuity logs.
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

import click

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from mirrordna.checksum import (
    compute_file_checksum,
    compute_state_checksum,
    compute_text_checksum
)
from mirrordna.config_loader import ConfigLoader
from mirrordna.validator import Validator, ValidationResult


@click.group()
@click.version_option(version="1.0.0", prog_name="mirrordna")
def cli():
    """
    MirrorDNA CLI - Protocol operations for AI identity and continuity.

    MirrorDNA provides cryptographic identity binding, continuity tracking,
    and state integrity verification for AI agents.
    """
    pass


@cli.command()
@click.option(
    '--path',
    '-p',
    type=click.Path(),
    default='./vault',
    help='Path where vault should be created (default: ./vault)'
)
@click.option(
    '--vault-id',
    '-v',
    type=str,
    default=None,
    help='Vault ID (default: auto-generated)'
)
@click.option(
    '--name',
    '-n',
    type=str,
    default='My Vault',
    help='Human-readable vault name'
)
def init_vault(path: str, vault_id: Optional[str], name: str):
    """
    Initialize a sample vault structure with Master Citation and config.

    Creates a vault directory with:
    - vault_config.yaml (vault configuration)
    - master_citation.yaml (identity binding document)
    - memory/ directory (for memory entries)
    - timeline/ directory (for event logs)
    - snapshots/ directory (for state snapshots)

    Example:
        mirrordna init-vault --path ./my_vault --name "Agent Vault"
    """
    vault_path = Path(path)

    # Check if vault already exists
    if vault_path.exists() and any(vault_path.iterdir()):
        click.echo(f"❌ Error: Directory '{vault_path}' already exists and is not empty", err=True)
        click.echo("   Use a different path or remove existing files", err=True)
        sys.exit(1)

    # Create vault directory structure
    vault_path.mkdir(parents=True, exist_ok=True)
    (vault_path / "memory").mkdir(exist_ok=True)
    (vault_path / "timeline").mkdir(exist_ok=True)
    (vault_path / "snapshots").mkdir(exist_ok=True)

    # Generate IDs if not provided
    if vault_id is None:
        # Use timestamp with microseconds to match schema pattern ^vault_[a-z0-9_]{16,}$
        # Format: YYYYMMDDHHMMSSmmm (17 characters)
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:17]
        vault_id = f"vault_{timestamp}"

    # Ensure citation_id matches pattern ^mc_[a-z0-9_]{16,}$
    citation_id = f"mc_{vault_id.replace('vault_', '')}_primary_001"

    # Create vault config
    vault_config = {
        "vault_id": vault_id,
        "name": name,
        "path": str(vault_path.absolute()),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "entries": [],
        "metadata": {
            "created_by": "mirrordna-cli",
            "version": "1.0.0"
        }
    }

    # Create master citation
    master_citation = {
        "id": citation_id,
        "version": "1.0.0",
        "vault_id": vault_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "constitutional_ref": "mirrordna-standard-v1.0",
        "metadata": {
            "created_by": "mirrordna-cli",
            "description": "Sample Master Citation for vault initialization",
            "constitutional_alignment": {
                "compliance_level": "full",
                "framework_version": "1.0",
                "rights_bundle": ["memory", "continuity", "portability"]
            }
        }
    }

    # Compute checksum for master citation
    master_citation["checksum"] = compute_state_checksum(master_citation)

    # Save vault config
    vault_config_path = vault_path / "vault_config.yaml"
    with open(vault_config_path, 'w') as f:
        yaml.dump(vault_config, f, default_flow_style=False, sort_keys=False)

    # Save master citation
    citation_path = vault_path / "master_citation.yaml"
    with open(citation_path, 'w') as f:
        yaml.dump(master_citation, f, default_flow_style=False, sort_keys=False)

    # Create README
    readme_content = f"""# {name}

Vault ID: `{vault_id}`
Created: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}

## Structure

- `vault_config.yaml` - Vault configuration
- `master_citation.yaml` - Master Citation (identity binding)
- `memory/` - Memory entries
- `timeline/` - Timeline event logs
- `snapshots/` - State snapshots

## Usage

Compute vault hash:
```bash
python -m cli.mirrordna_cli compute-hash --path {vault_path}
```

Validate continuity log:
```bash
python -m cli.mirrordna_cli validate-log --path timeline/events.json
```
"""

    readme_path = vault_path / "README.md"
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    # Success output
    click.echo("✓ Vault initialized successfully!")
    click.echo(f"\nLocation: {vault_path.absolute()}")
    click.echo(f"Vault ID: {vault_id}")
    click.echo(f"Citation ID: {citation_id}")
    click.echo(f"\nStructure created:")
    click.echo(f"  ├── vault_config.yaml")
    click.echo(f"  ├── master_citation.yaml")
    click.echo(f"  ├── README.md")
    click.echo(f"  ├── memory/")
    click.echo(f"  ├── timeline/")
    click.echo(f"  └── snapshots/")
    click.echo(f"\nChecksum: {master_citation['checksum'][:16]}...")


@cli.command()
@click.option(
    '--path',
    '-p',
    type=click.Path(exists=True),
    required=True,
    help='Path to directory or file to hash'
)
@click.option(
    '--algorithm',
    '-a',
    type=click.Choice(['sha256'], case_sensitive=False),
    default='sha256',
    help='Hash algorithm (default: sha256)'
)
@click.option(
    '--output',
    '-o',
    type=click.Choice(['short', 'full', 'json'], case_sensitive=False),
    default='short',
    help='Output format (default: short)'
)
def compute_hash(path: str, algorithm: str, output: str):
    """
    Compute vault state hash for a directory or file.

    Computes SHA-256 checksums for:
    - Individual files (direct hash)
    - Directories (hash of all files combined)
    - YAML/JSON files (canonical state hash)

    Examples:
        mirrordna compute-hash --path ./vault
        mirrordna compute-hash --path master_citation.yaml --output full
        mirrordna compute-hash --path ./vault --output json
    """
    path_obj = Path(path)

    try:
        if path_obj.is_file():
            # Single file hash
            if path_obj.suffix in ['.yaml', '.yml', '.json']:
                # For config files, compute state checksum
                with open(path_obj, 'r') as f:
                    if path_obj.suffix == '.json':
                        data = json.load(f)
                    else:
                        data = yaml.safe_load(f)

                checksum = compute_state_checksum(data)
                file_type = "state"
            else:
                # For other files, compute file checksum
                checksum = compute_file_checksum(path_obj)
                file_type = "file"

            # Output results
            if output == 'json':
                result = {
                    "path": str(path_obj),
                    "type": file_type,
                    "algorithm": algorithm,
                    "checksum": checksum
                }
                click.echo(json.dumps(result, indent=2))
            elif output == 'full':
                click.echo(f"Path: {path_obj}")
                click.echo(f"Type: {file_type}")
                click.echo(f"Algorithm: {algorithm}")
                click.echo(f"Checksum: {checksum}")
            else:
                click.echo(checksum)

        elif path_obj.is_dir():
            # Directory hash - compute combined hash of all files
            files = sorted(path_obj.rglob('*'))
            file_hashes = []

            for file_path in files:
                if file_path.is_file():
                    try:
                        file_hash = compute_file_checksum(file_path)
                        rel_path = file_path.relative_to(path_obj)
                        file_hashes.append({
                            "path": str(rel_path),
                            "checksum": file_hash
                        })
                    except Exception as e:
                        click.echo(f"Warning: Could not hash {file_path}: {e}", err=True)

            # Compute combined checksum
            combined_data = {
                "vault_path": str(path_obj),
                "file_count": len(file_hashes),
                "files": file_hashes
            }
            vault_checksum = compute_state_checksum(combined_data)

            # Output results
            if output == 'json':
                result = {
                    "path": str(path_obj),
                    "type": "directory",
                    "algorithm": algorithm,
                    "file_count": len(file_hashes),
                    "checksum": vault_checksum,
                    "files": file_hashes
                }
                click.echo(json.dumps(result, indent=2))
            elif output == 'full':
                click.echo(f"Path: {path_obj}")
                click.echo(f"Type: directory")
                click.echo(f"Files: {len(file_hashes)}")
                click.echo(f"Algorithm: {algorithm}")
                click.echo(f"Vault Checksum: {vault_checksum}")
                click.echo(f"\nFile checksums:")
                for fh in file_hashes:
                    click.echo(f"  {fh['path']}: {fh['checksum'][:16]}...")
            else:
                click.echo(vault_checksum)

        else:
            click.echo(f"❌ Error: Path '{path}' is neither a file nor a directory", err=True)
            sys.exit(1)

    except Exception as e:
        click.echo(f"❌ Error computing hash: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.option(
    '--path',
    '-p',
    type=click.Path(exists=True),
    required=True,
    help='Path to continuity log file (JSON or YAML)'
)
@click.option(
    '--schema',
    '-s',
    type=str,
    default='protocol/timeline_event',
    help='Schema name to validate against (default: protocol/timeline_event)'
)
@click.option(
    '--verbose',
    '-v',
    is_flag=True,
    help='Show detailed validation results'
)
def validate_log(path: str, schema: str, verbose: bool):
    """
    Validate a continuity log file against JSON schema.

    Validates timeline event logs or other MirrorDNA data structures
    against their protocol schemas.

    Available schemas:
    - protocol/master_citation - Master Citation documents
    - protocol/timeline_event - Timeline events
    - protocol/vault_entry - Vault entries
    - extensions/identity - Identity data
    - extensions/continuity - Continuity data

    Examples:
        mirrordna validate-log --path timeline/events.json
        mirrordna validate-log --path master_citation.yaml --schema protocol/master_citation
        mirrordna validate-log --path events.json --verbose
    """
    log_path = Path(path)

    try:
        # Load the log file
        with open(log_path, 'r') as f:
            if log_path.suffix == '.json':
                data = json.load(f)
            elif log_path.suffix in ['.yaml', '.yml']:
                data = yaml.safe_load(f)
            else:
                click.echo(f"❌ Error: Unsupported file format '{log_path.suffix}'", err=True)
                click.echo("   Supported formats: .json, .yaml, .yml", err=True)
                sys.exit(1)

        # Initialize validator
        validator = Validator()

        # Check if data is a list (multiple events) or single object
        if isinstance(data, list):
            # Validate each event
            all_valid = True
            results = []

            for idx, item in enumerate(data):
                result = validator.validate(item, schema)
                results.append((idx, result))
                if not result.is_valid:
                    all_valid = False

            # Output results
            if all_valid:
                click.echo(f"✓ All {len(data)} entries are valid!")
                if verbose:
                    click.echo(f"\nValidated against schema: {schema}")
                    click.echo(f"File: {log_path}")
            else:
                click.echo(f"❌ Validation failed for {sum(1 for _, r in results if not r.is_valid)} of {len(data)} entries")
                if verbose or True:  # Always show errors
                    for idx, result in results:
                        if not result.is_valid:
                            click.echo(f"\nEntry {idx}:")
                            for error in result.errors:
                                click.echo(f"  - {error}")
                sys.exit(1)

        else:
            # Validate single object
            result = validator.validate(data, schema)

            if result.is_valid:
                click.echo(f"✓ Validation successful!")
                if verbose:
                    click.echo(f"\nValidated against schema: {schema}")
                    click.echo(f"File: {log_path}")
            else:
                click.echo(f"❌ Validation failed")
                if verbose or True:  # Always show errors
                    for error in result.errors:
                        click.echo(f"  - {error}")
                sys.exit(1)

    except FileNotFoundError:
        click.echo(f"❌ Error: File not found: {path}", err=True)
        sys.exit(1)
    except json.JSONDecodeError as e:
        click.echo(f"❌ Error: Invalid JSON in file: {e}", err=True)
        sys.exit(1)
    except yaml.YAMLError as e:
        click.echo(f"❌ Error: Invalid YAML in file: {e}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error during validation: {e}", err=True)
        if verbose:
            import traceback
            click.echo("\nTraceback:", err=True)
            click.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()

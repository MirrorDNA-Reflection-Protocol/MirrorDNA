"""
compute-hash command - Computes deterministic vault state hash.
"""

import click
import hashlib
import json
from pathlib import Path
import sys
import os

# Add src to path to import mirrordna
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from mirrordna.checksum import compute_file_checksum


def normalize_text(content: bytes) -> bytes:
    """
    Normalize text content for deterministic hashing.

    - Normalizes line endings to LF
    - Strips trailing whitespace
    """
    try:
        text = content.decode('utf-8')
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Strip trailing whitespace from each line
        lines = [line.rstrip() for line in text.split('\n')]
        normalized = '\n'.join(lines)
        return normalized.encode('utf-8')
    except UnicodeDecodeError:
        # If not text, return as-is
        return content


def compute_vault_hash(vault_path: Path, verbose: bool = False) -> tuple[str, dict]:
    """
    Compute deterministic vault state hash.

    Args:
        vault_path: Path to vault directory
        verbose: Show per-file hashes

    Returns:
        Tuple of (final_hash, file_hashes_dict)
    """
    if not vault_path.exists():
        raise FileNotFoundError(f"Path not found: {vault_path}")

    if not vault_path.is_dir():
        raise ValueError(f"Path is not a directory: {vault_path}")

    # Collect all files with relative paths
    all_files = []
    for root, dirs, files in os.walk(vault_path):
        # Sort for determinism
        dirs.sort()
        files.sort()

        for file in files:
            file_path = Path(root) / file
            rel_path = file_path.relative_to(vault_path)
            all_files.append((str(rel_path), file_path))

    # Sort by relative path for determinism
    all_files.sort(key=lambda x: x[0])

    if not all_files:
        raise ValueError(f"No files found in vault: {vault_path}")

    # Compute per-file hashes
    file_hashes = {}
    combined_data = []

    for rel_path, file_path in all_files:
        # Read file content
        with open(file_path, 'rb') as f:
            content = f.read()

        # Normalize text files for determinism
        if file_path.suffix in ['.txt', '.md', '.json', '.yaml', '.yml', '.py', '.js']:
            content = normalize_text(content)

        # Compute file hash
        file_hash = hashlib.sha256(content).hexdigest()
        file_hashes[rel_path] = file_hash

        # Add to combined data (path + hash)
        combined_data.append(f"{rel_path}:{file_hash}")

    # Compute final vault hash from combined file data
    combined_string = "\n".join(combined_data)
    final_hash = hashlib.sha256(combined_string.encode('utf-8')).hexdigest()

    return final_hash, file_hashes


@click.command(name="compute-hash")
@click.argument("path", type=click.Path(exists=True))
@click.option("--verbose", "-v", is_flag=True, help="Show per-file hashes")
def compute_hash(path, verbose):
    """
    Compute deterministic vault state hash for a directory.

    The hash is computed by:
    1. Recursively finding all files
    2. Sorting file paths alphabetically
    3. Normalizing text files (line endings, whitespace)
    4. Computing SHA-256 hash for each file
    5. Combining all hashes into a final vault-state hash

    Example:
        mirrordna compute-hash ./vault
        mirrordna compute-hash ./vault --verbose
    """
    vault_path = Path(path)

    try:
        click.echo(f"Computing vault hash for: {vault_path.absolute()}")
        click.echo()

        final_hash, file_hashes = compute_vault_hash(vault_path, verbose)

        if verbose:
            click.echo("Per-file hashes:")
            click.echo("-" * 70)
            for rel_path, file_hash in sorted(file_hashes.items()):
                click.echo(f"{file_hash}  {rel_path}")
            click.echo("-" * 70)
            click.echo()

        click.echo(f"Files processed: {len(file_hashes)}")
        click.echo()
        click.secho("Vault State Hash:", fg="green", bold=True)
        click.secho(final_hash, fg="cyan", bold=True)

    except Exception as e:
        click.secho(f"Error computing hash: {e}", fg="red", err=True)
        raise click.Abort()

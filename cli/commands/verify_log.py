"""
verify-log command - Validates continuity log files.
"""

import click
import json
import yaml
from pathlib import Path
from datetime import datetime


def validate_log_entry(entry: dict, index: int) -> list[str]:
    """
    Validate a single log entry.

    Args:
        entry: Log entry dictionary
        index: Entry index for error reporting

    Returns:
        List of validation errors (empty if valid)
    """
    errors = []

    # Required fields
    required_fields = ["timestamp", "event_type", "message"]

    for field in required_fields:
        if field not in entry:
            errors.append(f"Entry {index}: Missing required field '{field}'")
        elif not entry[field]:
            errors.append(f"Entry {index}: Field '{field}' is empty")

    # Validate timestamp format if present
    if "timestamp" in entry and entry["timestamp"]:
        try:
            # Try parsing ISO 8601 format
            datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            errors.append(f"Entry {index}: Invalid timestamp format '{entry.get('timestamp')}'")

    # Validate event_type is a string
    if "event_type" in entry and not isinstance(entry["event_type"], str):
        errors.append(f"Entry {index}: Field 'event_type' must be a string")

    # Validate message is a string
    if "message" in entry and not isinstance(entry["message"], str):
        errors.append(f"Entry {index}: Field 'message' must be a string")

    return errors


def load_log_file(file_path: Path) -> list[dict]:
    """
    Load log file (JSON or YAML).

    Args:
        file_path: Path to log file

    Returns:
        List of log entries

    Raises:
        ValueError: If file format is invalid
    """
    with open(file_path, 'r') as f:
        content = f.read()

    # Try JSON first
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        # Try YAML
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid JSON/YAML format: {e}")

    if not isinstance(data, list):
        raise ValueError("Log file must contain a list/array of entries")

    return data


@click.command(name="verify-log")
@click.argument("file", type=click.Path(exists=True))
@click.option("--strict", is_flag=True, help="Fail on warnings as well as errors")
def verify_log(file, strict):
    """
    Validate a continuity log file (JSON or YAML).

    Checks for:
    - Required fields (timestamp, event_type, message)
    - Valid timestamp format (ISO 8601)
    - Non-empty required fields
    - Proper data types

    Example:
        mirrordna verify-log ./vault/logs/continuity.json
        mirrordna verify-log ./vault/logs/continuity.yaml --strict
    """
    file_path = Path(file)

    try:
        click.echo(f"Validating log file: {file_path.absolute()}")
        click.echo()

        # Load log file
        try:
            entries = load_log_file(file_path)
        except Exception as e:
            click.secho(f"✗ Failed to load file: {e}", fg="red", bold=True)
            raise click.Abort()

        if not entries:
            click.secho("⚠ Warning: Log file is empty", fg="yellow")
            if strict:
                raise click.Abort()
            return

        click.echo(f"Found {len(entries)} log entries")
        click.echo()

        # Validate each entry
        all_errors = []
        for i, entry in enumerate(entries):
            errors = validate_log_entry(entry, i)
            all_errors.extend(errors)

        # Report results
        if all_errors:
            click.secho("Validation Errors:", fg="red", bold=True)
            for error in all_errors:
                click.echo(f"  ✗ {error}")
            click.echo()
            click.secho(f"✗ Validation failed with {len(all_errors)} error(s)", fg="red", bold=True)
            raise click.Abort()
        else:
            click.secho("✓ All entries valid", fg="green", bold=True)
            click.echo()

            # Show summary
            event_types = {}
            for entry in entries:
                et = entry.get("event_type", "unknown")
                event_types[et] = event_types.get(et, 0) + 1

            click.echo("Event type summary:")
            for event_type, count in sorted(event_types.items()):
                click.echo(f"  - {event_type}: {count}")

            click.echo()
            click.secho(f"✓ Log file is valid ({len(entries)} entries)", fg="green", bold=True)

    except click.Abort:
        raise
    except Exception as e:
        click.secho(f"Error validating log: {e}", fg="red", err=True)
        raise click.Abort()

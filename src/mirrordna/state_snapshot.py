# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
State snapshot capture and serialization for MirrorDNA protocol.

Captures current identity, continuity, and vault state for persistence and transfer.
"""

import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union, List
from dataclasses import dataclass, asdict

from .checksum import compute_state_checksum


@dataclass
class StateSnapshot:
    """Complete state snapshot for MirrorDNA instance."""
    snapshot_id: str
    timestamp: str
    version: str
    checksum: str
    identity_state: Dict[str, Any]
    continuity_state: Dict[str, Any]
    vault_state: Optional[Dict[str, Any]] = None
    timeline_summary: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None


def capture_snapshot(
    snapshot_id: str,
    identity_state: Dict[str, Any],
    continuity_state: Dict[str, Any],
    vault_state: Optional[Dict[str, Any]] = None,
    timeline_summary: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    version: str = "1.0.0"
) -> StateSnapshot:
    """
    Capture a complete state snapshot.

    Args:
        snapshot_id: Unique identifier for snapshot
        identity_state: Current identity state data
        continuity_state: Current continuity/session state
        vault_state: Optional vault state
        timeline_summary: Optional timeline summary
        metadata: Optional additional metadata
        version: Snapshot format version

    Returns:
        StateSnapshot object with checksum
    """
    timestamp = datetime.utcnow().isoformat() + "Z"

    # Prepare snapshot data without checksum
    snapshot_data = {
        "snapshot_id": snapshot_id,
        "timestamp": timestamp,
        "version": version,
        "identity_state": identity_state,
        "continuity_state": continuity_state,
        "vault_state": vault_state,
        "timeline_summary": timeline_summary,
        "metadata": metadata
    }

    # Compute checksum
    checksum = compute_state_checksum(snapshot_data)

    # Create snapshot with checksum
    return StateSnapshot(
        snapshot_id=snapshot_id,
        timestamp=timestamp,
        version=version,
        checksum=checksum,
        identity_state=identity_state,
        continuity_state=continuity_state,
        vault_state=vault_state,
        timeline_summary=timeline_summary,
        metadata=metadata
    )


def serialize_snapshot(
    snapshot: StateSnapshot,
    format: str = "json"
) -> str:
    """
    Serialize snapshot to JSON or YAML string.

    Args:
        snapshot: StateSnapshot to serialize
        format: Output format ('json' or 'yaml')

    Returns:
        Serialized snapshot string
    """
    data = asdict(snapshot)

    if format == "yaml":
        try:
            return yaml.dump(data, default_flow_style=False, sort_keys=False)
        except NameError:
            raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
    else:
        return json.dumps(data, indent=2)


def save_snapshot(
    snapshot: StateSnapshot,
    path: Union[str, Path],
    format: Optional[str] = None
) -> None:
    """
    Save snapshot to file.

    Args:
        snapshot: StateSnapshot to save
        path: File path
        format: Output format (auto-detected from extension if None)
    """
    path = Path(path)

    if format is None:
        format = "yaml" if path.suffix in ['.yaml', '.yml'] else "json"

    content = serialize_snapshot(snapshot, format)

    with open(path, 'w') as f:
        f.write(content)


def load_snapshot(path: Union[str, Path]) -> StateSnapshot:
    """
    Load snapshot from file.

    Args:
        path: File path to snapshot

    Returns:
        StateSnapshot object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If checksum verification fails
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Snapshot file not found: {path}")

    with open(path, 'r') as f:
        if path.suffix in ['.yaml', '.yml']:
            try:
                data = yaml.safe_load(f)
            except NameError:
                raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
        else:
            data = json.load(f)

    # Verify checksum
    stored_checksum = data.get('checksum')
    if stored_checksum:
        data_without_checksum = {k: v for k, v in data.items() if k != 'checksum'}
        actual_checksum = compute_state_checksum(data_without_checksum)

        if actual_checksum != stored_checksum:
            raise ValueError(
                f"Snapshot checksum mismatch. "
                f"Expected: {stored_checksum}, Got: {actual_checksum}"
            )

    # Create StateSnapshot instance
    return StateSnapshot(**{
        k: v for k, v in data.items()
        if k in StateSnapshot.__dataclass_fields__
    })


def compare_snapshots(
    snapshot1: StateSnapshot,
    snapshot2: StateSnapshot
) -> Dict[str, Any]:
    """
    Compare two snapshots and identify differences.

    Args:
        snapshot1: First snapshot
        snapshot2: Second snapshot

    Returns:
        Dictionary describing differences
    """
    differences = {
        "checksum_changed": snapshot1.checksum != snapshot2.checksum,
        "timestamp_delta": snapshot2.timestamp,  # Could compute time difference
        "changed_sections": []
    }

    # Check each major section
    if snapshot1.identity_state != snapshot2.identity_state:
        differences["changed_sections"].append("identity_state")

    if snapshot1.continuity_state != snapshot2.continuity_state:
        differences["changed_sections"].append("continuity_state")

    if snapshot1.vault_state != snapshot2.vault_state:
        differences["changed_sections"].append("vault_state")

    return differences

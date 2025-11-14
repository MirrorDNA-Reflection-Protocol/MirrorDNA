"""
MirrorDNA - Identity and Continuity Protocol

The architecture of persistence for AI agents and users.

This package provides the core protocol implementation including:
- Configuration loading and validation
- Checksum computation and verification
- Timeline event management
- State snapshot capture and serialization
"""

__version__ = "1.0.0"

from .config_loader import ConfigLoader, MasterCitation, VaultConfig
from .checksum import (
    compute_file_checksum,
    compute_state_checksum,
    compute_text_checksum,
    verify_checksum
)
from .timeline import Timeline, TimelineEvent
from .state_snapshot import (
    StateSnapshot,
    capture_snapshot,
    serialize_snapshot,
    save_snapshot,
    load_snapshot,
    compare_snapshots
)

__all__ = [
    # Config loading
    "ConfigLoader",
    "MasterCitation",
    "VaultConfig",
    # Checksumming
    "compute_file_checksum",
    "compute_state_checksum",
    "compute_text_checksum",
    "verify_checksum",
    # Timeline
    "Timeline",
    "TimelineEvent",
    # State snapshots
    "StateSnapshot",
    "capture_snapshot",
    "serialize_snapshot",
    "save_snapshot",
    "load_snapshot",
    "compare_snapshots",
]

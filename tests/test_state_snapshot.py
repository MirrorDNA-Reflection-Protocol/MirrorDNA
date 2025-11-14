"""
Tests for StateSnapshot capture and management.
"""

import pytest
import json
from pathlib import Path
from mirrordna import (
    StateSnapshot,
    capture_snapshot,
    serialize_snapshot,
    save_snapshot,
    load_snapshot,
    compare_snapshots,
    compute_state_checksum
)


class TestSnapshotCapture:
    """Test snapshot capture functionality."""

    def test_capture_snapshot_minimal(self):
        """Test capturing snapshot with minimal required fields."""
        snapshot = capture_snapshot(
            snapshot_id="test_001",
            identity_state={"id": "alice"},
            continuity_state={"session_count": 1}
        )

        assert isinstance(snapshot, StateSnapshot)
        assert snapshot.snapshot_id == "test_001"
        assert snapshot.identity_state == {"id": "alice"}
        assert snapshot.continuity_state == {"session_count": 1}
        assert snapshot.checksum is not None
        assert snapshot.timestamp is not None
        assert snapshot.version is not None

    def test_capture_snapshot_full(self):
        """Test capturing snapshot with all fields."""
        snapshot = capture_snapshot(
            snapshot_id="test_full",
            identity_state={"id": "alice", "created": "2025-01-01"},
            continuity_state={"sessions": 5, "events": 100},
            vault_state={"vault_id": "vault_001", "entries": 10},
            timeline_summary={"total_events": 100, "event_types": {"session_start": 5}},
            metadata={"note": "Test snapshot"},
            version="1.0.0"
        )

        assert snapshot.snapshot_id == "test_full"
        assert snapshot.vault_state == {"vault_id": "vault_001", "entries": 10}
        assert snapshot.timeline_summary is not None
        assert snapshot.metadata == {"note": "Test snapshot"}
        assert snapshot.version == "1.0.0"

    def test_snapshot_has_timestamp(self):
        """Test that snapshot has ISO 8601 timestamp."""
        snapshot = capture_snapshot(
            "test",
            identity_state={},
            continuity_state={}
        )

        assert "T" in snapshot.timestamp  # ISO 8601 format
        assert snapshot.timestamp.endswith("Z")  # UTC timezone

    def test_snapshot_has_checksum(self):
        """Test that snapshot has SHA-256 checksum."""
        snapshot = capture_snapshot(
            "test",
            identity_state={"id": "test"},
            continuity_state={"count": 1}
        )

        assert snapshot.checksum is not None
        assert len(snapshot.checksum) == 64  # SHA-256 hex length


class TestSnapshotSerialization:
    """Test snapshot serialization."""

    def test_serialize_to_json(self):
        """Test serializing snapshot to JSON."""
        snapshot = capture_snapshot(
            "test",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 1}
        )

        json_str = serialize_snapshot(snapshot, format="json")

        assert isinstance(json_str, str)

        # Verify it's valid JSON
        data = json.loads(json_str)
        assert data["snapshot_id"] == "test"
        assert data["identity_state"] == {"id": "alice"}

    def test_serialize_to_yaml(self):
        """Test serializing snapshot to YAML."""
        pytest.importorskip("yaml")  # Skip if PyYAML not installed

        snapshot = capture_snapshot(
            "test",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 1}
        )

        yaml_str = serialize_snapshot(snapshot, format="yaml")

        assert isinstance(yaml_str, str)
        assert "snapshot_id:" in yaml_str
        assert "test" in yaml_str


class TestSnapshotPersistence:
    """Test snapshot save/load operations."""

    def test_save_snapshot_json(self, tmp_path):
        """Test saving snapshot to JSON file."""
        snapshot = capture_snapshot(
            "test_save",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5}
        )

        file_path = tmp_path / "snapshot.json"
        save_snapshot(snapshot, file_path)

        assert file_path.exists()

        # Verify content
        with open(file_path) as f:
            data = json.load(f)

        assert data["snapshot_id"] == "test_save"
        assert data["identity_state"] == {"id": "alice"}

    def test_save_snapshot_yaml(self, tmp_path):
        """Test saving snapshot to YAML file."""
        pytest.importorskip("yaml")

        snapshot = capture_snapshot(
            "test_save_yaml",
            identity_state={"id": "bob"},
            continuity_state={"sessions": 3}
        )

        file_path = tmp_path / "snapshot.yaml"
        save_snapshot(snapshot, file_path)

        assert file_path.exists()

    def test_save_snapshot_auto_detect_format(self, tmp_path):
        """Test auto-detecting format from file extension."""
        snapshot = capture_snapshot(
            "test",
            identity_state={},
            continuity_state={}
        )

        # JSON extension
        json_path = tmp_path / "test.json"
        save_snapshot(snapshot, json_path)
        assert json_path.exists()

        # YAML extension
        pytest.importorskip("yaml")
        yaml_path = tmp_path / "test.yml"
        save_snapshot(snapshot, yaml_path)
        assert yaml_path.exists()

    def test_load_snapshot_json(self, tmp_path):
        """Test loading snapshot from JSON file."""
        # Create and save snapshot
        original = capture_snapshot(
            "test_load",
            identity_state={"id": "charlie", "name": "Charlie"},
            continuity_state={"sessions": 7, "events": 200},
            vault_state={"entries": 15}
        )

        file_path = tmp_path / "snapshot.json"
        save_snapshot(original, file_path)

        # Load snapshot
        loaded = load_snapshot(file_path)

        assert isinstance(loaded, StateSnapshot)
        assert loaded.snapshot_id == "test_load"
        assert loaded.identity_state == {"id": "charlie", "name": "Charlie"}
        assert loaded.continuity_state == {"sessions": 7, "events": 200}
        assert loaded.vault_state == {"entries": 15}
        assert loaded.checksum == original.checksum

    def test_load_snapshot_yaml(self, tmp_path):
        """Test loading snapshot from YAML file."""
        pytest.importorskip("yaml")

        original = capture_snapshot(
            "test_yaml",
            identity_state={"id": "dave"},
            continuity_state={"sessions": 2}
        )

        file_path = tmp_path / "snapshot.yaml"
        save_snapshot(original, file_path)

        loaded = load_snapshot(file_path)

        assert loaded.snapshot_id == "test_yaml"
        assert loaded.identity_state == {"id": "dave"}

    def test_load_snapshot_not_found(self):
        """Test error when loading non-existent snapshot."""
        with pytest.raises(FileNotFoundError):
            load_snapshot("/nonexistent/snapshot.json")

    def test_load_snapshot_verifies_checksum(self, tmp_path):
        """Test that loading snapshot verifies checksum."""
        snapshot = capture_snapshot(
            "test",
            identity_state={"id": "test"},
            continuity_state={"count": 1}
        )

        file_path = tmp_path / "snapshot.json"
        save_snapshot(snapshot, file_path)

        # Tamper with file
        with open(file_path) as f:
            data = json.load(f)

        data["identity_state"]["id"] = "tampered"

        with open(file_path, "w") as f:
            json.dump(data, f)

        # Loading should fail due to checksum mismatch
        with pytest.raises(ValueError, match="checksum mismatch"):
            load_snapshot(file_path)


class TestSnapshotComparison:
    """Test snapshot comparison."""

    def test_compare_identical_snapshots(self):
        """Test comparing identical snapshots."""
        snapshot1 = capture_snapshot(
            "test1",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5}
        )

        snapshot2 = capture_snapshot(
            "test2",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5}
        )

        # Checksums will differ due to different IDs and timestamps
        diff = compare_snapshots(snapshot1, snapshot2)

        assert diff["checksum_changed"] is True

    def test_compare_different_identity_state(self):
        """Test detecting changes in identity state."""
        snapshot1 = capture_snapshot(
            "test1",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5}
        )

        snapshot2 = capture_snapshot(
            "test2",
            identity_state={"id": "bob"},  # Changed
            continuity_state={"sessions": 5}
        )

        diff = compare_snapshots(snapshot1, snapshot2)

        assert "identity_state" in diff["changed_sections"]

    def test_compare_different_continuity_state(self):
        """Test detecting changes in continuity state."""
        snapshot1 = capture_snapshot(
            "test1",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5}
        )

        snapshot2 = capture_snapshot(
            "test2",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 10}  # Changed
        )

        diff = compare_snapshots(snapshot1, snapshot2)

        assert "continuity_state" in diff["changed_sections"]

    def test_compare_different_vault_state(self):
        """Test detecting changes in vault state."""
        snapshot1 = capture_snapshot(
            "test1",
            identity_state={},
            continuity_state={},
            vault_state={"entries": 5}
        )

        snapshot2 = capture_snapshot(
            "test2",
            identity_state={},
            continuity_state={},
            vault_state={"entries": 10}  # Changed
        )

        diff = compare_snapshots(snapshot1, snapshot2)

        assert "vault_state" in diff["changed_sections"]

    def test_compare_multiple_changes(self):
        """Test detecting multiple changed sections."""
        snapshot1 = capture_snapshot(
            "test1",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 5},
            vault_state={"entries": 10}
        )

        snapshot2 = capture_snapshot(
            "test2",
            identity_state={"id": "bob"},  # Changed
            continuity_state={"sessions": 10},  # Changed
            vault_state={"entries": 10}  # Same
        )

        diff = compare_snapshots(snapshot1, snapshot2)

        assert "identity_state" in diff["changed_sections"]
        assert "continuity_state" in diff["changed_sections"]
        assert "vault_state" not in diff["changed_sections"]


class TestSnapshotIntegrity:
    """Test snapshot checksum integrity."""

    def test_checksum_changes_when_state_changes(self):
        """Test that checksum changes when state changes."""
        snapshot1 = capture_snapshot(
            "test",
            identity_state={"id": "alice"},
            continuity_state={"count": 1}
        )

        snapshot2 = capture_snapshot(
            "test",
            identity_state={"id": "alice"},
            continuity_state={"count": 2}  # Changed
        )

        assert snapshot1.checksum != snapshot2.checksum

    def test_checksum_deterministic_for_same_state(self):
        """Test that same state produces same checksum."""
        identity_state = {"id": "alice", "created": "2025-01-01"}
        continuity_state = {"sessions": 5}

        # Compute checksums for same data
        snapshot_data = {
            "snapshot_id": "test",
            "timestamp": "2025-11-14T10:00:00Z",
            "version": "1.0.0",
            "identity_state": identity_state,
            "continuity_state": continuity_state,
            "vault_state": None,
            "timeline_summary": None,
            "metadata": None
        }

        checksum1 = compute_state_checksum(snapshot_data)
        checksum2 = compute_state_checksum(snapshot_data)

        assert checksum1 == checksum2

    def test_round_trip_preserves_checksum(self, tmp_path):
        """Test that save/load round trip preserves checksum."""
        original = capture_snapshot(
            "test_roundtrip",
            identity_state={"id": "alice"},
            continuity_state={"sessions": 3}
        )

        file_path = tmp_path / "snapshot.json"
        save_snapshot(original, file_path)

        loaded = load_snapshot(file_path)

        assert loaded.checksum == original.checksum


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

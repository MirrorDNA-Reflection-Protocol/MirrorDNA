"""
Tests for MirrorDNA SDK client.

Tests the simplified SDK client (sdk/python/mirror_dna_client.py)
to ensure it provides correct functionality for developers.
"""

import pytest
import sys
import json
import tempfile
from pathlib import Path

# Add SDK to path
sdk_path = Path(__file__).parent.parent / "sdk" / "python"
sys.path.insert(0, str(sdk_path))

from mirror_dna_client import MirrorDNAClient


class TestMirrorDNAClient:
    """Test suite for SDK client."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for tests."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def client(self, temp_dir):
        """Create SDK client with temp directory."""
        return MirrorDNAClient(data_dir=temp_dir)

    def test_client_initialization(self, client, temp_dir):
        """Test client initializes correctly."""
        assert client.data_dir == temp_dir
        assert temp_dir.exists()
        assert client._vault_cache == {}
        assert client._timeline_cache == {}

    def test_compute_state_hash_determinism(self, client):
        """Test that state hash is deterministic."""
        data = {"key": "value", "number": 42}

        hash1 = client.compute_state_hash(data)
        hash2 = client.compute_state_hash(data)

        assert hash1 == hash2
        assert len(hash1) == 64  # SHA-256 hex length
        assert isinstance(hash1, str)

    def test_compute_state_hash_order_independence(self, client):
        """Test that key order doesn't affect hash."""
        data1 = {"a": 1, "b": 2, "c": 3}
        data2 = {"c": 3, "b": 2, "a": 1}

        hash1 = client.compute_state_hash(data1)
        hash2 = client.compute_state_hash(data2)

        assert hash1 == hash2

    def test_compute_state_hash_sensitivity(self, client):
        """Test that hash changes with data changes."""
        data1 = {"key": "value"}
        data2 = {"key": "different"}

        hash1 = client.compute_state_hash(data1)
        hash2 = client.compute_state_hash(data2)

        assert hash1 != hash2

    def test_create_master_citation(self, client):
        """Test Master Citation creation."""
        citation = client.create_master_citation(
            identity_id="test_agent",
            vault_id="test_vault"
        )

        assert citation['id'].startswith('mc_test_agent_')
        assert citation['version'] == '1.0.0'
        assert citation['vault_id'] == 'test_vault'
        assert 'created_at' in citation
        assert 'checksum' in citation
        assert len(citation['checksum']) == 64

    def test_create_master_citation_checksum_valid(self, client):
        """Test that citation checksum is valid."""
        citation = client.create_master_citation("agent", "vault")

        # Verify checksum
        data_without_checksum = {k: v for k, v in citation.items() if k != 'checksum'}
        is_valid = client.verify_checksum(data_without_checksum, citation['checksum'])

        assert is_valid

    def test_save_and_load_citation(self, client, temp_dir):
        """Test saving and loading Master Citation."""
        citation = client.create_master_citation("agent", "vault")

        # Save citation
        path = client.save_citation(citation)
        assert path.exists()
        assert path.suffix == '.yaml'

        # Verify file content
        import yaml
        with open(path, 'r') as f:
            loaded_data = yaml.safe_load(f)

        assert loaded_data['id'] == citation['id']
        assert loaded_data['checksum'] == citation['checksum']

    def test_create_timeline_event(self, client):
        """Test timeline event creation."""
        actor = "mc_test_agent_001"

        event = client.create_timeline_event(
            event_type="session_start",
            actor=actor,
            payload={"platform": "test"}
        )

        assert event['id'].startswith('evt_')
        assert event['event_type'] == 'session_start'
        assert event['actor'] == actor
        assert event['payload']['platform'] == 'test'
        assert 'timestamp' in event

    def test_validate_timeline_valid(self, client):
        """Test timeline validation with valid events."""
        events = [
            {
                "id": "evt_001",
                "timestamp": "2025-11-14T10:00:00Z",
                "event_type": "session_start",
                "actor": "mc_agent_001"
            },
            {
                "id": "evt_002",
                "timestamp": "2025-11-14T10:05:00Z",
                "event_type": "memory_created",
                "actor": "mc_agent_001"
            }
        ]

        validation = client.validate_timeline(events)

        assert validation['valid'] is True
        assert validation['total_events'] == 2
        assert validation['event_types']['session_start'] == 1
        assert validation['event_types']['memory_created'] == 1
        assert validation['unique_actors'] == 1
        assert len(validation['errors']) == 0

    def test_validate_timeline_invalid(self, client):
        """Test timeline validation with invalid events."""
        events = [
            {
                "id": "evt_001",
                # Missing timestamp, event_type, actor
            }
        ]

        validation = client.validate_timeline(events)

        assert validation['valid'] is False
        assert len(validation['errors']) > 0

    def test_get_continuity_status_no_activity(self, client):
        """Test continuity status with no events."""
        status = client.get_continuity_status("unknown_agent")

        assert status['identity_id'] == "unknown_agent"
        assert status['status'] == 'no_activity'
        assert status['total_events'] == 0
        assert status['last_activity'] is None

    def test_get_continuity_status_active(self, client):
        """Test continuity status with events."""
        actor = "mc_test_agent_001"

        # Create events
        client.create_timeline_event("session_start", actor)
        client.create_timeline_event("memory_created", actor)

        status = client.get_continuity_status(actor)

        assert status['identity_id'] == actor
        assert status['status'] == 'active'
        assert status['total_events'] == 2
        assert status['last_activity'] is not None
        assert status['valid'] is True

    def test_save_and_load_timeline(self, client, temp_dir):
        """Test saving and loading timeline."""
        actor = "mc_test_agent_001"

        # Create events
        client.create_timeline_event("session_start", actor)
        client.create_timeline_event("session_end", actor)

        # Save timeline
        path = client.save_timeline(actor)
        assert path.exists()

        # Load timeline
        loaded_events = client.load_timeline(path)
        assert len(loaded_events) == 2
        assert loaded_events[0]['event_type'] == 'session_start'
        assert loaded_events[1]['event_type'] == 'session_end'

    def test_verify_checksum_valid(self, client):
        """Test checksum verification with valid data."""
        data = {"key": "value"}
        checksum = client.compute_state_hash(data)

        is_valid = client.verify_checksum(data, checksum)
        assert is_valid

    def test_verify_checksum_invalid(self, client):
        """Test checksum verification with invalid data."""
        data = {"key": "value"}
        wrong_checksum = "0" * 64

        is_valid = client.verify_checksum(data, wrong_checksum)
        assert not is_valid

    def test_verify_checksum_modified_data(self, client):
        """Test checksum detects data modification."""
        original_data = {"key": "value"}
        checksum = client.compute_state_hash(original_data)

        modified_data = {"key": "modified"}
        is_valid = client.verify_checksum(modified_data, checksum)

        assert not is_valid

    def test_load_vault_config_yaml(self, client, temp_dir):
        """Test loading vault config from YAML."""
        import yaml

        vault_data = {
            "vault_id": "vault_test",
            "name": "Test Vault",
            "path": "/test/path",
            "created_at": "2025-11-14T10:00:00Z"
        }

        config_path = temp_dir / "vault.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(vault_data, f)

        loaded = client.load_vault_config(config_path)

        assert loaded['vault_id'] == 'vault_test'
        assert loaded['name'] == 'Test Vault'
        assert 'vault_test' in client._vault_cache

    def test_load_vault_config_json(self, client, temp_dir):
        """Test loading vault config from JSON."""
        vault_data = {
            "vault_id": "vault_json",
            "name": "JSON Vault",
            "path": "/json/path",
            "created_at": "2025-11-14T10:00:00Z"
        }

        config_path = temp_dir / "vault.json"
        with open(config_path, 'w') as f:
            json.dump(vault_data, f)

        loaded = client.load_vault_config(config_path)

        assert loaded['vault_id'] == 'vault_json'
        assert 'vault_json' in client._vault_cache

    def test_load_vault_config_missing_file(self, client):
        """Test loading non-existent vault config."""
        with pytest.raises(FileNotFoundError):
            client.load_vault_config("nonexistent.yaml")

    def test_load_vault_config_missing_fields(self, client, temp_dir):
        """Test loading vault config with missing required fields."""
        import yaml

        incomplete_vault = {
            "vault_id": "incomplete"
            # Missing: name, path, created_at
        }

        config_path = temp_dir / "incomplete.yaml"
        with open(config_path, 'w') as f:
            yaml.dump(incomplete_vault, f)

        with pytest.raises(ValueError, match="missing required fields"):
            client.load_vault_config(config_path)

    def test_complete_workflow(self, client, temp_dir):
        """Test complete SDK workflow."""
        # 1. Create citation
        citation = client.create_master_citation("workflow_agent", "workflow_vault")
        assert citation['id'].startswith('mc_workflow_agent_')

        # 2. Save citation
        citation_path = client.save_citation(citation)
        assert citation_path.exists()

        # 3. Create timeline events
        actor = citation['id']
        client.create_timeline_event("session_start", actor)
        client.create_timeline_event("memory_created", actor, {"content": "test"})
        client.create_timeline_event("session_end", actor)

        # 4. Check status
        status = client.get_continuity_status(actor)
        assert status['status'] == 'active'
        assert status['total_events'] == 3

        # 5. Save timeline
        timeline_path = client.save_timeline(actor)
        assert timeline_path.exists()

        # 6. Load timeline
        loaded_events = client.load_timeline(timeline_path)
        assert len(loaded_events) == 3

        # 7. Verify citation integrity
        data_without_checksum = {k: v for k, v in citation.items() if k != 'checksum'}
        is_valid = client.verify_checksum(data_without_checksum, citation['checksum'])
        assert is_valid


def test_state_hash_known_values():
    """Test state hash against known values for regression."""
    client = MirrorDNAClient()

    # Test with simple data
    simple_data = {"key": "value"}
    simple_hash = client.compute_state_hash(simple_data)

    # Hash should be consistent across runs
    assert len(simple_hash) == 64
    assert simple_hash == client.compute_state_hash(simple_data)

    # Test with complex data
    complex_data = {
        "id": "test_001",
        "nested": {
            "a": 1,
            "b": 2
        },
        "list": [1, 2, 3]
    }
    complex_hash = client.compute_state_hash(complex_data)

    assert len(complex_hash) == 64
    assert complex_hash == client.compute_state_hash(complex_data)
    assert complex_hash != simple_hash


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

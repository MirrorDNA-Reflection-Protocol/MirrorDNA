# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Tests for ConfigLoader - Master Citation and Vault Config loading.
"""

import pytest
import yaml
import json
from pathlib import Path
from mirrordna import ConfigLoader, MasterCitation, VaultConfig, compute_state_checksum


@pytest.fixture
def temp_citation_file(tmp_path):
    """Create a temporary Master Citation file."""
    citation_data = {
        "id": "mc_test_agent_001",
        "version": "1.0.0",
        "vault_id": "vault_test_main",
        "created_at": "2025-11-14T10:00:00Z",
        "predecessor": None,
        "successor": None,
        "constitutional_alignment": {
            "compliance_level": "full",
            "framework_version": "1.0"
        }
    }

    # Compute checksum
    checksum = compute_state_checksum(citation_data)
    citation_data["checksum"] = checksum

    # Save to file
    citation_path = tmp_path / "test_citation.yaml"
    with open(citation_path, "w") as f:
        yaml.dump(citation_data, f)

    return citation_path


@pytest.fixture
def temp_vault_file(tmp_path):
    """Create a temporary Vault Config file."""
    vault_data = {
        "vault_id": "vault_test_main",
        "version": "1.0.0",
        "created_at": "2025-11-14T10:00:00Z",
        "storage": {
            "type": "filesystem",
            "root_path": str(tmp_path / "vault_data")
        }
    }

    vault_path = tmp_path / "test_vault.yaml"
    with open(vault_path, "w") as f:
        yaml.dump(vault_data, f)

    return vault_path


class TestConfigLoader:
    """Test ConfigLoader functionality."""

    def test_init(self):
        """Test ConfigLoader initialization."""
        loader = ConfigLoader()
        assert loader is not None

    def test_load_master_citation_yaml(self, temp_citation_file):
        """Test loading Master Citation from YAML."""
        loader = ConfigLoader()
        citation = loader.load_master_citation(temp_citation_file)

        assert isinstance(citation, MasterCitation)
        assert citation.id == "mc_test_agent_001"
        assert citation.version == "1.0.0"
        assert citation.vault_id == "vault_test_main"
        assert citation.created_at == "2025-11-14T10:00:00Z"
        assert citation.checksum is not None

    def test_load_master_citation_json(self, tmp_path):
        """Test loading Master Citation from JSON."""
        citation_data = {
            "id": "mc_test_json_001",
            "version": "1.0.0",
            "vault_id": "vault_test_json",
            "created_at": "2025-11-14T10:00:00Z"
        }

        checksum = compute_state_checksum(citation_data)
        citation_data["checksum"] = checksum

        citation_path = tmp_path / "test_citation.json"
        with open(citation_path, "w") as f:
            json.dump(citation_data, f)

        loader = ConfigLoader()
        citation = loader.load_master_citation(citation_path)

        assert citation.id == "mc_test_json_001"
        assert citation.vault_id == "vault_test_json"

    def test_load_master_citation_checksum_verification(self, tmp_path):
        """Test that checksum is verified when loading."""
        citation_data = {
            "id": "mc_test_bad_checksum",
            "version": "1.0.0",
            "vault_id": "vault_test",
            "created_at": "2025-11-14T10:00:00Z",
            "checksum": "invalid_checksum_value"
        }

        citation_path = tmp_path / "bad_citation.yaml"
        with open(citation_path, "w") as f:
            yaml.dump(citation_data, f)

        loader = ConfigLoader()

        with pytest.raises(ValueError, match="Checksum mismatch"):
            loader.load_master_citation(citation_path, verify_checksum=True)

    def test_load_master_citation_skip_verification(self, tmp_path):
        """Test loading without checksum verification."""
        citation_data = {
            "id": "mc_test_no_verify",
            "version": "1.0.0",
            "vault_id": "vault_test",
            "created_at": "2025-11-14T10:00:00Z",
            "checksum": "any_value"
        }

        citation_path = tmp_path / "citation.yaml"
        with open(citation_path, "w") as f:
            yaml.dump(citation_data, f)

        loader = ConfigLoader()
        citation = loader.load_master_citation(citation_path, verify_checksum=False)

        assert citation.id == "mc_test_no_verify"

    def test_load_master_citation_file_not_found(self):
        """Test error when citation file doesn't exist."""
        loader = ConfigLoader()

        with pytest.raises(FileNotFoundError):
            loader.load_master_citation("/nonexistent/path.yaml")

    def test_load_vault_config_yaml(self, temp_vault_file):
        """Test loading Vault Config from YAML."""
        loader = ConfigLoader()
        vault = loader.load_vault_config(temp_vault_file)

        assert isinstance(vault, VaultConfig)
        assert vault.vault_id == "vault_test_main"
        assert vault.version == "1.0.0"
        assert vault.storage["type"] == "filesystem"

    def test_load_vault_config_json(self, tmp_path):
        """Test loading Vault Config from JSON."""
        vault_data = {
            "vault_id": "vault_json_test",
            "version": "1.0.0",
            "created_at": "2025-11-14T10:00:00Z",
            "storage": {
                "type": "database",
                "connection_string": "sqlite:///test.db"
            }
        }

        vault_path = tmp_path / "vault.json"
        with open(vault_path, "w") as f:
            json.dump(vault_data, f)

        loader = ConfigLoader()
        vault = loader.load_vault_config(vault_path)

        assert vault.vault_id == "vault_json_test"
        assert vault.storage["type"] == "database"

    def test_master_citation_with_lineage(self, tmp_path):
        """Test Master Citation with predecessor/successor."""
        citation_data = {
            "id": "mc_test_v2",
            "version": "1.0.0",
            "vault_id": "vault_test",
            "created_at": "2025-11-14T10:00:00Z",
            "predecessor": "mc_test_v1",
            "successor": "mc_test_v3"
        }

        checksum = compute_state_checksum(citation_data)
        citation_data["checksum"] = checksum

        citation_path = tmp_path / "citation_lineage.yaml"
        with open(citation_path, "w") as f:
            yaml.dump(citation_data, f)

        loader = ConfigLoader()
        citation = loader.load_master_citation(citation_path)

        assert citation.predecessor == "mc_test_v1"
        assert citation.successor == "mc_test_v3"

    def test_master_citation_with_constitutional_alignment(self, tmp_path):
        """Test Master Citation with full constitutional alignment."""
        citation_data = {
            "id": "mc_test_constitutional",
            "version": "1.0.0",
            "vault_id": "vault_test",
            "created_at": "2025-11-14T10:00:00Z",
            "constitutional_alignment": {
                "compliance_level": "full",
                "framework_version": "1.0",
                "rights_bundle": ["memory", "continuity", "portability"],
                "constraints": []
            }
        }

        checksum = compute_state_checksum(citation_data)
        citation_data["checksum"] = checksum

        citation_path = tmp_path / "citation_constitutional.yaml"
        with open(citation_path, "w") as f:
            yaml.dump(citation_data, f)

        loader = ConfigLoader()
        citation = loader.load_master_citation(citation_path)

        assert citation.constitutional_alignment is not None
        assert citation.constitutional_alignment["compliance_level"] == "full"
        assert "memory" in citation.constitutional_alignment["rights_bundle"]

    def test_master_citation_with_metadata(self, tmp_path):
        """Test Master Citation with metadata."""
        citation_data = {
            "id": "mc_test_metadata",
            "version": "1.0.0",
            "vault_id": "vault_test",
            "created_at": "2025-11-14T10:00:00Z",
            "metadata": {
                "display_name": "Test Agent",
                "description": "Agent for testing",
                "tags": ["test", "agent"]
            }
        }

        checksum = compute_state_checksum(citation_data)
        citation_data["checksum"] = checksum

        citation_path = tmp_path / "citation_metadata.yaml"
        with open(citation_path, "w") as f:
            yaml.dump(citation_data, f)

        loader = ConfigLoader()
        citation = loader.load_master_citation(citation_path)

        assert citation.metadata is not None
        assert citation.metadata["display_name"] == "Test Agent"
        assert "test" in citation.metadata["tags"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

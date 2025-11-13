"""
Tests for identity module.
"""

import pytest
from mirrordna.identity import IdentityManager
from mirrordna.storage import JSONFileStorage
import tempfile
from pathlib import Path


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONFileStorage(Path(tmpdir))
        yield storage


def test_create_user_identity(temp_storage):
    """Test creating a user identity."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity(
        identity_type="user",
        metadata={"name": "Test User"}
    )

    assert identity["identity_id"].startswith("mdna_usr_")
    assert identity["identity_type"] == "user"
    assert identity["public_key"] is not None
    assert "_private_key" in identity
    assert identity["metadata"]["name"] == "Test User"


def test_create_agent_identity(temp_storage):
    """Test creating an agent identity."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity(
        identity_type="agent",
        metadata={"name": "Test Agent", "version": "1.0.0"}
    )

    assert identity["identity_id"].startswith("mdna_agt_")
    assert identity["identity_type"] == "agent"
    assert identity["metadata"]["name"] == "Test Agent"


def test_create_system_identity(temp_storage):
    """Test creating a system identity."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity(
        identity_type="system",
        metadata={"name": "Test System"}
    )

    assert identity["identity_id"].startswith("mdna_sys_")
    assert identity["identity_type"] == "system"


def test_get_identity(temp_storage):
    """Test retrieving an identity."""
    identity_mgr = IdentityManager(storage=temp_storage)

    # Create identity
    created = identity_mgr.create_identity("user")
    identity_id = created["identity_id"]

    # Retrieve identity
    retrieved = identity_mgr.get_identity(identity_id)

    assert retrieved is not None
    assert retrieved["identity_id"] == identity_id
    assert "_private_key" not in retrieved  # Private key not stored


def test_validate_identity(temp_storage):
    """Test validating an identity."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity("user")

    # Remove private key for validation
    identity.pop("_private_key")

    is_valid = identity_mgr.validate_identity(identity)

    assert is_valid


def test_sign_and_verify_claim(temp_storage):
    """Test signing and verifying a claim."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity("user")
    identity_id = identity["identity_id"]
    private_key = identity["_private_key"]

    claim = "I am the legitimate user"

    # Sign claim
    signature = identity_mgr.sign_claim(identity_id, claim, private_key)

    assert signature is not None

    # Verify claim
    is_valid = identity_mgr.verify_claim(identity_id, claim, signature)

    assert is_valid


def test_verify_invalid_claim(temp_storage):
    """Test verifying an invalid claim."""
    identity_mgr = IdentityManager(storage=temp_storage)

    identity = identity_mgr.create_identity("user")
    identity_id = identity["identity_id"]
    private_key = identity["_private_key"]

    claim = "Original claim"
    tampered_claim = "Tampered claim"

    # Sign original claim
    signature = identity_mgr.sign_claim(identity_id, claim, private_key)

    # Verify with tampered claim
    is_valid = identity_mgr.verify_claim(identity_id, tampered_claim, signature)

    assert not is_valid


def test_invalid_identity_type(temp_storage):
    """Test creating identity with invalid type."""
    identity_mgr = IdentityManager(storage=temp_storage)

    with pytest.raises(ValueError):
        identity_mgr.create_identity("invalid_type")

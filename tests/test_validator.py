"""
Tests for validator module.
"""

import pytest
from mirrordna.validator import validate_schema, ValidationResult


def test_validate_valid_identity():
    """Test validation of a valid identity."""
    identity = {
        "identity_id": "mdna_usr_test123abc456",
        "identity_type": "user",
        "created_at": "2025-01-15T10:00:00Z",
        "public_key": "MCowBQYDK2VwAyEAGb9ECWmEzf6FQbrBZ9w7lP"
    }

    result = validate_schema(identity, "identity")

    assert result.is_valid
    assert len(result.errors) == 0
    assert result.schema_name == "identity"


def test_validate_invalid_identity_missing_field():
    """Test validation of identity missing required field."""
    identity = {
        "identity_id": "mdna_usr_test123abc456",
        "identity_type": "user",
        "created_at": "2025-01-15T10:00:00Z"
        # Missing public_key
    }

    result = validate_schema(identity, "identity")

    assert not result.is_valid
    assert len(result.errors) > 0


def test_validate_invalid_identity_wrong_type():
    """Test validation of identity with wrong type."""
    identity = {
        "identity_id": "mdna_usr_test123abc456",
        "identity_type": "invalid_type",  # Should be user, agent, or system
        "created_at": "2025-01-15T10:00:00Z",
        "public_key": "MCowBQYDK2VwAyEAGb9ECWmEzf6FQbrBZ9w7lP"
    }

    result = validate_schema(identity, "identity")

    assert not result.is_valid
    assert len(result.errors) > 0


def test_validate_valid_continuity():
    """Test validation of a valid continuity record."""
    continuity = {
        "session_id": "sess_20250115_100030_a7x9k",
        "parent_session_id": None,
        "agent_id": "mdna_agt_mirror01_v2",
        "user_id": "mdna_usr_alice7x9k2m",
        "started_at": "2025-01-15T10:00:30Z",
        "ended_at": None
    }

    result = validate_schema(continuity, "continuity")

    assert result.is_valid
    assert len(result.errors) == 0


def test_validate_valid_memory():
    """Test validation of a valid memory record."""
    memory = {
        "memory_id": "mem_20250115_100045_c3z7n",
        "tier": "long_term",
        "content": "User prefers Python",
        "source": {
            "session_id": "sess_20250115_100030_a7x9k",
            "timestamp": "2025-01-15T10:00:45Z",
            "agent_id": "mdna_agt_mirror01_v2",
            "user_id": "mdna_usr_alice7x9k2m"
        }
    }

    result = validate_schema(memory, "memory")

    assert result.is_valid
    assert len(result.errors) == 0


def test_validate_invalid_memory_wrong_tier():
    """Test validation of memory with invalid tier."""
    memory = {
        "memory_id": "mem_test123",
        "tier": "invalid_tier",  # Should be short_term, long_term, or episodic
        "content": "Some content",
        "source": {
            "session_id": "sess_test456",
            "timestamp": "2025-01-15T10:00:45Z",
            "agent_id": "mdna_agt_test",
            "user_id": "mdna_usr_test"
        }
    }

    result = validate_schema(memory, "memory")

    assert not result.is_valid
    assert len(result.errors) > 0


def test_validate_valid_agent_dna():
    """Test validation of a valid agent DNA record."""
    agent_dna = {
        "agent_dna_id": "dna_mirror01_v2_0_0",
        "agent_id": "mdna_agt_mirror01_v2",
        "version": "2.0.0",
        "personality_traits": {
            "tone": "reflective",
            "style": "conversational",
            "values": ["clarity", "honesty"]
        },
        "behavioral_constraints": [
            "Never impersonate users",
            "Respect privacy"
        ],
        "capabilities": [
            "reflection",
            "memory_management"
        ]
    }

    result = validate_schema(agent_dna, "agent")

    assert result.is_valid
    assert len(result.errors) == 0


def test_validation_result_structure():
    """Test ValidationResult structure."""
    result = ValidationResult(
        is_valid=True,
        errors=[],
        schema_name="test"
    )

    assert result.is_valid
    assert result.errors == []
    assert result.schema_name == "test"

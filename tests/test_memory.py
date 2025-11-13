"""
Tests for memory module.
"""

import pytest
from mirrordna.memory import MemoryManager
from mirrordna.storage import JSONFileStorage
import tempfile
from pathlib import Path


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONFileStorage(Path(tmpdir))
        yield storage


def test_write_short_term_memory(temp_storage):
    """Test writing a short-term memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content="Test short-term memory",
        tier="short_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    assert memory["memory_id"].startswith("mem_")
    assert memory["tier"] == "short_term"
    assert memory["content"] == "Test short-term memory"


def test_write_long_term_memory(temp_storage):
    """Test writing a long-term memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content="User prefers Python",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test",
        metadata={"tags": ["preference"], "relevance_score": 0.9}
    )

    assert memory["tier"] == "long_term"
    assert memory["metadata"]["tags"] == ["preference"]
    assert memory["metadata"]["relevance_score"] == 0.9


def test_write_episodic_memory(temp_storage):
    """Test writing an episodic memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content={"event": "First conversation", "outcome": "successful"},
        tier="episodic",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    assert memory["tier"] == "episodic"
    assert isinstance(memory["content"], dict)
    assert memory["content"]["event"] == "First conversation"


def test_read_memory_by_tier(temp_storage):
    """Test reading memories by tier."""
    memory_mgr = MemoryManager(storage=temp_storage)

    # Write memories
    memory_mgr.write_memory(
        content="Short term 1",
        tier="short_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    memory_mgr.write_memory(
        content="Long term 1",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    # Read short-term memories
    short_term = memory_mgr.read_memory(tier="short_term")

    assert len(short_term) == 1
    assert short_term[0]["tier"] == "short_term"


def test_get_memory(temp_storage):
    """Test retrieving a specific memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    created = memory_mgr.write_memory(
        content="Test memory",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    retrieved = memory_mgr.get_memory(created["memory_id"])

    assert retrieved is not None
    assert retrieved["memory_id"] == created["memory_id"]


def test_update_memory(temp_storage):
    """Test updating a memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content="Original content",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    updated = memory_mgr.update_memory(
        memory["memory_id"],
        {"metadata": {"updated": True}}
    )

    assert updated["metadata"]["updated"] is True


def test_search_memory(temp_storage):
    """Test searching memories."""
    memory_mgr = MemoryManager(storage=temp_storage)

    # Write memories
    memory_mgr.write_memory(
        content="User likes Python programming",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    memory_mgr.write_memory(
        content="User dislikes JavaScript",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    # Search for "Python"
    results = memory_mgr.search_memory("Python", tier="long_term")

    assert len(results) == 1
    assert "Python" in results[0]["content"]


def test_archive_memory(temp_storage):
    """Test archiving a memory."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content="To be archived",
        tier="short_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    archived = memory_mgr.archive_memory(memory["memory_id"])

    assert archived["metadata"]["archived"] is True
    assert "archived_at" in archived["metadata"]


def test_increment_access_count(temp_storage):
    """Test incrementing access count."""
    memory_mgr = MemoryManager(storage=temp_storage)

    memory = memory_mgr.write_memory(
        content="Test memory",
        tier="long_term",
        session_id="sess_test123",
        agent_id="mdna_agt_test",
        user_id="mdna_usr_test"
    )

    # Increment once
    updated = memory_mgr.increment_access_count(memory["memory_id"])
    assert updated["metadata"]["access_count"] == 1

    # Increment again
    updated = memory_mgr.increment_access_count(memory["memory_id"])
    assert updated["metadata"]["access_count"] == 2


def test_invalid_tier(temp_storage):
    """Test writing memory with invalid tier."""
    memory_mgr = MemoryManager(storage=temp_storage)

    with pytest.raises(ValueError):
        memory_mgr.write_memory(
            content="Test",
            tier="invalid_tier",
            session_id="sess_test123",
            agent_id="mdna_agt_test",
            user_id="mdna_usr_test"
        )

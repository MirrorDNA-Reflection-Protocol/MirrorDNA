# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Tests for continuity module.
"""

import pytest
from mirrordna.continuity import ContinuityTracker
from mirrordna.storage import JSONFileStorage
import tempfile
from pathlib import Path


@pytest.fixture
def temp_storage():
    """Create temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = JSONFileStorage(Path(tmpdir))
        yield storage


def test_create_session(temp_storage):
    """Test creating a session."""
    continuity = ContinuityTracker(storage=temp_storage)

    session = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    assert session["session_id"].startswith("sess_")
    assert session["agent_id"] == "mdna_agt_test123"
    assert session["user_id"] == "mdna_usr_test456"
    assert session["parent_session_id"] is None
    assert session["started_at"] is not None
    assert session["ended_at"] is None


def test_create_session_with_parent(temp_storage):
    """Test creating a session with parent."""
    continuity = ContinuityTracker(storage=temp_storage)

    # Create parent session
    parent = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    # Create child session
    child = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456",
        parent_session_id=parent["session_id"]
    )

    assert child["parent_session_id"] == parent["session_id"]


def test_get_session(temp_storage):
    """Test retrieving a session."""
    continuity = ContinuityTracker(storage=temp_storage)

    created = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    retrieved = continuity.get_session(created["session_id"])

    assert retrieved is not None
    assert retrieved["session_id"] == created["session_id"]


def test_end_session(temp_storage):
    """Test ending a session."""
    continuity = ContinuityTracker(storage=temp_storage)

    session = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    ended = continuity.end_session(
        session["session_id"],
        final_state={"outcome": "success"}
    )

    assert ended is not None
    assert ended["ended_at"] is not None
    assert "final_state" in ended.get("context_metadata", {})


def test_get_session_lineage(temp_storage):
    """Test getting session lineage."""
    continuity = ContinuityTracker(storage=temp_storage)

    # Create session chain
    session1 = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    session2 = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456",
        parent_session_id=session1["session_id"]
    )

    session3 = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456",
        parent_session_id=session2["session_id"]
    )

    lineage = continuity.get_session_lineage(session3["session_id"])

    assert len(lineage) == 3
    assert lineage[0]["session_id"] == session1["session_id"]
    assert lineage[1]["session_id"] == session2["session_id"]
    assert lineage[2]["session_id"] == session3["session_id"]


def test_get_context(temp_storage):
    """Test getting aggregated context."""
    continuity = ContinuityTracker(storage=temp_storage)

    session1 = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456",
        context_metadata={"topic": "Introduction"}
    )

    session2 = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456",
        parent_session_id=session1["session_id"],
        context_metadata={"topic": "Advanced"}
    )

    context = continuity.get_context(session2["session_id"])

    assert context["session_count"] == 2
    assert len(context["sessions"]) == 2


def test_session_exists(temp_storage):
    """Test checking if session exists."""
    continuity = ContinuityTracker(storage=temp_storage)

    session = continuity.create_session(
        agent_id="mdna_agt_test123",
        user_id="mdna_usr_test456"
    )

    assert continuity.session_exists(session["session_id"])
    assert not continuity.session_exists("sess_nonexistent")

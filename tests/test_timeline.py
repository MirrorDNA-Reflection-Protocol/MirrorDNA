# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Tests for Timeline event management.
"""

import pytest
import json
from pathlib import Path
from mirrordna import Timeline, TimelineEvent


class TestTimelineCreation:
    """Test Timeline initialization."""

    def test_init(self):
        """Test creating a timeline."""
        timeline = Timeline("test_timeline_001")

        assert timeline.timeline_id == "test_timeline_001"
        assert len(timeline.events) == 0

    def test_init_default_id(self):
        """Test creating a timeline with default ID."""
        timeline = Timeline()

        assert timeline.timeline_id == "default"
        assert len(timeline.events) == 0


class TestTimelineEvents:
    """Test timeline event operations."""

    def test_append_event(self):
        """Test appending an event."""
        timeline = Timeline("test")

        event = timeline.append_event(
            event_type="session_start",
            actor="test_agent"
        )

        assert isinstance(event, TimelineEvent)
        assert event.event_type == "session_start"
        assert event.actor == "test_agent"
        assert event.id is not None
        assert event.timestamp is not None
        assert len(timeline.events) == 1

    def test_append_event_with_payload(self):
        """Test appending event with payload."""
        timeline = Timeline("test")

        event = timeline.append_event(
            event_type="memory_created",
            actor="agent_001",
            payload={"content": "Test memory", "confidence": 0.95}
        )

        assert event.payload == {"content": "Test memory", "confidence": 0.95}

    def test_append_event_with_relationships(self):
        """Test appending event with related IDs."""
        timeline = Timeline("test")

        event = timeline.append_event(
            event_type="citation_created",
            actor="agent_001",
            related_vault_id="vault_main",
            related_agent_id="agent_001",
            related_session_id="session_042"
        )

        assert event.related_vault_id == "vault_main"
        assert event.related_agent_id == "agent_001"
        assert event.related_session_id == "session_042"

    def test_append_event_with_tags(self):
        """Test appending event with tags."""
        timeline = Timeline("test")

        event = timeline.append_event(
            event_type="memory_created",
            actor="agent_001",
            tags=["important", "user_preference"]
        )

        assert event.tags == ["important", "user_preference"]

    def test_append_multiple_events(self):
        """Test appending multiple events."""
        timeline = Timeline("test")

        event1 = timeline.append_event("session_start", "agent_001")
        event2 = timeline.append_event("memory_created", "agent_001")
        event3 = timeline.append_event("session_end", "agent_001")

        assert len(timeline.events) == 3
        assert timeline.events[0] == event1
        assert timeline.events[1] == event2
        assert timeline.events[2] == event3

    def test_event_ids_are_unique(self):
        """Test that event IDs are unique."""
        timeline = Timeline("test")

        event1 = timeline.append_event("session_start", "agent_001")
        event2 = timeline.append_event("session_start", "agent_001")

        assert event1.id != event2.id

    def test_event_ids_are_sequential(self):
        """Test that event IDs increment."""
        timeline = Timeline("test")

        event1 = timeline.append_event("test_event", "actor")
        event2 = timeline.append_event("test_event", "actor")

        # Event IDs should contain incrementing counters
        assert event1.id < event2.id


class TestTimelineQuerying:
    """Test timeline query operations."""

    @pytest.fixture
    def populated_timeline(self):
        """Create a timeline with multiple events."""
        timeline = Timeline("test")

        timeline.append_event("session_start", "agent_001")
        timeline.append_event("memory_created", "agent_001")
        timeline.append_event("memory_created", "agent_002")
        timeline.append_event("session_end", "agent_001")
        timeline.append_event("session_start", "agent_002")

        return timeline

    def test_get_events_all(self, populated_timeline):
        """Test getting all events."""
        events = populated_timeline.get_events()

        assert len(events) == 5

    def test_get_events_by_type(self, populated_timeline):
        """Test filtering events by type."""
        events = populated_timeline.get_events(event_type="session_start")

        assert len(events) == 2
        assert all(e.event_type == "session_start" for e in events)

    def test_get_events_by_actor(self, populated_timeline):
        """Test filtering events by actor."""
        events = populated_timeline.get_events(actor="agent_001")

        assert len(events) == 3
        assert all(e.actor == "agent_001" for e in events)

    def test_get_events_by_type_and_actor(self, populated_timeline):
        """Test filtering by both type and actor."""
        events = populated_timeline.get_events(
            event_type="memory_created",
            actor="agent_001"
        )

        assert len(events) == 1
        assert events[0].event_type == "memory_created"
        assert events[0].actor == "agent_001"

    def test_get_events_with_limit(self, populated_timeline):
        """Test limiting number of returned events."""
        events = populated_timeline.get_events(limit=2)

        assert len(events) == 2

    def test_get_event_by_id(self, populated_timeline):
        """Test getting specific event by ID."""
        first_event = populated_timeline.events[0]

        event = populated_timeline.get_event_by_id(first_event.id)

        assert event is not None
        assert event.id == first_event.id
        assert event.event_type == first_event.event_type

    def test_get_event_by_id_not_found(self, populated_timeline):
        """Test getting non-existent event returns None."""
        event = populated_timeline.get_event_by_id("nonexistent_id")

        assert event is None


class TestTimelinePersistence:
    """Test timeline save/load operations."""

    def test_save_to_file(self, tmp_path):
        """Test saving timeline to file."""
        timeline = Timeline("save_test")
        timeline.append_event("session_start", "agent_001")
        timeline.append_event("memory_created", "agent_001")

        output_file = tmp_path / "timeline.json"
        timeline.save_to_file(output_file)

        assert output_file.exists()

        # Verify JSON structure
        with open(output_file) as f:
            data = json.load(f)

        assert data["timeline_id"] == "save_test"
        assert data["event_count"] == 2
        assert len(data["events"]) == 2

    def test_load_from_file(self, tmp_path):
        """Test loading timeline from file."""
        # Create and save timeline
        original = Timeline("load_test")
        original.append_event("session_start", "agent_001", payload={"test": True})
        original.append_event("session_end", "agent_001")

        file_path = tmp_path / "timeline.json"
        original.save_to_file(file_path)

        # Load timeline
        loaded = Timeline.load_from_file(file_path)

        assert loaded.timeline_id == "load_test"
        assert len(loaded.events) == 2
        assert loaded.events[0].event_type == "session_start"
        assert loaded.events[0].payload == {"test": True}
        assert loaded.events[1].event_type == "session_end"

    def test_load_from_file_not_found(self, tmp_path):
        """Test error when loading non-existent file."""
        with pytest.raises(FileNotFoundError):
            Timeline.load_from_file(tmp_path / "nonexistent.json")

    def test_save_and_load_preserves_all_fields(self, tmp_path):
        """Test that save/load preserves all event fields."""
        timeline = Timeline("full_test")

        timeline.append_event(
            event_type="memory_created",
            actor="agent_001",
            payload={"content": "Test"},
            related_vault_id="vault_001",
            related_agent_id="agent_001",
            related_session_id="session_001",
            checksum="abc123",
            tags=["test", "important"]
        )

        file_path = tmp_path / "timeline.json"
        timeline.save_to_file(file_path)

        loaded = Timeline.load_from_file(file_path)

        event = loaded.events[0]
        assert event.event_type == "memory_created"
        assert event.actor == "agent_001"
        assert event.payload == {"content": "Test"}
        assert event.related_vault_id == "vault_001"
        assert event.related_agent_id == "agent_001"
        assert event.related_session_id == "session_001"
        assert event.checksum == "abc123"
        assert event.tags == ["test", "important"]


class TestTimelineSummary:
    """Test timeline summary operations."""

    def test_get_summary_empty(self):
        """Test summary of empty timeline."""
        timeline = Timeline("empty")
        summary = timeline.get_summary()

        assert summary["timeline_id"] == "empty"
        assert summary["total_events"] == 0
        assert summary["unique_actors"] == 0
        assert summary["first_event"] is None
        assert summary["last_event"] is None
        assert summary["event_types"] == {}

    def test_get_summary_with_events(self):
        """Test summary of timeline with events."""
        timeline = Timeline("test")

        timeline.append_event("session_start", "agent_001")
        timeline.append_event("memory_created", "agent_001")
        timeline.append_event("memory_created", "agent_002")
        timeline.append_event("session_end", "agent_001")

        summary = timeline.get_summary()

        assert summary["timeline_id"] == "test"
        assert summary["total_events"] == 4
        assert summary["unique_actors"] == 2
        assert summary["first_event"] is not None
        assert summary["last_event"] is not None
        assert summary["event_types"]["session_start"] == 1
        assert summary["event_types"]["memory_created"] == 2
        assert summary["event_types"]["session_end"] == 1

    def test_export_events(self):
        """Test exporting events as dictionaries."""
        timeline = Timeline("test")

        timeline.append_event("session_start", "agent_001", payload={"test": True})

        exported = timeline.export_events()

        assert isinstance(exported, list)
        assert len(exported) == 1
        assert isinstance(exported[0], dict)
        assert exported[0]["event_type"] == "session_start"
        assert exported[0]["actor"] == "agent_001"
        assert exported[0]["payload"] == {"test": True}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

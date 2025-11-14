"""
Timeline management for MirrorDNA protocol.

Provides in-memory and file-backed timeline for tracking continuity events.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class TimelineEvent:
    """Single event in MirrorDNA timeline."""
    id: str
    timestamp: str
    event_type: str
    actor: str
    payload: Optional[Dict[str, Any]] = None
    related_vault_id: Optional[str] = None
    related_agent_id: Optional[str] = None
    related_session_id: Optional[str] = None
    checksum: Optional[str] = None
    tags: Optional[List[str]] = None


class Timeline:
    """MirrorDNA Timeline for continuity tracking."""

    def __init__(self, timeline_id: str = "default"):
        """
        Initialize timeline.

        Args:
            timeline_id: Unique identifier for this timeline
        """
        self.timeline_id = timeline_id
        self.events: List[TimelineEvent] = []
        self._event_counter = 0

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        self._event_counter += 1
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"evt_{timestamp}_{self._event_counter:04d}"

    def append_event(
        self,
        event_type: str,
        actor: str,
        payload: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> TimelineEvent:
        """
        Append event to timeline.

        Args:
            event_type: Type of event (session_start, memory_created, etc.)
            actor: Identity ID of actor triggering event
            payload: Event-specific data
            **kwargs: Additional event fields (related_vault_id, etc.)

        Returns:
            Created TimelineEvent
        """
        event = TimelineEvent(
            id=self._generate_event_id(),
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type=event_type,
            actor=actor,
            payload=payload or {},
            **{k: v for k, v in kwargs.items() if k in TimelineEvent.__dataclass_fields__}
        )

        self.events.append(event)
        return event

    def get_events(
        self,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        limit: Optional[int] = None
    ) -> List[TimelineEvent]:
        """
        Retrieve events with optional filtering.

        Args:
            event_type: Filter by event type
            actor: Filter by actor
            limit: Maximum number of events to return

        Returns:
            List of matching TimelineEvent objects
        """
        filtered = self.events

        if event_type:
            filtered = [e for e in filtered if e.event_type == event_type]

        if actor:
            filtered = [e for e in filtered if e.actor == actor]

        if limit:
            filtered = filtered[:limit]

        return filtered

    def get_event_by_id(self, event_id: str) -> Optional[TimelineEvent]:
        """
        Get specific event by ID.

        Args:
            event_id: Event identifier

        Returns:
            TimelineEvent if found, None otherwise
        """
        for event in self.events:
            if event.id == event_id:
                return event
        return None

    def export_events(self) -> List[Dict[str, Any]]:
        """
        Export all events as dictionaries.

        Returns:
            List of event dictionaries
        """
        return [asdict(event) for event in self.events]

    def save_to_file(self, path: Union[str, Path]) -> None:
        """
        Save timeline to JSON file.

        Args:
            path: File path to save to
        """
        path = Path(path)

        timeline_data = {
            "timeline_id": self.timeline_id,
            "event_count": len(self.events),
            "events": self.export_events()
        }

        with open(path, 'w') as f:
            json.dump(timeline_data, f, indent=2)

    @classmethod
    def load_from_file(cls, path: Union[str, Path]) -> "Timeline":
        """
        Load timeline from JSON file.

        Args:
            path: File path to load from

        Returns:
            Timeline instance

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Timeline file not found: {path}")

        with open(path, 'r') as f:
            data = json.load(f)

        timeline = cls(timeline_id=data.get("timeline_id", "loaded"))

        for event_data in data.get("events", []):
            # Create TimelineEvent from loaded data
            event = TimelineEvent(**{
                k: v for k, v in event_data.items()
                if k in TimelineEvent.__dataclass_fields__
            })
            timeline.events.append(event)

        timeline._event_counter = len(timeline.events)

        return timeline

    def get_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics about timeline.

        Returns:
            Dictionary with timeline statistics
        """
        event_types = {}
        actors = set()

        for event in self.events:
            event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
            actors.add(event.actor)

        return {
            "timeline_id": self.timeline_id,
            "total_events": len(self.events),
            "event_types": event_types,
            "unique_actors": len(actors),
            "first_event": self.events[0].timestamp if self.events else None,
            "last_event": self.events[-1].timestamp if self.events else None
        }

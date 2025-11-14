#!/usr/bin/env python3
"""
Simple Timeline Demo

Demonstrates basic timeline usage for MirrorDNA protocol:
- Creating a timeline
- Appending events
- Filtering events
- Saving and loading from file
- Getting timeline summary
"""

from mirrordna import Timeline
from pathlib import Path

def main():
    print("MirrorDNA Timeline Demo")
    print("=" * 50)

    # Create a new timeline
    timeline = Timeline(timeline_id="demo_agent_session_001")
    print(f"\nCreated timeline: {timeline.timeline_id}")

    # Append session start event
    event1 = timeline.append_event(
        event_type="session_start",
        actor="mc_demo_agent_001",
        payload={
            "platform": "MirrorDNA Demo",
            "version": "1.0.0"
        }
    )
    print(f"\nAdded event: {event1.id}")
    print(f"  Type: {event1.event_type}")
    print(f"  Timestamp: {event1.timestamp}")

    # Append memory creation event
    event2 = timeline.append_event(
        event_type="memory_created",
        actor="mc_demo_agent_001",
        payload={
            "content": "User prefers Python examples",
            "confidence": 0.95
        },
        tags=["preference", "learned"]
    )
    print(f"\nAdded event: {event2.id}")
    print(f"  Payload: {event2.payload}")
    print(f"  Tags: {event2.tags}")

    # Append citation created event
    event3 = timeline.append_event(
        event_type="citation_created",
        actor="mc_demo_agent_001",
        related_vault_id="vault_demo_main",
        payload={"citation_id": "mc_demo_agent_001"}
    )
    print(f"\nAdded event: {event3.id}")

    # Append session end event
    event4 = timeline.append_event(
        event_type="session_end",
        actor="mc_demo_agent_001",
        payload={"duration_seconds": 120}
    )
    print(f"\nAdded event: {event4.id}")

    # Get all events
    print(f"\n\nTotal events: {len(timeline.events)}")

    # Filter events by type
    session_events = timeline.get_events(event_type="session_start")
    print(f"\nSession start events: {len(session_events)}")
    for event in session_events:
        print(f"  - {event.id} at {event.timestamp}")

    # Filter events by actor
    agent_events = timeline.get_events(actor="mc_demo_agent_001")
    print(f"\nEvents by mc_demo_agent_001: {len(agent_events)}")

    # Get timeline summary
    summary = timeline.get_summary()
    print(f"\n\nTimeline Summary:")
    print(f"  Timeline ID: {summary['timeline_id']}")
    print(f"  Total Events: {summary['total_events']}")
    print(f"  Unique Actors: {summary['unique_actors']}")
    print(f"  First Event: {summary['first_event']}")
    print(f"  Last Event: {summary['last_event']}")
    print(f"\n  Event Types:")
    for event_type, count in summary['event_types'].items():
        print(f"    - {event_type}: {count}")

    # Save timeline to file
    output_path = Path("demo_timeline.json")
    timeline.save_to_file(output_path)
    print(f"\n\nTimeline saved to: {output_path}")

    # Load timeline from file
    loaded_timeline = Timeline.load_from_file(output_path)
    print(f"\nLoaded timeline: {loaded_timeline.timeline_id}")
    print(f"  Events loaded: {len(loaded_timeline.events)}")

    # Verify loaded timeline matches original
    assert loaded_timeline.timeline_id == timeline.timeline_id
    assert len(loaded_timeline.events) == len(timeline.events)
    print("\n✓ Timeline loaded successfully and verified")

    # Continue the loaded timeline with a new event
    event5 = loaded_timeline.append_event(
        event_type="session_start",
        actor="mc_demo_agent_001",
        payload={"resumed": True, "previous_session": "demo_agent_session_001"}
    )
    print(f"\n\nContinued timeline with new event: {event5.id}")
    print(f"  Total events now: {len(loaded_timeline.events)}")

    # Save updated timeline
    loaded_timeline.save_to_file(output_path)
    print(f"✓ Updated timeline saved")

    print("\n" + "=" * 50)
    print("Demo complete!")
    print(f"\nOutput file: {output_path}")
    print("You can inspect the timeline JSON to see the event structure.")


if __name__ == "__main__":
    main()

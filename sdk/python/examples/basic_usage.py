#!/usr/bin/env python3
"""
Basic usage example for MirrorDNA SDK.

This example demonstrates:
1. Creating a MirrorDNA client
2. Creating a Master Citation
3. Computing state hashes
4. Creating and validating timeline events
5. Checking continuity status

No backend required - everything runs locally with files.
"""

import sys
from pathlib import Path

# Add parent directory to path to import SDK
sys.path.insert(0, str(Path(__file__).parent.parent))

from mirror_dna_client import MirrorDNAClient


def main():
    print("=" * 60)
    print("MirrorDNA SDK - Basic Usage Example")
    print("=" * 60)
    print()

    # 1. Initialize client
    print("1. Initializing MirrorDNA client...")
    client = MirrorDNAClient(data_dir="./sdk_demo_data")
    print(f"   ✓ Client initialized, data dir: {client.data_dir}")
    print()

    # 2. Create a Master Citation
    print("2. Creating Master Citation...")
    citation = client.create_master_citation(
        identity_id="agent_assistant_001",
        vault_id="vault_main_storage",
        version="1.0.0"
    )
    print(f"   Citation ID: {citation['id']}")
    print(f"   Vault ID: {citation['vault_id']}")
    print(f"   Checksum: {citation['checksum'][:16]}...")
    print()

    # 3. Save citation to file
    print("3. Saving citation to file...")
    citation_path = client.save_citation(citation)
    print(f"   ✓ Saved to: {citation_path}")
    print()

    # 4. Compute state hash for arbitrary data
    print("4. Computing state hashes...")
    user_data = {
        "name": "Alice",
        "preferences": {
            "language": "Python",
            "theme": "dark"
        },
        "created": "2025-11-14T10:00:00Z"
    }

    hash1 = client.compute_state_hash(user_data)
    print(f"   Hash of user data: {hash1}")

    # Demonstrate determinism - same data = same hash
    hash2 = client.compute_state_hash(user_data)
    print(f"   Hash (computed again): {hash2}")
    print(f"   ✓ Hashes match: {hash1 == hash2}")
    print()

    # 5. Create timeline events
    print("5. Creating timeline events...")
    actor_id = citation['id']

    # Session start
    event1 = client.create_timeline_event(
        event_type="session_start",
        actor=actor_id,
        payload={
            "platform": "SDK_Demo",
            "version": "1.0.0"
        }
    )
    print(f"   Event 1: {event1['event_type']} ({event1['id']})")

    # Memory created
    event2 = client.create_timeline_event(
        event_type="memory_created",
        actor=actor_id,
        payload={
            "content": "User prefers Python for development",
            "tier": "long_term"
        }
    )
    print(f"   Event 2: {event2['event_type']} ({event2['id']})")

    # Memory created
    event3 = client.create_timeline_event(
        event_type="memory_created",
        actor=actor_id,
        payload={
            "content": "User uses dark theme",
            "tier": "long_term"
        }
    )
    print(f"   Event 3: {event3['event_type']} ({event3['id']})")

    # Session end
    event4 = client.create_timeline_event(
        event_type="session_end",
        actor=actor_id,
        payload={
            "duration_seconds": 300,
            "outcome": "successful"
        }
    )
    print(f"   Event 4: {event4['event_type']} ({event4['id']})")
    print()

    # 6. Validate timeline
    print("6. Validating timeline...")
    events = [event1, event2, event3, event4]
    validation = client.validate_timeline(events)

    print(f"   Valid: {validation['valid']}")
    print(f"   Total events: {validation['total_events']}")
    print(f"   Event types: {validation['event_types']}")
    print(f"   Unique actors: {validation['unique_actors']}")
    print(f"   Timespan: {validation['timespan']['first']} to {validation['timespan']['last']}")
    print()

    # 7. Check continuity status
    print("7. Checking continuity status...")
    status = client.get_continuity_status(actor_id)

    print(f"   Identity: {status['identity_id'][:40]}...")
    print(f"   Status: {status['status']}")
    print(f"   Total events: {status['total_events']}")
    print(f"   Last activity: {status['last_activity']}")
    print()

    # 8. Save timeline to file
    print("8. Saving timeline...")
    timeline_path = client.save_timeline(actor_id)
    print(f"   ✓ Saved to: {timeline_path}")
    print()

    # 9. Verify checksum
    print("9. Verifying citation checksum...")
    citation_without_checksum = {k: v for k, v in citation.items() if k != 'checksum'}
    is_valid = client.verify_checksum(
        citation_without_checksum,
        citation['checksum']
    )
    print(f"   ✓ Checksum valid: {is_valid}")
    print()

    # 10. Load timeline from file
    print("10. Loading timeline from file...")
    loaded_events = client.load_timeline(timeline_path)
    print(f"    ✓ Loaded {len(loaded_events)} events")
    print()

    print("=" * 60)
    print("✓ Demo completed successfully!")
    print("=" * 60)
    print()
    print("Files created:")
    print(f"  - {citation_path}")
    print(f"  - {timeline_path}")
    print()
    print("Continuity Status Summary:")
    print(f"  Identity: {status['identity_id'][:50]}...")
    print(f"  Status: {status['status'].upper()}")
    print(f"  Events: {status['total_events']}")
    print(f"  Valid: {status['valid']}")
    print()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
MirrorDNA SDK - Basic Usage Example

Demonstrates how to use the MirrorDNA Python SDK for common operations:
1. Load a vault configuration
2. Compute state hash for a directory
3. Validate a timeline file
4. Get continuity status
"""

import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from mirrordna_client import MirrorDNAClient


def print_section(title: str):
    """Print section header."""
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print('=' * 60)


def main():
    """Run basic SDK examples."""
    print("MirrorDNA Python SDK - Basic Usage Example")
    print("=" * 60)

    # Initialize client
    client = MirrorDNAClient()

    # Example 1: Load vault configuration
    print_section("1. Loading Vault Configuration")

    # Use example vault from repo if it exists
    vault_path = Path(__file__).parent.parent.parent.parent / "examples" / "minimal_vault.yaml"

    if vault_path.exists():
        try:
            vault_config = client.load_vault_config(str(vault_path))
            print(f"✓ Loaded vault configuration")
            print(f"  Vault ID: {vault_config['vault_id']}")
            print(f"  Name: {vault_config['name']}")
            print(f"  Path: {vault_config['path']}")
            print(f"  Created: {vault_config['created_at']}")
        except Exception as e:
            print(f"✗ Error loading vault: {e}")
    else:
        print(f"ℹ Example vault not found at: {vault_path}")
        print("  Creating a sample vault config in memory...")

        # Create sample config
        vault_config = {
            "vault_id": "vault_demo_001",
            "name": "Demo Vault",
            "path": "./demo_data",
            "created_at": "2025-11-14T10:00:00Z"
        }
        print(f"  Created sample vault: {vault_config['vault_id']}")

    # Example 2: Compute state hash for a directory
    print_section("2. Computing Directory State Hash")

    # Use current directory as example
    test_dir = Path(__file__).parent.parent  # sdk/python directory

    try:
        state_hash = client.compute_state_hash(str(test_dir))
        print(f"✓ Computed state hash for: {test_dir}")
        print(f"  Hash: {state_hash}")
        print(f"  Length: {len(state_hash)} characters (SHA-256)")

        # Compute again to show determinism
        state_hash2 = client.compute_state_hash(str(test_dir))
        if state_hash == state_hash2:
            print(f"✓ Hash is deterministic (same result on re-computation)")
        else:
            print(f"✗ Warning: Hash changed between computations")

    except Exception as e:
        print(f"✗ Error computing state hash: {e}")

    # Example 3: Validate timeline
    print_section("3. Validating Timeline File")

    # Create a sample timeline for demonstration
    sample_timeline = {
        "timeline_id": "demo_timeline_001",
        "event_count": 2,
        "events": [
            {
                "id": "evt_001",
                "timestamp": "2025-11-14T10:00:00Z",
                "event_type": "session_start",
                "actor": "mc_demo_agent_001",
                "payload": {"platform": "Demo"}
            },
            {
                "id": "evt_002",
                "timestamp": "2025-11-14T10:05:00Z",
                "event_type": "memory_created",
                "actor": "mc_demo_agent_001",
                "payload": {"content": "User prefers Python"}
            }
        ]
    }

    # Save to temporary file
    timeline_path = Path("/tmp/demo_timeline.json")
    with open(timeline_path, 'w') as f:
        json.dump(sample_timeline, f, indent=2)

    try:
        result = client.validate_timeline(str(timeline_path))

        if result['valid']:
            print(f"✓ Timeline is valid")
            print(f"  Timeline ID: {result['timeline_id']}")
            print(f"  Event count: {result['event_count']}")
            print(f"  First event: {result.get('first_event', 'N/A')}")
            print(f"  Last event: {result.get('last_event', 'N/A')}")
        else:
            print(f"✗ Timeline validation failed")
            print(f"  Errors: {result['errors']}")

    except Exception as e:
        print(f"✗ Error validating timeline: {e}")

    # Example 4: Get continuity status
    print_section("4. Getting Continuity Status")

    try:
        status = client.get_continuity_status(
            timeline_path=str(timeline_path)
        )

        print(f"Continuity Status:")
        print(f"  Timestamp: {status['timestamp']}")
        print(f"  Timeline valid: {status['timeline_valid']}")
        print(f"  Event count: {status.get('event_count', 0)}")

        if status.get('state_hash'):
            print(f"  State hash: {status['state_hash'][:16]}...")

    except Exception as e:
        print(f"✗ Error getting continuity status: {e}")

    # Example 5: Data checksum
    print_section("5. Computing Data Checksum")

    sample_data = {
        "id": "mc_example_001",
        "version": "1.0.0",
        "vault_id": "vault_example",
        "created_at": "2025-11-14T10:00:00Z"
    }

    checksum = client.compute_data_checksum(sample_data)
    print(f"✓ Computed checksum for sample data")
    print(f"  Checksum: {checksum}")
    print(f"  Data: {json.dumps(sample_data, sort_keys=True)}")

    # Verify determinism
    checksum2 = client.compute_data_checksum(sample_data)
    if checksum == checksum2:
        print(f"✓ Checksum is deterministic")

    # Summary
    print_section("Summary")
    print("""
The MirrorDNA SDK provides simple tools for:
- Loading and validating vault configurations
- Computing deterministic state hashes
- Validating timeline event logs
- Tracking continuity status

All operations are local-only and use standard Python libraries.

Next steps:
- Explore the full protocol in src/mirrordna/
- Check out examples/ for more advanced usage
- Read docs/ for protocol specifications
    """)

    print("✓ Example completed successfully!\n")


if __name__ == "__main__":
    main()

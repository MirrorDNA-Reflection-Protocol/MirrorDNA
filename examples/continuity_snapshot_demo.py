#!/usr/bin/env python3
# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Continuity Snapshot Demo

Demonstrates MirrorDNA continuity through state snapshots:
- Capturing snapshots with checksums
- Saving and loading snapshots
- Verifying checksum integrity
- Comparing snapshots
- Detecting changes in state
"""

from mirrordna import (
    capture_snapshot,
    save_snapshot,
    load_snapshot,
    compare_snapshots,
    compute_state_checksum,
    verify_checksum
)
from pathlib import Path


def main():
    print("MirrorDNA Continuity Snapshot Demo")
    print("=" * 60)

    # ========== Session 1 ==========
    print("\n" + "=" * 60)
    print("SESSION 1: Initial State")
    print("=" * 60)

    # Define initial state
    identity_state_v1 = {
        "citation_id": "mc_demo_agent_001",
        "created_at": "2025-11-14T10:00:00Z",
        "name": "Demo Agent"
    }

    continuity_state_v1 = {
        "session_count": 1,
        "total_interactions": 10,
        "last_active": "2025-11-14T10:30:00Z"
    }

    vault_state_v1 = {
        "vault_id": "vault_demo_main",
        "entry_count": 5,
        "total_size_bytes": 1024
    }

    # Capture snapshot
    snapshot_v1 = capture_snapshot(
        snapshot_id="snap_session_001",
        identity_state=identity_state_v1,
        continuity_state=continuity_state_v1,
        vault_state=vault_state_v1,
        metadata={"session_description": "Initial agent session"}
    )

    print(f"\nSnapshot ID: {snapshot_v1.snapshot_id}")
    print(f"Timestamp: {snapshot_v1.timestamp}")
    print(f"Version: {snapshot_v1.version}")
    print(f"Checksum: {snapshot_v1.checksum}")

    print(f"\nIdentity State:")
    for key, value in snapshot_v1.identity_state.items():
        print(f"  {key}: {value}")

    print(f"\nContinuity State:")
    for key, value in snapshot_v1.continuity_state.items():
        print(f"  {key}: {value}")

    # Save snapshot
    snapshot_path_v1 = Path("demo_snapshot_v1.json")
    save_snapshot(snapshot_v1, snapshot_path_v1)
    print(f"\n✓ Snapshot saved to: {snapshot_path_v1}")

    # ========== Session 2 ==========
    print("\n" + "=" * 60)
    print("SESSION 2: Resumed State (with changes)")
    print("=" * 60)

    # Load previous snapshot
    loaded_snapshot = load_snapshot(snapshot_path_v1)
    print(f"\n✓ Loaded snapshot: {loaded_snapshot.snapshot_id}")
    print(f"✓ Checksum verified automatically on load")

    # Modify state for session 2
    identity_state_v2 = loaded_snapshot.identity_state.copy()
    # Identity stays the same

    continuity_state_v2 = {
        "session_count": 2,  # Incremented
        "total_interactions": 25,  # Increased
        "last_active": "2025-11-14T11:00:00Z"  # Updated timestamp
    }

    vault_state_v2 = {
        "vault_id": "vault_demo_main",
        "entry_count": 8,  # More entries
        "total_size_bytes": 2048  # Larger vault
    }

    # Capture new snapshot
    snapshot_v2 = capture_snapshot(
        snapshot_id="snap_session_002",
        identity_state=identity_state_v2,
        continuity_state=continuity_state_v2,
        vault_state=vault_state_v2,
        metadata={
            "session_description": "Resumed session with new activity",
            "previous_snapshot": snapshot_v1.snapshot_id
        }
    )

    print(f"\nNew Snapshot ID: {snapshot_v2.snapshot_id}")
    print(f"New Checksum: {snapshot_v2.checksum}")
    print(f"\nContinuity State:")
    for key, value in snapshot_v2.continuity_state.items():
        print(f"  {key}: {value}")

    # Save second snapshot
    snapshot_path_v2 = Path("demo_snapshot_v2.json")
    save_snapshot(snapshot_v2, snapshot_path_v2)
    print(f"\n✓ Snapshot saved to: {snapshot_path_v2}")

    # ========== Snapshot Comparison ==========
    print("\n" + "=" * 60)
    print("SNAPSHOT COMPARISON")
    print("=" * 60)

    # Compare snapshots
    diff = compare_snapshots(snapshot_v1, snapshot_v2)

    print(f"\nChecksum Changed: {diff['checksum_changed']}")
    print(f"Changed Sections: {', '.join(diff['changed_sections'])}")

    if "continuity_state" in diff["changed_sections"]:
        print("\nContinuity State Changes:")
        print(f"  Session 1 -> Session 2:")
        print(f"    Session count: {continuity_state_v1['session_count']} -> {continuity_state_v2['session_count']}")
        print(f"    Total interactions: {continuity_state_v1['total_interactions']} -> {continuity_state_v2['total_interactions']}")

    # ========== Checksum Verification ==========
    print("\n" + "=" * 60)
    print("CHECKSUM VERIFICATION")
    print("=" * 60)

    # Manual checksum verification
    print("\nManual checksum verification for snapshot_v2:")

    data_without_checksum = {
        "snapshot_id": snapshot_v2.snapshot_id,
        "timestamp": snapshot_v2.timestamp,
        "version": snapshot_v2.version,
        "identity_state": snapshot_v2.identity_state,
        "continuity_state": snapshot_v2.continuity_state,
        "vault_state": snapshot_v2.vault_state,
        "timeline_summary": snapshot_v2.timeline_summary,
        "metadata": snapshot_v2.metadata
    }

    recomputed_checksum = compute_state_checksum(data_without_checksum)
    print(f"Stored checksum:     {snapshot_v2.checksum}")
    print(f"Recomputed checksum: {recomputed_checksum}")

    is_valid = verify_checksum(data_without_checksum, snapshot_v2.checksum)
    print(f"\n✓ Checksum verification: {'PASS' if is_valid else 'FAIL'}")

    # ========== Tampering Detection ==========
    print("\n" + "=" * 60)
    print("TAMPERING DETECTION DEMO")
    print("=" * 60)

    print("\nSimulating data tampering...")

    # Tamper with data
    tampered_data = data_without_checksum.copy()
    tampered_data["continuity_state"] = {
        "session_count": 999,  # Tampered!
        "total_interactions": 9999,  # Tampered!
        "last_active": "2099-01-01T00:00:00Z"
    }

    tampered_checksum = compute_state_checksum(tampered_data)
    print(f"\nOriginal checksum:  {snapshot_v2.checksum}")
    print(f"Tampered checksum:  {tampered_checksum}")
    print(f"Checksums match:    {tampered_checksum == snapshot_v2.checksum}")

    is_tampered = not verify_checksum(tampered_data, snapshot_v2.checksum)
    print(f"\n✓ Tampering detected: {is_tampered}")

    if is_tampered:
        print("  The checksum mismatch proves the data was modified!")
        print("  This is how MirrorDNA ensures continuity integrity.")

    # ========== Summary ==========
    print("\n" + "=" * 60)
    print("DEMO SUMMARY")
    print("=" * 60)

    print(f"""
Key Concepts Demonstrated:

1. Snapshot Capture:
   - Captured state at two points in time
   - Each snapshot has a unique ID and timestamp
   - SHA-256 checksum computed over all state data

2. Snapshot Persistence:
   - Saved snapshots to JSON files
   - Loaded snapshots with automatic checksum verification
   - Files can be backed up, versioned, or transferred

3. Continuity Tracking:
   - Session count incremented from 1 to 2
   - Changes detected via snapshot comparison
   - Previous snapshot referenced in metadata

4. Integrity Verification:
   - Checksums are deterministic (same data = same checksum)
   - Manual verification confirms stored checksum
   - Tampering is immediately detectable

5. State Evolution:
   - Identity state remained constant
   - Continuity state changed (sessions, interactions)
   - Vault state grew (more entries, larger size)

Output Files:
- {snapshot_path_v1}
- {snapshot_path_v2}

These snapshots prove an unbroken chain of continuity from
Session 1 to Session 2, with cryptographic integrity guarantees.
""")

    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

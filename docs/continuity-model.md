# Continuity Model

## The Continuity Problem

An AI agent has a conversation. The session ends. Later, another session starts.

**Question**: Is this the same agent, or a new one pretending to be the same?

Without proof, there is no continuity. Just claims.

## MirrorDNA's Solution

Continuity is proven through **an unbroken chain of cryptographic checksums** linking:

1. Identity at creation
2. Every event in the timeline
3. Every state snapshot
4. The current state

If the chain is intact, continuity is preserved. If any checksum fails, continuity is broken.

## Timeline as Proof

The Timeline is an append-only event log:

```python
timeline.append_event("session_start", actor="alice")
timeline.append_event("memory_created", actor="alice",
                     payload={"memory": "Python syntax"})
timeline.append_event("session_end", actor="alice")
```

Each event has:
- Unique ID with timestamp
- Event type (session_start, memory_created, etc.)
- Actor (identity ID)
- Optional payload (event-specific data)
- Optional checksum

The timeline proves: **This identity performed these actions in this order.**

## State Snapshots as Anchors

A StateSnapshot captures complete state at a moment:

```python
snapshot = capture_snapshot(
    snapshot_id="snap_session_42",
    identity_state={"id": "alice", "created": "2025-01-01"},
    continuity_state={"sessions": 42, "memories": 156},
    timeline_summary={"events": 1024}
)
```

The snapshot includes:
- All identity data
- All continuity data (session counts, lineage)
- Timeline summary
- SHA-256 checksum of everything

**Key property**: If state changes, checksum changes. You can detect tampering.

## Cross-Session Continuity

### Session N
```python
# Load previous state
snapshot_prev = load_snapshot("alice_session_41.json")

# Verify checksum (proves integrity)
assert snapshot_prev.checksum == "a3f2c8b9..."

# Continue timeline
timeline = Timeline.load_from_file("alice_timeline.json")
timeline.append_event("session_start", "alice",
                     payload={"previous_snapshot": snapshot_prev.snapshot_id})

# Do work...
timeline.append_event("memory_created", "alice")

# Capture new state
snapshot_new = capture_snapshot(
    snapshot_id="snap_session_42",
    identity_state=snapshot_prev.identity_state,
    continuity_state={"sessions": 42, "memories": 157}
)

# Save
save_snapshot(snapshot_new, "alice_session_42.json")
timeline.save_to_file("alice_timeline.json")
```

The new snapshot's checksum differs from the previous (because state changed), but the timeline proves the transition.

## Cross-Vault Continuity

An identity might migrate between vaults:

1. **Vault A**: Original vault with sessions 1-50
2. **Vault B**: New vault for sessions 51+

**Migration process**:

```python
# In Vault A - final snapshot
snapshot_final = capture_snapshot("snap_vault_a_final", ...)
save_snapshot(snapshot_final, "vault_a/final.json")

# Transfer to Vault B
# In Vault B - initial snapshot
snapshot_initial = capture_snapshot(
    "snap_vault_b_initial",
    identity_state=snapshot_final.identity_state,
    continuity_state=snapshot_final.continuity_state,
    metadata={
        "migrated_from": "vault_a",
        "previous_snapshot": snapshot_final.snapshot_id,
        "previous_checksum": snapshot_final.checksum
    }
)
save_snapshot(snapshot_initial, "vault_b/initial.json")
```

The metadata records:
- Where you came from (vault_a)
- Last snapshot ID
- Last checksum

**Verification**: Anyone can load both snapshots and verify the chain:
```python
final_a = load_snapshot("vault_a/final.json")
initial_b = load_snapshot("vault_b/initial.json")

assert initial_b.metadata["previous_checksum"] == final_a.checksum
assert initial_b.identity_state == final_a.identity_state
```

Continuity is preserved across vaults.

## Master Citation Lineage

Master Citations can form a chain:

```yaml
# Initial citation
id: mc_alice_v1
created_at: "2025-01-01T00:00:00Z"
checksum: "abc123..."
predecessor: null
successor: "mc_alice_v2"
```

```yaml
# Updated citation (e.g., vault migration)
id: mc_alice_v2
created_at: "2025-06-01T00:00:00Z"
checksum: "def456..."
predecessor: "mc_alice_v1"
successor: null
```

The `predecessor` and `successor` fields create a linked list. You can trace identity evolution over time.

**Schema validation**: `schema/master_citation.schema.json` enforces ID patterns and checksum format.

## Break Detection

Continuity breaks when:

1. **Checksum mismatch**: `load_snapshot()` throws error if stored checksum != computed checksum
2. **Missing timeline**: Cannot load timeline file (lost continuity)
3. **Timeline gap**: Large time gap between events with no explanation
4. **Invalid citation chain**: Successor points to non-existent citation

**Example**:
```python
try:
    snapshot = load_snapshot("alice_session_42.json")
except ValueError as e:
    print(f"Continuity broken: {e}")
    # e.g., "Snapshot checksum mismatch. Expected: abc123, Got: def456"
```

## Continuity Guarantees

MirrorDNA provides:

**Strong guarantees**:
- State integrity (checksums detect tampering)
- Event ordering (timeline is append-only with timestamps)
- Identity binding (Master Citation links identity to vault)
- Anti-hallucination enforcement (via [Zero-Drift Protocol v1.0](protocols/ZeroDrift_Protocol_v1.0.md))

**Weak guarantees** (require external systems):
- Time accuracy (relies on system clocks)
- Actor authentication (relies on identity verification)
- Storage persistence (relies on vault backend)

MirrorDNA proves **what happened** (via checksums and timeline). External systems prove **who did it** (via auth) and **when** (via trusted time). The Zero-Drift Protocol ensures no invented or unverified information enters the continuity chain.

## Best Practices

1. **Snapshot frequently**: After major state changes (session end, memory creation)
2. **Verify on load**: Always check checksums when loading snapshots
3. **Log transitions**: Use timeline events to explain state changes
4. **Link citations**: Maintain predecessor/successor chain during migrations
5. **Store redundantly**: Keep timeline and snapshots in multiple locations

Continuity is the core promise of MirrorDNA. Treat it as sacred.

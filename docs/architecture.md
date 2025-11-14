# MirrorDNA Architecture

## At a Glance

**Purpose:** Understand how MirrorDNA works internally
**Key Topics:** 4-layer protocol architecture, checksum verification, timeline tracking, state snapshots
**Audience:** System architects, protocol implementers
**Read Time:** 10 minutes

---

## Protocol Layers

MirrorDNA is structured in four conceptual layers:

```
┌─────────────────────────────────────┐
│      Applications & Agents          │  ← Use MirrorDNA for persistence
├─────────────────────────────────────┤
│       Identity & Continuity         │  ← Timeline, StateSnapshot
├─────────────────────────────────────┤
│     Master Citation & Vault         │  ← Configuration, Storage
├─────────────────────────────────────┤
│      Checksum & Verification        │  ← SHA-256, Integrity
└─────────────────────────────────────┘
```

## Layer 1: Checksum & Verification

**Purpose**: Ensure data integrity and detect tampering.

**Components**:
- `compute_file_checksum()` — Hash files with SHA-256
- `compute_state_checksum()` — Hash dictionaries with canonical JSON
- `verify_checksum()` — Compare expected vs actual checksums

**Key Property**: Deterministic. Same input → same checksum, always.

This is the foundation. All higher layers use checksums to prove integrity.

## Layer 2: Master Citation & Vault

**Purpose**: Define identity and where its state lives.

### Master Citation

A Master Citation is a YAML/JSON document that declares:
```yaml
id: mc_alice_primary_001
version: "1.0.0"
vault_id: vault_alice_main
created_at: "2025-01-15T10:00:00Z"
checksum: "a3f2c8b9..."
constitutional_alignment:
  compliance_level: full
  framework_version: "1.0"
```

**Schema**: `schema/master_citation.schema.json`

**Function**: Loaded by `ConfigLoader.load_master_citation()`

### Vault

A Vault is a structured store of:
- Identity documents
- Memory artifacts
- State snapshots
- Configuration files

**Schema**: `schema/vault_entry.schema.json`

**Function**: Loaded by `ConfigLoader.load_vault_config()`

Each entry has:
- Unique ID
- Type (identity, memory, snapshot, artifact)
- Checksum
- Metadata (compression, encryption)

## Layer 3: Identity & Continuity

**Purpose**: Track state changes over time and prove unbroken lineage.

### Timeline

An append-only event log:
```python
timeline = Timeline("alice_session_001")
timeline.append_event(
    event_type="session_start",
    actor="identity_alice_primary",
    payload={"platform": "ActiveMirrorOS"}
)
```

**Schema**: `schema/timeline_event.schema.json`

**Key Operations**:
- `append_event()` — Add new event with auto-generated ID and timestamp
- `get_events()` — Retrieve events with filtering
- `save_to_file()` / `load_from_file()` — Persist timeline
- `get_summary()` — Statistics about event types and actors

### State Snapshot

A point-in-time capture of complete state:
```python
snapshot = capture_snapshot(
    snapshot_id="snap_001",
    identity_state={"name": "Alice", "id": "alice_primary"},
    continuity_state={"session_count": 42},
    vault_state={"entry_count": 15}
)
```

**Includes**:
- Identity state
- Continuity state
- Vault state
- Timeline summary
- SHA-256 checksum of all data

**Functions**:
- `capture_snapshot()` — Create snapshot with checksum
- `save_snapshot()` — Write to JSON/YAML
- `load_snapshot()` — Read and verify checksum
- `compare_snapshots()` — Identify differences

## Layer 4: Applications & Agents

**Purpose**: Use MirrorDNA protocol for actual persistence.

Applications integrate by:

1. **Loading configuration** via `ConfigLoader`
2. **Tracking events** via `Timeline`
3. **Capturing state** via `StateSnapshot`
4. **Verifying integrity** via checksum functions

Example agent lifecycle:
```python
# Session start
loader = ConfigLoader()
citation = loader.load_master_citation("alice_citation.yaml")
timeline = Timeline(citation.id)

# Track activity
timeline.append_event("session_start", citation.id)
timeline.append_event("memory_created", citation.id,
                     payload={"content": "learned Python"})

# Capture state
snapshot = capture_snapshot(
    snapshot_id="snap_end_session",
    identity_state={"citation_id": citation.id},
    continuity_state={"session_duration": 3600}
)

# Persist
timeline.save_to_file(f"{citation.id}_timeline.json")
save_snapshot(snapshot, f"{citation.id}_snapshot.json")
```

## Data Flow

```
Master Citation ──→ Identity Binding
        ↓
    Vault ID ──→ Storage Location
        ↓
   Timeline ──→ Event Stream ──→ Continuity Proof
        ↓
State Snapshot ──→ Point-in-Time State ──→ Checksum Verification
```

Every component produces checksums. Every load operation verifies checksums. This creates an integrity chain from raw data to application logic.

## Storage Model

MirrorDNA doesn't mandate specific storage backends. It defines:

- **Schemas** for data structures
- **Checksums** for verification
- **Formats** for serialization (JSON, YAML)

Storage can be:
- Local filesystem (reference implementation)
- Object storage (S3, MinIO)
- Databases (PostgreSQL with JSONB)
- IPFS or content-addressed storage
- Git repositories (for version control)

The protocol is storage-agnostic. Checksums ensure integrity regardless of backend.

## Extension Points

MirrorDNA provides core protocol. Extensions can add:

- **AgentDNA** — Personality traits and behavioral patterns
- **GlyphTrail** — Visual interaction lineage
- **Reflection Engine** — Self-analysis and introspection
- **Constitutional Framework** — Rights and constraints

These build on MirrorDNA's identity and continuity primitives.

# Glossary

## Core Terms

### Master Citation
The binding document that declares an identity's vault location, constitutional alignment, and lineage. Entry point to a MirrorDNA identity.

**Format**: YAML or JSON
**Schema**: `schema/master_citation.schema.json`
**Required fields**: id, version, vault_id, created_at, checksum

### Vault
Structured storage system holding identity state, memories, snapshots, and artifacts. Can be file-based, object storage, or database.

**Entry types**: identity, memory, config, snapshot, artifact, reference
**Schema**: `schema/vault_entry.schema.json`

### Timeline
Append-only event log tracking identity actions over time. Proves continuity through unbroken event chain.

**Schema**: `schema/timeline_event.schema.json`
**Event types**: session_start, session_end, memory_created, identity_verified, citation_created, state_snapshot

### State Snapshot
Point-in-time capture of complete identity, continuity, and vault state with SHA-256 checksum.

**Includes**: identity_state, continuity_state, vault_state, timeline_summary, checksum
**Functions**: `capture_snapshot()`, `save_snapshot()`, `load_snapshot()`, `compare_snapshots()`

### Checksum
SHA-256 cryptographic hash ensuring data integrity. Computed from canonical JSON representation with sorted keys.

**Functions**: `compute_file_checksum()`, `compute_state_checksum()`, `compute_text_checksum()`, `verify_checksum()`

### Continuity
Unbroken chain of verified state transitions from identity creation to present. Proven via checksums and timeline.

**Break conditions**: Checksum mismatch, missing timeline, timeline gap, invalid citation chain

---

## Identity Concepts

### Identity
Persistent entity with unique ID, state, and continuity. Can be human, AI agent, or organizational unit.

**Binding**: Master Citation → Vault → Timeline → State

### Actor
Entity performing actions in timeline (referenced by identity ID).

**Example**: `timeline.append_event("session_start", actor="alice")`

### Lineage
Chain of predecessor/successor citations showing identity evolution.

**Example**: `mc_alice_v1` → `mc_alice_v2` → `mc_alice_v3`

---

## Constitutional Concepts

### Constitutional Alignment
Declaration of adherence to a constitutional framework defining rights and constraints.

**Compliance levels**: full, partial, custom, none
**Rights bundle**: memory, continuity, portability, sovereignty
**Constraints**: no_export, read_only, limited_retention

### Rights Bundle
Set of rights granted to an identity (e.g., right to memory, continuity, portability).

**Defined in**: Master Citation `constitutional_alignment.rights_bundle`

---

## Agent Concepts

### Agent Link
Connection between MirrorDNA identity and AgentDNA personality traits.

**Schema**: `schema/agent_link.schema.json`
**Fields**: agent_id, role, personality_traits, constitutional_alignment

### AgentDNA
Separate protocol defining agent personality, traits, and behavioral patterns. Complementary to MirrorDNA.

**Relationship**: MirrorDNA provides identity/continuity, AgentDNA provides personality

---

## Event Concepts

### Timeline Event
Single entry in timeline log with ID, timestamp, event_type, actor, and optional payload.

**Auto-generated**: ID (with timestamp), timestamp (ISO 8601)
**Required**: event_type, actor

### Event Type
Classification of timeline event (e.g., session_start, memory_created, citation_created).

**Full list**: See `schema/timeline_event.schema.json` for enumeration

### Payload
Event-specific data attached to timeline event (optional).

**Example**: `{"memory": "learned Python", "confidence": 0.95}`

---

## Storage Concepts

### Vault Entry
Single item stored in vault (identity doc, memory, snapshot, artifact, config).

**Required fields**: id, vault_id, path, type, created_at, checksum
**Metadata**: content_type, compression, encryption

### Vault Configuration
YAML/JSON document defining vault structure, storage backend, and access patterns.

**Loaded by**: `ConfigLoader.load_vault_config()`

### Canonical JSON
JSON representation with sorted keys and minimal whitespace for deterministic hashing.

**Format**: `json.dumps(data, sort_keys=True, separators=(',', ':'))`
**Purpose**: Ensure same data → same checksum

---

## Interaction Concepts

### GlyphTrail
Visual interaction lineage log using BeaconGlyphs as markers.

**Schema**: `schema/glyphtrail_entry.schema.json`
**Glyph types**: beacon, marker, anchor, transition, reflection, custom

### Session
Period of activity bounded by session_start and session_end timeline events.

**Tracking**: Session count in continuity_state
**Example**: `{"sessions": 42, "total_duration": 86400}`

---

## Technical Concepts

### ConfigLoader
Python class for loading and validating MasterCitation and VaultConfig documents.

**Functions**: `load_master_citation()`, `load_vault_config()`
**Validation**: Against JSON schemas with checksum verification

### Snapshot ID
Unique identifier for state snapshot (user-defined or auto-generated).

**Pattern**: Typically `snap_{description}_{timestamp}` (no schema constraint)
**Example**: `snap_session_42_20250115`

### Predecessor / Successor
Fields in Master Citation forming linked list of identity evolution.

**Predecessor**: Previous citation in chain (null if first)
**Successor**: Next citation in chain (null if current)

### Metadata
Additional context attached to vault entries, citations, or snapshots.

**Common fields**: display_name, description, tags, content_type, compression

---

## Protocol Concepts

### Protocol Layer
Conceptual layer in MirrorDNA architecture (Checksum → Master Citation/Vault → Identity/Continuity → Applications).

**Purpose**: Separation of concerns for implementation clarity

### Reference Implementation
Production-ready code demonstrating protocol usage (Python in `src/mirrordna/`).

**Not**: A service or platform
**Is**: A library implementing the protocol spec

### Schema Validation
Verification that data structures conform to JSON Schema specifications.

**Schemas**: master_citation, vault_entry, timeline_event, agent_link, glyphtrail_entry
**Validator**: JSON Schema Draft 7

### Deterministic Hashing
Property that same input always produces same hash (enables checksum verification).

**Implementation**: Canonical JSON with sorted keys

---

## Integration Concepts

### Storage Backend
Underlying system storing vault data (filesystem, S3, database, IPFS, git).

**Protocol stance**: Storage-agnostic (checksums ensure integrity regardless)

### Portability
Ability to export identity and move to different platform/vault while preserving continuity.

**Mechanism**: Master Citation successor chain + state snapshot transfer

### Interoperability
Ability for different systems to read/write MirrorDNA data via shared protocol.

**Enabled by**: Standard schemas, deterministic checksums, open specification

---

## Ecosystem Terms

### ActiveMirrorOS
Product layer: AI operating system using MirrorDNA for agent persistence.

**Relationship**: MirrorDNA is the protocol, ActiveMirrorOS is an implementation

### LingOS
Language-native operating system concept (related ecosystem project).

### MirrorDNA-Standard
Constitutional framework specification (separate repository).

**Referenced in**: Master Citation `constitutional_alignment.framework_version`

### BeaconGlyphs
Visual glyph system for interaction markers (used by GlyphTrail).

---

## Data Formats

### ISO 8601
Timestamp format used throughout MirrorDNA (e.g., `2025-01-15T10:00:00Z`).

**Timezone**: Always UTC (Z suffix)

### SHA-256
Cryptographic hash algorithm producing 64 hexadecimal characters.

**Use**: All checksums in MirrorDNA

### YAML / JSON
Serialization formats for Master Citations, Vault Configs, Snapshots.

**YAML**: Human-readable (`.yaml`, `.yml`)
**JSON**: Machine-readable (`.json`)

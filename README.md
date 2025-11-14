# MirrorDNA

**The Architecture of Persistence**

MirrorDNA is the foundational protocol defining identity, continuity, and state integrity for AI agents and users. It provides the core primitives that enable persistence across sessions, platforms, and time.

## What is MirrorDNA?

MirrorDNA is a **protocol specification**, not a platform or service. It defines:

- **Master Citations** — Binding documents declaring identity, vault location, and constitutional alignment
- **Timeline Events** — Append-only logs proving continuity through event history
- **State Snapshots** — Point-in-time captures of complete state with SHA-256 checksums
- **Vault Storage** — Structured persistence for identity artifacts, memories, and configurations
- **Checksum Verification** — Cryptographic integrity guarantees for all protocol data

Think of it as the "law of persistence" — a protocol ensuring AI agents and users can maintain coherent, verifiable identities across any system that implements it.

## Core Concepts

### Master Citation
The entry point to a MirrorDNA identity. Declares:
- Identity ID and version
- Vault location
- Constitutional alignment (rights and constraints)
- Lineage (predecessor/successor citations)
- SHA-256 checksum of all data

### Timeline
Append-only event log tracking identity actions:
- Session starts and ends
- Memory creation
- State changes
- Citation creation

Each event has a unique ID, timestamp, actor, and optional payload.

### State Snapshot
Point-in-time capture of complete state:
- Identity state
- Continuity state (session counts, metrics)
- Vault state (entry counts, sizes)
- Timeline summary
- SHA-256 checksum proving integrity

### Checksum
Every component uses SHA-256 checksums computed from canonical JSON:
- Deterministic (same data → same checksum)
- Tamper-evident (any change breaks the checksum)
- Verifiable (anyone can recompute and verify)

## Quick Start

### 1. Create a Master Citation

```yaml
# my_citation.yaml
id: mc_myagent_primary_001
version: "1.0.0"
vault_id: vault_myagent_main
created_at: "2025-11-14T10:00:00Z"
checksum: "a3f2c8b9..."  # Computed with compute_state_checksum()

constitutional_alignment:
  compliance_level: full
  framework_version: "1.0"
  rights_bundle:
    - memory
    - continuity
    - portability
```

```python
from mirrordna import ConfigLoader, compute_state_checksum

# Load and verify checksum
loader = ConfigLoader()
citation = loader.load_master_citation("my_citation.yaml")

print(f"Loaded citation: {citation.id}")
print(f"Vault: {citation.vault_id}")
print(f"Checksum verified: ✓")
```

### 2. Track Events with Timeline

```python
from mirrordna import Timeline

# Create timeline
timeline = Timeline(timeline_id=citation.id)

# Add events
timeline.append_event(
    event_type="session_start",
    actor=citation.id,
    payload={"platform": "MyPlatform"}
)

timeline.append_event(
    event_type="memory_created",
    actor=citation.id,
    payload={"content": "User prefers Python"}
)

# Save timeline
timeline.save_to_file(f"{citation.id}_timeline.json")
```

### 3. Capture State Snapshots

```python
from mirrordna import capture_snapshot, save_snapshot

# Capture current state
snapshot = capture_snapshot(
    snapshot_id="snap_session_001",
    identity_state={"citation_id": citation.id},
    continuity_state={"session_count": 1},
    timeline_summary=timeline.get_summary()
)

# Save snapshot
save_snapshot(snapshot, f"{citation.id}_snapshot_001.json")

print(f"Snapshot checksum: {snapshot.checksum}")
```

### 4. Resume from Previous State

```python
from mirrordna import load_snapshot, Timeline

# Load previous snapshot
snapshot = load_snapshot("mc_myagent_primary_001_snapshot_001.json")
print(f"Checksum verified: ✓")

# Load timeline
timeline = Timeline.load_from_file("mc_myagent_primary_001_timeline.json")

# Continue from where you left off
timeline.append_event(
    "session_start",
    actor=citation.id,
    payload={"resumed_from": snapshot.snapshot_id}
)
```

See [examples/](examples/) for complete working demos.

## Repository Structure

```
MirrorDNA/
├── README.md              # You are here
├── LICENSE                # MIT License
├── setup.py               # Package installation
├── pytest.ini             # Test configuration
├── schema/                # JSON schema definitions (Protocol Layer)
│   ├── master_citation.schema.json
│   ├── vault_entry.schema.json
│   ├── timeline_event.schema.json
│   ├── agent_link.schema.json
│   └── glyphtrail_entry.schema.json
├── src/mirrordna/         # Python protocol implementation
│   ├── __init__.py        # Protocol exports
│   ├── config_loader.py   # Load Master Citations and Vault Configs
│   ├── checksum.py        # SHA-256 checksumming
│   ├── timeline.py        # Timeline event management
│   └── state_snapshot.py  # State snapshot capture
├── docs/                  # Protocol documentation
│   ├── overview.md        # What + why of MirrorDNA
│   ├── architecture.md    # Protocol layers
│   ├── continuity-model.md # How continuity works
│   ├── master-citation.md  # Master Citation details
│   ├── glossary.md        # Core terms
│   └── integration-guide.md # How to adopt MirrorDNA
├── examples/              # Protocol-focused examples
│   ├── minimal_master_citation.yaml
│   ├── minimal_vault.yaml
│   ├── simple_timeline_demo.py
│   └── continuity_snapshot_demo.py
└── tests/                 # Protocol validation tests
    ├── test_config_loader.py
    ├── test_checksum.py
    ├── test_timeline.py
    └── test_state_snapshot.py
```

## Documentation

- **[Overview](docs/overview.md)** — What is MirrorDNA and why it exists
- **[Architecture](docs/architecture.md)** — Protocol layers and data flow
- **[Continuity Model](docs/continuity-model.md)** — How continuity works across sessions
- **[Master Citation](docs/master-citation.md)** — The binding document for identity
- **[Glossary](docs/glossary.md)** — Core protocol terms
- **[Integration Guide](docs/integration-guide.md)** — How to adopt MirrorDNA in your system

## Protocol Schemas

All protocol data structures are defined as JSON schemas:

- **master_citation.schema.json** — Identity binding document
- **vault_entry.schema.json** — Vault storage entries
- **timeline_event.schema.json** — Event log entries
- **agent_link.schema.json** — Links to AgentDNA
- **glyphtrail_entry.schema.json** — Interaction lineage

Schemas use JSON Schema Draft 7 and enforce:
- Required vs optional fields
- ID patterns (`^mc_`, `^vault_`, `^evt_`)
- Enum types for controlled vocabularies
- Checksum format (64 hex characters for SHA-256)

## Installation

```bash
# Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA.git
cd MirrorDNA

# Install (Python 3.8+)
pip install -e .
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/test_checksum.py -v
pytest tests/test_timeline.py -v
pytest tests/test_state_snapshot.py -v
pytest tests/test_config_loader.py -v
```

## Protocol Principles

1. **Protocol, Not Platform** — Defines data structures and verification rules, not services
2. **Cryptographic Integrity** — SHA-256 checksums on all state data
3. **Deterministic** — Same input → same checksum, always
4. **Storage Agnostic** — Works with filesystems, databases, S3, IPFS, git
5. **Human Readable** — YAML/JSON formats, not binary blobs
6. **No Central Authority** — Anyone can implement, no gatekeepers

## How MirrorDNA Fits in the Ecosystem

```
┌─────────────────────────────────────┐
│     ActiveMirrorOS (Product)        │  ← User-facing AI system
├─────────────────────────────────────┤
│      MirrorDNA (This Layer)         │  ← Identity + Continuity Protocol
├─────────────────────────────────────┤
│  AgentDNA │ GlyphTrail │ LingOS     │  ← Complementary systems
└─────────────────────────────────────┘
```

**MirrorDNA** provides the protocol layer:
- Identity binding (Master Citations)
- Continuity tracking (Timeline)
- State integrity (Checksums)

**AgentDNA** adds personality and traits (built on MirrorDNA identity).

**GlyphTrail** adds visual interaction lineage (built on MirrorDNA timeline).

**ActiveMirrorOS** uses all of these to create a product-grade AI system.

## Related Projects

- **[MirrorDNA-Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)** — Constitutional framework specification
- **[ActiveMirrorOS](https://github.com/MirrorDNA-Reflection-Protocol/ActiveMirrorOS)** — Product implementation using MirrorDNA
- **[AgentDNA](https://github.com/MirrorDNA-Reflection-Protocol/AgentDNA)** — Agent personality protocol
- **[BeaconGlyphs](https://github.com/MirrorDNA-Reflection-Protocol/BeaconGlyphs)** — Visual glyph system for GlyphTrail
- **[LingOS](https://github.com/MirrorDNA-Reflection-Protocol/LingOS)** — Language-native reflective OS

## Use Cases

### For AI Agents
- Maintain identity across sessions
- Prove unbroken continuity via timeline
- Preserve memory with checksummed snapshots
- Migrate between platforms with Master Citations

### For Platforms
- Implement interoperable agent identity
- Verify agent continuity with checksums
- Store agent state in any backend (file, DB, S3)
- Support constitutional compliance via Master Citations

### For Users
- Portable digital identity across platforms
- Verifiable history via timeline
- Data sovereignty (own your identity and state)

## License

MIT License — See [LICENSE](LICENSE) for details.

## Contributing

This is currently a private repository. If you have access and want to contribute:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes, add tests
3. Ensure `pytest` passes
4. Update documentation if needed
5. Submit a pull request

## Questions?

- Check the [docs/](docs/) for detailed protocol documentation
- See [examples/](examples/) for working code samples
- Open an issue for bugs or feature requests

---

**MirrorDNA** — The architecture of persistence.

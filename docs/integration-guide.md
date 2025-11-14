# Integration Guide

## How to Adopt MirrorDNA

This guide shows how to integrate MirrorDNA protocol into your application, platform, or agent system.

## Prerequisites

- Python 3.8+ or JavaScript/TypeScript environment
- Basic understanding of JSON/YAML formats
- Familiarity with checksums and data integrity concepts

## Installation

### Python

```bash
pip install mirrordna
```

Or install from source:
```bash
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA
cd MirrorDNA
pip install -e .
```

### JavaScript/TypeScript

```bash
npm install mirrordna
```

## Step 1: Create a Master Citation

A Master Citation is the entry point to your MirrorDNA identity.

### Define the Citation Document

Create `my_citation.yaml`:

```yaml
id: mc_myagent_primary_001
version: "1.0.0"
vault_id: vault_myagent_main
created_at: "2025-11-14T10:00:00Z"
predecessor: null
successor: null

constitutional_alignment:
  compliance_level: full
  framework_version: "1.0"
  rights_bundle:
    - memory
    - continuity
    - portability

metadata:
  display_name: MyAgent
  description: Primary identity for MyAgent
  tags:
    - agent
    - production
```

### Compute and Add Checksum

```python
import yaml
from mirrordna import compute_state_checksum

# Load document
with open("my_citation.yaml") as f:
    data = yaml.safe_load(f)

# Remove checksum field if present
data_without_checksum = {k: v for k, v in data.items() if k != "checksum"}

# Compute checksum
checksum = compute_state_checksum(data_without_checksum)

# Add to file
data["checksum"] = checksum

with open("my_citation.yaml", "w") as f:
    yaml.dump(data, f, sort_keys=False)
```

### Validate the Citation

```python
from mirrordna import ConfigLoader

loader = ConfigLoader()
citation = loader.load_master_citation("my_citation.yaml")

print(f"Loaded citation: {citation.id}")
print(f"Vault: {citation.vault_id}")
print(f"Checksum verified: ✓")
```

## Step 2: Initialize a Timeline

Track continuity through an event timeline.

```python
from mirrordna import Timeline

# Create timeline
timeline = Timeline(timeline_id=citation.id)

# Add session start event
timeline.append_event(
    event_type="session_start",
    actor=citation.id,
    payload={"platform": "MyPlatform", "version": "1.0"}
)

# Add memory creation event
timeline.append_event(
    event_type="memory_created",
    actor=citation.id,
    payload={"content": "User preferences loaded"}
)

# Save timeline
timeline.save_to_file(f"{citation.id}_timeline.json")
```

## Step 3: Capture State Snapshots

Preserve point-in-time state with checksums.

```python
from mirrordna import capture_snapshot, save_snapshot

# Capture current state
snapshot = capture_snapshot(
    snapshot_id="snap_session_001",
    identity_state={
        "citation_id": citation.id,
        "created_at": citation.created_at
    },
    continuity_state={
        "session_count": 1,
        "total_events": timeline.get_summary()["total_events"]
    },
    vault_state={
        "vault_id": citation.vault_id,
        "entry_count": 0
    },
    timeline_summary=timeline.get_summary()
)

# Save snapshot
save_snapshot(snapshot, f"{citation.id}_snapshot_001.json")

print(f"Snapshot checksum: {snapshot.checksum}")
```

## Step 4: Restore State on Resumption

Load and verify state when resuming a session.

```python
from mirrordna import load_snapshot, Timeline

# Load previous snapshot
snapshot = load_snapshot("mc_myagent_primary_001_snapshot_001.json")
print(f"Restored snapshot: {snapshot.snapshot_id}")
print(f"Checksum verified: ✓")

# Load timeline
timeline = Timeline.load_from_file("mc_myagent_primary_001_timeline.json")
print(f"Timeline events: {len(timeline.events)}")

# Continue timeline
timeline.append_event(
    event_type="session_start",
    actor=citation.id,
    payload={"resumed_from": snapshot.snapshot_id}
)
```

## Step 5: Verify Integrity

Always verify checksums to detect tampering.

```python
from mirrordna import verify_checksum, load_snapshot

# Load snapshot
snapshot = load_snapshot("mc_myagent_primary_001_snapshot_001.json")

# Manually verify
data_without_checksum = {
    "snapshot_id": snapshot.snapshot_id,
    "timestamp": snapshot.timestamp,
    "version": snapshot.version,
    "identity_state": snapshot.identity_state,
    "continuity_state": snapshot.continuity_state,
    "vault_state": snapshot.vault_state,
    "timeline_summary": snapshot.timeline_summary,
    "metadata": snapshot.metadata
}

is_valid = verify_checksum(data_without_checksum, snapshot.checksum)
print(f"Integrity check: {'PASS' if is_valid else 'FAIL'}")
```

## Integration Patterns

### Pattern 1: Stateless Agent with MirrorDNA Persistence

For agents that don't maintain in-memory state between runs.

```python
# On agent start
loader = ConfigLoader()
citation = loader.load_master_citation("agent_citation.yaml")
snapshot = load_snapshot(f"{citation.id}_latest.json")
timeline = Timeline.load_from_file(f"{citation.id}_timeline.json")

# Restore state from snapshot
agent_state = snapshot.identity_state
session_count = snapshot.continuity_state["session_count"]

# Do work...
timeline.append_event("memory_created", citation.id)

# On agent stop
new_snapshot = capture_snapshot(
    snapshot_id=f"snap_session_{session_count + 1}",
    identity_state=agent_state,
    continuity_state={"session_count": session_count + 1}
)
save_snapshot(new_snapshot, f"{citation.id}_latest.json")
timeline.save_to_file(f"{citation.id}_timeline.json")
```

### Pattern 2: Multi-User Platform

For platforms managing multiple identities.

```python
from pathlib import Path

class MirrorDNAPlatform:
    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.loader = ConfigLoader()

    def get_user_citation(self, user_id: str):
        citation_path = self.vault_root / f"{user_id}_citation.yaml"
        return self.loader.load_master_citation(citation_path)

    def get_user_timeline(self, user_id: str):
        timeline_path = self.vault_root / f"{user_id}_timeline.json"
        return Timeline.load_from_file(timeline_path)

    def create_user_session(self, user_id: str):
        citation = self.get_user_citation(user_id)
        timeline = self.get_user_timeline(user_id)

        timeline.append_event("session_start", citation.id)
        return {"citation": citation, "timeline": timeline}
```

### Pattern 3: Cross-Platform Identity

For identities that move between platforms.

```python
# Export from Platform A
snapshot_a = capture_snapshot(
    snapshot_id="snap_final_platform_a",
    identity_state=current_state,
    continuity_state={"sessions_on_platform_a": 100},
    metadata={"exported_from": "platform_a"}
)
save_snapshot(snapshot_a, "export_snapshot.json")

# Import to Platform B
snapshot_a = load_snapshot("export_snapshot.json")
print(f"Checksum verified from Platform A: ✓")

snapshot_b = capture_snapshot(
    snapshot_id="snap_initial_platform_b",
    identity_state=snapshot_a.identity_state,
    continuity_state={
        "sessions_on_platform_a": 100,
        "sessions_on_platform_b": 0
    },
    metadata={
        "imported_from": "platform_a",
        "previous_snapshot": snapshot_a.snapshot_id,
        "previous_checksum": snapshot_a.checksum
    }
)
save_snapshot(snapshot_b, "platform_b_initial.json")
```

## Vault Storage

### File-Based Vault (Simplest)

```
vault_root/
├── citations/
│   └── mc_myagent_primary_001.yaml
├── timelines/
│   └── mc_myagent_primary_001_timeline.json
├── snapshots/
│   ├── snap_session_001.json
│   ├── snap_session_002.json
│   └── snap_latest.json
└── artifacts/
    └── custom_data.bin
```

### Database-Backed Vault

```python
import json
from pathlib import Path
from dataclasses import asdict

class DatabaseVault:
    def __init__(self, db_connection):
        self.db = db_connection

    def store_snapshot(self, snapshot):
        self.db.execute("""
            INSERT INTO snapshots (snapshot_id, checksum, data, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            snapshot.snapshot_id,
            snapshot.checksum,
            json.dumps(asdict(snapshot)),
            snapshot.timestamp
        ))

    def load_snapshot(self, snapshot_id):
        row = self.db.execute(
            "SELECT data FROM snapshots WHERE snapshot_id = ?",
            (snapshot_id,)
        ).fetchone()

        data = json.loads(row[0])
        from mirrordna import StateSnapshot
        return StateSnapshot(**data)
```

## Schema Validation

### Validate Master Citation

```python
import json
import yaml
import jsonschema

# Load schema
with open("schema/master_citation.schema.json") as f:
    schema = json.load(f)

# Load citation
with open("my_citation.yaml") as f:
    citation_data = yaml.safe_load(f)

# Validate
try:
    jsonschema.validate(citation_data, schema)
    print("Citation is valid ✓")
except jsonschema.ValidationError as e:
    print(f"Validation error: {e.message}")
```

### Validate Timeline Event

```python
# Load event schema
with open("schema/timeline_event.schema.json") as f:
    event_schema = json.load(f)

# Create event data
event_data = {
    "id": "evt_20251114_0001",
    "timestamp": "2025-11-14T10:00:00Z",
    "event_type": "session_start",
    "actor": "mc_myagent_primary_001"
}

# Validate
jsonschema.validate(event_data, event_schema)
```

## Best Practices

### 1. Always Verify Checksums

```python
# Good
snapshot = load_snapshot("snapshot.json")  # Automatically verifies

# Also good (manual verification)
is_valid = verify_checksum(data, expected_checksum)
if not is_valid:
    raise ValueError("Checksum mismatch!")
```

### 2. Snapshot Frequently

Capture snapshots at key moments:
- Session end
- After significant state changes
- Before/after migrations
- On critical errors (for recovery)

### 3. Maintain Timeline Continuity

```python
# Link sessions explicitly
timeline.append_event(
    "session_start",
    actor=citation.id,
    payload={"previous_session": "sess_042"}
)
```

### 4. Use Consistent ID Patterns

```
Master Citations:  mc_{name}_{variant}_{version}
Vaults:           vault_{name}_{purpose}
Snapshots:        snap_{description}_{timestamp}
Events:           evt_{timestamp}_{counter}
```

### 5. Store Redundantly

Keep multiple copies:
- Local filesystem
- Remote backup (S3, etc.)
- Git repository (for version control)

## Troubleshooting

### Checksum Mismatch

**Problem**: `ValueError: Snapshot checksum mismatch`

**Cause**: File was modified after checksum was computed

**Solution**: Recompute checksum or restore from backup

### Timeline Not Found

**Problem**: `FileNotFoundError: Timeline file not found`

**Cause**: Timeline file was deleted or moved

**Solution**: Create new timeline or restore from backup

### Invalid Schema

**Problem**: `jsonschema.ValidationError: 'id' is a required property`

**Cause**: Master Citation missing required field

**Solution**: Add missing field and recompute checksum

## Next Steps

- Read [continuity-model.md](continuity-model.md) to understand how continuity works
- See [master-citation.md](master-citation.md) for Master Citation details
- Check [glossary.md](glossary.md) for term definitions
- Explore [examples/](../examples/) for working code samples

## Support

- GitHub Issues: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/issues
- Documentation: https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/tree/main/docs

# MirrorDNA Python SDK

Simple Python SDK for integrating MirrorDNA protocol concepts into your applications.

## What is This?

A lightweight client library that provides high-level methods for working with MirrorDNA:
- **Load vault configurations** from YAML/JSON files
- **Compute state hashes** for data integrity verification
- **Validate timeline events** and track continuity
- **Create Master Citations** for identity binding

**No backend required** - everything works locally with files and in-memory operations.

## Installation

### Option 1: Use the SDK directly

```bash
# Copy mirror_dna_client.py to your project
cp sdk/python/mirror_dna_client.py your_project/

# Install dependencies
pip install pyyaml
```

### Option 2: Install in development mode

```bash
cd sdk/python
pip install -e .
```

### Option 3: Use full MirrorDNA protocol implementation

For the complete protocol implementation with schema validation:

```bash
# From repository root
pip install -e .
```

## Quick Start

```python
from mirror_dna_client import MirrorDNAClient

# Initialize client
client = MirrorDNAClient(data_dir="./my_data")

# Create a Master Citation
citation = client.create_master_citation(
    identity_id="my_agent_001",
    vault_id="vault_main"
)

# Compute state hash
user_data = {"name": "Alice", "role": "admin"}
hash_value = client.compute_state_hash(user_data)

# Create timeline events
event = client.create_timeline_event(
    event_type="session_start",
    actor=citation['id'],
    payload={"platform": "MyApp"}
)

# Check continuity status
status = client.get_continuity_status(citation['id'])
print(f"Status: {status['status']}, Events: {status['total_events']}")
```

## Running the Example

```bash
cd sdk/python/examples
python basic_usage.py
```

This will:
1. Create a Master Citation
2. Compute deterministic state hashes
3. Create and validate timeline events
4. Track continuity metrics
5. Save data to local files

## API Reference

### MirrorDNAClient

Main client class for MirrorDNA operations.

#### `__init__(data_dir=None)`

Initialize client with optional data directory.

```python
client = MirrorDNAClient(data_dir="./mirrordna_data")
```

#### `load_vault_config(path)`

Load and validate a vault configuration file.

```python
vault = client.load_vault_config("vault.yaml")
# Returns: {'vault_id': '...', 'name': '...', 'path': '...', ...}
```

#### `compute_state_hash(data)`

Compute deterministic SHA-256 hash of data.

```python
hash_value = client.compute_state_hash({"key": "value"})
# Returns: '5d41402abc4b2a76b9719d911017c592...'
```

**Note**: Same data always produces the same hash (deterministic).

#### `validate_timeline(events)`

Validate timeline events and compute metrics.

```python
validation = client.validate_timeline([event1, event2])
# Returns: {
#   'valid': True,
#   'total_events': 2,
#   'event_types': {'session_start': 1, 'memory_created': 1},
#   'unique_actors': 1,
#   'timespan': {...},
#   'errors': []
# }
```

#### `create_master_citation(identity_id, vault_id, version="1.0.0")`

Create a Master Citation document.

```python
citation = client.create_master_citation(
    identity_id="agent_001",
    vault_id="vault_main"
)
# Returns: {
#   'id': 'mc_agent_001_20251114_120000',
#   'version': '1.0.0',
#   'vault_id': 'vault_main',
#   'checksum': '...'
# }
```

#### `save_citation(citation, filename=None)`

Save Master Citation to YAML file.

```python
path = client.save_citation(citation)
# Returns: Path to saved file
```

#### `create_timeline_event(event_type, actor, payload=None)`

Create a timeline event.

```python
event = client.create_timeline_event(
    event_type="session_start",
    actor="mc_agent_001",
    payload={"platform": "MyApp"}
)
```

#### `get_continuity_status(identity_id)`

Get continuity metrics for an identity.

```python
status = client.get_continuity_status("mc_agent_001")
# Returns: {
#   'identity_id': '...',
#   'status': 'active',
#   'total_events': 5,
#   'event_types': {...},
#   'last_activity': '2025-11-14T10:30:00Z',
#   'valid': True
# }
```

#### `save_timeline(identity_id, filename=None)`

Save timeline events to JSON file.

```python
path = client.save_timeline("mc_agent_001")
# Returns: Path to saved file
```

#### `load_timeline(path)`

Load timeline from file.

```python
events = client.load_timeline("timeline.json")
# Returns: List of timeline events
```

#### `verify_checksum(data, expected_checksum)`

Verify data matches expected checksum.

```python
is_valid = client.verify_checksum(
    {"key": "value"},
    "5d41402abc4b2a76b9719d911017c592..."
)
# Returns: True or False
```

## Features

✅ **Local-first** - No backend required, works with files
✅ **Deterministic** - Same data = same hash, always
✅ **Simple API** - High-level methods for common tasks
✅ **File formats** - Supports JSON and YAML
✅ **Continuity tracking** - Timeline validation and metrics
✅ **Lightweight** - Minimal dependencies (only PyYAML)

## Dependencies

- **Required**: PyYAML (for YAML file support)
- **Optional**: None - works standalone

```bash
pip install pyyaml
```

## Use Cases

### For Developers

```python
# Track user preferences with integrity verification
preferences = {"theme": "dark", "lang": "python"}
hash_value = client.compute_state_hash(preferences)

# Later, verify preferences haven't been tampered with
is_valid = client.verify_checksum(preferences, hash_value)
```

### For AI Agents

```python
# Create identity
citation = client.create_master_citation("agent_001", "vault_main")

# Track session activities
client.create_timeline_event("session_start", citation['id'])
client.create_timeline_event("memory_created", citation['id'],
                            {"content": "User likes Python"})

# Check continuity
status = client.get_continuity_status(citation['id'])
if status['status'] == 'active':
    print("Agent continuity maintained ✓")
```

### For Platform Builders

```python
# Load vault configuration
vault = client.load_vault_config("vault.yaml")

# Validate timeline integrity
events = client.load_timeline("agent_timeline.json")
validation = client.validate_timeline(events)

if not validation['valid']:
    print(f"Timeline errors: {validation['errors']}")
```

## Relationship to Protocol

This SDK is a **simplified interface** to MirrorDNA concepts:

```
┌─────────────────────────────────────┐
│  Your Application                   │
├─────────────────────────────────────┤
│  Python SDK (this layer)            │  ← Simple client API
├─────────────────────────────────────┤
│  MirrorDNA Protocol                 │  ← Core protocol (../src/mirrordna/)
│  - Master Citations                 │
│  - Timeline Events                  │
│  - State Snapshots                  │
│  - Schema Validation                │
└─────────────────────────────────────┘
```

For **full protocol implementation** with schema validation and advanced features, use the main `mirrordna` package in `src/mirrordna/`.

## Design Philosophy

This SDK is intentionally **simple and standalone**:

- **No complex dependencies** - Works with just Python stdlib + PyYAML
- **Local operations** - No network calls, no databases
- **Educational** - Easy to understand and extend
- **Conceptual** - Shows MirrorDNA principles in action

For production use with full schema validation, use the main protocol implementation.

## Examples

See `examples/basic_usage.py` for a complete working demonstration.

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## Questions?

- Main protocol docs: [../../docs/](../../docs/)
- Integration guide: [../../docs/integration-guide.md](../../docs/integration-guide.md)
- Schema reference: [../../docs/schema-reference.md](../../docs/schema-reference.md)

---

**MirrorDNA** - The architecture of persistence.

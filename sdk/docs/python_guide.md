# MirrorDNA Python SDK Guide

Complete guide to using the MirrorDNA Python SDK.

## Installation

### Quick Start (Copy File)

```bash
# Copy the SDK client to your project
cp sdk/python/mirror_dna_client.py your_project/

# Install dependencies
pip install pyyaml
```

### Development Installation

```bash
cd sdk/python
pip install -e .
```

### Full Protocol Installation

For complete protocol implementation with schema validation:

```bash
# From repository root
pip install -e .
```

## Dependencies

- **Required**: None (works with Python stdlib only)
- **Optional**: PyYAML (for YAML file support)

```bash
pip install pyyaml
```

## Basic Usage

### 1. Initialize Client

```python
from mirror_dna_client import MirrorDNAClient

# Initialize with default data directory
client = MirrorDNAClient()

# Or specify custom directory
client = MirrorDNAClient(data_dir="./my_data")
```

### 2. Create Master Citation

```python
citation = client.create_master_citation(
    identity_id="agent_001",
    vault_id="vault_main",
    version="1.0.0"
)

print(f"Citation ID: {citation['id']}")
print(f"Checksum: {citation['checksum']}")
```

### 3. Save Citation to File

```python
# Save with auto-generated filename
path = client.save_citation(citation)

# Save with custom filename
path = client.save_citation(citation, filename="my_citation.yaml")

print(f"Saved to: {path}")
```

### 4. Compute State Hashes

```python
data = {
    "user": "alice",
    "preferences": {
        "theme": "dark",
        "language": "python"
    }
}

hash_value = client.compute_state_hash(data)
print(f"Hash: {hash_value}")

# Verify hash is deterministic
hash2 = client.compute_state_hash(data)
assert hash_value == hash2  # Always true for same data
```

### 5. Create Timeline Events

```python
# Create events
event1 = client.create_timeline_event(
    event_type="session_start",
    actor=citation['id'],
    payload={"platform": "MyApp"}
)

event2 = client.create_timeline_event(
    event_type="memory_created",
    actor=citation['id'],
    payload={
        "content": "User prefers Python",
        "tier": "long_term"
    }
)

event3 = client.create_timeline_event(
    event_type="session_end",
    actor=citation['id'],
    payload={"outcome": "successful"}
)
```

### 6. Validate Timeline

```python
events = [event1, event2, event3]
validation = client.validate_timeline(events)

if validation['valid']:
    print("✓ Timeline is valid")
    print(f"Total events: {validation['total_events']}")
    print(f"Event types: {validation['event_types']}")
    print(f"Unique actors: {validation['unique_actors']}")
else:
    print("✗ Timeline has errors:")
    for error in validation['errors']:
        print(f"  - {error}")
```

### 7. Check Continuity Status

```python
status = client.get_continuity_status(citation['id'])

print(f"Status: {status['status']}")
print(f"Total events: {status['total_events']}")
print(f"Last activity: {status['last_activity']}")
print(f"Valid: {status['valid']}")
```

### 8. Save and Load Timeline

```python
# Save timeline
timeline_path = client.save_timeline(citation['id'])
print(f"Timeline saved to: {timeline_path}")

# Load timeline
loaded_events = client.load_timeline(timeline_path)
print(f"Loaded {len(loaded_events)} events")
```

### 9. Verify Checksums

```python
# Verify data integrity
data_without_checksum = {k: v for k, v in citation.items() if k != 'checksum'}

is_valid = client.verify_checksum(
    data_without_checksum,
    citation['checksum']
)

if is_valid:
    print("✓ Checksum valid - data integrity verified")
else:
    print("✗ Checksum mismatch - data may be corrupted")
```

### 10. Load Vault Configuration

```python
# Load vault config from file
vault = client.load_vault_config("vault.yaml")

print(f"Vault ID: {vault['vault_id']}")
print(f"Name: {vault['name']}")
print(f"Path: {vault['path']}")
```

## API Reference

### MirrorDNAClient

#### Constructor

```python
MirrorDNAClient(data_dir=None)
```

- `data_dir` (optional): Directory for storing data files. Defaults to `./mirrordna_data/`

#### Methods

##### `load_vault_config(path)`

Load and validate vault configuration.

**Parameters**:
- `path`: Path to vault config file (JSON or YAML)

**Returns**: Dictionary with vault configuration

**Raises**:
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If required fields missing

##### `compute_state_hash(data)`

Compute SHA-256 hash of state data.

**Parameters**:
- `data`: Dictionary to hash

**Returns**: 64-character hex string

##### `validate_timeline(events)`

Validate timeline events.

**Parameters**:
- `events`: List of event dictionaries

**Returns**: Dictionary with:
- `valid`: Boolean
- `total_events`: Count
- `event_types`: Dict of event type counts
- `unique_actors`: Count
- `timespan`: First and last timestamps
- `errors`: List of validation errors

##### `create_master_citation(identity_id, vault_id, version='1.0.0')`

Create Master Citation document.

**Parameters**:
- `identity_id`: Unique identity identifier
- `vault_id`: Vault to bind to
- `version`: Protocol version (default: "1.0.0")

**Returns**: Master Citation dictionary with checksum

##### `save_citation(citation, filename=None)`

Save Master Citation to file.

**Parameters**:
- `citation`: Master Citation dictionary
- `filename`: Optional filename (defaults to citation ID)

**Returns**: Path to saved file

##### `create_timeline_event(event_type, actor, payload=None)`

Create timeline event.

**Parameters**:
- `event_type`: Event type string
- `actor`: Identity ID of actor
- `payload`: Optional event data (dict)

**Returns**: Timeline event dictionary

##### `get_continuity_status(identity_id)`

Get continuity status for identity.

**Parameters**:
- `identity_id`: Identity to check

**Returns**: Dictionary with:
- `identity_id`: Identity ID
- `status`: "active", "degraded", or "no_activity"
- `total_events`: Count
- `event_types`: Breakdown
- `last_activity`: Timestamp
- `valid`: Boolean

##### `save_timeline(identity_id, filename=None)`

Save timeline to file.

**Parameters**:
- `identity_id`: Identity whose timeline to save
- `filename`: Optional filename

**Returns**: Path to saved file

##### `load_timeline(path)`

Load timeline from file.

**Parameters**:
- `path`: Path to timeline file

**Returns**: List of timeline events

**Raises**:
- `FileNotFoundError`: If file doesn't exist

##### `verify_checksum(data, expected_checksum)`

Verify data checksum.

**Parameters**:
- `data`: Dictionary to verify (without checksum field)
- `expected_checksum`: Expected hash value

**Returns**: Boolean (True if match)

## Examples

### Complete Workflow

```python
from mirror_dna_client import MirrorDNAClient

# 1. Initialize
client = MirrorDNAClient(data_dir="./demo_data")

# 2. Create identity
citation = client.create_master_citation(
    identity_id="agent_demo",
    vault_id="vault_demo"
)

# 3. Save citation
citation_path = client.save_citation(citation)

# 4. Create timeline
client.create_timeline_event("session_start", citation['id'])
client.create_timeline_event("memory_created", citation['id'], {
    "content": "Demo memory"
})
client.create_timeline_event("session_end", citation['id'])

# 5. Check status
status = client.get_continuity_status(citation['id'])
print(f"Status: {status['status']}, Events: {status['total_events']}")

# 6. Save timeline
timeline_path = client.save_timeline(citation['id'])

# 7. Verify integrity
data_to_verify = {k: v for k, v in citation.items() if k != 'checksum'}
is_valid = client.verify_checksum(data_to_verify, citation['checksum'])
print(f"Integrity: {'✓' if is_valid else '✗'}")
```

### Data Integrity Checking

```python
# Store data with checksum
user_preferences = {
    "theme": "dark",
    "notifications": True,
    "language": "en"
}

# Compute checksum
checksum = client.compute_state_hash(user_preferences)

# Save both
import json
with open("preferences.json", "w") as f:
    json.dump({
        "data": user_preferences,
        "checksum": checksum
    }, f)

# Later, load and verify
with open("preferences.json", "r") as f:
    loaded = json.load(f)

if client.verify_checksum(loaded["data"], loaded["checksum"]):
    print("✓ Data integrity verified")
    preferences = loaded["data"]
else:
    print("✗ Data may be corrupted!")
```

### Agent Session Tracking

```python
# Create agent
citation = client.create_master_citation("agent_001", "vault_main")
agent_id = citation['id']

# Start session
client.create_timeline_event("session_start", agent_id, {
    "platform": "MyPlatform",
    "version": "1.0"
})

# Agent activities
client.create_timeline_event("memory_created", agent_id, {
    "content": "User asked about Python"
})

client.create_timeline_event("memory_created", agent_id, {
    "content": "User prefers concise responses"
})

# End session
client.create_timeline_event("session_end", agent_id, {
    "duration": 300,
    "outcome": "successful"
})

# Review session
status = client.get_continuity_status(agent_id)
print(f"Session summary: {status['event_types']}")
```

## Running the Demo

```bash
cd sdk/python/examples
python basic_usage.py
```

Expected output:
- Creates Master Citation
- Computes state hashes
- Creates and validates timeline
- Shows continuity status
- Saves files to `./sdk_demo_data/`

## Tips and Best Practices

### 1. Deterministic Hashing

Always use `compute_state_hash()` for data that needs integrity verification:

```python
# DO: Use compute_state_hash
hash_value = client.compute_state_hash(data)

# DON'T: Try to hash manually (may not be deterministic)
```

### 2. Checksum Verification

Remove checksum field before verification:

```python
# Correct
data_without_checksum = {k: v for k, v in citation.items() if k != 'checksum'}
client.verify_checksum(data_without_checksum, citation['checksum'])

# Incorrect (includes checksum in data)
client.verify_checksum(citation, citation['checksum'])  # Will fail
```

### 3. Event Ordering

Timeline events are chronological - create them in order:

```python
# Good: Events in order
client.create_timeline_event("session_start", actor)
client.create_timeline_event("action_taken", actor)
client.create_timeline_event("session_end", actor)
```

### 4. Error Handling

```python
try:
    vault = client.load_vault_config("vault.yaml")
except FileNotFoundError:
    print("Vault config not found")
except ValueError as e:
    print(f"Invalid vault config: {e}")
```

## Upgrading to Full Protocol

For production use, upgrade to the full protocol implementation:

```bash
# Install full protocol
pip install -e .

# Use protocol implementation
from mirrordna import ConfigLoader, Timeline, compute_state_checksum

loader = ConfigLoader()
citation = loader.load_master_citation("citation.yaml")
timeline = Timeline(timeline_id=citation.id)
```

Full protocol adds:
- JSON schema validation
- Advanced state snapshots
- Cryptographic signing
- Complete protocol compliance

## Questions?

- **SDK Overview**: [overview.md](overview.md)
- **Design Details**: [design_notes.md](design_notes.md)
- **Protocol Docs**: [../../docs/](../../docs/)

---

**MirrorDNA Python SDK** - Simple tools for building with persistence.

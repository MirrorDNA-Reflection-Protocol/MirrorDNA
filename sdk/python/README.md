# MirrorDNA Python SDK

Simple, local-first Python SDK for MirrorDNA protocol operations.

## What is This?

This SDK provides a simplified interface for working with MirrorDNA concepts locally:

- **Load vault configurations** from YAML/JSON files
- **Compute state hashes** for directories (deterministic, SHA-256)
- **Validate timeline files** against basic schema requirements
- **Track continuity status** across sessions

**This SDK is for:**
- Local development and testing
- Understanding MirrorDNA concepts
- Building simple integrations
- Learning the protocol

**This SDK is NOT:**
- A hosted service or API client
- A complete vault manager
- A production-grade system (for that, see `src/mirrordna/`)

## Installation

### Option 1: Use within MirrorDNA repo

```bash
# From MirrorDNA root directory
cd sdk/python
python examples/basic_usage.py
```

### Option 2: Install as a module

```bash
# Install dependencies
pip install pyyaml

# Add to your Python path or copy mirrordna_client.py to your project
```

## Dependencies

- **Python 3.7+** (uses standard library)
- **pyyaml** (optional, only needed for YAML file support)

```bash
pip install pyyaml
```

That's it! No heavy frameworks or external services required.

## Quick Start

### Basic Example

```python
from mirrordna_client import MirrorDNAClient

# Initialize client
client = MirrorDNAClient()

# Load vault configuration
vault = client.load_vault_config("vault.yaml")
print(f"Loaded vault: {vault['vault_id']}")

# Compute state hash for a directory
state_hash = client.compute_state_hash("./my_vault_data")
print(f"State hash: {state_hash}")

# Validate timeline
result = client.validate_timeline("timeline.json")
if result['valid']:
    print(f"Timeline valid with {result['event_count']} events")
```

### Running the Example

```bash
cd sdk/python
python examples/basic_usage.py
```

This will demonstrate:
1. Loading a vault configuration
2. Computing deterministic state hashes
3. Validating timeline files
4. Getting continuity status

## API Reference

### MirrorDNAClient

Main client class for MirrorDNA operations.

#### `load_vault_config(path: str) -> Dict`

Load and validate a vault configuration file.

```python
vault = client.load_vault_config("vault.yaml")
print(vault['vault_id'])  # vault_example_001
print(vault['name'])      # My Vault
```

**Args:**
- `path`: Path to vault config file (JSON or YAML)

**Returns:** Dictionary with vault configuration

**Raises:**
- `FileNotFoundError`: If file doesn't exist
- `ValueError`: If config is invalid

---

#### `compute_state_hash(directory: str, ignore_patterns: list = None) -> str`

Compute deterministic SHA-256 hash of directory contents.

```python
hash1 = client.compute_state_hash("./my_vault")
# ... make changes ...
hash2 = client.compute_state_hash("./my_vault")

if hash1 != hash2:
    print("Vault state changed!")
```

**Args:**
- `directory`: Path to directory
- `ignore_patterns`: Optional patterns to ignore (default: `['.git', '__pycache__', '.DS_Store', '*.pyc']`)

**Returns:** 64-character hexadecimal SHA-256 hash

**Raises:**
- `FileNotFoundError`: If directory doesn't exist

**How it works:**
- Walks directory tree in deterministic order
- Hashes file contents and paths
- Combines into single SHA-256 hash
- Same directory state → same hash (always)

---

#### `validate_timeline(path: str) -> Dict`

Validate timeline file structure.

```python
result = client.validate_timeline("timeline.json")

if result['valid']:
    print(f"Timeline has {result['event_count']} events")
    print(f"From {result['first_event']} to {result['last_event']}")
else:
    print(f"Errors: {result['errors']}")
```

**Args:**
- `path`: Path to timeline file (JSON or YAML)

**Returns:** Dictionary with validation results:
```python
{
    'valid': bool,
    'event_count': int,
    'timeline_id': str,
    'errors': list,
    'first_event': str,  # ISO timestamp
    'last_event': str    # ISO timestamp
}
```

---

#### `compute_data_checksum(data: Dict) -> str`

Compute deterministic checksum for dictionary data.

```python
data = {"id": "test", "version": "1.0"}
checksum = client.compute_data_checksum(data)
# Always produces same checksum for same data
```

**Args:**
- `data`: Dictionary to hash

**Returns:** SHA-256 hash string

---

#### `get_continuity_status(vault_path: str = None, timeline_path: str = None) -> Dict`

Get combined continuity status.

```python
status = client.get_continuity_status(
    vault_path="vault.yaml",
    timeline_path="timeline.json"
)

print(f"Vault: {status['vault_id']}")
print(f"Events: {status['event_count']}")
print(f"State hash: {status['state_hash']}")
```

**Args:**
- `vault_path`: Optional path to vault config
- `timeline_path`: Optional path to timeline

**Returns:** Status dictionary with vault info, timeline validation, and state hash

---

### Convenience Functions

Quick utilities for common operations:

```python
from mirrordna_client import quick_hash_directory, quick_validate_timeline

# Quick hash
hash = quick_hash_directory("./my_data")

# Quick validation
is_valid = quick_validate_timeline("timeline.json")
```

## Usage Patterns

### Pattern 1: Detect Vault Changes

```python
client = MirrorDNAClient()

# Compute initial hash
hash1 = client.compute_state_hash("./vault_data")

# ... user makes changes ...

# Check for changes
hash2 = client.compute_state_hash("./vault_data")

if hash1 != hash2:
    print("Vault state has changed!")
    print(f"Old: {hash1}")
    print(f"New: {hash2}")
```

### Pattern 2: Validate Continuity

```python
client = MirrorDNAClient()

# Load vault
vault = client.load_vault_config("vault.yaml")

# Validate timeline
result = client.validate_timeline("timeline.json")

if result['valid']:
    print(f"✓ Continuity intact: {result['event_count']} events")
else:
    print(f"✗ Continuity broken: {result['errors']}")
```

### Pattern 3: Session Tracking

```python
client = MirrorDNAClient()

# Start of session
status_start = client.get_continuity_status(
    vault_path="vault.yaml",
    timeline_path="timeline.json"
)

print(f"Session started at: {status_start['timestamp']}")
print(f"Starting event count: {status_start['event_count']}")

# ... session activity ...

# End of session
status_end = client.get_continuity_status(
    vault_path="vault.yaml",
    timeline_path="timeline.json"
)

events_added = status_end['event_count'] - status_start['event_count']
print(f"Events added this session: {events_added}")
```

## File Format Examples

### Vault Config (vault.yaml)

```yaml
vault_id: vault_example_001
name: My Example Vault
path: ./vault_data
created_at: "2025-11-14T10:00:00Z"

entries:
  - id: entry_001
    type: memory
    created_at: "2025-11-14T10:00:00Z"
```

### Timeline (timeline.json)

```json
{
  "timeline_id": "mc_agent_001",
  "event_count": 2,
  "events": [
    {
      "id": "evt_001",
      "timestamp": "2025-11-14T10:00:00Z",
      "event_type": "session_start",
      "actor": "mc_agent_001",
      "payload": {"platform": "Local"}
    },
    {
      "id": "evt_002",
      "timestamp": "2025-11-14T10:05:00Z",
      "event_type": "memory_created",
      "actor": "mc_agent_001",
      "payload": {"content": "Example memory"}
    }
  ]
}
```

## Limitations

This SDK is intentionally simple and has the following limitations:

1. **Local only** - No network operations or hosted APIs
2. **Basic validation** - Does not perform deep JSON schema validation
3. **No encryption** - Files are read/written in plaintext
4. **No signing** - Does not handle cryptographic signatures
5. **In-memory only** - Does not maintain persistent state

For production use cases, see the full protocol implementation in `src/mirrordna/`.

## Relation to MirrorDNA Protocol

This SDK is a **simplified wrapper** around core MirrorDNA concepts:

```
┌─────────────────────────────────────┐
│  Your Application                   │
├─────────────────────────────────────┤
│  SDK (this directory)               │  ← Simple, local operations
│  - MirrorDNAClient                  │
│  - Basic validation                 │
│  - State hashing                    │
├─────────────────────────────────────┤
│  MirrorDNA Protocol (src/mirrordna/)│  ← Full implementation
│  - ConfigLoader                     │
│  - Timeline                         │
│  - State Snapshots                  │
│  - Checksum verification            │
└─────────────────────────────────────┘
```

**For full features**, use the protocol implementation:
- Schema validation with jsonschema
- Timeline event management
- State snapshot capture
- Master Citation handling

**For simple local operations**, use this SDK:
- Quick vault config checks
- Directory hashing
- Basic timeline validation

## Next Steps

- **Try the example:** `python examples/basic_usage.py`
- **Read the protocol docs:** `../../docs/overview.md`
- **Explore full implementation:** `../../src/mirrordna/`
- **Check schemas:** `../../schemas/protocol/`

## License

MIT License — See [LICENSE](../../LICENSE) for details.

---

**MirrorDNA SDK** — Simple tools for identity and continuity.

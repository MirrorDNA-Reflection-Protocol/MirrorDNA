# MirrorDNA SDK Overview

## What is the MirrorDNA SDK?

The MirrorDNA SDK is a **developer toolkit** that makes it easy to integrate MirrorDNA protocol concepts into your applications. It provides simple, high-level APIs in both Python and JavaScript for working with:

- **Master Citations** - Identity binding documents
- **State Hashing** - Deterministic integrity verification
- **Timeline Events** - Continuity tracking
- **Vault Configurations** - Storage management

## Design Philosophy

The SDK is designed to be:

✅ **Simple** - Easy-to-use APIs without complex setup
✅ **Local-first** - Works with files, no backend required
✅ **Conceptual** - Demonstrates MirrorDNA principles
✅ **Educational** - Great for learning and experimentation
✅ **Lightweight** - Minimal dependencies

## SDK vs Protocol

```
┌─────────────────────────────────────┐
│  Your Application                   │
├─────────────────────────────────────┤
│  SDK Layer (this toolkit)           │  ← Simple client APIs
│  - Python: mirror_dna_client.py     │
│  - JavaScript: mirror_dna_client.js │
├─────────────────────────────────────┤
│  MirrorDNA Protocol                 │  ← Core protocol implementation
│  - Master Citations                 │
│  - Timeline Events                  │
│  - State Snapshots                  │
│  - Schema Validation                │
└─────────────────────────────────────┘
```

**SDK Layer** (this directory):
- High-level convenience methods
- Minimal dependencies
- Quick integration
- Educational examples

**Protocol Layer** (`/src/mirrordna/`):
- Full protocol implementation
- Schema validation
- Production-grade
- Complete feature set

## What Can You Build?

### For Developers

```python
# Track data integrity
data = {"user": "alice", "preferences": {...}}
hash_value = client.compute_state_hash(data)

# Later, verify integrity
if client.verify_checksum(data, hash_value):
    print("Data integrity verified ✓")
```

### For AI Agents

```javascript
// Create agent identity
const citation = client.createMasterCitation('agent_001', 'vault_main');

// Track activities
client.createTimelineEvent('session_start', citation.id);
client.createTimelineEvent('memory_created', citation.id, {
    content: 'User prefers dark mode'
});

// Check continuity
const status = client.getContinuityStatus(citation.id);
console.log(`Agent status: ${status.status}`);
```

### For Platform Builders

```python
# Load configuration
vault = client.load_vault_config('vault.yaml')

# Validate timeline integrity
events = client.load_timeline('agent_timeline.json')
validation = client.validate_timeline(events)

if not validation['valid']:
    print(f"Errors detected: {validation['errors']}")
```

## Available SDKs

### Python SDK

- **Location**: `sdk/python/`
- **File**: `mirror_dna_client.py`
- **Dependencies**: PyYAML (optional)
- **Examples**: `sdk/python/examples/basic_usage.py`
- **Guide**: [python_guide.md](python_guide.md)

### JavaScript SDK

- **Location**: `sdk/javascript/`
- **File**: `mirror_dna_client.js`
- **Dependencies**: js-yaml
- **Examples**: `sdk/javascript/examples/basic_usage.js`
- **Guide**: [javascript_guide.md](javascript_guide.md)

## Core Features

### 1. Master Citation Management

Create and manage identity binding documents:

```python
citation = client.create_master_citation(
    identity_id="agent_001",
    vault_id="vault_main"
)
```

Every citation includes:
- Unique ID
- Vault binding
- Constitutional alignment
- SHA-256 checksum

### 2. State Hashing

Compute deterministic hashes for data integrity:

```javascript
const hash = client.computeStateHash(data);
// Same data → same hash, always
```

Uses SHA-256 with canonical JSON representation (sorted keys).

### 3. Timeline Validation

Validate event structures and track continuity:

```python
validation = client.validate_timeline(events)

# Returns:
# - valid: True/False
# - total_events: count
# - event_types: breakdown
# - unique_actors: count
# - errors: list of issues
```

### 4. Continuity Tracking

Monitor identity activity and status:

```javascript
const status = client.getContinuityStatus('agent_001');
// Returns: status, total_events, last_activity, valid
```

## How It Relates to MirrorDNA-Standard

**MirrorDNA** (this repository) provides the **protocol layer**:
- Data structures (Master Citations, Timeline, Snapshots)
- Checksum verification
- Storage-agnostic design

**MirrorDNA-Standard** provides the **constitutional framework**:
- Rights and responsibilities
- Compliance levels
- Governance model

**SDK** (this toolkit) provides the **developer interface**:
- Simple APIs
- Quick integration
- Local operations

Together, they enable:
1. **Identity** - Via Master Citations (MirrorDNA)
2. **Rights** - Via Constitutional alignment (Standard)
3. **Integration** - Via SDK (this toolkit)

## Offline/Local Design

The SDK is intentionally designed for **local, offline operation**:

✅ No network calls
✅ No database required
✅ No authentication needed
✅ No hosted services

Everything works with:
- **Files** - JSON/YAML configs
- **In-memory** - Cached data
- **Filesystem** - Local storage

This makes it perfect for:
- Development and testing
- Educational purposes
- Proof-of-concept projects
- Edge/offline environments

## Use Cases

### Prototyping

Quickly experiment with MirrorDNA concepts:

```python
client = MirrorDNAClient()
citation = client.create_master_citation('test_agent', 'test_vault')
client.create_timeline_event('session_start', citation['id'])
status = client.get_continuity_status(citation['id'])
```

### Learning

Understand how MirrorDNA works without complex setup:

```javascript
// Create identity
const citation = client.createMasterCitation('learning_agent', 'vault');

// Track events
client.createTimelineEvent('memory_created', citation.id, {...});

// Validate
const validation = client.validateTimeline(events);
```

### Integration

Add MirrorDNA concepts to your existing application:

```python
# Existing app
user_data = load_user_preferences()

# Add integrity verification
checksum = client.compute_state_hash(user_data)
save_with_checksum(user_data, checksum)

# Later, verify
if client.verify_checksum(loaded_data, stored_checksum):
    process_user_data(loaded_data)
```

### Testing

Test MirrorDNA-compatible systems:

```javascript
// Test identity creation
const citation = client.createMasterCitation('test', 'vault');
assert(citation.checksum.length === 64);

// Test timeline validation
const events = generateTestEvents();
const validation = client.validateTimeline(events);
assert(validation.valid === true);
```

## Next Steps

1. **Choose your language**:
   - [Python Guide](python_guide.md)
   - [JavaScript Guide](javascript_guide.md)

2. **Run the examples**:
   - Python: `python sdk/python/examples/basic_usage.py`
   - JavaScript: `node sdk/javascript/examples/basic_usage.js`

3. **Read the design notes**:
   - [Design Notes](design_notes.md)

4. **Explore the protocol**:
   - [Protocol Documentation](../../docs/)
   - [Integration Guide](../../docs/integration-guide.md)

## Questions?

- **SDK Issues**: Check the README files in each SDK directory
- **Protocol Questions**: See [/docs/](../../docs/)
- **Integration Help**: Read [integration-guide.md](../../docs/integration-guide.md)
- **Concepts**: See [glossary.md](../../docs/glossary.md)

---

**MirrorDNA SDK** - Simple tools for building with the architecture of persistence.

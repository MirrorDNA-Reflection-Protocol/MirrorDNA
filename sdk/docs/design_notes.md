# MirrorDNA SDK Design Notes

Technical design decisions and implementation details for the MirrorDNA SDK.

## Overview

The MirrorDNA SDK provides a **simplified, educational interface** to MirrorDNA protocol concepts. It's designed to be:

- **Conceptual** - Demonstrates core principles
- **Standalone** - Minimal dependencies
- **Local-first** - No backend required
- **Educational** - Easy to understand and extend

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Application Layer                                      │
│  - User applications                                    │
│  - Integration code                                     │
│  - Tests and demos                                      │
├─────────────────────────────────────────────────────────┤
│  SDK Layer (this toolkit)                               │
│  ┌───────────────────┐  ┌───────────────────────────┐  │
│  │  Python SDK       │  │  JavaScript SDK           │  │
│  │  - Client API     │  │  - Client API             │  │
│  │  - File ops       │  │  - File ops               │  │
│  │  - Hashing        │  │  - Hashing                │  │
│  │  - Validation     │  │  - Validation             │  │
│  └───────────────────┘  └───────────────────────────┘  │
├─────────────────────────────────────────────────────────┤
│  MirrorDNA Protocol Layer                               │
│  - Master Citations (identity binding)                  │
│  - Timeline Events (continuity tracking)                │
│  - State Snapshots (integrity verification)             │
│  - Schema Validation (protocol compliance)              │
└─────────────────────────────────────────────────────────┘
```

## Design Principles

### 1. Local-First Operations

**Decision**: SDK operates entirely locally without network dependencies.

**Rationale**:
- Enables offline development
- Reduces complexity
- Educational clarity
- No authentication required
- Fast iteration

**Implementation**:
- File-based storage (JSON/YAML)
- In-memory caching
- No HTTP calls
- No database connections

### 2. Minimal Dependencies

**Decision**: Keep dependencies to absolute minimum.

**Python**:
- Required: None (stdlib only)
- Optional: PyYAML (for YAML support)

**JavaScript**:
- Required: js-yaml
- Node.js 14+

**Rationale**:
- Easy installation
- Reduced security surface
- Educational clarity
- Portable code

### 3. Deterministic Hashing

**Decision**: Use SHA-256 with canonical JSON representation.

**Implementation**:
```python
# Python
canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))
sha256 = hashlib.sha256()
sha256.update(canonical_json.encode('utf-8'))
return sha256.hexdigest()
```

```javascript
// JavaScript
const canonical = JSON.stringify(data, Object.keys(data).sort(), '');
const hash = crypto.createHash('sha256');
hash.update(canonical);
return hash.digest('hex');
```

**Why**:
- Same data → same hash (always)
- Sorted keys ensure consistency
- No whitespace variance
- Standard SHA-256 algorithm

### 4. Simple API Surface

**Decision**: High-level methods covering common use cases.

**Core operations**:
1. `load_vault_config()` - Configuration loading
2. `compute_state_hash()` - Integrity hashing
3. `validate_timeline()` - Event validation
4. `create_master_citation()` - Identity creation
5. `create_timeline_event()` - Event tracking
6. `get_continuity_status()` - Status checking
7. `save/load` methods - Persistence

**Rationale**:
- Covers 80% of use cases
- Easy to learn
- Clear naming
- Consistent patterns

### 5. In-Memory Caching

**Decision**: Cache loaded data in memory for quick access.

**Implementation**:
```python
self._vault_cache: Dict[str, Any] = {}
self._timeline_cache: Dict[str, List[Dict]] = {}
```

**Rationale**:
- Fast repeated access
- Session-scoped data
- No external state management
- Simple cleanup (process exit)

## Implementation Details

### State Hashing Algorithm

**Requirement**: Deterministic, tamper-evident hashing.

**Algorithm**:
1. Accept dictionary/object input
2. Create canonical JSON:
   - Sort keys alphabetically
   - Remove all whitespace (`,` separator, `:` key-value separator)
   - UTF-8 encoding
3. Compute SHA-256 hash
4. Return 64-character hex string

**Example**:
```python
Input: {"name": "Alice", "age": 30}
Canonical: {"age":30,"name":"Alice"}
Hash: 5d41402abc4b2a76b9719d911017c592...
```

**Properties**:
- Order-independent (keys sorted)
- Deterministic (same input → same output)
- Collision-resistant (SHA-256)
- Tamper-evident (any change → different hash)

### Timeline Validation

**Validation checks**:

1. **Required fields**:
   - `id` - Unique event identifier
   - `timestamp` - ISO 8601 timestamp
   - `event_type` - Event category
   - `actor` - Identity performing action

2. **Metrics computed**:
   - Total event count
   - Event type breakdown
   - Unique actors
   - Timespan (first → last)

3. **Error collection**:
   - Missing field errors
   - Format validation errors

**Returns**:
```python
{
    'valid': True/False,
    'total_events': N,
    'event_types': {...},
    'unique_actors': N,
    'timespan': {'first': ..., 'last': ...},
    'errors': [...]
}
```

### Master Citation Structure

**Fields**:
```yaml
id: mc_<identity>_<timestamp>
version: "1.0.0"
vault_id: vault_<name>
created_at: "2025-11-14T10:00:00Z"
constitutional_alignment:
  compliance_level: "full"
  framework_version: "1.0"
  rights_bundle:
    - memory
    - continuity
    - portability
checksum: <SHA-256 of above fields>
```

**ID Generation**:
```python
timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
citation_id = f"mc_{identity_id}_{timestamp}"
```

**Checksum Computation**:
- Exclude `checksum` field from hash
- Compute hash of remaining data
- Add checksum to final document

### File Formats

**YAML for Citations** (human-readable identity):
```yaml
id: mc_agent_001_20251114_120000
version: "1.0.0"
vault_id: vault_main
created_at: "2025-11-14T12:00:00Z"
checksum: 5d41402abc4b2a76b9719d911017c592...
```

**JSON for Timelines** (structured events):
```json
{
  "timeline_id": "mc_agent_001",
  "event_count": 3,
  "events": [...]
}
```

**Rationale**:
- YAML: Better for config/identity (comments, readability)
- JSON: Better for events (tooling, parsing)

## Comparison: SDK vs Protocol

| Feature | SDK Layer | Protocol Layer |
|---------|-----------|----------------|
| **Purpose** | Quick integration | Full implementation |
| **Dependencies** | Minimal | Complete |
| **Validation** | Basic | Schema-based |
| **Storage** | Files only | Pluggable backends |
| **Crypto** | Hashing only | Signing + verification |
| **Audience** | Developers, learners | Production systems |
| **Complexity** | Low | Medium-High |
| **Completeness** | Core concepts | Full protocol |

**When to use SDK**:
- Learning MirrorDNA concepts
- Prototyping
- Simple integrations
- Educational projects

**When to use Protocol**:
- Production systems
- Schema validation required
- Advanced features needed
- Full protocol compliance

## Design Trade-offs

### 1. Simplicity vs Features

**Choice**: Favor simplicity

**Trade-offs**:
- ✅ Easy to learn
- ✅ Quick integration
- ✅ Clear code
- ❌ Limited features
- ❌ No schema validation
- ❌ No cryptographic signing

**Mitigation**: Provide upgrade path to full protocol.

### 2. Performance vs Readability

**Choice**: Favor readability

**Trade-offs**:
- ✅ Clear implementation
- ✅ Easy to debug
- ✅ Educational value
- ❌ Not optimized
- ❌ In-memory limits
- ❌ File I/O on every save

**Mitigation**: Document performance characteristics.

### 3. Flexibility vs Constraints

**Choice**: Opinionated defaults

**Trade-offs**:
- ✅ Quick start
- ✅ Consistent usage
- ✅ Fewer decisions
- ❌ Less flexibility
- ❌ Fixed patterns

**Mitigation**: Allow customization where it matters (data_dir, filenames).

## Extension Points

### Custom Storage

Current: File-based only

**How to extend**:
```python
class CustomMirrorDNAClient(MirrorDNAClient):
    def save_citation(self, citation, filename=None):
        # Custom storage logic (S3, database, etc.)
        pass

    def load_timeline(self, path):
        # Custom retrieval logic
        pass
```

### Additional Validation

Current: Basic field checking

**How to extend**:
```python
def validate_timeline(self, events):
    validation = super().validate_timeline(events)

    # Add custom validation
    for event in events:
        if event['event_type'] == 'custom_type':
            # Custom logic
            pass

    return validation
```

### Event Types

Current: Open-ended strings

**How to extend**:
```python
# Define custom event types
CUSTOM_EVENT_TYPES = [
    'user_login',
    'data_export',
    'permission_change'
]

def create_timeline_event(self, event_type, actor, payload=None):
    if event_type not in CUSTOM_EVENT_TYPES:
        raise ValueError(f"Unknown event type: {event_type}")

    return super().create_timeline_event(event_type, actor, payload)
```

## Testing Strategy

### Unit Tests

**Coverage**:
- Hash determinism
- Timeline validation
- Checksum verification
- File I/O

**Example**:
```python
def test_hash_determinism():
    client = MirrorDNAClient()
    data = {"key": "value"}

    hash1 = client.compute_state_hash(data)
    hash2 = client.compute_state_hash(data)

    assert hash1 == hash2
    assert len(hash1) == 64
```

### Integration Tests

**Coverage**:
- Complete workflows
- File creation/loading
- Multi-step operations

**Example**:
```python
def test_complete_workflow():
    client = MirrorDNAClient()

    # Create citation
    citation = client.create_master_citation('test', 'vault')

    # Save and load
    path = client.save_citation(citation)
    # ... verify file exists and is valid
```

## Future Enhancements

### Potential Additions

1. **Schema validation** (optional dependency on jsonschema)
2. **Async operations** (async/await support)
3. **Batch operations** (save multiple entities)
4. **Export formats** (CSV, XML)
5. **CLI tool** (command-line interface)

### Migration Path

**From SDK to Protocol**:

```python
# SDK code
from mirror_dna_client import MirrorDNAClient
client = MirrorDNAClient()
citation = client.create_master_citation('agent', 'vault')

# Protocol code
from mirrordna import ConfigLoader, compute_state_checksum
loader = ConfigLoader()
citation_data = {...}
citation_data['checksum'] = compute_state_checksum(citation_data)
```

**Key differences**:
- Protocol uses dataclasses
- Schema validation included
- More configuration options
- Production-ready features

## Performance Characteristics

### Time Complexity

- `compute_state_hash()`: O(n) where n = data size
- `validate_timeline()`: O(m) where m = event count
- `create_timeline_event()`: O(1) amortized
- `get_continuity_status()`: O(m) where m = event count

### Space Complexity

- In-memory cache: O(v + t) where v = vaults, t = total events
- File storage: Unlimited (filesystem-bound)

### Scalability Limits

**Good for**:
- < 10,000 events per timeline
- < 100 vaults cached
- < 100 MB total data

**Not designed for**:
- Millions of events
- Real-time streaming
- Distributed systems
- High-concurrency writes

## Security Considerations

### What's Included

✅ Data integrity (SHA-256 hashing)
✅ Tamper detection (checksum verification)
✅ Deterministic verification

### What's NOT Included

❌ Authentication
❌ Authorization
❌ Encryption at rest
❌ Cryptographic signing
❌ Access control

**Note**: SDK is designed for local development. For production security, use the full protocol with cryptographic signing.

## Questions & Decisions

### Q: Why no database support?

**A**: Simplicity. Files are universal, portable, and easy to understand. For database support, use the full protocol or extend the SDK.

### Q: Why SHA-256 instead of newer algorithms?

**A**: SHA-256 is:
- Widely supported
- Well-understood
- Sufficient for integrity checking
- Standard in blockchain/crypto

### Q: Why both Python and JavaScript?

**A**: Reach the broadest developer audience:
- Python: AI/ML, data science, backend
- JavaScript: Frontend, Node.js, full-stack

### Q: Will you add more languages?

**A**: Possible future additions:
- Go (performance, systems)
- Rust (safety, embedded)
- TypeScript (better than .js wrapper)

Depends on community demand.

## References

- **Protocol Documentation**: [/docs/](../../docs/)
- **Schema Reference**: [/docs/schema-reference.md](../../docs/schema-reference.md)
- **Integration Guide**: [/docs/integration-guide.md](../../docs/integration-guide.md)
- **SHA-256 Spec**: [NIST FIPS 180-4](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf)

---

**MirrorDNA SDK** - Thoughtfully designed for simplicity and education.

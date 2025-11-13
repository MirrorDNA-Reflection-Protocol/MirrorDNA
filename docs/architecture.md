# MirrorDNA Architecture

This document describes the internal architecture of the MirrorDNA protocol and reference implementation.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Application Layer                       │
│         (ActiveMirrorOS, LingOS, etc.)                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              MirrorDNA Protocol Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Identity    │  │  Continuity  │  │   Memory     │  │
│  │  Manager     │  │   Tracker    │  │   Manager    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Agent DNA   │  │  Validator   │  │    Crypto    │  │
│  │  Manager     │  │    Engine    │  │    Utils     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  Storage Layer                           │
│    (Local files, Database, Key-Value Store, etc.)       │
└─────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Identity Manager

**Purpose:** Create, validate, and manage identities for users and agents.

**Key Operations:**
- `create_identity(type, metadata)` → Identity record
- `validate_identity(identity)` → Boolean
- `sign_claim(identity, claim, private_key)` → Signature
- `verify_claim(identity, claim, signature)` → Boolean

**Data Flow:**
1. Application requests a new identity
2. Identity Manager generates unique ID with namespace
3. Crypto Utils generate key pair
4. Identity record created with public key
5. Validator checks against schema
6. Identity stored in Storage Layer
7. Private key returned to application (NOT stored)

**Schema:** `schemas/identity.schema.json`

### 2. Continuity Tracker

**Purpose:** Track session lineage and context preservation across interactions.

**Key Operations:**
- `create_session(agent_id, user_id, parent_session_id)` → Session record
- `get_session_lineage(session_id)` → List of ancestor sessions
- `get_context(session_id)` → Context metadata from lineage
- `end_session(session_id, final_state)` → Updated session record

**Data Flow:**
1. Application starts new interaction
2. Continuity Tracker creates session with link to parent (if any)
3. Lineage retrieved to restore context
4. Session ID used to tag all memories and events
5. When interaction ends, session marked complete with final state

**Schema:** `schemas/continuity.schema.json`

### 3. Memory Manager

**Purpose:** Store, retrieve, and manage memory records across three tiers.

**Key Operations:**
- `write_memory(content, tier, metadata)` → Memory record
- `read_memory(query, tier, limit)` → List of memory records
- `search_memory(query_vector, tier, limit)` → Ranked memory records
- `archive_memory(memory_id)` → Archived memory record
- `consolidate_memories(memory_ids)` → Consolidated memory record

**Data Flow:**
1. Application writes new memory (fact, event, conversation turn)
2. Memory Manager assigns tier (short, long, episodic)
3. Timestamps and metadata added
4. Stored in appropriate tier
5. When queried, memories ranked by relevance, recency, or score
6. Old short-term memories promoted to long-term or archived

**Tiers:**
- **Short-term:** Current session, immediate context (ephemeral)
- **Long-term:** Persistent facts, patterns (indefinite retention)
- **Episodic:** Specific events, conversations (timestamped narratives)

**Schema:** `schemas/memory.schema.json`

### 4. Agent DNA Manager

**Purpose:** Define and manage agent personality, behavior, and alignment.

**Key Operations:**
- `create_agent_dna(traits, constraints, capabilities)` → Agent DNA record
- `validate_agent_dna(agent_dna)` → Boolean
- `update_agent_dna(agent_dna_id, updates)` → Updated DNA record
- `get_behavior_constraints(agent_dna_id)` → List of constraints

**Data Flow:**
1. Application defines agent personality and constraints
2. Agent DNA Manager validates against schema
3. Constitutional alignment rules embedded
4. DNA versioned and stored
5. When agent acts, constraints checked against DNA
6. DNA can evolve over time with version history

**Schema:** `schemas/agent.schema.json`

### 5. Validator Engine

**Purpose:** Validate all MirrorDNA data structures against schemas.

**Key Operations:**
- `validate_schema(data, schema_name)` → Validation result
- `load_schema(schema_name)` → JSON schema object
- `get_validation_errors(data, schema_name)` → List of error messages

**Data Flow:**
1. Any create/update operation calls Validator first
2. Validator loads appropriate JSON schema
3. Data validated using JSON Schema Draft 7 rules
4. If invalid, return detailed error messages
5. If valid, operation proceeds

**Schemas Location:** `schemas/*.schema.json`

### 6. Crypto Utils

**Purpose:** Cryptographic operations for identity and verification.

**Key Operations:**
- `generate_keypair()` → (public_key, private_key)
- `sign(message, private_key)` → Signature
- `verify(message, signature, public_key)` → Boolean
- `hash(data)` → Hash digest

**Implementation:**
- Uses standard cryptographic libraries (e.g., Python `cryptography`)
- Ed25519 for signatures (fast, secure, compact)
- SHA-256 for hashing
- No custom crypto (avoid reinventing wheels)

## Data Schemas

All data structures defined as JSON schemas in the `schemas/` directory:

### Identity Schema

```json
{
  "identity_id": "mdna_usr_abc123",
  "identity_type": "user | agent | system",
  "created_at": "ISO 8601 timestamp",
  "public_key": "Base64-encoded public key",
  "metadata": {
    "name": "Optional name",
    "description": "Optional description",
    "version": "Optional version string"
  }
}
```

### Continuity Schema

```json
{
  "session_id": "sess_xyz789",
  "parent_session_id": "sess_abc456 | null",
  "agent_id": "mdna_agt_mirror01",
  "user_id": "mdna_usr_alice",
  "started_at": "ISO 8601 timestamp",
  "ended_at": "ISO 8601 timestamp | null",
  "context_metadata": {
    "restored_from": "parent session ID",
    "topic": "Optional topic",
    "tags": ["tag1", "tag2"]
  }
}
```

### Memory Schema

```json
{
  "memory_id": "mem_xyz123",
  "tier": "short_term | long_term | episodic",
  "content": "Text or structured data",
  "source": {
    "session_id": "sess_xyz789",
    "timestamp": "ISO 8601",
    "agent_id": "mdna_agt_mirror01"
  },
  "metadata": {
    "tags": ["fact", "preference"],
    "relevance_score": 0.95,
    "access_count": 3,
    "last_accessed": "ISO 8601"
  }
}
```

### Agent DNA Schema

```json
{
  "agent_dna_id": "dna_mirror01_v2",
  "agent_id": "mdna_agt_mirror01",
  "version": "2.1.0",
  "personality_traits": {
    "tone": "reflective",
    "style": "conversational",
    "values": ["clarity", "honesty", "growth"]
  },
  "behavioral_constraints": [
    "Never impersonate users",
    "Acknowledge uncertainty",
    "Respect privacy"
  ],
  "capabilities": ["reflection", "continuity", "memory"],
  "constitutional_alignment": {
    "framework": "MirrorDNA-Standard v1.0",
    "safety_rules": ["..."]
  }
}
```

## Storage Layer

MirrorDNA is **storage-agnostic**. The reference implementation provides adapters for:

1. **Local JSON files** (default, simplest)
2. **SQLite** (lightweight embedded database)
3. **Redis** (key-value store for high-speed access)
4. **PostgreSQL** (relational database for production)

### Storage Interface

All storage adapters implement:

```python
class StorageAdapter:
    def create(self, collection: str, record: dict) -> str:
        """Create a new record, return ID"""

    def read(self, collection: str, record_id: str) -> dict:
        """Read a record by ID"""

    def update(self, collection: str, record_id: str, updates: dict) -> dict:
        """Update a record"""

    def delete(self, collection: str, record_id: str) -> bool:
        """Delete a record"""

    def query(self, collection: str, filters: dict, limit: int) -> list:
        """Query records with filters"""
```

Collections:
- `identities`
- `sessions`
- `memories`
- `agent_dna`

## Security Considerations

### 1. Private Key Management

- Private keys are **never stored** by MirrorDNA
- Applications responsible for secure key storage
- Consider hardware security modules (HSMs) for production
- Key rotation supported via identity versioning

### 2. Data Encryption

- Sensitive memory content should be encrypted at rest
- Use application-level encryption before storing
- MirrorDNA provides hooks for encryption adapters
- Transport layer security (TLS) for network operations

### 3. Access Control

- Identity-based access control for memory and sessions
- Agent DNA defines what an agent can/cannot do
- Storage layer can enforce additional ACLs
- Audit logs track all access to sensitive data

### 4. Privacy

- Minimal data collection (only what's needed for functionality)
- Local-first design (no required cloud services)
- User data sovereignty (users control their data)
- Clear data retention policies (configurable)

## Performance Characteristics

### Identity Operations
- **Create:** O(1) — constant time
- **Validate:** O(1) — schema check, signature verify
- **Lookup:** O(1) — indexed by ID

### Continuity Operations
- **Create session:** O(1)
- **Get lineage:** O(n) where n = depth of session tree
- **Restore context:** O(n*m) where m = avg memories per session

### Memory Operations
- **Write:** O(1) — append to tier
- **Read by ID:** O(1) — indexed lookup
- **Search:** O(n) naive, O(log n) with indexes, O(1) with vector DB
- **Consolidate:** O(k) where k = number of memories consolidated

### Scaling

- **Vertical:** Single-instance can handle 10k+ identities, 100k+ memories
- **Horizontal:** Shard by user_id or agent_id for multi-instance deployments
- **Memory tier:** Archive old memories to cold storage, keep hot memories in fast DB

## Extension Points

MirrorDNA is designed to be extended:

1. **Custom storage adapters** — Add support for new databases
2. **Custom validators** — Add domain-specific validation rules
3. **Custom memory tiers** — Define new tiers beyond short/long/episodic
4. **Custom crypto** — Swap crypto primitives (e.g., different signature schemes)
5. **Plugins** — Hook into lifecycle events (onCreate, onRead, etc.)

See `docs/integration-guide.md` for extension examples.

## Next Steps

- Read **[Schema Reference](schema-reference.md)** for detailed schema docs
- See **[Integration Guide](integration-guide.md)** for step-by-step integration
- Check **[examples/](../examples/)** for working code

---

**MirrorDNA** — The architecture of persistence.

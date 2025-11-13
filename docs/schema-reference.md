# MirrorDNA Schema Reference

This document provides detailed specifications for all MirrorDNA schemas.

## Schema Versioning

Current schema version: **1.0.0**

All schemas follow [Semantic Versioning](https://semver.org/):
- **Major:** Breaking changes to schema structure
- **Minor:** New optional fields
- **Patch:** Documentation or clarification updates

## Identity Schema

**File:** `schemas/identity.schema.json`

### Purpose
Represents a stable, verifiable identity for a user, agent, or system.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `identity_id` | string | ✓ | Unique identifier with namespace prefix |
| `identity_type` | enum | ✓ | One of: `user`, `agent`, `system` |
| `created_at` | string | ✓ | ISO 8601 timestamp of creation |
| `public_key` | string | ✓ | Base64-encoded Ed25519 public key |
| `metadata` | object | - | Optional metadata (see below) |

#### Identity ID Format

Format: `mdna_{type}_{unique_suffix}`

- **Namespace:** Always `mdna_`
- **Type prefix:**
  - `usr_` for users
  - `agt_` for agents
  - `sys_` for systems
- **Unique suffix:** 12+ alphanumeric characters

Examples:
- `mdna_usr_alice7x9k2m`
- `mdna_agt_mirror01_v2`
- `mdna_sys_platform_auth`

#### Identity Type

Valid values:
- **`user`** — Human user or entity controlling the system
- **`agent`** — AI agent or autonomous system
- **`system`** — Platform or infrastructure component

#### Metadata Object (Optional)

```json
{
  "name": "Human-readable name",
  "description": "Brief description of this identity",
  "version": "Semantic version string (for agents)",
  "custom": {
    "any_key": "Custom application-specific data"
  }
}
```

### Example

```json
{
  "identity_id": "mdna_usr_alice7x9k2m",
  "identity_type": "user",
  "created_at": "2025-01-15T10:00:00Z",
  "public_key": "MCowBQYDK2VwAyEA...",
  "metadata": {
    "name": "Alice",
    "description": "Primary user account"
  }
}
```

### Validation Rules

1. `identity_id` must match pattern: `^mdna_(usr|agt|sys)_[a-z0-9_]{12,}$`
2. `identity_type` must be one of: `user`, `agent`, `system`
3. `created_at` must be valid ISO 8601 timestamp
4. `public_key` must be valid base64-encoded key
5. If `metadata` present, must be valid JSON object

---

## Continuity Schema

**File:** `schemas/continuity.schema.json`

### Purpose
Tracks session lineage and context preservation across interactions.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `session_id` | string | ✓ | Unique session identifier |
| `parent_session_id` | string | - | ID of previous session (null if first) |
| `agent_id` | string | ✓ | Agent identity ID |
| `user_id` | string | ✓ | User identity ID |
| `started_at` | string | ✓ | ISO 8601 timestamp when session started |
| `ended_at` | string | - | ISO 8601 timestamp when session ended |
| `context_metadata` | object | - | Context restored from parent session |

#### Session ID Format

Format: `sess_{unique_suffix}`

- **Prefix:** Always `sess_`
- **Unique suffix:** 12+ alphanumeric characters, often timestamp-based

Examples:
- `sess_20250115_100030_a7x9k`
- `sess_xyz789abc123`

#### Context Metadata Object (Optional)

```json
{
  "restored_from": "parent_session_id",
  "topic": "Brief topic or context description",
  "tags": ["tag1", "tag2", "tag3"],
  "prior_memories_count": 5,
  "custom": {
    "any_key": "Application-specific context"
  }
}
```

### Example

```json
{
  "session_id": "sess_20250115_100030_a7x9k",
  "parent_session_id": "sess_20250114_150000_b2y8m",
  "agent_id": "mdna_agt_mirror01_v2",
  "user_id": "mdna_usr_alice7x9k2m",
  "started_at": "2025-01-15T10:00:30Z",
  "ended_at": null,
  "context_metadata": {
    "restored_from": "sess_20250114_150000_b2y8m",
    "topic": "Continuing discussion about project planning",
    "tags": ["planning", "productivity"],
    "prior_memories_count": 12
  }
}
```

### Validation Rules

1. `session_id` must match pattern: `^sess_[a-z0-9_]{12,}$`
2. `parent_session_id` if present, must match session ID pattern
3. `agent_id` must match valid identity ID pattern
4. `user_id` must match valid identity ID pattern
5. `started_at` must be valid ISO 8601 timestamp
6. `ended_at` if present, must be later than `started_at`

---

## Memory Schema

**File:** `schemas/memory.schema.json`

### Purpose
Represents a single memory record stored in one of three tiers.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `memory_id` | string | ✓ | Unique memory identifier |
| `tier` | enum | ✓ | One of: `short_term`, `long_term`, `episodic` |
| `content` | string/object | ✓ | Memory content (text or structured data) |
| `source` | object | ✓ | Source metadata (see below) |
| `metadata` | object | - | Additional metadata (see below) |

#### Memory ID Format

Format: `mem_{unique_suffix}`

- **Prefix:** Always `mem_`
- **Unique suffix:** 12+ alphanumeric characters

Examples:
- `mem_20250115_100045_c3z7n`
- `mem_abc123xyz789`

#### Tier

Valid values:
- **`short_term`** — Current session, immediate context (ephemeral)
- **`long_term`** — Persistent facts, patterns (indefinite retention)
- **`episodic`** — Specific events, conversations (timestamped narratives)

#### Source Object (Required)

```json
{
  "session_id": "sess_xyz789",
  "timestamp": "ISO 8601 timestamp",
  "agent_id": "mdna_agt_mirror01_v2",
  "user_id": "mdna_usr_alice7x9k2m"
}
```

#### Metadata Object (Optional)

```json
{
  "tags": ["fact", "preference", "goal"],
  "relevance_score": 0.95,
  "access_count": 3,
  "last_accessed": "ISO 8601 timestamp",
  "embedding_vector": [0.1, 0.2, ...],
  "custom": {
    "any_key": "Application-specific metadata"
  }
}
```

### Example

```json
{
  "memory_id": "mem_20250115_100045_c3z7n",
  "tier": "long_term",
  "content": "User prefers markdown documentation over video tutorials.",
  "source": {
    "session_id": "sess_20250115_100030_a7x9k",
    "timestamp": "2025-01-15T10:00:45Z",
    "agent_id": "mdna_agt_mirror01_v2",
    "user_id": "mdna_usr_alice7x9k2m"
  },
  "metadata": {
    "tags": ["preference", "learning"],
    "relevance_score": 0.92,
    "access_count": 1,
    "last_accessed": "2025-01-15T10:00:45Z"
  }
}
```

### Validation Rules

1. `memory_id` must match pattern: `^mem_[a-z0-9_]{12,}$`
2. `tier` must be one of: `short_term`, `long_term`, `episodic`
3. `content` must be non-empty (string or object)
4. `source.session_id` must be valid session ID
5. `source.timestamp` must be valid ISO 8601 timestamp
6. `source.agent_id` and `source.user_id` must be valid identity IDs

---

## Agent DNA Schema

**File:** `schemas/agent.schema.json`

### Purpose
Defines agent personality, behavior constraints, and constitutional alignment.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent_dna_id` | string | ✓ | Unique DNA record identifier |
| `agent_id` | string | ✓ | Associated agent identity ID |
| `version` | string | ✓ | Semantic version of this DNA |
| `personality_traits` | object | ✓ | Personality definition (see below) |
| `behavioral_constraints` | array | ✓ | List of behavior rules |
| `capabilities` | array | ✓ | List of agent capabilities |
| `constitutional_alignment` | object | - | Alignment framework reference |

#### Agent DNA ID Format

Format: `dna_{agent_name}_{version_suffix}`

- **Prefix:** Always `dna_`
- **Agent name:** Identifier from agent_id
- **Version suffix:** Version identifier

Examples:
- `dna_mirror01_v2_1_0`
- `dna_assistant_alpha`

#### Personality Traits Object (Required)

```json
{
  "tone": "reflective | conversational | formal | casual",
  "style": "concise | detailed | narrative | technical",
  "values": ["clarity", "honesty", "growth"],
  "custom": {
    "any_key": "Application-specific traits"
  }
}
```

#### Behavioral Constraints Array (Required)

List of strings defining what the agent will/won't do:

```json
[
  "Never impersonate users",
  "Acknowledge uncertainty when present",
  "Respect user privacy and data sovereignty",
  "Refuse harmful or unethical requests"
]
```

#### Capabilities Array (Required)

List of strings defining what the agent can do:

```json
[
  "reflection",
  "continuity",
  "memory_management",
  "conversation",
  "task_planning"
]
```

#### Constitutional Alignment Object (Optional)

```json
{
  "framework": "MirrorDNA-Standard v1.0",
  "safety_rules": [
    "Rule 1: Prioritize user safety",
    "Rule 2: Maintain transparency"
  ],
  "compliance_level": "full | partial | custom"
}
```

### Example

```json
{
  "agent_dna_id": "dna_mirror01_v2_1_0",
  "agent_id": "mdna_agt_mirror01_v2",
  "version": "2.1.0",
  "personality_traits": {
    "tone": "reflective",
    "style": "conversational",
    "values": ["clarity", "honesty", "growth"]
  },
  "behavioral_constraints": [
    "Never impersonate users",
    "Acknowledge uncertainty when present",
    "Respect user privacy and data sovereignty"
  ],
  "capabilities": [
    "reflection",
    "continuity",
    "memory_management",
    "conversation"
  ],
  "constitutional_alignment": {
    "framework": "MirrorDNA-Standard v1.0",
    "safety_rules": [
      "Prioritize user safety and wellbeing",
      "Maintain transparency about capabilities and limitations"
    ],
    "compliance_level": "full"
  }
}
```

### Validation Rules

1. `agent_dna_id` must match pattern: `^dna_[a-z0-9_]+$`
2. `agent_id` must be valid agent identity ID
3. `version` must follow semantic versioning (e.g., `1.2.3`)
4. `personality_traits` must be valid object
5. `behavioral_constraints` must be non-empty array of strings
6. `capabilities` must be non-empty array of strings

---

## Common Patterns

### Timestamps

All timestamps use **ISO 8601 format** with timezone:

```
2025-01-15T10:00:00Z        # UTC
2025-01-15T10:00:00-05:00   # EST
2025-01-15T10:00:00.123Z    # With milliseconds
```

### IDs

All IDs are **lowercase alphanumeric** with underscores:
- No spaces, no special characters (except `_`)
- Prefixes clearly identify the entity type
- Sufficient length to avoid collisions (12+ characters)

### Extensibility

All schemas support `custom` fields within metadata objects for application-specific data. This allows extension without breaking the core protocol.

---

## Validation

Use the MirrorDNA validator to check schema compliance:

```bash
python -m mirrordna.validate --schema identity --file my_identity.json
```

Or programmatically:

```python
from mirrordna import validate_schema

result = validate_schema(data, "identity")
if not result.is_valid:
    print(result.errors)
```

---

**MirrorDNA** — The architecture of persistence.

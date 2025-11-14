# Master Citation

## What is a Master Citation?

A Master Citation is **the binding document** that declares:

1. **Who you are** (identity ID)
2. **Where your state lives** (vault ID)
3. **What you align to** (constitutional framework)
4. **Your lineage** (predecessor/successor citations)

It's the entry point to a MirrorDNA identity. Everything else (timeline, snapshots, vault entries) references the Master Citation.

## Schema

**Location**: `schema/master_citation.schema.json`

**Required fields**:
```json
{
  "id": "mc_alice_primary_001",           // Pattern: ^mc_[a-z0-9_]{16,}$
  "version": "1.0.0",                      // Semantic version
  "vault_id": "vault_alice_main",         // Pattern: ^vault_[a-z0-9_]{16,}$
  "created_at": "2025-01-15T10:00:00Z",   // ISO 8601 timestamp
  "checksum": "a3f2c8b9e1d4..."           // SHA-256 (64 hex chars)
}
```

**Optional fields**:
```json
{
  "predecessor": "mc_alice_previous_v0",  // Previous citation ID
  "successor": "mc_alice_next_v2",        // Next citation ID (null if current)
  "constitutional_alignment": {
    "compliance_level": "full",           // full | partial | custom | none
    "framework_version": "1.0",
    "rights_bundle": ["memory", "continuity", "portability"],
    "constraints": []
  },
  "linked_agents": [                      // Optional AgentDNA links
    {
      "agent_id": "agent_alice_001",
      "role": "primary"
    }
  ],
  "metadata": {
    "display_name": "Alice",
    "description": "Primary identity for Alice",
    "tags": ["human", "verified"]
  }
}
```

## Loading a Master Citation

```python
from mirrordna import ConfigLoader

loader = ConfigLoader()

# Load and verify checksum
citation = loader.load_master_citation(
    "alice_citation.yaml",
    verify_checksum=True  # Default: True
)

print(citation.id)        # mc_alice_primary_001
print(citation.vault_id)  # vault_alice_main
```

If checksum verification fails, `ConfigLoader` raises `ValueError`.

## Creating a Master Citation

### Step 1: Define the document

Create `alice_citation.yaml`:
```yaml
id: mc_alice_primary_001
version: "1.0.0"
vault_id: vault_alice_main
created_at: "2025-01-15T10:00:00Z"
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
  display_name: Alice
  description: Primary identity for Alice
  tags:
    - human
    - verified
```

### Step 2: Compute checksum

```python
import yaml
from mirrordna import compute_state_checksum

# Load document
with open("alice_citation.yaml") as f:
    data = yaml.safe_load(f)

# Remove checksum field if present
data_without_checksum = {k: v for k, v in data.items() if k != "checksum"}

# Compute checksum
checksum = compute_state_checksum(data_without_checksum)
print(checksum)  # e.g., a3f2c8b9e1d4f7a2c5b8...
```

### Step 3: Add checksum to document

Update `alice_citation.yaml`:
```yaml
checksum: "a3f2c8b9e1d4f7a2c5b8..."
```

### Step 4: Validate

```python
loader = ConfigLoader()
citation = loader.load_master_citation("alice_citation.yaml")
# If no error, citation is valid!
```

## Constitutional Alignment

The `constitutional_alignment` section declares adherence to a constitutional framework (e.g., MirrorDNA-Standard).

**Fields**:

- `compliance_level`:
  - `full` — Full compliance with framework
  - `partial` — Partial compliance (specify which parts)
  - `custom` — Custom constitutional rules
  - `none` — No constitutional alignment

- `framework_version`: Which version of the constitution (e.g., "1.0", "2.1")

- `rights_bundle`: Which rights are granted (e.g., `["memory", "continuity", "portability"]`)

- `constraints`: Optional constraints (e.g., `["no_export", "read_only"]`)

**Example**:
```yaml
constitutional_alignment:
  compliance_level: full
  framework_version: "1.0"
  rights_bundle:
    - memory          # Right to persistent memory
    - continuity      # Right to unbroken timeline
    - portability     # Right to export identity
  constraints: []     # No constraints
```

This allows agents/platforms to verify: "Does this identity comply with constitutional requirements?"

## Lineage (Predecessor/Successor)

Master Citations form a **linked list** via `predecessor` and `successor` fields.

**Use case**: Identity evolution over time.

### Example: Vault Migration

```yaml
# Original citation (vault_a)
id: mc_alice_v1
vault_id: vault_alice_a
created_at: "2025-01-01T00:00:00Z"
checksum: "abc123..."
predecessor: null
successor: "mc_alice_v2"
```

```yaml
# Migrated citation (vault_b)
id: mc_alice_v2
vault_id: vault_alice_b
created_at: "2025-06-01T00:00:00Z"
checksum: "def456..."
predecessor: "mc_alice_v1"
successor: null  # Current/latest
```

The chain proves: `mc_alice_v1` → `mc_alice_v2` → (current)

**Verification**:
```python
citation_v1 = loader.load_master_citation("alice_v1.yaml")
citation_v2 = loader.load_master_citation("alice_v2.yaml")

assert citation_v1.successor == citation_v2.id
assert citation_v2.predecessor == citation_v1.id
```

## Agent Links

The `linked_agents` field connects a MirrorDNA identity to AgentDNA personalities.

```yaml
linked_agents:
  - agent_id: agent_alice_assistant_001
    role: primary
    personality_traits:
      - helpful
      - analytical
  - agent_id: agent_alice_creative_002
    role: secondary
    personality_traits:
      - creative
      - explorative
```

**Schema reference**: `schema/agent_link.schema.json`

This allows one identity to have multiple agent personalities (e.g., work persona vs. personal persona).

## Master Citation vs. Identity State

**Master Citation**:
- Static binding document
- Declares constitutional alignment and vault location
- Changes rarely (only on major identity events like vault migration)
- Checksummed at creation

**Identity State** (in StateSnapshot):
- Dynamic runtime data
- Includes current session count, memory count, etc.
- Changes every session
- Checksummed at every snapshot

The Master Citation is the **anchor**. The Identity State is the **current value**.

## Validation

`ConfigLoader` validates Master Citations against `schema/master_citation.schema.json`:

- ID matches pattern `^mc_[a-z0-9_]{16,}$`
- Vault ID matches pattern `^vault_[a-z0-9_]{16,}$`
- Checksum is 64 hex characters (SHA-256)
- Timestamps are valid ISO 8601
- Constitutional alignment uses enum values

Invalid documents raise `ValueError` with details.

## Storage Recommendations

**File format**: YAML (human-readable) or JSON (machine-readable)

**Naming**: `{identity_name}_citation_v{version}.yaml`

**Location**:
- In vault: `{vault_root}/citations/mc_{id}.yaml`
- External reference: Separate from vault for portability

**Backup**: Store in multiple locations (local + remote + git)

**Permissions**: Read-only after creation (immutable binding)

## Use in MirrorDNA Protocol

The Master Citation is the **entry point**:

1. Load Master Citation → get vault_id
2. Open vault → load timeline and snapshots
3. Verify checksums → prove continuity
4. Resume session with intact identity

Without a valid Master Citation, there is no MirrorDNA identity.

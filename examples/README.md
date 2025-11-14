# MirrorDNA Examples

This directory contains working examples demonstrating how to use MirrorDNA.

## Running Examples

First, make sure MirrorDNA is installed:

```bash
cd MirrorDNA
pip install -e .
```

Then run any example:

```bash
python examples/basic_identity.py
python examples/basic_continuity.py
python examples/basic_memory.py
python examples/agent_dna_example.py
python examples/validation_example.py
```

## Example Descriptions

### Core Protocol Examples

#### basic_identity.py

**Purpose:** Demonstrates identity creation, retrieval, signing, and verification.

**Key concepts:**
- Creating user and agent identities
- Generating cryptographic keypairs
- Signing and verifying claims
- Validating identity structure

**Output:** Shows how to create identities and perform cryptographic operations.

---

#### basic_continuity.py

**Purpose:** Shows session continuity and lineage tracking.

**Key concepts:**
- Creating sessions
- Linking sessions (parent-child relationships)
- Ending sessions
- Retrieving session lineage
- Getting aggregated context

**Output:** Demonstrates how to maintain conversation continuity across multiple sessions.

---

#### basic_memory.py

**Purpose:** Covers memory management across three tiers.

**Key concepts:**
- Creating memories (short-term, long-term, episodic)
- Reading memories by tier
- Searching memories by content
- Updating memory metadata (access count)
- Archiving memories

**Output:** Shows how to store and retrieve different types of memories.

---

#### agent_dna_example.py

**Purpose:** Demonstrates agent DNA definition and versioning.

**Key concepts:**
- Defining agent personality traits
- Setting behavioral constraints
- Listing capabilities
- Constitutional alignment
- DNA versioning

**Output:** Shows how to define and evolve agent DNA over time.

---

#### validation_example.py

**Purpose:** Explains schema validation for all MirrorDNA data types.

**Key concepts:**
- Validating identities
- Validating continuity records
- Validating memories
- Validating agent DNA
- Understanding validation errors

**Output:** Demonstrates both valid and invalid data structures.

---

### Advanced Features Examples

#### reflection_engine_example.py

**Purpose:** Demonstrates agent introspection and meta-cognition.

**Key concepts:**
- Reflecting on decisions with rationale
- Tracking capability usage and performance
- State introspection and monitoring
- Meta-reflection (reflecting on reflections)
- Capability introspection

**Output:** Shows how agents can maintain self-awareness and track their own performance.

---

#### config_loader_example.py

**Purpose:** Shows verified configuration loading with checksums.

**Key concepts:**
- Saving configurations with integrity hashes
- Loading and verifying configurations
- Checksum algorithms (SHA-256, SHA-512)
- Secure config loading with whitelists
- Tamper detection

**Output:** Demonstrates how to ensure configuration integrity and prevent tampering.

---

#### timeline_analyzer_example.py

**Purpose:** Advanced lineage analysis and timeline querying.

**Key concepts:**
- Building complete lineage trees
- Detecting session branches
- Tracking context evolution
- Finding related sessions
- Calculating session metrics
- Temporal analysis

**Output:** Shows powerful timeline and relationship analysis capabilities.

---

## Example Data Storage

By default, examples store data in `~/.mirrordna/data/`:

```
~/.mirrordna/data/
├── identities.json
├── sessions.json
├── memories.json
└── agent_dna.json
```

You can clear this data at any time:

```bash
rm -rf ~/.mirrordna/data/
```

## Next Steps

After running the examples:

1. Read the **[Integration Guide](../docs/integration-guide.md)** for more advanced patterns
2. Check the **[Schema Reference](../docs/schema-reference.md)** for detailed field specs
3. Review **[Architecture](../docs/architecture.md)** to understand internal design
4. Build your own integration!

## Need Help?

- Check the [main README](../README.md)
- Read the [documentation](../docs/)
- Open an issue on GitHub

---

**MirrorDNA** — The architecture of persistence.

# MirrorDNA

**The Identity and Continuity Protocol Layer**

MirrorDNA is the foundational protocol that enables persistent identity, memory, and continuity for AI agents and users across the Active MirrorOS ecosystem.

## What is MirrorDNA?

MirrorDNA provides a standardized protocol for:

- **Identity Persistence** — Stable, cryptographically-verifiable agent and user identities
- **Continuity Tracking** — Session lineage, interaction history, and context preservation
- **Memory Architecture** — Structured schemas for short-term, long-term, and episodic memory
- **Agent DNA** — Personality traits, behavioral patterns, and constitutional alignment

Think of it as the "genetic code" for AI agents — a protocol that ensures they remain coherent, trustworthy, and contextually aware across sessions, platforms, and time.

## Who is this for?

- **Developers** building AI applications that need persistent agent identity
- **System Architects** designing multi-agent or conversational AI systems
- **Researchers** exploring memory, continuity, and agent alignment
- **Product Teams** using Active MirrorOS, LingOS, or related ecosystem tools

## How it fits in the ecosystem

```
┌─────────────────────────────────────┐
│     Active MirrorOS (Product)       │  ← User-facing intelligence
├─────────────────────────────────────┤
│      MirrorDNA (This Layer)         │  ← Identity + Continuity Protocol
├─────────────────────────────────────┤
│  LingOS │ AgentDNA │ Glyphtrail     │  ← Supporting systems
└─────────────────────────────────────┘
```

**MirrorDNA** sits between the product layer (Active MirrorOS) and supporting systems, providing the protocol contracts that ensure continuity, identity, and memory work reliably across the ecosystem.

## Quick Start

### 1. Create identities

```python
from mirrordna import IdentityManager

identity_mgr = IdentityManager()

# Create a user identity
user = identity_mgr.create_identity(
    identity_type="user",
    metadata={"name": "Alice"}
)

# Create an agent identity
agent = identity_mgr.create_identity(
    identity_type="agent",
    metadata={"name": "MirrorAgent"}
)
```

### 2. Start a session with continuity

```python
from mirrordna import ContinuityTracker

continuity = ContinuityTracker()

session = continuity.create_session(
    agent_id=agent['identity_id'],
    user_id=user['identity_id'],
    parent_session_id=None  # First session
)
```

### 3. Create and retrieve memories

```python
from mirrordna import MemoryManager

memory_mgr = MemoryManager()

# Write a long-term memory
memory = memory_mgr.write_memory(
    content="User prefers Python for development",
    tier="long_term",
    session_id=session['session_id'],
    agent_id=agent['identity_id'],
    user_id=user['identity_id']
)

# Retrieve memories
memories = memory_mgr.read_memory(tier="long_term", limit=10)
```

### 4. Validate schemas

```python
from mirrordna import validate_schema

result = validate_schema(identity_data, "identity")
if result.is_valid:
    print("Valid!")
```

See [examples/](examples/) for more detailed usage patterns.

## Repository Structure

```
MirrorDNA/
├── README.md              # You are here
├── LICENSE                # MIT License
├── setup.py               # Package installation
├── pytest.ini             # Test configuration
├── docs/                  # Detailed documentation
│   ├── index.md           # Documentation hub
│   ├── overview.md        # High-level concepts
│   ├── architecture.md    # Protocol architecture
│   ├── schema-reference.md # Schema specifications
│   └── integration-guide.md # How to integrate
├── schemas/               # JSON schema definitions
│   ├── identity.schema.json
│   ├── continuity.schema.json
│   ├── memory.schema.json
│   └── agent.schema.json
├── src/mirrordna/         # Python implementation
│   ├── __init__.py
│   ├── validator.py       # Schema validation
│   ├── crypto.py          # Cryptographic utilities
│   ├── storage.py         # Storage layer
│   ├── identity.py        # Identity management
│   ├── continuity.py      # Continuity tracking
│   ├── memory.py          # Memory management
│   └── agent_dna.py       # Agent DNA management
├── examples/              # Working usage examples
│   ├── README.md
│   ├── basic_identity.py
│   ├── basic_continuity.py
│   ├── basic_memory.py
│   ├── agent_dna_example.py
│   └── validation_example.py
└── tests/                 # Comprehensive test suite
    ├── README.md
    ├── conftest.py
    ├── test_validator.py
    ├── test_identity.py
    ├── test_continuity.py
    └── test_memory.py
```

## Documentation

- **[Overview](docs/overview.md)** — Core concepts and design philosophy
- **[Architecture](docs/architecture.md)** — How MirrorDNA works internally
- **[Schema Reference](docs/schema-reference.md)** — Detailed schema documentation
- **[Integration Guide](docs/integration-guide.md)** — How to integrate MirrorDNA into your system

## Installation

```bash
# Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA.git
cd MirrorDNA

# Install (Python 3.8+)
pip install -e .
```

## Running Tests

```bash
pytest tests/ -v
```

## Design Principles

1. **Simple and Robust** — No clever tricks, just clear protocols
2. **No External Dependencies** — Works with standard SDKs and local tools only
3. **Cryptographically Sound** — Identity verification uses established crypto primitives
4. **Human Readable** — All schemas are JSON, documented, and easy to inspect
5. **Privacy First** — Minimal data, local-first architecture, no tracking

## Related Projects

- **[Active MirrorOS](https://github.com/MirrorDNA-Reflection-Protocol/ActiveMirrorOS)** — Product-facing AI that remembers
- **[MirrorDNA-Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)** — Constitutional spec and compliance
- **[LingOS](https://github.com/MirrorDNA-Reflection-Protocol/LingOS)** — Language-native reflective dialogue OS
- **[AgentDNA](https://github.com/MirrorDNA-Reflection-Protocol/AgentDNA)** — Agent personality and persistence
- **[Glyphtrail](https://github.com/MirrorDNA-Reflection-Protocol/Glyphtrail)** — Interaction lineage logs

## License

MIT License — See [LICENSE](LICENSE) for details.

## Contributing

This is currently a private repository. If you have access and want to contribute:

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes, add tests
3. Ensure `pytest` passes
4. Submit a pull request

## Questions?

Open an issue or check the [docs/](docs/) folder for deeper explanations.

---

**MirrorDNA** — The architecture of persistence.

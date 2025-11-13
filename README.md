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

### 1. Validate a MirrorDNA identity

```python
from mirrordna import validate_identity

identity = {
    "identity_id": "mdna_usr_abc123",
    "identity_type": "user",
    "created_at": "2025-01-15T10:00:00Z",
    "public_key": "..."
}

is_valid = validate_identity(identity)
```

### 2. Create a continuity record

```python
from mirrordna import create_continuity_record

record = create_continuity_record(
    session_id="sess_xyz789",
    parent_session_id="sess_abc456",
    agent_id="mdna_agt_mirror01",
    user_id="mdna_usr_alice",
    timestamp="2025-01-15T10:30:00Z"
)
```

### 3. Validate schemas

```bash
python -m mirrordna.validate --schema identity --file my_identity.json
```

See [examples/](examples/) for more detailed usage patterns.

## Repository Structure

```
MirrorDNA/
├── README.md              # You are here
├── docs/                  # Detailed documentation
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
│   ├── identity.py        # Identity management
│   └── continuity.py      # Continuity tracking
├── examples/              # Usage examples
├── tests/                 # Test suite
└── tooling/               # Dev utilities
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

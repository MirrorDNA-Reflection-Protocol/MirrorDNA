# MirrorDNA

**Persistent identity and continuity protocol for AI agents operating across sessions, platforms, and time.**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

---

MirrorDNA is an open protocol specification with reference implementations in Python and TypeScript. It defines how AI agents and users maintain verifiable identity, append-only event history, and cryptographic state integrity without dependence on any single platform or vendor.

The protocol is storage-agnostic, vendor-neutral, and designed to be embedded in governed AI systems where auditability and continuity are non-negotiable.

## Problem

AI agents today have no memory between sessions. Every conversation starts from zero. Users have no portable identity across platforms. There is no standard mechanism for an agent to prove it is the same entity it was yesterday, or that its state has not been tampered with.

MirrorDNA addresses this by providing a minimal, verifiable protocol layer for identity binding, continuity tracking, and state integrity.

## Architecture

```
+---------------------------------------+
|        Applications & Agents          |   Consume the protocol
+---------------------------------------+
|        Identity & Continuity          |   Timeline, StateSnapshot
+---------------------------------------+
|       Master Citation & Vault         |   Configuration, Storage
+---------------------------------------+
|       Checksum & Verification         |   SHA-256, Integrity
+---------------------------------------+
```

**Layer 1 -- Checksum & Verification.** Deterministic SHA-256 hashing of files, dictionaries, and state objects. All higher layers use checksums to prove integrity.

**Layer 2 -- Master Citation & Vault.** A Master Citation is a signed document declaring an identity's constitutional alignment, vault location, and lineage. The Vault is structured storage for identity artifacts, memory, and state snapshots.

**Layer 3 -- Identity & Continuity.** An append-only Timeline provides an event log proving unbroken lineage. StateSnapshots capture point-in-time state with cryptographic checksums for comparison and verification.

**Layer 4 -- Applications & Agents.** Systems integrate by loading configuration, tracking events, capturing snapshots, and verifying integrity at each step.

### Data Flow

```
Master Citation ---> Identity Binding
       |
    Vault ID ---> Storage Location
       |
   Timeline ---> Event Stream ---> Continuity Proof
       |
State Snapshot ---> Point-in-Time State ---> Checksum Verification
```

## Protocol Schemas

MirrorDNA defines nine JSON Schemas (Draft-07) covering the full protocol surface:

**Core protocol** -- `master_citation`, `vault_entry`, `timeline_event`, `glyphtrail_entry`, `agent_link`

**Extensions** -- `identity`, `memory`, `continuity`, `agent`

All schemas are self-contained and can be validated with any JSON Schema implementation.

## SDKs

### Python

```bash
pip install mirrordna
```

```python
from mirrordna import ConfigLoader, Timeline, capture_snapshot, verify_checksum

# Load identity
loader = ConfigLoader()
citation = loader.load_master_citation("citation.yaml")

# Track events
timeline = Timeline(citation.id)
timeline.append_event("session_start", citation.id)
timeline.append_event("memory_created", citation.id,
                      payload={"content": "learned Python"})

# Capture and persist state
snapshot = capture_snapshot(
    snapshot_id="snap_001",
    identity_state={"citation_id": citation.id},
    continuity_state={"session_duration": 3600}
)
timeline.save_to_file(f"{citation.id}_timeline.json")
```

The Python SDK requires Python 3.8+ with `jsonschema` and `cryptography` as dependencies.

### TypeScript

A TypeScript SDK is available under `sdk/javascript/` as the `@mirrordna/sdk` package, providing equivalent identity, memory, continuity, and cryptographic verification modules.

## Testing

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run the test suite
pytest tests/ -v
```

The test suite covers checksum computation, configuration loading, continuity tracking, identity management, memory operations, state snapshots, timeline events, and schema validation.

## CI/CD

The repository includes GitHub Actions workflows for:

- **Lint, type-check, and test** on every push and pull request
- **Security scanning** via safety, pip-audit, bandit, and TruffleHog (weekly schedule)
- **License verification** for dependency compliance

## Project Structure

```
MirrorDNA/
  src/mirrordna/          Python SDK and protocol implementation
  sdk/javascript/         TypeScript SDK
  schemas/
    protocol/             Core protocol JSON Schemas
    extensions/           Extension JSON Schemas
  examples/               Working code samples
  tests/                  Pytest suite (8 test modules)
  docs/                   Architecture, integration guide, glossary
  .github/workflows/      CI, security scanning, license checks
```

## Relationship to MirrorDNA-Standard

MirrorDNA is the **protocol implementation**. [MirrorDNA-Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard) is the **governance specification** that defines compliance levels, constitutional principles, and validation tooling. Systems that implement MirrorDNA can validate their compliance against the Standard.

## License

MIT. See [LICENSE](LICENSE) for terms.

## Documentation

- [Architecture](docs/architecture.md) -- Protocol layer design and data flow
- [Overview](docs/overview.md) -- What MirrorDNA is and who it serves
- [Integration Guide](docs/integration-guide.md) -- Step-by-step implementation
- [Schema Reference](docs/schema-reference.md) -- Field-level schema documentation
- [Continuity Model](docs/continuity-model.md) -- How lineage and state integrity work
- [Glossary](docs/glossary.md) -- Canonical term definitions

---

Built by [Active Mirror](https://activemirror.ai). Governed AI for institutional work.

# MirrorDNA Protocol Overview

## At a Glance

**What:** Protocol for AI identity, continuity, and cryptographic state verification
**Key Primitives:** Master Citations (identity), Timeline (events), State Snapshots (checksum-verified state)
**Core Benefit:** Persistent, portable, verifiable agent identities across platforms and sessions
**Read Time:** 5 minutes

---

## What is MirrorDNA?

MirrorDNA is **the architecture of persistence for AI agents and users**. It defines how identity, memory, and continuity are preserved across sessions, systems, and time.

At its core, MirrorDNA provides:

1. **Identity binding** — A persistent identifier tied to verifiable state
2. **Continuity tracking** — Timeline of events proving unbroken lineage
3. **State integrity** — Cryptographic checksums ensuring data hasn't been tampered with
4. **Vault storage** — Structured persistence of identity artifacts and memories

## Why MirrorDNA?

Without MirrorDNA, AI agents have no memory between sessions. Every conversation starts from zero. Users have no portable identity across platforms.

MirrorDNA solves this by providing:

- **Persistence**: State survives beyond a single session or platform
- **Portability**: Identity and memory can transfer between systems
- **Verification**: Checksums prove continuity hasn't been broken
- **Sovereignty**: Users and agents own their identity data

## Protocol, Not Platform

MirrorDNA is a **protocol specification**, not a service. It defines:

- JSON schemas for Master Citations, Vault Entries, Timeline Events
- Checksum algorithms for state verification
- Configuration formats for identity binding
- Reference implementations in Python and JavaScript

Any system can implement MirrorDNA. No central authority controls it.

## Core Concepts

**Master Citation**: The binding document that declares an identity's constitutional alignment, vault location, and lineage.

**Vault**: A structured storage system holding identity state, memories, and artifacts.

**Timeline**: An append-only event log proving continuity from creation to present.

**Checksum**: SHA-256 hash proving state integrity and detecting tampering.

## Who Uses MirrorDNA?

- **AI agents** maintaining memory across conversations
- **Users** creating portable digital identities
- **Platforms** implementing interoperable identity systems
- **Applications** building on persistent agent state

## Integration Path

1. Create a Master Citation document for your identity
2. Initialize a Vault for storing state
3. Start a Timeline to track events
4. Capture StateSnapshots at key moments
5. Verify checksums to prove continuity

See [integration-guide.md](integration-guide.md) for implementation details.

## Part of the MirrorDNA Ecosystem

MirrorDNA is the foundational protocol layer in a larger ecosystem:

- **MirrorDNA** (this protocol) — Identity, continuity, and state verification
- **[MirrorDNA-Standard](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA-Standard)** — Constitutional framework and rights specification
- **[AgentDNA](https://github.com/MirrorDNA-Reflection-Protocol/AgentDNA)** — Agent personality and behavioral traits (built on MirrorDNA)
- **[GlyphTrail](https://github.com/MirrorDNA-Reflection-Protocol/GlyphTrail)** — Visual interaction lineage and continuity logs
- **[BeaconGlyphs](https://github.com/MirrorDNA-Reflection-Protocol/BeaconGlyphs)** — Visual glyph system for interaction markers
- **[ActiveMirrorOS](https://github.com/MirrorDNA-Reflection-Protocol/ActiveMirrorOS)** — Product implementation using these protocols
- **[LingOS](https://github.com/MirrorDNA-Reflection-Protocol/LingOS)** — Language-native reflective operating system

Each protocol serves a distinct purpose. MirrorDNA provides the identity and continuity layer that others build upon.

# MirrorDNA Overview

## Core Concepts

MirrorDNA is a protocol specification for **identity, continuity, and memory** in AI agent systems. It provides the foundational data structures and validation rules that enable agents to maintain stable identities, preserve context across sessions, and build reliable memory architectures.

## Design Philosophy

### 1. Protocol, Not Platform

MirrorDNA is a **protocol specification**, not a monolithic system. You can implement it in any language, on any platform. We provide reference implementations, schemas, and validation tools — but the core value is the protocol itself.

### 2. Simplicity Over Cleverness

We favor:
- Clear, human-readable JSON schemas
- Explicit field names and types
- Minimal dependencies
- Straightforward validation logic

We avoid:
- Complex abstractions
- "Clever" compression or optimization
- Proprietary formats
- Unnecessary indirection

### 3. Privacy and Sovereignty

MirrorDNA is designed to work **locally-first**:
- No required cloud services
- No tracking or telemetry by default
- Cryptographic identity without centralized registries
- User and agent data stays under your control

### 4. Interoperability

MirrorDNA aims to be a **common language** across the AI agent ecosystem:
- Standard schemas work across platforms
- Identity verification doesn't require specific vendors
- Memory structures can migrate between systems
- Integration is straightforward, not proprietary

## Key Components

### Identity

An **identity** in MirrorDNA represents a stable, verifiable entity — either a user or an agent.

Key properties:
- **Unique ID** with namespace (e.g., `mdna_usr_`, `mdna_agt_`)
- **Identity type** (user, agent, system)
- **Public key** for verification
- **Creation timestamp**
- **Optional metadata** (name, description, version)

Identities are meant to be:
- Long-lived (survive across sessions)
- Cryptographically verifiable (no impersonation)
- Portable (work across platforms)

### Continuity

**Continuity** tracks the lineage and context of interactions over time.

Key properties:
- **Session ID** — current interaction session
- **Parent session ID** — previous session (if any)
- **Agent and user IDs** — who's involved
- **Timestamp** — when this session began
- **Context metadata** — relevant state from prior sessions

Continuity enables:
- Session threading (remembering prior conversations)
- Context restoration (picking up where you left off)
- Audit trails (who did what, when)

### Memory

**Memory** structures define how agents store and retrieve information.

Three tiers:
1. **Short-term** — current session, immediate context
2. **Long-term** — persistent facts, learned patterns
3. **Episodic** — specific events, conversations, experiences

Memory records include:
- Memory type and tier
- Content (text, structured data, embeddings)
- Source (where it came from)
- Timestamps (created, accessed, updated)
- Relevance scores (for retrieval)

### Agent DNA

**Agent DNA** captures the personality, behavior patterns, and constitutional alignment of an agent.

Includes:
- **Personality traits** (tone, style, values)
- **Behavioral constraints** (what it will/won't do)
- **Constitutional alignment** (ethical frameworks, safety rules)
- **Capabilities** (what it can do)
- **Version history** (how the agent has evolved)

Agent DNA ensures:
- Consistent personality across sessions
- Reliable safety and alignment
- Transparency about agent capabilities

## How MirrorDNA Works

### 1. Identity Creation

When a new user or agent joins a system:
1. Generate a unique identity ID
2. Create a cryptographic key pair
3. Store public key in the identity record
4. Validate the identity against MirrorDNA schema
5. Store the identity record locally or in your database

### 2. Session Initiation

When starting a new interaction:
1. Create a continuity record linking this session to any prior session
2. Restore relevant context from previous sessions
3. Initialize short-term memory for the current session
4. Link the session to the appropriate user and agent identities

### 3. Memory Operations

During an interaction:
- **Write** new memories (facts learned, events that happened)
- **Read** relevant memories (search by recency, relevance, or content)
- **Update** existing memories (refine, consolidate, mark as outdated)
- **Archive** old memories (move to long-term storage, reduce noise)

### 4. Validation

Throughout the process:
- Validate all data against MirrorDNA schemas
- Verify cryptographic signatures on identity claims
- Ensure continuity links are valid and unbroken
- Check that memory structures conform to protocol

## Integration Patterns

### Pattern 1: Standalone Agent

A single agent using MirrorDNA for its own memory and identity:

```
Agent Process
├── MirrorDNA Identity (self)
├── Continuity Tracker (session lineage)
└── Memory Manager (short, long, episodic)
```

### Pattern 2: Multi-User System

A platform with many users and agents:

```
Platform
├── User Identities (mdna_usr_*)
├── Agent Identities (mdna_agt_*)
├── Session Manager (tracks continuity for all users)
└── Memory Store (shared or per-user)
```

### Pattern 3: Federated System

Multiple systems sharing MirrorDNA identities:

```
System A          System B
├── Shared user identity (mdna_usr_alice)
├── Local continuity records
└── Local memory (but portable)
```

The user's identity is verified across systems, but memory and continuity can stay local or sync as needed.

## Why MirrorDNA?

Without a protocol like MirrorDNA, every AI agent system invents its own:
- Identity format
- Session tracking approach
- Memory architecture
- Agent personality encoding

This leads to:
- Fragmentation (agents can't move between systems)
- Reinvented wheels (everyone solves the same problems)
- Trust issues (no standard way to verify identity)
- Poor user experience (start from scratch every time)

MirrorDNA provides a **common foundation** so that:
- Agents can maintain identity across platforms
- Users don't lose context when switching tools
- Developers can focus on innovation, not plumbing
- The ecosystem can interoperate reliably

## Next Steps

- Read the **[Architecture](architecture.md)** doc to understand how MirrorDNA is implemented
- Check the **[Schema Reference](schema-reference.md)** for detailed field specifications
- See the **[Integration Guide](integration-guide.md)** for step-by-step integration instructions
- Explore **[examples/](../examples/)** for working code samples

---

**MirrorDNA** — The architecture of persistence.

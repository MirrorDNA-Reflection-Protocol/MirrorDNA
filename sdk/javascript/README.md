# MirrorDNA JavaScript/TypeScript SDK

Official JavaScript/TypeScript SDK for the MirrorDNA protocol.

> **Note**: This SDK provides high-level abstractions built **on top of** the MirrorDNA protocol. For protocol-level primitives (Master Citations, Timeline, Checksums), see the main [MirrorDNA repository](../../README.md).

## What is This SDK?

This SDK provides application-layer abstractions for building MirrorDNA-compatible systems in JavaScript/TypeScript:

- **IdentityManager** — High-level identity creation and management
- **ContinuityTracker** — Session tracking and lineage
- **MemoryManager** — Multi-tier memory system
- **StorageAdapters** — Pluggable storage backends

**Protocol Layer** (in `../../src/mirrordna/`):
- Master Citations
- Timeline Events
- State Snapshots
- Checksum Verification

**SDK Layer** (this directory):
- Application-friendly APIs
- Storage abstractions
- Memory management helpers

## Installation

```bash
npm install @mirrordna/sdk
```

## Quick Start

```typescript
import { IdentityManager, ContinuityTracker, MemoryManager } from '@mirrordna/sdk';

// Create identities
const identityMgr = new IdentityManager();
const user = await identityMgr.createIdentity('user', { name: 'Alice' });
const agent = await identityMgr.createIdentity('agent', { name: 'Assistant' });

// Start a session
const continuity = new ContinuityTracker();
const session = await continuity.createSession(
  agent.identity_id,
  user.identity_id
);

// Create memories
const memoryMgr = new MemoryManager();
const memory = await memoryMgr.writeMemory(
  'User prefers TypeScript',
  'long_term',
  session.session_id,
  agent.identity_id,
  user.identity_id
);
```

## Features

- ✅ **Identity Management** — Create and verify user/agent identities
- ✅ **Session Continuity** — Track conversation lineage
- ✅ **Memory System** — Three-tier memory (short/long/episodic)
- ✅ **Cryptographic Security** — Ed25519 signatures
- ✅ **TypeScript Support** — Full type definitions
- ✅ **Multiple Storage** — Memory or file-based storage

## API Documentation

### Identity Manager

```typescript
const identityMgr = new IdentityManager();

// Create identity
const identity = await identityMgr.createIdentity('user', {
  name: 'Alice',
  description: 'Primary user'
});

// Get identity
const retrieved = await identityMgr.getIdentity(identity.identity_id);

// Sign and verify claims
const signature = identityMgr.signClaim(
  identity.identity_id,
  'I am Alice',
  identity._privateKey
);

const isValid = await identityMgr.verifyClaim(
  identity.identity_id,
  'I am Alice',
  signature
);
```

### Continuity Tracker

```typescript
const continuity = new ContinuityTracker();

// Create session
const session = await continuity.createSession(
  agentId,
  userId,
  parentSessionId  // null for first session
);

// End session
await continuity.endSession(session.session_id, {
  outcome: 'successful'
});

// Get lineage
const lineage = await continuity.getSessionLineage(session.session_id);

// Get context
const context = await continuity.getContext(session.session_id);
```

### Memory Manager

```typescript
const memoryMgr = new MemoryManager();

// Write memory
const memory = await memoryMgr.writeMemory(
  'User likes Python',
  'long_term',
  sessionId,
  agentId,
  userId,
  { tags: ['preference'], relevance_score: 0.9 }
);

// Read memories
const memories = await memoryMgr.readMemory('long_term', {}, 10);

// Search memories
const results = await memoryMgr.searchMemory('Python', 'long_term');

// Archive memory
await memoryMgr.archiveMemory(memory.memory_id);
```

## Storage Options

### In-Memory Storage (Default)

```typescript
import { MemoryStorage } from '@mirrordna/sdk';

const storage = new MemoryStorage();
const identityMgr = new IdentityManager(storage);
```

### File-Based Storage

```typescript
import { JSONFileStorage } from '@mirrordna/sdk';

const storage = new JSONFileStorage('/path/to/data');
const identityMgr = new IdentityManager(storage);
```

### Custom Storage

Implement the `StorageAdapter` interface:

```typescript
import { StorageAdapter } from '@mirrordna/sdk';

class MyStorage implements StorageAdapter {
  async create(collection: string, record: any): Promise<string> {
    // Your implementation
  }

  async read(collection: string, recordId: string): Promise<any | null> {
    // Your implementation
  }

  // ... other methods
}
```

## TypeScript Support

Full TypeScript definitions are included:

```typescript
import { Identity, Session, Memory, MemoryTier } from '@mirrordna/sdk';

const identity: Identity = {
  identity_id: 'mdna_usr_abc123',
  identity_type: 'user',
  created_at: '2025-01-15T10:00:00Z',
  public_key: '...'
};

const tier: MemoryTier = 'long_term';
```

## Protocol Integration

This SDK builds on the MirrorDNA protocol. Under the hood:

- **IdentityManager** creates Master Citations (protocol layer)
- **ContinuityTracker** writes to Timeline (protocol layer)
- **MemoryManager** captures State Snapshots (protocol layer)

To work directly with protocol primitives, use the Python implementation or implement the protocol yourself following the JSON schemas.

## Building

```bash
npm install
npm run build
```

## Testing

```bash
npm test
```

## Relationship to Protocol

```
┌─────────────────────────────────────┐
│  Your Application                   │
├─────────────────────────────────────┤
│  JS SDK (this directory)            │  ← High-level APIs
│  - IdentityManager                  │
│  - ContinuityTracker                │
│  - MemoryManager                    │
├─────────────────────────────────────┤
│  MirrorDNA Protocol                 │  ← Core primitives
│  - Master Citations                 │
│  - Timeline Events                  │
│  - State Snapshots                  │
│  - Checksum Verification            │
└─────────────────────────────────────┘
```

This SDK is **one way** to use the MirrorDNA protocol. You can also:
- Use the Python implementation directly
- Implement the protocol in any language using the JSON schemas
- Build your own SDK with different abstractions

## License

MIT License — See [LICENSE](../../LICENSE) for details.

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for contribution guidelines.

---

**MirrorDNA** — The architecture of persistence.

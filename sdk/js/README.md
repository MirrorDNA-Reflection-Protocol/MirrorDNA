# MirrorDNA JavaScript SDK

Simple, local-first JavaScript SDK for MirrorDNA protocol operations.

## What is This?

This SDK provides a simplified Node.js interface for working with MirrorDNA concepts locally:

- **Load vault configurations** from JSON/YAML files
- **Compute state hashes** for directories (deterministic, SHA-256)
- **Validate timeline files** against basic schema requirements
- **Track continuity status** across sessions

**This SDK is for:**
- Local development and testing with Node.js
- Understanding MirrorDNA concepts
- Building simple integrations
- Learning the protocol

**This SDK is NOT:**
- A hosted service or API client
- A complete vault manager
- A production-grade system (for that, see `../javascript/`)

## Installation

### Option 1: Use within MirrorDNA repo

```bash
# From MirrorDNA root directory
cd sdk/js
node examples/basicUsage.js
```

### Option 2: Copy to your project

```bash
# Copy the SDK file to your project
cp sdk/js/mirrordnaClient.js ./your-project/

# Use in your code
const { MirrorDNAClient } = require('./mirrordnaClient.js');
```

## Dependencies

- **Node.js 14+** (uses built-in modules: fs, path, crypto)
- **js-yaml** (optional, only needed for YAML file support)

```bash
# Optional: For YAML support
npm install js-yaml
```

That's it! No heavy frameworks or external services required.

## Quick Start

### Basic Example

```javascript
const { MirrorDNAClient } = require('./mirrordnaClient.js');

// Initialize client
const client = new MirrorDNAClient();

// Load vault configuration
const vault = client.loadVaultConfig('vault.json');
console.log(`Loaded vault: ${vault.vault_id}`);

// Compute state hash for a directory
const stateHash = client.computeStateHash('./my_vault_data');
console.log(`State hash: ${stateHash}`);

// Validate timeline
const result = client.validateTimeline('timeline.json');
if (result.valid) {
    console.log(`Timeline valid with ${result.event_count} events`);
}
```

### Running the Example

```bash
cd sdk/js
node examples/basicUsage.js
```

This will demonstrate:
1. Loading a vault configuration
2. Computing deterministic state hashes
3. Validating timeline files
4. Getting continuity status

## API Reference

### MirrorDNAClient

Main client class for MirrorDNA operations.

#### `loadVaultConfig(path)`

Load and validate a vault configuration file.

```javascript
const vault = client.loadVaultConfig('vault.json');
console.log(vault.vault_id);  // vault_example_001
console.log(vault.name);      // My Vault
```

**Parameters:**
- `path` (string): Path to vault config file (JSON or YAML)

**Returns:** Object with vault configuration

**Throws:** Error if file doesn't exist or config is invalid

---

#### `computeStateHash(directory, ignorePatterns)`

Compute deterministic SHA-256 hash of directory contents.

```javascript
const hash1 = client.computeStateHash('./my_vault');
// ... make changes ...
const hash2 = client.computeStateHash('./my_vault');

if (hash1 !== hash2) {
    console.log('Vault state changed!');
}
```

**Parameters:**
- `directory` (string): Path to directory
- `ignorePatterns` (string[], optional): Patterns to ignore (default: `['.git', 'node_modules', '__pycache__', '.DS_Store', '.pyc']`)

**Returns:** 64-character hexadecimal SHA-256 hash

**Throws:** Error if directory doesn't exist

**How it works:**
- Walks directory tree in deterministic order
- Hashes file contents and paths
- Combines into single SHA-256 hash
- Same directory state → same hash (always)

---

#### `validateTimeline(path)`

Validate timeline file structure.

```javascript
const result = client.validateTimeline('timeline.json');

if (result.valid) {
    console.log(`Timeline has ${result.event_count} events`);
    console.log(`From ${result.first_event} to ${result.last_event}`);
} else {
    console.log(`Errors: ${result.errors.join(', ')}`);
}
```

**Parameters:**
- `path` (string): Path to timeline file (JSON or YAML)

**Returns:** Object with validation results:
```javascript
{
    valid: boolean,
    event_count: number,
    timeline_id: string,
    errors: string[],
    first_event: string,  // ISO timestamp
    last_event: string    // ISO timestamp
}
```

---

#### `computeDataChecksum(data)`

Compute deterministic checksum for object data.

```javascript
const data = { id: 'test', version: '1.0' };
const checksum = client.computeDataChecksum(data);
// Always produces same checksum for same data
```

**Parameters:**
- `data` (Object): Object to hash

**Returns:** SHA-256 hash string

---

#### `getContinuityStatus({ vaultPath, timelinePath })`

Get combined continuity status.

```javascript
const status = client.getContinuityStatus({
    vaultPath: 'vault.json',
    timelinePath: 'timeline.json'
});

console.log(`Vault: ${status.vault_id}`);
console.log(`Events: ${status.event_count}`);
console.log(`State hash: ${status.state_hash}`);
```

**Parameters:**
- `vaultPath` (string, optional): Path to vault config
- `timelinePath` (string, optional): Path to timeline

**Returns:** Status object with vault info, timeline validation, and state hash

---

### Convenience Functions

Quick utilities for common operations:

```javascript
const { quickHashDirectory, quickValidateTimeline } = require('./mirrordnaClient.js');

// Quick hash
const hash = quickHashDirectory('./my_data');

// Quick validation
const isValid = quickValidateTimeline('timeline.json');
```

## Usage Patterns

### Pattern 1: Detect Vault Changes

```javascript
const client = new MirrorDNAClient();

// Compute initial hash
const hash1 = client.computeStateHash('./vault_data');

// ... user makes changes ...

// Check for changes
const hash2 = client.computeStateHash('./vault_data');

if (hash1 !== hash2) {
    console.log('Vault state has changed!');
    console.log(`Old: ${hash1}`);
    console.log(`New: ${hash2}`);
}
```

### Pattern 2: Validate Continuity

```javascript
const client = new MirrorDNAClient();

// Load vault
const vault = client.loadVaultConfig('vault.json');

// Validate timeline
const result = client.validateTimeline('timeline.json');

if (result.valid) {
    console.log(`✓ Continuity intact: ${result.event_count} events`);
} else {
    console.log(`✗ Continuity broken: ${result.errors.join(', ')}`);
}
```

### Pattern 3: Session Tracking

```javascript
const client = new MirrorDNAClient();

// Start of session
const statusStart = client.getContinuityStatus({
    vaultPath: 'vault.json',
    timelinePath: 'timeline.json'
});

console.log(`Session started at: ${statusStart.timestamp}`);
console.log(`Starting event count: ${statusStart.event_count}`);

// ... session activity ...

// End of session
const statusEnd = client.getContinuityStatus({
    vaultPath: 'vault.json',
    timelinePath: 'timeline.json'
});

const eventsAdded = statusEnd.event_count - statusStart.event_count;
console.log(`Events added this session: ${eventsAdded}`);
```

## File Format Examples

### Vault Config (vault.json)

```json
{
  "vault_id": "vault_example_001",
  "name": "My Example Vault",
  "path": "./vault_data",
  "created_at": "2025-11-14T10:00:00Z",
  "entries": [
    {
      "id": "entry_001",
      "type": "memory",
      "created_at": "2025-11-14T10:00:00Z"
    }
  ]
}
```

### Timeline (timeline.json)

```json
{
  "timeline_id": "mc_agent_001",
  "event_count": 2,
  "events": [
    {
      "id": "evt_001",
      "timestamp": "2025-11-14T10:00:00Z",
      "event_type": "session_start",
      "actor": "mc_agent_001",
      "payload": { "platform": "Local" }
    },
    {
      "id": "evt_002",
      "timestamp": "2025-11-14T10:05:00Z",
      "event_type": "memory_created",
      "actor": "mc_agent_001",
      "payload": { "content": "Example memory" }
    }
  ]
}
```

## Limitations

This SDK is intentionally simple and has the following limitations:

1. **Local only** - No network operations or hosted APIs
2. **Basic validation** - Does not perform deep JSON schema validation
3. **No encryption** - Files are read/written in plaintext
4. **No signing** - Does not handle cryptographic signatures
5. **Synchronous operations** - No async/await (uses blocking I/O)

For production use cases with TypeScript support and advanced features, see `../javascript/`.

## Relation to MirrorDNA Protocol

This SDK is a **simplified wrapper** around core MirrorDNA concepts:

```
┌─────────────────────────────────────┐
│  Your Node.js Application           │
├─────────────────────────────────────┤
│  SDK (this directory)               │  ← Simple, local operations
│  - MirrorDNAClient                  │
│  - Basic validation                 │
│  - State hashing                    │
├─────────────────────────────────────┤
│  MirrorDNA Protocol                 │  ← Full implementation
│  - Master Citations                 │
│  - Timeline Events                  │
│  - State Snapshots                  │
│  - Checksum verification            │
└─────────────────────────────────────┘
```

**For full features with TypeScript**, use `../javascript/`:
- IdentityManager with Ed25519 signatures
- ContinuityTracker with session management
- MemoryManager with multi-tier storage
- TypeScript type definitions

**For simple local operations**, use this SDK:
- Quick vault config checks
- Directory hashing
- Basic timeline validation

## Next Steps

- **Try the example:** `node examples/basicUsage.js`
- **Read the protocol docs:** `../../docs/overview.md`
- **Explore TypeScript SDK:** `../javascript/`
- **Check schemas:** `../../schemas/protocol/`

## License

MIT License — See [LICENSE](../../LICENSE) for details.

---

**MirrorDNA SDK** — Simple tools for identity and continuity.

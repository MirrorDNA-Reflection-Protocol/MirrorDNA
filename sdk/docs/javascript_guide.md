# MirrorDNA JavaScript SDK Guide

Complete guide to using the MirrorDNA JavaScript/Node.js SDK.

## Installation

### Quick Start (Copy File)

```bash
# Copy the SDK client to your project
cp sdk/javascript/mirror_dna_client.js your_project/

# Install dependencies
npm install js-yaml
```

### Using the Examples

```bash
cd sdk/javascript/examples
npm install
npm run demo
```

## Dependencies

- **Required**: js-yaml (for YAML file support)
- **Node.js**: 14.0.0 or higher

```bash
npm install js-yaml
```

## Basic Usage

### 1. Initialize Client

```javascript
const MirrorDNAClient = require('./mirror_dna_client');

// Initialize with default data directory
const client = new MirrorDNAClient();

// Or specify custom directory
const client = new MirrorDNAClient('./my_data');
```

### 2. Create Master Citation

```javascript
const citation = client.createMasterCitation(
    'agent_001',
    'vault_main',
    '1.0.0'
);

console.log(`Citation ID: ${citation.id}`);
console.log(`Checksum: ${citation.checksum}`);
```

### 3. Save Citation to File

```javascript
// Save with auto-generated filename
const path = client.saveCitation(citation);

// Save with custom filename
const path = client.saveCitation(citation, 'my_citation.yaml');

console.log(`Saved to: ${path}`);
```

### 4. Compute State Hashes

```javascript
const data = {
    user: 'alice',
    preferences: {
        theme: 'dark',
        language: 'javascript'
    }
};

const hash = client.computeStateHash(data);
console.log(`Hash: ${hash}`);

// Verify hash is deterministic
const hash2 = client.computeStateHash(data);
console.log(`Hashes match: ${hash === hash2}`); // Always true
```

### 5. Create Timeline Events

```javascript
// Create events
const event1 = client.createTimelineEvent(
    'session_start',
    citation.id,
    { platform: 'MyApp' }
);

const event2 = client.createTimelineEvent(
    'memory_created',
    citation.id,
    {
        content: 'User prefers JavaScript',
        tier: 'long_term'
    }
);

const event3 = client.createTimelineEvent(
    'session_end',
    citation.id,
    { outcome: 'successful' }
);
```

### 6. Validate Timeline

```javascript
const events = [event1, event2, event3];
const validation = client.validateTimeline(events);

if (validation.valid) {
    console.log('✓ Timeline is valid');
    console.log(`Total events: ${validation.total_events}`);
    console.log(`Event types: ${JSON.stringify(validation.event_types)}`);
    console.log(`Unique actors: ${validation.unique_actors}`);
} else {
    console.log('✗ Timeline has errors:');
    validation.errors.forEach(error => {
        console.log(`  - ${error}`);
    });
}
```

### 7. Check Continuity Status

```javascript
const status = client.getContinuityStatus(citation.id);

console.log(`Status: ${status.status}`);
console.log(`Total events: ${status.total_events}`);
console.log(`Last activity: ${status.last_activity}`);
console.log(`Valid: ${status.valid}`);
```

### 8. Save and Load Timeline

```javascript
// Save timeline
const timelinePath = client.saveTimeline(citation.id);
console.log(`Timeline saved to: ${timelinePath}`);

// Load timeline
const loadedEvents = client.loadTimeline(timelinePath);
console.log(`Loaded ${loadedEvents.length} events`);
```

### 9. Verify Checksums

```javascript
// Verify data integrity
const dataWithoutChecksum = Object.fromEntries(
    Object.entries(citation).filter(([k]) => k !== 'checksum')
);

const isValid = client.verifyChecksum(
    dataWithoutChecksum,
    citation.checksum
);

if (isValid) {
    console.log('✓ Checksum valid - data integrity verified');
} else {
    console.log('✗ Checksum mismatch - data may be corrupted');
}
```

### 10. Load Vault Configuration

```javascript
// Load vault config from file
const vault = client.loadVaultConfig('vault.yaml');

console.log(`Vault ID: ${vault.vault_id}`);
console.log(`Name: ${vault.name}`);
console.log(`Path: ${vault.path}`);
```

## API Reference

### MirrorDNAClient

#### Constructor

```javascript
new MirrorDNAClient(dataDir = './mirrordna_data')
```

- `dataDir` (optional): Directory for storing data files

#### Methods

##### `loadVaultConfig(filePath)`

Load and validate vault configuration.

**Parameters**:
- `filePath`: Path to vault config file (JSON or YAML)

**Returns**: Object with vault configuration

**Throws**:
- `Error`: If file doesn't exist or required fields missing

##### `computeStateHash(data)`

Compute SHA-256 hash of state data.

**Parameters**:
- `data`: Object to hash

**Returns**: 64-character hex string

##### `validateTimeline(events)`

Validate timeline events.

**Parameters**:
- `events`: Array of event objects

**Returns**: Object with:
- `valid`: Boolean
- `total_events`: Number
- `event_types`: Object with event type counts
- `unique_actors`: Number
- `timespan`: Object with first and last timestamps
- `errors`: Array of validation errors

##### `createMasterCitation(identityId, vaultId, version = '1.0.0')`

Create Master Citation document.

**Parameters**:
- `identityId`: Unique identity identifier
- `vaultId`: Vault to bind to
- `version`: Protocol version (default: "1.0.0")

**Returns**: Master Citation object with checksum

##### `saveCitation(citation, filename = null)`

Save Master Citation to file.

**Parameters**:
- `citation`: Master Citation object
- `filename`: Optional filename (defaults to citation ID)

**Returns**: Path to saved file

##### `createTimelineEvent(eventType, actor, payload = {})`

Create timeline event.

**Parameters**:
- `eventType`: Event type string
- `actor`: Identity ID of actor
- `payload`: Optional event data (object)

**Returns**: Timeline event object

##### `getContinuityStatus(identityId)`

Get continuity status for identity.

**Parameters**:
- `identityId`: Identity to check

**Returns**: Object with:
- `identity_id`: Identity ID
- `status`: "active", "degraded", or "no_activity"
- `total_events`: Number
- `event_types`: Breakdown
- `last_activity`: Timestamp string
- `valid`: Boolean

##### `saveTimeline(identityId, filename = null)`

Save timeline to file.

**Parameters**:
- `identityId`: Identity whose timeline to save
- `filename`: Optional filename

**Returns**: Path to saved file

##### `loadTimeline(filePath)`

Load timeline from file.

**Parameters**:
- `filePath`: Path to timeline file

**Returns**: Array of timeline events

**Throws**:
- `Error`: If file doesn't exist

##### `verifyChecksum(data, expectedChecksum)`

Verify data checksum.

**Parameters**:
- `data`: Object to verify (without checksum field)
- `expectedChecksum`: Expected hash value

**Returns**: Boolean (true if match)

## Examples

### Complete Workflow

```javascript
const MirrorDNAClient = require('./mirror_dna_client');

// 1. Initialize
const client = new MirrorDNAClient('./demo_data');

// 2. Create identity
const citation = client.createMasterCitation(
    'agent_demo',
    'vault_demo'
);

// 3. Save citation
const citationPath = client.saveCitation(citation);

// 4. Create timeline
client.createTimelineEvent('session_start', citation.id);
client.createTimelineEvent('memory_created', citation.id, {
    content: 'Demo memory'
});
client.createTimelineEvent('session_end', citation.id);

// 5. Check status
const status = client.getContinuityStatus(citation.id);
console.log(`Status: ${status.status}, Events: ${status.total_events}`);

// 6. Save timeline
const timelinePath = client.saveTimeline(citation.id);

// 7. Verify integrity
const dataToVerify = Object.fromEntries(
    Object.entries(citation).filter(([k]) => k !== 'checksum')
);
const isValid = client.verifyChecksum(dataToVerify, citation.checksum);
console.log(`Integrity: ${isValid ? '✓' : '✗'}`);
```

### Data Integrity Checking

```javascript
const fs = require('fs');

// Store data with checksum
const userPreferences = {
    theme: 'dark',
    notifications: true,
    language: 'en'
};

// Compute checksum
const checksum = client.computeStateHash(userPreferences);

// Save both
fs.writeFileSync('preferences.json', JSON.stringify({
    data: userPreferences,
    checksum: checksum
}, null, 2));

// Later, load and verify
const loaded = JSON.parse(fs.readFileSync('preferences.json', 'utf8'));

if (client.verifyChecksum(loaded.data, loaded.checksum)) {
    console.log('✓ Data integrity verified');
    const preferences = loaded.data;
} else {
    console.log('✗ Data may be corrupted!');
}
```

### Agent Session Tracking

```javascript
// Create agent
const citation = client.createMasterCitation('agent_001', 'vault_main');
const agentId = citation.id;

// Start session
client.createTimelineEvent('session_start', agentId, {
    platform: 'MyPlatform',
    version: '1.0'
});

// Agent activities
client.createTimelineEvent('memory_created', agentId, {
    content: 'User asked about JavaScript'
});

client.createTimelineEvent('memory_created', agentId, {
    content: 'User prefers concise responses'
});

// End session
client.createTimelineEvent('session_end', agentId, {
    duration: 300,
    outcome: 'successful'
});

// Review session
const status = client.getContinuityStatus(agentId);
console.log(`Session summary: ${JSON.stringify(status.event_types)}`);
```

### Express.js Integration

```javascript
const express = require('express');
const MirrorDNAClient = require('./mirror_dna_client');

const app = express();
const client = new MirrorDNAClient('./agent_data');

app.use(express.json());

// Create agent identity
app.post('/api/agent/create', (req, res) => {
    const { identity_id, vault_id } = req.body;
    const citation = client.createMasterCitation(identity_id, vault_id);
    const path = client.saveCitation(citation);

    res.json({
        citation_id: citation.id,
        checksum: citation.checksum,
        saved_to: path
    });
});

// Log agent activity
app.post('/api/agent/:id/event', (req, res) => {
    const { id } = req.params;
    const { event_type, payload } = req.body;

    const event = client.createTimelineEvent(event_type, id, payload);
    const status = client.getContinuityStatus(id);

    res.json({
        event_id: event.id,
        continuity_status: status
    });
});

// Get agent status
app.get('/api/agent/:id/status', (req, res) => {
    const { id } = req.params;
    const status = client.getContinuityStatus(id);
    res.json(status);
});

app.listen(3000, () => {
    console.log('MirrorDNA API running on port 3000');
});
```

## Running the Demo

```bash
cd sdk/javascript/examples
npm install
node basic_usage.js
```

Expected output:
- Creates Master Citation
- Computes state hashes
- Creates and validates timeline
- Shows continuity status
- Saves files to `./sdk_demo_data_js/`

## TypeScript Support

For TypeScript projects, you can add type definitions:

```typescript
// types.d.ts
declare module 'mirror_dna_client' {
    interface MasterCitation {
        id: string;
        version: string;
        vault_id: string;
        created_at: string;
        checksum: string;
        constitutional_alignment: {
            compliance_level: string;
            framework_version: string;
            rights_bundle: string[];
        };
    }

    interface TimelineEvent {
        id: string;
        timestamp: string;
        event_type: string;
        actor: string;
        payload: Record<string, any>;
    }

    class MirrorDNAClient {
        constructor(dataDir?: string);
        loadVaultConfig(filePath: string): Record<string, any>;
        computeStateHash(data: Record<string, any>): string;
        validateTimeline(events: TimelineEvent[]): any;
        createMasterCitation(identityId: string, vaultId: string, version?: string): MasterCitation;
        saveCitation(citation: MasterCitation, filename?: string): string;
        createTimelineEvent(eventType: string, actor: string, payload?: Record<string, any>): TimelineEvent;
        getContinuityStatus(identityId: string): any;
        saveTimeline(identityId: string, filename?: string): string;
        loadTimeline(filePath: string): TimelineEvent[];
        verifyChecksum(data: Record<string, any>, expectedChecksum: string): boolean;
    }

    export = MirrorDNAClient;
}
```

## Tips and Best Practices

### 1. Deterministic Hashing

Always use `computeStateHash()` for data that needs integrity verification:

```javascript
// DO: Use computeStateHash
const hash = client.computeStateHash(data);

// DON'T: Try to hash manually (may not be deterministic)
```

### 2. Checksum Verification

Remove checksum field before verification:

```javascript
// Correct
const dataWithoutChecksum = Object.fromEntries(
    Object.entries(citation).filter(([k]) => k !== 'checksum')
);
client.verifyChecksum(dataWithoutChecksum, citation.checksum);

// Incorrect (includes checksum in data)
client.verifyChecksum(citation, citation.checksum);  // Will fail
```

### 3. Event Ordering

Timeline events are chronological - create them in order:

```javascript
// Good: Events in order
client.createTimelineEvent('session_start', actor);
client.createTimelineEvent('action_taken', actor);
client.createTimelineEvent('session_end', actor);
```

### 4. Error Handling

```javascript
try {
    const vault = client.loadVaultConfig('vault.yaml');
} catch (error) {
    if (error.message.includes('not found')) {
        console.log('Vault config not found');
    } else if (error.message.includes('missing required fields')) {
        console.log('Invalid vault config:', error.message);
    }
}
```

### 5. Async/Await Pattern

While the SDK is synchronous, you can wrap it for async patterns:

```javascript
async function createAgentIdentity(identityId, vaultId) {
    return new Promise((resolve) => {
        const citation = client.createMasterCitation(identityId, vaultId);
        const path = client.saveCitation(citation);
        resolve({ citation, path });
    });
}

// Usage
const { citation, path } = await createAgentIdentity('agent_001', 'vault_main');
```

## Upgrading to TypeScript SDK

For full TypeScript support with type safety:

```bash
cd sdk/javascript
npm install
npm run build
```

Then import from the TypeScript SDK:

```typescript
import { IdentityManager, ContinuityTracker } from '@mirrordna/sdk';

const identityMgr = new IdentityManager();
const identity = await identityMgr.createIdentity('user', { name: 'Alice' });
```

TypeScript SDK adds:
- Full type definitions
- Ed25519 signatures
- Advanced memory management
- Storage adapters

## Questions?

- **SDK Overview**: [overview.md](overview.md)
- **Design Details**: [design_notes.md](design_notes.md)
- **Protocol Docs**: [../../docs/](../../docs/)

---

**MirrorDNA JavaScript SDK** - Simple tools for building with persistence.

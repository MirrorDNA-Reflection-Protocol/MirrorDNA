# MirrorDNA Developer SDK - Overview

## What is the MirrorDNA SDK?

The MirrorDNA Developer SDK is a collection of simplified, language-specific client libraries for working with the MirrorDNA protocol in local development environments.

Unlike the full protocol implementation, these SDKs are designed for:

- **Learning** — Understanding MirrorDNA concepts through simple examples
- **Local Development** — Building and testing integrations on your machine
- **Prototyping** — Quickly validating ideas without complex infrastructure
- **Educational Use** — Teaching identity and continuity concepts

## Available SDKs

### Python SDK (`/sdk/python/`)

Simple Python client with zero external dependencies (except optional PyYAML).

**Features:**
- Load vault configurations from YAML/JSON
- Compute deterministic state hashes for directories
- Validate timeline files
- Track continuity status

**Best for:**
- Python developers
- Data scientists
- Researchers
- Command-line tools

**Quick start:**
```bash
cd sdk/python
python examples/basic_usage.py
```

### JavaScript SDK (`/sdk/js/`)

Simple Node.js client using built-in modules.

**Features:**
- Load vault configurations from JSON/YAML
- Compute deterministic state hashes for directories
- Validate timeline files
- Track continuity status

**Best for:**
- JavaScript/Node.js developers
- Web backend integration
- CLI tools
- Simple automation scripts

**Quick start:**
```bash
cd sdk/js
node examples/basicUsage.js
```

## What the SDK Does

### 1. Vault Configuration Loading

Load and validate MirrorDNA vault configurations from files:

```python
# Python
client = MirrorDNAClient()
vault = client.load_vault_config("vault.yaml")
```

```javascript
// JavaScript
const client = new MirrorDNAClient();
const vault = client.loadVaultConfig('vault.json');
```

### 2. State Hash Computation

Compute deterministic SHA-256 hashes of directory contents:

```python
# Python
hash1 = client.compute_state_hash("./vault_data")
# ... make changes ...
hash2 = client.compute_state_hash("./vault_data")
if hash1 != hash2:
    print("State changed!")
```

```javascript
// JavaScript
const hash1 = client.computeStateHash('./vault_data');
// ... make changes ...
const hash2 = client.computeStateHash('./vault_data');
if (hash1 !== hash2) {
    console.log('State changed!');
}
```

### 3. Timeline Validation

Validate timeline event logs against basic schema requirements:

```python
# Python
result = client.validate_timeline("timeline.json")
if result['valid']:
    print(f"Timeline has {result['event_count']} events")
```

```javascript
// JavaScript
const result = client.validateTimeline('timeline.json');
if (result.valid) {
    console.log(`Timeline has ${result.event_count} events`);
}
```

### 4. Continuity Status

Get combined status across vault, timeline, and state:

```python
# Python
status = client.get_continuity_status(
    vault_path="vault.yaml",
    timeline_path="timeline.json"
)
```

```javascript
// JavaScript
const status = client.getContinuityStatus({
    vaultPath: 'vault.json',
    timelinePath: 'timeline.json'
});
```

## What the SDK Does NOT Do

To keep the SDK simple and local-friendly, it **does not** include:

1. **Network operations** — No API calls, no cloud services
2. **Cryptographic signing** — No Ed25519 signatures or key management
3. **Complex state management** — No session persistence or databases
4. **Deep schema validation** — Basic structure checks only
5. **Production features** — No high availability, scaling, or enterprise features

For these capabilities, see:
- Full protocol implementation: `/src/mirrordna/`
- TypeScript SDK with advanced features: `/sdk/javascript/`

## Typical Use Cases

### Use Case 1: Learning MirrorDNA

**Goal:** Understand how MirrorDNA tracks continuity

**Approach:**
1. Load example vault configuration
2. Compute initial state hash
3. Create some timeline events
4. Recompute state hash to see changes
5. Validate timeline structure

**SDK:** Either Python or JavaScript

### Use Case 2: Local Integration Testing

**Goal:** Test how your app integrates with MirrorDNA vaults

**Approach:**
1. Create test vault configs
2. Generate sample timelines
3. Validate your app produces correct structures
4. Verify state hashing works as expected

**SDK:** Python (for pytest) or JavaScript (for Jest)

### Use Case 3: Simple CLI Tool

**Goal:** Build a command-line tool to inspect MirrorDNA files

**Approach:**
1. Accept vault/timeline paths as arguments
2. Use SDK to load and validate
3. Print status and errors
4. Optionally compute checksums

**SDK:** Python (for scripting) or JavaScript (for npm packages)

### Use Case 4: Educational Workshop

**Goal:** Teach developers about identity and continuity

**Approach:**
1. Show how state hashing works (deterministic, tamper-evident)
2. Demonstrate timeline event structure
3. Explain vault configuration format
4. Let students build simple integrations

**SDK:** Both (students choose their language)

## Relation to MirrorDNA Ecosystem

```
┌─────────────────────────────────────────────────┐
│  ActiveMirrorOS                                 │  ← Production system
│  Full-featured AI identity platform             │
└─────────────────────────────────────────────────┘
                     ↓ uses
┌─────────────────────────────────────────────────┐
│  MirrorDNA Protocol (src/mirrordna/)            │  ← Core implementation
│  - ConfigLoader, Timeline, StateSnapshot        │
│  - Schema validation, cryptographic checksums   │
└─────────────────────────────────────────────────┘
                     ↓ simplified by
┌─────────────────────────────────────────────────┐
│  Developer SDK (sdk/python/, sdk/js/)           │  ← This layer
│  - Simple clients for local development         │
│  - Basic validation and hashing                 │
└─────────────────────────────────────────────────┘
                     ↓ used by
┌─────────────────────────────────────────────────┐
│  Your Application                               │  ← Your code
│  Local tools, integrations, prototypes          │
└─────────────────────────────────────────────────┘
```

## Getting Started

### 1. Choose Your Language

Pick the SDK that matches your development environment:

- **Python developers** → `/sdk/python/`
- **JavaScript/Node.js developers** → `/sdk/js/`

### 2. Run the Example

Each SDK includes a working example:

```bash
# Python
cd sdk/python
python examples/basic_usage.py

# JavaScript
cd sdk/js
node examples/basicUsage.js
```

### 3. Read the API Docs

Check the README in each SDK directory:

- `/sdk/python/README.md`
- `/sdk/js/README.md`

### 4. Build Something

Start with a simple tool:
- Vault config validator
- Timeline event counter
- State change detector
- Continuity checker

### 5. Graduate to Full Protocol

When you need more features, move to:
- Full Python implementation: `/src/mirrordna/`
- TypeScript SDK: `/sdk/javascript/`

## Design Philosophy

The SDK follows these principles:

1. **Local First** — Everything runs on your machine
2. **Minimal Dependencies** — Use standard libraries where possible
3. **Simple APIs** — Easy to understand and use
4. **Educational Focus** — Clear examples and documentation
5. **Conceptual Alignment** — Reflects MirrorDNA protocol concepts

See [design_principles.md](design_principles.md) for details.

## Next Steps

- **Explore examples** — Run the included example scripts
- **Read language docs** — Check SDK-specific READMEs
- **Study the protocol** — See `/docs/` for protocol specifications
- **Build a tool** — Create your own MirrorDNA integration
- **Join the community** — Contribute examples and improvements

---

**MirrorDNA Developer SDK** — Simple tools for identity and continuity.

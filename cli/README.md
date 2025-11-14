# MirrorDNA CLI

Command-line interface for MirrorDNA protocol operations.

The MirrorDNA CLI provides tools for initializing vaults, computing cryptographic hashes, and validating continuity logs against protocol schemas.

## Installation

### Prerequisites

- Python 3.7+
- Required packages: `click`, `pyyaml`, `jsonschema`

### Setup

```bash
# Install MirrorDNA package (from repo root)
pip install -e .

# Or install dependencies manually
pip install click pyyaml jsonschema
```

## Usage

The CLI can be invoked in two ways:

```bash
# Method 1: Using the root entry point
python mirrordna.py [command] [options]

# Method 2: Using Python module syntax
python -m cli.mirrordna_cli [command] [options]
```

## Commands

### `init-vault` - Initialize Vault Structure

Create a new vault with sample Master Citation and directory structure.

**Syntax:**
```bash
python mirrordna.py init-vault [OPTIONS]
```

**Options:**
- `--path, -p PATH` - Path where vault should be created (default: `./vault`)
- `--vault-id, -v ID` - Vault ID (default: auto-generated with timestamp)
- `--name, -n NAME` - Human-readable vault name (default: "My Vault")
- `--help` - Show command help

**Creates:**
- `vault_config.yaml` - Vault configuration file
- `master_citation.yaml` - Master Citation (identity binding document)
- `memory/` - Directory for memory entries
- `timeline/` - Directory for timeline event logs
- `snapshots/` - Directory for state snapshots
- `README.md` - Vault documentation

**Examples:**

```bash
# Create vault with default settings
python mirrordna.py init-vault

# Create vault at specific path with custom name
python mirrordna.py init-vault --path ./my_agent_vault --name "Agent Alpha Vault"

# Create vault with custom ID
python mirrordna.py init-vault --path ./vault --vault-id vault_alpha_001 --name "Production Vault"
```

**Output:**
```
✓ Vault initialized successfully!

Location: /home/user/vault
Vault ID: vault_20251114120000
Citation ID: mc_vault_20251114120000_primary_001

Structure created:
  ├── vault_config.yaml
  ├── master_citation.yaml
  ├── README.md
  ├── memory/
  ├── timeline/
  └── snapshots/

Checksum: a3f2b8c9d1e4f5a6...
```

---

### `compute-hash` - Compute Vault State Hash

Compute SHA-256 checksums for files, directories, or vault states.

**Syntax:**
```bash
python mirrordna.py compute-hash --path PATH [OPTIONS]
```

**Options:**
- `--path, -p PATH` - **Required.** Path to directory or file to hash
- `--algorithm, -a ALGO` - Hash algorithm (default: `sha256`)
- `--output, -o FORMAT` - Output format: `short`, `full`, `json` (default: `short`)
- `--help` - Show command help

**Hash Types:**
- **Single file** - Direct SHA-256 hash of file contents
- **Config file** (`.yaml`, `.yml`, `.json`) - Canonical state hash (deterministic, sorted)
- **Directory** - Combined hash of all files with structure

**Examples:**

```bash
# Compute hash of entire vault directory
python mirrordna.py compute-hash --path ./vault

# Compute hash of Master Citation file
python mirrordna.py compute-hash --path ./vault/master_citation.yaml

# Full output with details
python mirrordna.py compute-hash --path ./vault --output full

# JSON output (machine-readable)
python mirrordna.py compute-hash --path ./vault --output json
```

**Output Examples:**

**Short format** (checksum only):
```
a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0
```

**Full format:**
```
Path: /home/user/vault
Type: directory
Files: 5
Algorithm: sha256
Vault Checksum: a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0

File checksums:
  master_citation.yaml: 1234567890abcdef...
  vault_config.yaml: fedcba0987654321...
  README.md: abcdef1234567890...
```

**JSON format:**
```json
{
  "path": "/home/user/vault",
  "type": "directory",
  "algorithm": "sha256",
  "file_count": 5,
  "checksum": "a3f2b8c9d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0",
  "files": [
    {
      "path": "master_citation.yaml",
      "checksum": "1234567890abcdef..."
    }
  ]
}
```

---

### `validate-log` - Validate Continuity Log

Validate timeline event logs or other MirrorDNA data structures against JSON schemas.

**Syntax:**
```bash
python mirrordna.py validate-log --path PATH [OPTIONS]
```

**Options:**
- `--path, -p PATH` - **Required.** Path to continuity log file (JSON or YAML)
- `--schema, -s SCHEMA` - Schema name to validate against (default: `protocol/timeline_event`)
- `--verbose, -v` - Show detailed validation results
- `--help` - Show command help

**Available Schemas:**
- `protocol/master_citation` - Master Citation documents
- `protocol/timeline_event` - Timeline events
- `protocol/vault_entry` - Vault entries
- `protocol/agent_link` - Agent links
- `protocol/glyphtrail_entry` - GlyphTrail entries
- `extensions/identity` - Identity data structures
- `extensions/continuity` - Continuity data structures
- `extensions/memory` - Memory data structures
- `extensions/agent` - Agent data structures

**Examples:**

```bash
# Validate timeline events file
python mirrordna.py validate-log --path timeline/events.json

# Validate Master Citation with specific schema
python mirrordna.py validate-log --path master_citation.yaml --schema protocol/master_citation

# Validate with verbose output
python mirrordna.py validate-log --path events.json --verbose

# Validate identity data
python mirrordna.py validate-log --path identity.yaml --schema extensions/identity
```

**Output Examples:**

**Success:**
```
✓ Validation successful!

Validated against schema: protocol/timeline_event
File: /home/user/vault/timeline/events.json
```

**Success (multiple entries):**
```
✓ All 15 entries are valid!

Validated against schema: protocol/timeline_event
File: /home/user/vault/timeline/events.json
```

**Failure:**
```
❌ Validation failed
  - Validation error: 'id' is a required property at path: 0
  - Validation error: 'timestamp' does not match pattern '^[0-9]{4}-[0-9]{2}-[0-9]{2}T' at path: 1.timestamp
```

---

## Global Options

All commands support these global options:

- `--help` - Show help message
- `--version` - Show CLI version

## Workflow Examples

### 1. Create and Validate a New Vault

```bash
# Initialize vault
python mirrordna.py init-vault --path ./agent_vault --name "My Agent"

# Compute initial vault hash
python mirrordna.py compute-hash --path ./agent_vault

# Validate Master Citation
python mirrordna.py validate-log --path ./agent_vault/master_citation.yaml --schema protocol/master_citation
```

### 2. Verify Vault Integrity

```bash
# Compute vault hash before changes
python mirrordna.py compute-hash --path ./vault > hash_before.txt

# ... make changes to vault ...

# Compute vault hash after changes
python mirrordna.py compute-hash --path ./vault > hash_after.txt

# Compare hashes
diff hash_before.txt hash_after.txt
```

### 3. Validate Timeline Events

```bash
# Create timeline events file (example)
cat > timeline_events.json << 'EOF'
[
  {
    "event_id": "evt_001",
    "event_type": "session_start",
    "timestamp": "2025-11-14T10:00:00Z",
    "actor": "mc_agent_001",
    "payload": {}
  }
]
EOF

# Validate events
python mirrordna.py validate-log --path timeline_events.json --schema protocol/timeline_event --verbose
```

### 4. Batch Operations

```bash
# Initialize multiple vaults
for agent in alpha beta gamma; do
  python mirrordna.py init-vault --path ./vault_$agent --name "Agent $agent"
done

# Compute hashes for all vaults
for vault in vault_*; do
  echo "$vault: $(python mirrordna.py compute-hash --path $vault)"
done
```

## Integration with MirrorDNA Python API

The CLI uses the same core functions as the Python API:

```python
# Equivalent Python code for CLI operations
from mirrordna import compute_state_checksum, ConfigLoader, Validator

# CLI: python mirrordna.py compute-hash --path file.yaml
checksum = compute_state_checksum(data)

# CLI: python mirrordna.py validate-log --path events.json
validator = Validator()
result = validator.validate(data, "protocol/timeline_event")
```

## Troubleshooting

### Command not found

If you get "command not found", ensure you're in the repository root and use:
```bash
python mirrordna.py [command]
```

### Module import errors

If you get import errors, install dependencies:
```bash
pip install click pyyaml jsonschema
```

Or install the package in development mode:
```bash
pip install -e .
```

### Schema validation errors

If validation fails with "Schema file not found", ensure:
1. You're running from the repository root
2. The `schemas/` directory exists
3. Schema files are present in `schemas/protocol/` and `schemas/extensions/`

### Permission errors

If you get permission errors when creating vaults:
```bash
# Ensure you have write permissions
chmod u+w .

# Or use a different path
python mirrordna.py init-vault --path ~/my_vault
```

## Exit Codes

- `0` - Success
- `1` - Error (validation failure, file not found, etc.)

## Development

### Running tests

```bash
# Test CLI commands
python mirrordna.py --version
python mirrordna.py --help
python mirrordna.py init-vault --help
```

### Adding new commands

Edit `cli/mirrordna_cli.py` and add new commands using the `@cli.command()` decorator:

```python
@cli.command()
@click.option('--path', '-p', required=True)
def my_command(path):
    """My new command description."""
    click.echo(f"Running my command on {path}")
```

## See Also

- [MirrorDNA Protocol Documentation](../docs/)
- [Python API Reference](../src/mirrordna/)
- [Examples](../examples/)
- [Schema Reference](../schemas/)

## License

MIT License - See [LICENSE](../LICENSE) for details.

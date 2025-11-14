# MirrorDNA CLI

A powerful command-line interface for the MirrorDNA protocol, giving developers a local interface into core MirrorDNA concepts.

## Features

- **Vault Scaffolding** - Create example vault structures with sample configs
- **Continuity Hashing** - Compute deterministic vault state hashes
- **Log Validation** - Verify continuity log files for correctness
- **Simple Reflection** - Perform local reflections with automatic logging

## Installation

Install MirrorDNA with CLI support:

```bash
# From the repository root
pip install -e .

# Or install specific dependencies
pip install click PyYAML
```

After installation, the `mirrordna` command will be available globally.

## Commands

### `mirrordna init-vault`

Creates a minimal example vault structure.

**Usage:**
```bash
mirrordna init-vault [TARGET_DIR] [OPTIONS]
```

**Arguments:**
- `TARGET_DIR` - Directory to create vault in (default: current directory)

**Options:**
- `--format [yaml|json]` - Config file format (default: yaml)

**Creates:**
```
vault/
├── config/
│   └── vault_config.yaml (or .json)
├── logs/
│   └── continuity.json
├── docs/
└── README.md
```

**Examples:**
```bash
# Create vault in current directory
mirrordna init-vault

# Create vault in specific location
mirrordna init-vault ./my-project

# Use JSON format instead of YAML
mirrordna init-vault --format json
```

---

### `mirrordna compute-hash`

Computes a deterministic "vault state hash" for a directory.

**Usage:**
```bash
mirrordna compute-hash PATH [OPTIONS]
```

**Arguments:**
- `PATH` - Path to vault directory

**Options:**
- `--verbose`, `-v` - Show per-file hashes

**How it works:**
1. Recursively finds all files in the directory
2. Sorts file paths alphabetically for determinism
3. Normalizes text files (line endings, trailing whitespace)
4. Computes SHA-256 hash for each file
5. Combines all hashes into a final vault-state hash

**Examples:**
```bash
# Compute hash for vault
mirrordna compute-hash ./vault

# Show per-file hashes
mirrordna compute-hash ./vault --verbose

# Short form
mirrordna compute-hash ./vault -v
```

**Output:**
```
Computing vault hash for: /path/to/vault

Files processed: 5

Vault State Hash:
a1b2c3d4e5f6...
```

**With --verbose:**
```
Per-file hashes:
----------------------------------------------------------------------
a1b2c3...  config/vault_config.yaml
d4e5f6...  logs/continuity.json
789abc...  README.md
----------------------------------------------------------------------

Files processed: 3

Vault State Hash:
xyz123...
```

---

### `mirrordna verify-log`

Validates a continuity log file (JSON or YAML).

**Usage:**
```bash
mirrordna verify-log FILE [OPTIONS]
```

**Arguments:**
- `FILE` - Path to log file

**Options:**
- `--strict` - Fail on warnings as well as errors

**Validation checks:**
- Required fields present: `timestamp`, `event_type`, `message`
- Valid timestamp format (ISO 8601)
- Non-empty required fields
- Proper data types

**Examples:**
```bash
# Validate a log file
mirrordna verify-log ./vault/logs/continuity.json

# Strict mode (fail on warnings)
mirrordna verify-log ./vault/logs/continuity.yaml --strict
```

**Success output:**
```
Validating log file: /path/to/continuity.json

Found 5 log entries

✓ All entries valid

Event type summary:
  - session_start: 2
  - vault_created: 1
  - memory_created: 2

✓ Log file is valid (5 entries)
```

**Error output:**
```
Validation Errors:
  ✗ Entry 2: Missing required field 'timestamp'
  ✗ Entry 4: Invalid timestamp format 'not-a-date'

✗ Validation failed with 2 error(s)
```

---

### `mirrordna reflect`

Performs a simple local reflection on text.

**Usage:**
```bash
mirrordna reflect TEXT [OPTIONS]
```

**Arguments:**
- `TEXT` - Text to reflect upon (use quotes for multi-word input)

**Options:**
- `--no-log` - Don't write to log file
- `--show-log` - Show log file location

**How it works:**
1. Takes input text
2. Generates a reflective paraphrase
3. Displays the reflection
4. Writes entry to `~/.mirrordna/logs/reflect.log` (unless --no-log)

**Examples:**
```bash
# Simple reflection
mirrordna reflect "Today's work was productive"

# Reflect on a question
mirrordna reflect "How can I improve my workflow?"

# Don't log the reflection
mirrordna reflect "Quick thought" --no-log

# Show log file location
mirrordna reflect "Making progress" --show-log
```

**Output:**
```
Original:
  Today's work was productive

Reflection:
  Reflecting on your progress: "Today's work was productive".
  This represents meaningful forward movement.

✓ Reflection logged
```

**Log file location:**
- Default: `~/.mirrordna/logs/reflect.log`
- Each entry is a JSON line with timestamp, original text, and reflection

---

## Running as a Module

If you don't have the CLI installed globally, you can run it as a Python module:

```bash
python -m cli.main --help
python -m cli.main init-vault
python -m cli.main compute-hash ./vault
```

## Development

### Running Tests

```bash
# Run all CLI tests
pytest cli/tests/ -v

# Run specific test file
pytest cli/tests/test_compute_hash.py -v

# Run with coverage
pytest cli/tests/ --cov=cli --cov-report=html
```

### Project Structure

```
cli/
├── __init__.py           # Package initialization
├── main.py               # CLI entry point
├── commands/             # Command modules
│   ├── __init__.py
│   ├── init_vault.py     # init-vault command
│   ├── compute_hash.py   # compute-hash command
│   ├── verify_log.py     # verify-log command
│   └── reflect.py        # reflect command
├── tests/                # Test suite
│   ├── __init__.py
│   ├── test_compute_hash.py
│   ├── test_verify_log.py
│   └── test_reflect.py
└── README.md             # This file
```

## Common Workflows

### Setting up a new vault

```bash
# Create vault structure
mirrordna init-vault ./my-vault

# Verify the continuity log
mirrordna verify-log ./my-vault/vault/logs/continuity.json

# Compute initial state hash
mirrordna compute-hash ./my-vault/vault
```

### Monitoring vault changes

```bash
# Compute hash before changes
mirrordna compute-hash ./vault > hash-before.txt

# ... make changes to vault ...

# Compute hash after changes
mirrordna compute-hash ./vault > hash-after.txt

# Compare hashes
diff hash-before.txt hash-after.txt
```

### Maintaining a reflection log

```bash
# Daily reflections
mirrordna reflect "Completed user authentication feature"
mirrordna reflect "Need to refactor database layer tomorrow"
mirrordna reflect "Team collaboration was excellent today"

# View your reflection log
cat ~/.mirrordna/logs/reflect.log | jq .
```

## Tips

1. **Use quotes for multi-word arguments:**
   ```bash
   mirrordna reflect "This is a multi-word reflection"
   ```

2. **Chain commands in scripts:**
   ```bash
   #!/bin/bash
   mirrordna init-vault ./new-vault
   cd new-vault/vault
   mirrordna verify-log logs/continuity.json
   mirrordna compute-hash .
   ```

3. **Integrate with git hooks:**
   ```bash
   # In .git/hooks/pre-commit
   mirrordna compute-hash ./vault > .vault-hash
   git add .vault-hash
   ```

4. **Use verbose mode for debugging:**
   ```bash
   mirrordna compute-hash ./vault -v | tee vault-audit.log
   ```

## Troubleshooting

### Command not found

If `mirrordna` command is not found after installation:

```bash
# Reinstall with pip
pip install -e .

# Or use module form
python -m cli.main --help
```

### Import errors

If you get import errors, ensure you're running from the repository root:

```bash
cd /path/to/MirrorDNA
python -m cli.main --help
```

### Permission errors

If you get permission errors when writing logs:

```bash
# Check log directory permissions
ls -la ~/.mirrordna/logs/

# Create directory manually if needed
mkdir -p ~/.mirrordna/logs
```

## See Also

- [MirrorDNA Protocol Documentation](../docs/)
- [MirrorDNA Examples](../examples/)
- [Contributing Guide](../CONTRIBUTING.md)

---

**MirrorDNA CLI** — Local command-line interface for the MirrorDNA protocol.

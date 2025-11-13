# MirrorDNA Tests

This directory contains a comprehensive test suite for MirrorDNA.

## Test Coverage

- **test_validator.py** — Schema validation tests (8 tests)
- **test_identity.py** — Identity management tests (9 tests)
- **test_continuity.py** — Session continuity tests (7 tests)
- **test_memory.py** — Memory management tests (10 tests)

Total: **34 tests** covering all core functionality

## Running Tests

### Standard approach

```bash
# Install dependencies
pip install pytest jsonschema cryptography

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_identity.py -v

# Run with coverage
pytest tests/ --cov=mirrordna --cov-report=html
```

###Environment setup (if needed)

If you encounter import errors, set PYTHONPATH:

```bash
export PYTHONPATH=/path/to/MirrorDNA/src:$PYTHONPATH
pytest tests/ -v
```

## Test Structure

All tests use:
- **pytest** as the testing framework
- **Temporary storage** via fixtures (no persistent test data)
- **Isolated environments** (each test is independent)

## What's Tested

### Validator Tests
- Valid schema validation for all data types
- Invalid schema detection (missing fields, wrong types, wrong formats)
- Error message generation

### Identity Tests
- Creating user, agent, and system identities
- Retrieving identities from storage
- Cryptographic signing and verification
- Identity validation
- Invalid identity type handling

### Continuity Tests
- Creating sessions with and without parents
- Ending sessions
- Retrieving session lineage
- Getting aggregated context
- Session existence checks

### Memory Tests
- Writing memories to all three tiers (short-term, long-term, episodic)
- Reading memories by tier
- Searching memories by content
- Updating memory metadata
- Archiving memories
- Incrementing access counts
- Invalid tier handling

## Dependencies

Tests require:
- `pytest>=7.0.0`
- `jsonschema>=4.0.0`
- `cryptography>=40.0.0`

Optional (for coverage):
- `pytest-cov>=4.0.0`

## Notes

- Tests use temporary directories for storage (cleaned up automatically)
- No external services or network access required
- All tests are deterministic and should pass consistently
- Tests validate both success and failure cases

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest tests/ -v
```

---

**MirrorDNA** — The architecture of persistence.

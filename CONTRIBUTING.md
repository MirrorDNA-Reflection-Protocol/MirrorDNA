# Contributing to MirrorDNA

Thank you for considering contributing to MirrorDNA! This document provides guidelines for contributing to the protocol specification and reference implementations.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Documentation Guidelines](#documentation-guidelines)

---

## Code of Conduct

### Our Standards

- **Be respectful** — Treat all contributors with respect
- **Be collaborative** — Work together to improve the protocol
- **Be constructive** — Provide helpful feedback and suggestions
- **Be patient** — Remember that everyone is learning
- **Focus on the protocol** — Keep discussions technical and protocol-focused

---

## How Can I Contribute?

### 1. Report Bugs

If you find a bug in the protocol implementation:

1. Check if the bug has already been reported in [Issues](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/issues)
2. If not, open a new issue with:
   - Clear title describing the bug
   - Steps to reproduce
   - Expected behavior vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Minimal code example demonstrating the bug

### 2. Suggest Protocol Enhancements

For protocol-level changes:

1. Open a [Discussion](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/discussions) first
2. Describe the use case and motivation
3. Propose the protocol change with examples
4. Gather community feedback
5. If consensus is reached, create an issue and submit a PR

**Note**: Protocol changes require careful consideration as they affect all implementations.

### 3. Improve Documentation

Documentation improvements are always welcome:

- Fix typos or clarify confusing sections
- Add examples or use cases
- Improve code comments
- Write tutorials or guides

### 4. Add Tests

Help improve test coverage:

- Add tests for edge cases
- Add integration tests
- Add performance benchmarks
- Add protocol compliance tests

### 5. Implement Features

Check the [ROADMAP.md](ROADMAP.md) for planned features:

- Comment on the issue to claim it
- Discuss implementation approach
- Submit a PR when ready

---

## Development Setup

### Python Implementation

```bash
# Clone the repository
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA.git
cd MirrorDNA

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ --cov=src/mirrordna --cov-report=html
```

### JavaScript/TypeScript SDK

```bash
# Navigate to SDK directory
cd sdk/javascript

# Install dependencies
npm install

# Run tests
npm test

# Build
npm run build

# Type check
npm run typecheck
```

---

## Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, readable code
   - Follow coding standards (see below)
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests locally**
   ```bash
   pytest tests/ -v
   ```

4. **Run code formatters** (Python)
   ```bash
   black src/mirrordna tests/
   isort src/mirrordna tests/
   ```

5. **Check type hints** (Python)
   ```bash
   mypy src/mirrordna
   ```

### Submitting the PR

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** with:
   - Clear title summarizing the change
   - Description explaining:
     - What changed and why
     - Related issues (use "Fixes #123" to auto-close issues)
     - Any breaking changes
     - How to test the changes
   - Screenshots/examples if applicable

3. **Wait for review**
   - Address reviewer feedback
   - Make requested changes
   - Push updates to the same branch

4. **Merge**
   - Once approved, a maintainer will merge your PR
   - Your contribution will be included in the next release

---

## Coding Standards

### Python

- **Style**: Follow [PEP 8](https://pep8.org/)
- **Formatting**: Use `black` (line length: 88)
- **Imports**: Use `isort` for consistent import ordering
- **Type hints**: Use type hints for all public APIs
- **Docstrings**: Use Google-style docstrings

Example:

```python
def compute_checksum(data: Dict[str, Any]) -> str:
    """
    Compute SHA-256 checksum of data dictionary.

    Args:
        data: Dictionary to checksum using canonical JSON

    Returns:
        Hex-encoded SHA-256 checksum (64 characters)

    Raises:
        ValueError: If data contains non-serializable values
    """
    canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()
```

### JavaScript/TypeScript

- **Style**: Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- **Formatting**: Use Prettier (configured in `sdk/javascript/.prettierrc`)
- **Linting**: Use ESLint (configured in `sdk/javascript/.eslintrc`)
- **Type safety**: Use TypeScript strict mode

Example:

```typescript
/**
 * Compute SHA-256 checksum of data object
 */
export function computeChecksum(data: Record<string, unknown>): string {
  const canonicalJson = JSON.stringify(data, Object.keys(data).sort());
  return createHash('sha256').update(canonicalJson).digest('hex');
}
```

### JSON Schemas

- **Standard**: Use JSON Schema Draft 7
- **Patterns**: Use regex patterns for ID validation
- **Descriptions**: Add clear descriptions for all fields
- **Examples**: Include examples in schema files

---

## Testing Requirements

### Test Coverage Requirements

- **Minimum coverage**: 80% for new code
- **Critical paths**: 100% coverage for checksumming, validation
- **Edge cases**: Test both happy paths and error cases

### Test Structure

```python
def test_feature_name():
    """Test that feature does what it should."""
    # Arrange
    input_data = {...}

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_value
```

### What to Test

- ✅ **Happy paths** — Normal usage scenarios
- ✅ **Error cases** — Invalid inputs, missing files, etc.
- ✅ **Edge cases** — Empty data, very large data, unicode, etc.
- ✅ **Round-trip** — Save/load, serialize/deserialize
- ✅ **Determinism** — Same input produces same output
- ✅ **Checksums** — Verify integrity guarantees

---

## Documentation Guidelines

### Code Documentation

- Document all public APIs with docstrings
- Explain **why**, not just **what**
- Include usage examples
- Document exceptions and edge cases

### Documentation Files

Located in `docs/`:

- **Be concise** — Short sections, clear explanations
- **Include examples** — Real, working code
- **No fluff** — Every sentence should add value
- **Cross-reference** — Link to related docs
- **Keep updated** — Update docs when code changes

### README Updates

When adding features:

- Update Quick Start if API changes
- Update Repository Structure if files added
- Update Documentation section if docs added
- Keep examples working and current

---

## Schema Changes

Protocol schema changes require special care:

### Minor Changes (Backward Compatible)

- Adding optional fields
- Relaxing validation constraints
- Adding new enum values

**Process**:
1. Update schema file
2. Update documentation
3. Add migration notes
4. Bump minor version

### Major Changes (Breaking)

- Removing required fields
- Changing field types
- Renaming fields
- Tightening validation

**Process**:
1. Discuss in GitHub Discussion first
2. Get community consensus
3. Create migration guide
4. Update all implementations
5. Bump major version

---

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
<type>: <short summary>

<optional body>

<optional footer>
```

**Types**:
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `test:` — Test additions or changes
- `refactor:` — Code refactoring
- `chore:` — Maintenance tasks

**Examples**:

```
feat: Add support for encrypted state snapshots

Add new encryption parameter to capture_snapshot() that allows
encrypting snapshot data with AES-256 before saving.

Fixes #123
```

```
docs: Clarify Master Citation lineage behavior

Update master-citation.md to explain how predecessor/successor
chains work in distributed scenarios.
```

---

## Release Process

(For maintainers)

1. Update version in `setup.py`
2. Update `docs/CHANGELOG.md`
3. Create git tag: `git tag -a v1.1.0 -m "Release v1.1.0"`
4. Push tag: `git push origin v1.1.0`
5. Create GitHub release with changelog
6. Publish to PyPI (Python) and npm (JavaScript)

---

## Questions?

- **General questions**: Open a [Discussion](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/discussions)
- **Bug reports**: Open an [Issue](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/issues)
- **Protocol proposals**: Start with a [Discussion](https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA/discussions)

---

## License

By contributing to MirrorDNA, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MirrorDNA! 🎉

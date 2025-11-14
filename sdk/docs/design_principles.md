# MirrorDNA Developer SDK - Design Principles

## Core Philosophy

The MirrorDNA Developer SDK is designed around a simple premise: **make it easy to understand and use MirrorDNA concepts locally**.

We deliberately chose simplicity over features, clarity over completeness, and learning over production-readiness.

## Design Principles

### 1. Local First

**Principle:** All operations run entirely on the developer's local machine.

**Why:**
- No network dependency means fast, reliable operations
- Privacy by default (no data leaves your machine)
- Works offline
- Easy to reason about (no distributed systems complexity)

**Implementation:**
- File I/O only (no HTTP, no sockets)
- No authentication or authorization
- No hosted services or API endpoints
- No telemetry or analytics

**Example:**
```python
# Runs entirely locally
client = MirrorDNAClient()
vault = client.load_vault_config("./vault.yaml")  # File read
hash = client.compute_state_hash("./data")        # Directory scan
```

### 2. Minimal Dependencies

**Principle:** Use only standard library features wherever possible.

**Why:**
- Reduces installation friction
- Minimizes security surface area
- Makes code easier to audit and understand
- Prevents dependency conflicts

**Implementation:**
- Python SDK: Standard library + optional PyYAML
- JavaScript SDK: Node.js built-ins + optional js-yaml
- No frameworks, no ORMs, no heavy libraries

**Dependency Policy:**
- ✅ Standard library: Always use when possible
- ✅ Optional dependencies: For convenience (YAML parsing)
- ❌ Required heavy dependencies: Avoid
- ❌ Framework lock-in: Never

### 3. Deterministic Hashing

**Principle:** Same input always produces same hash.

**Why:**
- Enables reliable state verification
- Makes testing predictable
- Supports tamper detection
- Aligns with MirrorDNA protocol checksumming

**Implementation:**
- Canonical JSON serialization (sorted keys)
- Alphabetical file traversal
- Consistent encoding (UTF-8)
- SHA-256 for all hashing

**Example:**
```python
# These always produce the same hash
hash1 = client.compute_state_hash("./vault")
hash2 = client.compute_state_hash("./vault")
assert hash1 == hash2  # Always true if directory unchanged
```

### 4. Conceptual Alignment with MirrorDNA Standard

**Principle:** SDK concepts map directly to MirrorDNA protocol concepts.

**Why:**
- Easier to learn the protocol through the SDK
- Smooth transition to full implementation
- Maintains protocol integrity
- Educates developers about core concepts

**Mapping:**

| SDK Concept | Protocol Concept |
|-------------|------------------|
| `load_vault_config()` | Vault Configuration Loading |
| `compute_state_hash()` | State Checksum Computation |
| `validate_timeline()` | Timeline Event Validation |
| `compute_data_checksum()` | Canonical State Checksumming |

**Anti-pattern:**
Don't abstract away protocol concepts or introduce new terminology that doesn't exist in the spec.

### 5. Educational Focus

**Principle:** Code should teach MirrorDNA concepts.

**Why:**
- SDK is often the first MirrorDNA code developers see
- Good examples create good practices
- Clear code reduces support burden
- Builds community understanding

**Implementation:**
- Extensive inline comments
- Detailed docstrings with examples
- Working example scripts
- README with multiple use cases
- Error messages that explain what's wrong

**Example:**
```python
def compute_state_hash(self, directory: str, ignore_patterns: Optional[list] = None) -> str:
    """
    Compute deterministic SHA-256 hash of directory contents.

    Creates a hash based on file paths and contents in alphabetical order.
    Useful for detecting changes in vault state.

    Args:
        directory: Path to directory to hash
        ignore_patterns: Optional list of patterns to ignore

    Returns:
        Hexadecimal SHA-256 hash string

    Example:
        >>> client = MirrorDNAClient()
        >>> hash1 = client.compute_state_hash("./my_vault")
        >>> # Make changes to files...
        >>> hash2 = client.compute_state_hash("./my_vault")
        >>> if hash1 != hash2:
        ...     print("Vault state has changed!")
    """
```

### 6. Fail Fast with Clear Errors

**Principle:** Detect problems early and explain them clearly.

**Why:**
- Reduces debugging time
- Helps developers learn correct usage
- Prevents silent failures
- Builds trust in the SDK

**Implementation:**
- Validate inputs immediately
- Check file existence before reading
- Verify data structure before processing
- Provide actionable error messages

**Good Error Messages:**
```python
# ✅ Good - Explains what's wrong and how to fix it
raise ImportError(
    "PyYAML required for YAML files. Install with: pip install pyyaml"
)

# ✅ Good - Specific and actionable
raise ValueError(f"Vault config missing required fields: {missing}")

# ❌ Bad - Vague and unhelpful
raise Exception("Error loading file")
```

### 7. No Magic, No Surprises

**Principle:** Operations should do exactly what they say, nothing more.

**Why:**
- Predictable behavior
- Easy to debug
- No hidden side effects
- Maintainable code

**Implementation:**
- Functions have single, clear purposes
- No global state modifications
- No hidden network calls
- No automatic syncing or caching (except where explicit)

**Example:**
```python
# ✅ Good - Does exactly what it says
def load_vault_config(self, path: str) -> Dict[str, Any]:
    """Load and validate a vault configuration file."""
    # Only loads and validates, nothing else

# ❌ Bad - Hidden side effects
def load_vault_config(self, path: str) -> Dict[str, Any]:
    """Load and validate a vault configuration file."""
    self._sync_to_cloud()  # Surprise!
    self._update_index()   # Hidden side effect!
```

### 8. Simple APIs

**Principle:** APIs should be intuitive and hard to misuse.

**Why:**
- Lower learning curve
- Fewer bugs
- Better developer experience
- Easier documentation

**Guidelines:**
- Methods do one thing well
- Parameters are obvious in meaning
- Return types are consistent
- Errors are catchable

**Example:**
```python
# ✅ Good - Clear, simple API
client = MirrorDNAClient()
vault = client.load_vault_config("vault.yaml")
hash = client.compute_state_hash("./data")

# ❌ Bad - Confusing, complex API
client = MirrorDNAClient(
    config=ConfigOptions(
        vault_loader=VaultLoaderFactory.create(
            strategy="yaml",
            cache=CachePolicy.AGGRESSIVE
        )
    )
)
```

## Non-Goals

These are explicitly **not** goals for the SDK:

### 1. Production Readiness

The SDK is for **learning and development**, not production deployments.

For production:
- Use `/src/mirrordna/` (Python)
- Use `/sdk/javascript/` (TypeScript with advanced features)

### 2. Complete Protocol Implementation

The SDK implements a **subset** of MirrorDNA concepts.

Missing features (intentionally):
- Cryptographic signatures
- Master Citation creation
- Timeline event generation
- State snapshot capture
- Schema validation (deep)

For complete features, use the full protocol implementation.

### 3. Performance Optimization

The SDK prioritizes **clarity over speed**.

Trade-offs:
- Synchronous I/O (simpler to understand)
- No caching (predictable behavior)
- Basic algorithms (easy to audit)

For high performance, use production implementations.

### 4. Framework Integration

The SDK does **not** integrate with web frameworks, ORMs, or platforms.

Reason: Keep it simple and framework-agnostic.

For framework integration, build on top of the SDK or use advanced SDKs.

## Design Decisions

### Why Two Language SDKs (Python and JavaScript)?

**Reason:** Maximum reach to developer communities.

- Python: Data science, AI research, scripting
- JavaScript: Web development, Node.js tools

Both share identical concepts and similar APIs for consistency.

### Why Not TypeScript for the JS SDK?

**Reason:** Lower barrier to entry.

- JavaScript is more universally understood
- No build step required
- Easier for beginners
- TypeScript SDK exists separately (`/sdk/javascript/`)

### Why Basic Validation Only?

**Reason:** Keep dependencies minimal.

- Full JSON Schema validation requires `jsonschema` library
- Basic validation catches 90% of errors
- Developers can add schema validation if needed

### Why No Async/Await in JavaScript?

**Reason:** Simplicity.

- All operations are local file I/O (fast)
- Synchronous code is easier to understand
- No callback/promise complexity
- For async operations, use the TypeScript SDK

## Future Considerations

As the SDK evolves, we'll maintain these principles while considering:

1. **More languages** (Go, Rust) following the same design
2. **Better examples** showing real-world use cases
3. **Testing utilities** to help developers validate integrations
4. **Migration guides** to move from SDK to full implementation

But we will **never** compromise on:
- Local-first operation
- Minimal dependencies
- Conceptual alignment
- Educational focus

## Contributing

When contributing to the SDK, please:

1. **Read these principles** before coding
2. **Keep it simple** — resist feature creep
3. **Document everything** — code should teach
4. **Test locally** — no network dependencies
5. **Follow existing patterns** — consistency matters

See `/CONTRIBUTING.md` for detailed guidelines.

---

**MirrorDNA Developer SDK** — Simple, local, educational tools for identity and continuity.

# MirrorDNA Integration Guide

This guide walks you through integrating MirrorDNA into your application.

## Prerequisites

- Python 3.8 or higher
- Basic understanding of JSON schemas
- Familiarity with identity and session management concepts

## Installation

### Option 1: Install from source

```bash
git clone https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA.git
cd MirrorDNA
pip install -e .
```

### Option 2: Install as dependency

```bash
pip install git+https://github.com/MirrorDNA-Reflection-Protocol/MirrorDNA.git
```

## Quick Integration

### Step 1: Create an Identity

```python
from mirrordna import IdentityManager

# Initialize the identity manager
identity_mgr = IdentityManager()

# Create a user identity
user_identity = identity_mgr.create_identity(
    identity_type="user",
    metadata={
        "name": "Alice",
        "description": "Primary user account"
    }
)

print(f"Created user: {user_identity['identity_id']}")
# Output: Created user: mdna_usr_abc123...

# Save the private key securely (NOT shown in identity record)
# private_key = user_identity['_private_key']  # Handle with care!
```

### Step 2: Create an Agent Identity

```python
# Create an agent identity
agent_identity = identity_mgr.create_identity(
    identity_type="agent",
    metadata={
        "name": "MirrorAgent",
        "version": "1.0.0",
        "description": "Reflective conversation agent"
    }
)

print(f"Created agent: {agent_identity['identity_id']}")
# Output: Created agent: mdna_agt_mirror01...
```

### Step 3: Start a Session

```python
from mirrordna import ContinuityTracker

# Initialize continuity tracker
continuity = ContinuityTracker()

# Create first session (no parent)
session = continuity.create_session(
    agent_id=agent_identity['identity_id'],
    user_id=user_identity['identity_id'],
    parent_session_id=None  # First session
)

print(f"Started session: {session['session_id']}")
# Output: Started session: sess_20250115_100030...
```

### Step 4: Create Memories

```python
from mirrordna import MemoryManager

# Initialize memory manager
memory_mgr = MemoryManager()

# Create a short-term memory (current session)
short_term = memory_mgr.write_memory(
    content="User asked about MirrorDNA integration",
    tier="short_term",
    session_id=session['session_id'],
    agent_id=agent_identity['identity_id'],
    user_id=user_identity['identity_id']
)

# Create a long-term memory (persistent fact)
long_term = memory_mgr.write_memory(
    content="User prefers Python for backend development",
    tier="long_term",
    session_id=session['session_id'],
    agent_id=agent_identity['identity_id'],
    user_id=user_identity['identity_id'],
    metadata={
        "tags": ["preference", "technology"],
        "relevance_score": 0.95
    }
)

print(f"Created {len([short_term, long_term])} memories")
```

### Step 5: Retrieve Memories

```python
# Retrieve all long-term memories for this user
memories = memory_mgr.read_memory(
    tier="long_term",
    filters={"source.user_id": user_identity['identity_id']},
    limit=10
)

for memory in memories:
    print(f"- {memory['content']}")
```

### Step 6: End Session

```python
# End the session
ended_session = continuity.end_session(
    session_id=session['session_id'],
    final_state={
        "topic": "MirrorDNA integration",
        "memories_created": 2,
        "outcome": "successful"
    }
)

print(f"Session ended at: {ended_session['ended_at']}")
```

### Step 7: Resume with Context

```python
# Start a new session linked to previous one
new_session = continuity.create_session(
    agent_id=agent_identity['identity_id'],
    user_id=user_identity['identity_id'],
    parent_session_id=session['session_id']  # Link to previous
)

# Get context from previous session
context = continuity.get_context(new_session['session_id'])
print(f"Restored context: {context}")

# Retrieve relevant memories
relevant_memories = memory_mgr.search_memory(
    query="integration preferences",
    tier="long_term",
    filters={"source.user_id": user_identity['identity_id']},
    limit=5
)
```

## Advanced Integration

### Custom Storage Backend

MirrorDNA supports custom storage backends:

```python
from mirrordna import StorageAdapter, IdentityManager

class PostgresStorageAdapter(StorageAdapter):
    def __init__(self, connection_string):
        self.conn = psycopg2.connect(connection_string)

    def create(self, collection, record):
        # Insert into PostgreSQL
        cursor = self.conn.cursor()
        cursor.execute(
            f"INSERT INTO {collection} (id, data) VALUES (%s, %s)",
            (record['id'], json.dumps(record))
        )
        self.conn.commit()
        return record['id']

    def read(self, collection, record_id):
        # Retrieve from PostgreSQL
        cursor = self.conn.cursor()
        cursor.execute(
            f"SELECT data FROM {collection} WHERE id = %s",
            (record_id,)
        )
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None

    # Implement update, delete, query methods...

# Use custom storage
storage = PostgresStorageAdapter("postgresql://localhost/mirrordna")
identity_mgr = IdentityManager(storage=storage)
```

### Agent DNA Definition

```python
from mirrordna import AgentDNAManager

# Initialize DNA manager
dna_mgr = AgentDNAManager()

# Define agent personality and constraints
agent_dna = dna_mgr.create_agent_dna(
    agent_id=agent_identity['identity_id'],
    version="1.0.0",
    personality_traits={
        "tone": "reflective",
        "style": "conversational",
        "values": ["clarity", "honesty", "growth"]
    },
    behavioral_constraints=[
        "Never impersonate users",
        "Acknowledge uncertainty when present",
        "Respect user privacy"
    ],
    capabilities=[
        "reflection",
        "continuity",
        "memory_management"
    ],
    constitutional_alignment={
        "framework": "MirrorDNA-Standard v1.0",
        "safety_rules": [
            "Prioritize user safety",
            "Maintain transparency"
        ]
    }
)

print(f"Created Agent DNA: {agent_dna['agent_dna_id']}")
```

### Validation

```python
from mirrordna import validate_schema

# Validate any MirrorDNA data structure
identity_data = {
    "identity_id": "mdna_usr_test123",
    "identity_type": "user",
    "created_at": "2025-01-15T10:00:00Z",
    "public_key": "MCowBQYDK2VwAyEA..."
}

result = validate_schema(identity_data, "identity")

if result.is_valid:
    print("✓ Valid identity")
else:
    print("✗ Validation errors:")
    for error in result.errors:
        print(f"  - {error}")
```

### Cryptographic Operations

```python
from mirrordna import CryptoUtils

crypto = CryptoUtils()

# Generate a keypair
public_key, private_key = crypto.generate_keypair()

# Sign a message
message = "This is a signed message"
signature = crypto.sign(message, private_key)

# Verify the signature
is_valid = crypto.verify(message, signature, public_key)
print(f"Signature valid: {is_valid}")  # True

# Hash data
data_hash = crypto.hash({"some": "data"})
print(f"Hash: {data_hash}")
```

## Integration Patterns

### Pattern 1: Stateless API Server

For stateless APIs that need to restore context per request:

```python
# In your API endpoint
@app.post("/chat")
def chat_endpoint(user_id: str, message: str, session_id: str = None):
    # Get or create session
    if session_id:
        session = continuity.get_session(session_id)
    else:
        session = continuity.create_session(
            agent_id="mdna_agt_api_assistant",
            user_id=user_id,
            parent_session_id=None
        )

    # Restore relevant memories
    memories = memory_mgr.read_memory(
        tier="long_term",
        filters={"source.user_id": user_id},
        limit=10
    )

    # Process message with context...
    response = process_chat(message, memories)

    # Save new memories
    memory_mgr.write_memory(
        content=f"User said: {message}",
        tier="short_term",
        session_id=session['session_id'],
        agent_id=session['agent_id'],
        user_id=user_id
    )

    return {"response": response, "session_id": session['session_id']}
```

### Pattern 2: Long-Running Agent Process

For agents that run continuously:

```python
class MirrorAgent:
    def __init__(self, agent_id, storage):
        self.agent_id = agent_id
        self.identity_mgr = IdentityManager(storage)
        self.continuity = ContinuityTracker(storage)
        self.memory_mgr = MemoryManager(storage)
        self.current_session = None

    def start_conversation(self, user_id, parent_session_id=None):
        self.current_session = self.continuity.create_session(
            agent_id=self.agent_id,
            user_id=user_id,
            parent_session_id=parent_session_id
        )

        # Restore context
        if parent_session_id:
            context = self.continuity.get_context(self.current_session['session_id'])
            self.restore_context(context)

    def process_message(self, message):
        # Retrieve relevant memories
        memories = self.memory_mgr.search_memory(
            query=message,
            tier="long_term",
            filters={"source.agent_id": self.agent_id}
        )

        # Generate response with context
        response = self.generate_response(message, memories)

        # Save interaction
        self.memory_mgr.write_memory(
            content=f"User: {message}\nAgent: {response}",
            tier="episodic",
            session_id=self.current_session['session_id'],
            agent_id=self.agent_id,
            user_id=self.current_session['user_id']
        )

        return response

    def end_conversation(self):
        self.continuity.end_session(
            session_id=self.current_session['session_id'],
            final_state={"status": "completed"}
        )
```

### Pattern 3: Multi-Agent System

For systems with multiple agents:

```python
class MultiAgentSystem:
    def __init__(self, storage):
        self.storage = storage
        self.agents = {}

    def register_agent(self, agent_identity, agent_dna):
        agent = MirrorAgent(agent_identity['identity_id'], self.storage)
        self.agents[agent_identity['identity_id']] = agent
        return agent

    def coordinate(self, user_id, task):
        # Create shared session for coordination
        session = continuity.create_session(
            agent_id="mdna_sys_coordinator",
            user_id=user_id,
            parent_session_id=None
        )

        # Each agent contributes
        results = {}
        for agent_id, agent in self.agents.items():
            agent.start_conversation(user_id, parent_session_id=session['session_id'])
            results[agent_id] = agent.process_message(task)
            agent.end_conversation()

        return results
```

## Testing Your Integration

```python
import pytest
from mirrordna import IdentityManager, ContinuityTracker, MemoryManager

def test_full_workflow():
    # Setup
    identity_mgr = IdentityManager()
    continuity = ContinuityTracker()
    memory_mgr = MemoryManager()

    # Create identities
    user = identity_mgr.create_identity("user", {"name": "Test User"})
    agent = identity_mgr.create_identity("agent", {"name": "Test Agent"})

    # Create session
    session = continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id']
    )

    # Write and read memory
    memory = memory_mgr.write_memory(
        content="Test memory",
        tier="short_term",
        session_id=session['session_id'],
        agent_id=agent['identity_id'],
        user_id=user['identity_id']
    )

    retrieved = memory_mgr.read_memory(
        tier="short_term",
        filters={"memory_id": memory['memory_id']}
    )

    assert len(retrieved) == 1
    assert retrieved[0]['content'] == "Test memory"

    # End session
    ended = continuity.end_session(session['session_id'])
    assert ended['ended_at'] is not None
```

## Troubleshooting

### Common Issues

**Issue:** Validation fails with "Invalid identity_id format"

**Solution:** Ensure your ID matches the pattern `mdna_{type}_{suffix}` with at least 12 characters in the suffix.

---

**Issue:** Cannot find schema files

**Solution:** Make sure you've installed MirrorDNA properly and that `schemas/` directory is accessible.

---

**Issue:** Session lineage breaks

**Solution:** Verify that `parent_session_id` exists before creating child session. Use `continuity.session_exists(session_id)` to check.

---

**Issue:** Memory retrieval is slow

**Solution:** Add indexes to your storage backend on common query fields like `user_id`, `agent_id`, `tier`, and `timestamp`.

## Next Steps

- Explore **[examples/](../examples/)** for complete working examples
- Read **[Schema Reference](schema-reference.md)** for detailed field specs
- Check **[Architecture](architecture.md)** to understand internal design
- Review tests in **[tests/](../tests/)** for usage patterns

## Getting Help

- Open an issue in the GitHub repository
- Check existing documentation in **[docs/](../docs/)**
- Review example code in **[examples/](../examples/)**

---

**MirrorDNA** — The architecture of persistence.

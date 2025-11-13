"""
Basic example: Memory management across tiers.
"""

from mirrordna import IdentityManager, ContinuityTracker, MemoryManager

def main():
    print("MirrorDNA Memory Example\n" + "=" * 50)

    # Setup
    identity_mgr = IdentityManager()
    continuity = ContinuityTracker()
    memory_mgr = MemoryManager()

    # Create identities and session
    print("\n1. Setting up identities and session...")
    user = identity_mgr.create_identity("user", {"name": "Charlie"})
    agent = identity_mgr.create_identity("agent", {"name": "MemoryBot"})

    session = continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id']
    )

    print(f"   ✓ User: {user['metadata']['name']}")
    print(f"   ✓ Agent: {agent['metadata']['name']}")
    print(f"   ✓ Session: {session['session_id']}")

    # Create short-term memory
    print("\n2. Creating short-term memory...")
    short_term = memory_mgr.write_memory(
        content="User asked about memory tiers in MirrorDNA",
        tier="short_term",
        session_id=session['session_id'],
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        metadata={
            "tags": ["question", "memory"],
            "relevance_score": 0.8
        }
    )

    print(f"   ✓ Memory: {short_term['memory_id']}")
    print(f"   - Tier: {short_term['tier']}")
    print(f"   - Content: {short_term['content']}")

    # Create long-term memory
    print("\n3. Creating long-term memory...")
    long_term = memory_mgr.write_memory(
        content="User prefers detailed explanations with examples",
        tier="long_term",
        session_id=session['session_id'],
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        metadata={
            "tags": ["preference", "learning_style"],
            "relevance_score": 0.95
        }
    )

    print(f"   ✓ Memory: {long_term['memory_id']}")
    print(f"   - Tier: {long_term['tier']}")
    print(f"   - Content: {long_term['content']}")

    # Create episodic memory
    print("\n4. Creating episodic memory...")
    episodic = memory_mgr.write_memory(
        content={
            "event": "First MirrorDNA tutorial session",
            "outcome": "User understood memory concepts",
            "key_points": ["Tiers", "Storage", "Retrieval"]
        },
        tier="episodic",
        session_id=session['session_id'],
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        metadata={
            "tags": ["tutorial", "milestone"],
            "relevance_score": 0.9
        }
    )

    print(f"   ✓ Memory: {episodic['memory_id']}")
    print(f"   - Tier: {episodic['tier']}")
    print(f"   - Content: {episodic['content']}")

    # Read memories by tier
    print("\n5. Reading long-term memories...")
    long_term_memories = memory_mgr.read_memory(tier="long_term", limit=10)

    print(f"   ✓ Found {len(long_term_memories)} long-term memory(ies):")
    for mem in long_term_memories:
        print(f"      - {mem['content'][:50]}...")

    # Search memories
    print("\n6. Searching for 'preference' memories...")
    matching = memory_mgr.search_memory(
        query="preference",
        tier="long_term",
        limit=5
    )

    print(f"   ✓ Found {len(matching)} matching memory(ies):")
    for mem in matching:
        print(f"      - {mem['content']}")

    # Retrieve specific memory
    print("\n7. Retrieving specific memory...")
    retrieved = memory_mgr.get_memory(short_term['memory_id'])

    if retrieved:
        print(f"   ✓ Retrieved: {retrieved['memory_id']}")
        print(f"   - Created: {retrieved['source']['timestamp']}")
        print(f"   - Access count: {retrieved.get('metadata', {}).get('access_count', 0)}")

    # Increment access count
    print("\n8. Incrementing access count...")
    updated = memory_mgr.increment_access_count(short_term['memory_id'])

    print(f"   ✓ Access count: {updated['metadata']['access_count']}")
    print(f"   - Last accessed: {updated['metadata']['last_accessed']}")

    # Archive a memory
    print("\n9. Archiving a memory...")
    archived = memory_mgr.archive_memory(short_term['memory_id'])

    print(f"   ✓ Archived: {archived['memory_id']}")
    print(f"   - Archived at: {archived['metadata']['archived_at']}")

    # Get all memories for user
    print("\n10. Getting all memories for user...")
    all_user_memories = memory_mgr.read_memory(
        filters={"source.user_id": user['identity_id']},
        limit=100
    )

    print(f"   ✓ Found {len(all_user_memories)} total memory(ies)")

    print("\n" + "=" * 50)
    print("Memory tier summary:")
    print(f"  - Short-term: Ephemeral, current session")
    print(f"  - Long-term: Persistent facts and preferences")
    print(f"  - Episodic: Specific events and experiences")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

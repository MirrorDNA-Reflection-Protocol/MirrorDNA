# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Basic example: Session continuity and lineage tracking.
"""

from mirrordna import IdentityManager, ContinuityTracker

def main():
    print("MirrorDNA Continuity Example\n" + "=" * 50)

    # Setup
    identity_mgr = IdentityManager()
    continuity = ContinuityTracker()

    # Create identities
    print("\n1. Creating identities...")
    user = identity_mgr.create_identity("user", {"name": "Bob"})
    agent = identity_mgr.create_identity("agent", {"name": "Assistant"})

    print(f"   ✓ User: {user['identity_id']}")
    print(f"   ✓ Agent: {agent['identity_id']}")

    # Create first session
    print("\n2. Creating first session...")
    session1 = continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=None,  # First session
        context_metadata={
            "topic": "Introduction to MirrorDNA",
            "tags": ["tutorial", "beginner"]
        }
    )

    print(f"   ✓ Session 1: {session1['session_id']}")
    print(f"   - Started: {session1['started_at']}")
    print(f"   - Topic: {session1['context_metadata']['topic']}")

    # End first session
    print("\n3. Ending first session...")
    ended_session1 = continuity.end_session(
        session1['session_id'],
        final_state={
            "outcome": "successful",
            "memories_created": 5
        }
    )

    print(f"   ✓ Session ended: {ended_session1['ended_at']}")

    # Create second session (linked to first)
    print("\n4. Creating second session (linked to first)...")
    session2 = continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session1['session_id'],  # Link to previous
        context_metadata={
            "restored_from": session1['session_id'],
            "topic": "Advanced MirrorDNA features",
            "tags": ["tutorial", "advanced"]
        }
    )

    print(f"   ✓ Session 2: {session2['session_id']}")
    print(f"   - Parent: {session2['parent_session_id']}")
    print(f"   - Topic: {session2['context_metadata']['topic']}")

    # Get session lineage
    print("\n5. Retrieving session lineage...")
    lineage = continuity.get_session_lineage(session2['session_id'])

    print(f"   ✓ Found {len(lineage)} session(s) in lineage:")
    for i, sess in enumerate(lineage, 1):
        print(f"   {i}. {sess['session_id']}")
        print(f"      Topic: {sess.get('context_metadata', {}).get('topic', 'N/A')}")

    # Get aggregated context
    print("\n6. Getting aggregated context...")
    context = continuity.get_context(session2['session_id'])

    print(f"   ✓ Session count: {context['session_count']}")
    print(f"   ✓ Sessions:")
    for sess in context['sessions']:
        print(f"      - {sess['session_id']}")

    # Create third session (fork from first)
    print("\n7. Creating third session (fork from first)...")
    session3 = continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session1['session_id'],  # Also links to session1
        context_metadata={
            "restored_from": session1['session_id'],
            "topic": "MirrorDNA integration patterns",
            "tags": ["integration", "patterns"]
        }
    )

    print(f"   ✓ Session 3: {session3['session_id']}")
    print(f"   - Parent: {session3['parent_session_id']}")
    print(f"   - Topic: {session3['context_metadata']['topic']}")

    print("\n" + "=" * 50)
    print("Session lineage tree:")
    print("  Session 1 (Introduction)")
    print("    ├─ Session 2 (Advanced features)")
    print("    └─ Session 3 (Integration patterns)")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

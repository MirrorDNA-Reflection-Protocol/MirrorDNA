# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Example: Using the timeline analyzer for advanced lineage tracking.
"""

import asyncio
from mirrordna import (
    IdentityManager,
    ContinuityTracker,
    TimelineAnalyzer
)


async def main():
    print("MirrorDNA Timeline Analyzer Example\n" + "=" * 50)

    # Setup
    identity_mgr = IdentityManager()
    continuity = ContinuityTracker()
    timeline = TimelineAnalyzer(continuity=continuity)

    # Create identities
    print("\n1. Creating identities...")
    user = identity_mgr.create_identity("user", {"name": "Alice"})
    agent = identity_mgr.create_identity("agent", {"name": "TimelineBot"})

    print(f"   ✓ User: {user['metadata']['name']}")
    print(f"   ✓ Agent: {agent['metadata']['name']}")

    # Create a complex session tree with branches
    print("\n2. Creating session tree with branches...")

    # Root session
    session1 = await continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        context_metadata={"topic": "Project planning"}
    )

    # Child sessions (branch A)
    session2a = await continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session1['session_id'],
        context_metadata={"topic": "Feature design", "branch": "A"}
    )

    session3a = await continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session2a['session_id'],
        context_metadata={"topic": "Implementation details", "branch": "A"}
    )

    # Child sessions (branch B)
    session2b = await continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session1['session_id'],
        context_metadata={"topic": "Testing strategy", "branch": "B"}
    )

    session3b = await continuity.create_session(
        agent_id=agent['identity_id'],
        user_id=user['identity_id'],
        parent_session_id=session2b['session_id'],
        context_metadata={"topic": "Test automation", "branch": "B"}
    )

    print(f"   ✓ Created 5 sessions in tree structure")
    print(f"      Root: {session1['session_id']}")
    print(f"      Branch A: {session2a['session_id']} → {session3a['session_id']}")
    print(f"      Branch B: {session2b['session_id']} → {session3b['session_id']}")

    # Get timeline
    print("\n3. Retrieving timeline...")
    session_timeline = await timeline.get_timeline(
        user_id=user['identity_id'],
        limit=10
    )

    print(f"   ✓ Found {len(session_timeline)} sessions in timeline:")
    for sess in session_timeline:
        topic = sess.get('context_metadata', {}).get('topic', 'N/A')
        print(f"      - {sess['session_id'][:20]}... : {topic}")

    # Get lineage tree
    print("\n4. Building lineage tree from root...")
    tree = await timeline.get_lineage_tree(session1['session_id'])

    def print_tree(node, indent=0):
        sess = node['session']
        topic = sess.get('context_metadata', {}).get('topic', 'N/A')
        print(f"{'  ' * indent}• {topic}")
        for child in node.get('children', []):
            print_tree(child, indent + 1)

    print("   ✓ Session tree:")
    print_tree(tree, indent=2)

    # Detect branches
    print("\n5. Detecting branches...")
    branches = await timeline.detect_branches(session1['session_id'])

    print(f"   ✓ Found {len(branches)} branch(es):")
    for i, branch in enumerate(branches, 1):
        print(f"      Branch {i}: {len(branch)} sessions")
        for sess_id in branch:
            sess = await continuity.get_session(sess_id)
            topic = sess.get('context_metadata', {}).get('topic', 'N/A')
            print(f"         → {topic}")

    # Track context evolution
    print("\n6. Tracking context evolution on Branch A...")
    branch_a_ids = [s['session_id'] for s in [session1, session2a, session3a]]
    evolution = await timeline.get_context_evolution(branch_a_ids)

    print(f"   ✓ Context evolution ({len(evolution)} steps):")
    for step in evolution:
        print(f"      Step: {step['context'].get('topic', 'N/A')}")
        if step['diff']['added']:
            print(f"        Added: {list(step['diff']['added'].keys())}")

    # Get session metrics
    print("\n7. Calculating session metrics...")
    metrics = await timeline.get_session_metrics(user_id=user['identity_id'])

    print(f"   ✓ Metrics:")
    print(f"      Total sessions: {metrics['total_sessions']}")
    print(f"      Active sessions: {metrics['active_sessions']}")
    print(f"      Max lineage depth: {metrics['max_lineage_depth']}")
    print(f"      Max branching factor: {metrics['max_branching_factor']}")

    # Find related sessions
    print("\n8. Finding sessions related to {session2a['session_id'][:20]}...")
    related = await timeline.find_related_sessions(session2a['session_id'])

    print(f"   ✓ Related sessions:")
    print(f"      Ancestors: {len(related['ancestors'])}")
    print(f"      Descendants: {len(related['descendants'])}")
    print(f"      Siblings: {len(related['siblings'])}")

    # End some sessions and check concurrent
    print("\n9. Ending sessions and detecting concurrent activity...")
    await continuity.end_session(session3a['session_id'])
    await continuity.end_session(session3b['session_id'])

    concurrent = await timeline.get_concurrent_sessions()

    print(f"   ✓ Concurrent session groups: {len(concurrent)}")

    print("\n" + "=" * 50)
    print("Timeline analyzer provides:")
    print("  - Complete lineage tree visualization")
    print("  - Branch detection and analysis")
    print("  - Context evolution tracking")
    print("  - Session relationship mapping")
    print("  - Temporal metrics and analytics")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())

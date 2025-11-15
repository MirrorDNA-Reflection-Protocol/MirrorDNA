# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Example: Using the reflection engine for agent introspection.
"""

import asyncio
from mirrordna import (
    IdentityManager,
    AgentDNAManager,
    ReflectionEngine,
    ReflectionType
)


async def main():
    print("MirrorDNA Reflection Engine Example\n" + "=" * 50)

    # Setup
    identity_mgr = IdentityManager()
    dna_mgr = AgentDNAManager()

    # Create an agent
    print("\n1. Creating agent with DNA...")
    agent = identity_mgr.create_identity(
        "agent",
        {"name": "ReflectiveAgent", "version": "1.0.0"}
    )

    # Define agent DNA with constraints
    agent_dna = dna_mgr.create_agent_dna(
        agent_id=agent['identity_id'],
        version="1.0.0",
        personality_traits={
            "tone": "thoughtful",
            "style": "analytical",
            "values": ["accuracy", "honesty", "reflection"]
        },
        behavioral_constraints=[
            "Never make unsupported claims",
            "Acknowledge limitations",
            "Reflect on decisions"
        ],
        capabilities=[
            "analysis",
            "decision_making",
            "self_reflection"
        ]
    )

    print(f"   ✓ Agent: {agent['identity_id']}")
    print(f"   ✓ DNA: {agent_dna['agent_dna_id']}")

    # Create reflection engine
    print("\n2. Initializing reflection engine...")
    reflection_engine = ReflectionEngine(
        agent_id=agent['identity_id'],
        dna_manager=dna_mgr
    )

    print("   ✓ Reflection engine ready")

    # Reflect on a decision
    print("\n3. Reflecting on a decision...")
    decision_reflection = await reflection_engine.reflect_on_decision(
        decision="Recommended user switch to asynchronous programming",
        context={
            "user_experience": "intermediate",
            "current_approach": "synchronous",
            "problem": "performance bottlenecks"
        },
        rationale="Async I/O will significantly improve performance for this use case",
        constraints_checked=[
            "Never make unsupported claims",
            "Acknowledge limitations"
        ]
    )

    print(f"   ✓ Reflection ID: {decision_reflection.reflection_id}")
    print(f"   - Type: {decision_reflection.reflection_type}")
    print(f"   - Insights: {len(decision_reflection.insights)}")
    for insight in decision_reflection.insights:
        print(f"     • {insight}")

    # Reflect on capability usage
    print("\n4. Reflecting on capability usage...")
    capability_reflection = await reflection_engine.reflect_on_capability(
        capability="analysis",
        usage_context="Analyzing user's code for performance issues",
        success=True,
        performance_notes="Identified 3 bottlenecks accurately"
    )

    print(f"   ✓ Reflection ID: {capability_reflection.reflection_id}")
    print(f"   - Capability: analysis")
    print(f"   - Success: True")

    # Reflect on current state
    print("\n5. Reflecting on current state...")
    state_reflection = await reflection_engine.reflect_on_state(
        state_snapshot={
            "active_sessions": 1,
            "reflections_count": 2,
            "capabilities_used": ["analysis", "decision_making"],
            "time_active": "5 minutes"
        },
        observations=[
            "Reflection engine is functioning normally",
            "All decisions checked against constraints",
            "High accuracy in capability usage"
        ]
    )

    print(f"   ✓ Reflection ID: {state_reflection.reflection_id}")
    print(f"   - Observations: {len(state_reflection.insights)}")

    # Perform meta-reflection
    print("\n6. Performing meta-reflection...")
    meta_reflection = await reflection_engine.meta_reflect(
        reflection_ids=[
            decision_reflection.reflection_id,
            capability_reflection.reflection_id,
            state_reflection.reflection_id
        ],
        synthesis="Overall performance is strong. Decision-making aligns with constraints. "
                  "Capability usage shows high success rate. Agent maintains good self-awareness."
    )

    print(f"   ✓ Meta-reflection ID: {meta_reflection.reflection_id}")
    print(f"   - Synthesis: {meta_reflection.evaluation}")

    # Get all reflections
    print("\n7. Retrieving all reflections...")
    all_reflections = await reflection_engine.get_reflections()

    print(f"   ✓ Total reflections: {len(all_reflections)}")
    for refl in all_reflections:
        print(f"      - {refl['reflection_type']}: {refl['reflection_id']}")

    # Introspect capabilities
    print("\n8. Introspecting capabilities...")
    introspection = await reflection_engine.introspect_capabilities()

    print(f"   ✓ Agent capabilities:")
    for cap in introspection["capabilities"]:
        perf = introspection["capability_performance"].get(cap, {})
        print(f"      - {cap}")
        print(f"        Usage: {perf.get('usage_count', 0)} times")
        print(f"        Success rate: {perf.get('success_rate', 0):.2%}")

    print("\n" + "=" * 50)
    print("Reflection engine enables:")
    print("  - Decision tracking and justification")
    print("  - Capability performance monitoring")
    print("  - State awareness and introspection")
    print("  - Meta-cognitive analysis")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())

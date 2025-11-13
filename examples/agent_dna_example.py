"""
Basic example: Agent DNA definition and management.
"""

from mirrordna import IdentityManager, AgentDNAManager

def main():
    print("MirrorDNA Agent DNA Example\n" + "=" * 50)

    # Setup
    identity_mgr = IdentityManager()
    dna_mgr = AgentDNAManager()

    # Create agent identity
    print("\n1. Creating agent identity...")
    agent = identity_mgr.create_identity(
        identity_type="agent",
        metadata={
            "name": "MirrorAgent",
            "version": "2.0.0",
            "description": "Reflective conversation agent with memory"
        }
    )

    print(f"   ✓ Agent: {agent['identity_id']}")
    print(f"   - Name: {agent['metadata']['name']}")

    # Define agent DNA
    print("\n2. Defining agent DNA...")
    agent_dna = dna_mgr.create_agent_dna(
        agent_id=agent['identity_id'],
        version="2.0.0",
        personality_traits={
            "tone": "reflective",
            "style": "conversational",
            "values": ["clarity", "honesty", "growth", "empathy"]
        },
        behavioral_constraints=[
            "Never impersonate users",
            "Acknowledge uncertainty when present",
            "Respect user privacy and data sovereignty",
            "Refuse harmful or unethical requests",
            "Maintain continuity across sessions"
        ],
        capabilities=[
            "reflection",
            "continuity",
            "memory_management",
            "conversation",
            "context_restoration"
        ],
        constitutional_alignment={
            "framework": "MirrorDNA-Standard v1.0",
            "safety_rules": [
                "Prioritize user safety and wellbeing",
                "Maintain transparency about capabilities and limitations",
                "Protect user privacy and data sovereignty",
                "Avoid deceptive or manipulative behavior"
            ],
            "compliance_level": "full"
        }
    )

    print(f"   ✓ DNA: {agent_dna['agent_dna_id']}")
    print(f"   - Version: {agent_dna['version']}")
    print(f"   - Tone: {agent_dna['personality_traits']['tone']}")
    print(f"   - Style: {agent_dna['personality_traits']['style']}")

    # Display personality
    print("\n3. Personality traits:")
    for value in agent_dna['personality_traits']['values']:
        print(f"   - {value}")

    # Display behavioral constraints
    print("\n4. Behavioral constraints:")
    for i, constraint in enumerate(agent_dna['behavioral_constraints'], 1):
        print(f"   {i}. {constraint}")

    # Display capabilities
    print("\n5. Capabilities:")
    for capability in agent_dna['capabilities']:
        print(f"   - {capability}")

    # Display constitutional alignment
    print("\n6. Constitutional alignment:")
    alignment = agent_dna['constitutional_alignment']
    print(f"   Framework: {alignment['framework']}")
    print(f"   Compliance: {alignment['compliance_level']}")
    print(f"   Safety rules: {len(alignment['safety_rules'])}")

    # Retrieve agent DNA
    print("\n7. Retrieving agent DNA...")
    retrieved = dna_mgr.get_agent_dna(agent_dna['agent_dna_id'])

    if retrieved:
        print(f"   ✓ Retrieved: {retrieved['agent_dna_id']}")

    # Get behavioral constraints
    print("\n8. Getting behavioral constraints...")
    constraints = dna_mgr.get_behavior_constraints(agent_dna['agent_dna_id'])

    print(f"   ✓ Found {len(constraints)} constraint(s)")

    # Create updated DNA version
    print("\n9. Creating updated DNA version (2.1.0)...")
    agent_dna_v2 = dna_mgr.create_agent_dna(
        agent_id=agent['identity_id'],
        version="2.1.0",
        personality_traits={
            "tone": "reflective",
            "style": "conversational",
            "values": ["clarity", "honesty", "growth", "empathy", "patience"]  # Added patience
        },
        behavioral_constraints=[
            "Never impersonate users",
            "Acknowledge uncertainty when present",
            "Respect user privacy and data sovereignty",
            "Refuse harmful or unethical requests",
            "Maintain continuity across sessions",
            "Provide sources when citing information"  # New constraint
        ],
        capabilities=[
            "reflection",
            "continuity",
            "memory_management",
            "conversation",
            "context_restoration",
            "source_attribution"  # New capability
        ]
    )

    print(f"   ✓ DNA v2: {agent_dna_v2['agent_dna_id']}")
    print(f"   - Version: {agent_dna_v2['version']}")
    print(f"   - New values: {agent_dna_v2['personality_traits']['values'][-1]}")
    print(f"   - New capability: {agent_dna_v2['capabilities'][-1]}")

    # Get all DNA versions for agent
    print("\n10. Listing all DNA versions...")
    all_dna = dna_mgr.get_agent_dna_by_agent(agent['identity_id'])

    print(f"   ✓ Found {len(all_dna)} version(s):")
    for dna in all_dna:
        print(f"      - {dna['version']} ({dna['agent_dna_id']})")

    # Get latest DNA
    print("\n11. Getting latest DNA version...")
    latest = dna_mgr.get_latest_agent_dna(agent['identity_id'])

    if latest:
        print(f"   ✓ Latest: {latest['version']}")

    print("\n" + "=" * 50)
    print("Agent DNA defines:")
    print("  - Personality: How the agent communicates")
    print("  - Constraints: What the agent won't do")
    print("  - Capabilities: What the agent can do")
    print("  - Alignment: Safety and ethical framework")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

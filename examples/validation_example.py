# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Basic example: Schema validation.
"""

from mirrordna import validate_schema

def main():
    print("MirrorDNA Validation Example\n" + "=" * 50)

    # Valid identity
    print("\n1. Validating a VALID identity...")
    valid_identity = {
        "identity_id": "mdna_usr_test123abc456",
        "identity_type": "user",
        "created_at": "2025-01-15T10:00:00Z",
        "public_key": "MCowBQYDK2VwAyEAGb9ECWmEzf6FQbrBZ9w7lP"
    }

    result = validate_schema(valid_identity, "identity")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Schema: {result.schema_name}")
    print(f"   - Errors: {len(result.errors)}")

    # Invalid identity (missing required field)
    print("\n2. Validating an INVALID identity (missing public_key)...")
    invalid_identity = {
        "identity_id": "mdna_usr_test456def789",
        "identity_type": "user",
        "created_at": "2025-01-15T10:00:00Z"
        # Missing public_key
    }

    result = validate_schema(invalid_identity, "identity")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Errors: {len(result.errors)}")
    for error in result.errors:
        print(f"      * {error}")

    # Invalid identity (wrong ID format)
    print("\n3. Validating an INVALID identity (wrong ID format)...")
    invalid_identity2 = {
        "identity_id": "wrong_format_123",  # Doesn't match pattern
        "identity_type": "user",
        "created_at": "2025-01-15T10:00:00Z",
        "public_key": "MCowBQYDK2VwAyEAGb9ECWmEzf6FQbrBZ9w7lP"
    }

    result = validate_schema(invalid_identity2, "identity")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Errors: {len(result.errors)}")
    for error in result.errors:
        print(f"      * {error}")

    # Valid continuity record
    print("\n4. Validating a VALID continuity record...")
    valid_continuity = {
        "session_id": "sess_20250115_100030_a7x9k",
        "parent_session_id": None,
        "agent_id": "mdna_agt_mirror01_v2",
        "user_id": "mdna_usr_alice7x9k2m",
        "started_at": "2025-01-15T10:00:30Z",
        "ended_at": None
    }

    result = validate_schema(valid_continuity, "continuity")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Schema: {result.schema_name}")
    print(f"   - Errors: {len(result.errors)}")

    # Valid memory record
    print("\n5. Validating a VALID memory record...")
    valid_memory = {
        "memory_id": "mem_20250115_100045_c3z7n",
        "tier": "long_term",
        "content": "User prefers Python over JavaScript",
        "source": {
            "session_id": "sess_20250115_100030_a7x9k",
            "timestamp": "2025-01-15T10:00:45Z",
            "agent_id": "mdna_agt_mirror01_v2",
            "user_id": "mdna_usr_alice7x9k2m"
        }
    }

    result = validate_schema(valid_memory, "memory")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Schema: {result.schema_name}")
    print(f"   - Errors: {len(result.errors)}")

    # Invalid memory (wrong tier)
    print("\n6. Validating an INVALID memory (wrong tier)...")
    invalid_memory = {
        "memory_id": "mem_test123",
        "tier": "medium_term",  # Invalid tier
        "content": "Some content",
        "source": {
            "session_id": "sess_test456",
            "timestamp": "2025-01-15T10:00:45Z",
            "agent_id": "mdna_agt_test",
            "user_id": "mdna_usr_test"
        }
    }

    result = validate_schema(invalid_memory, "memory")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Errors: {len(result.errors)}")
    for error in result.errors:
        print(f"      * {error}")

    # Valid agent DNA
    print("\n7. Validating a VALID agent DNA record...")
    valid_agent_dna = {
        "agent_dna_id": "dna_mirror01_v2_0_0",
        "agent_id": "mdna_agt_mirror01_v2",
        "version": "2.0.0",
        "personality_traits": {
            "tone": "reflective",
            "style": "conversational",
            "values": ["clarity", "honesty"]
        },
        "behavioral_constraints": [
            "Never impersonate users",
            "Respect privacy"
        ],
        "capabilities": [
            "reflection",
            "memory_management"
        ]
    }

    result = validate_schema(valid_agent_dna, "agent")

    print(f"   ✓ Valid: {result.is_valid}")
    print(f"   - Schema: {result.schema_name}")
    print(f"   - Errors: {len(result.errors)}")

    print("\n" + "=" * 50)
    print("Validation ensures:")
    print("  - Required fields are present")
    print("  - Data types are correct")
    print("  - Values match allowed patterns")
    print("  - IDs follow proper format")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

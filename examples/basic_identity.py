"""
Basic example: Creating and managing identities.
"""

from mirrordna import IdentityManager

def main():
    print("MirrorDNA Identity Example\n" + "=" * 50)

    # Initialize identity manager
    identity_mgr = IdentityManager()

    # Create a user identity
    print("\n1. Creating user identity...")
    user_identity = identity_mgr.create_identity(
        identity_type="user",
        metadata={
            "name": "Alice",
            "description": "Primary user account"
        }
    )

    print(f"   ✓ Created user: {user_identity['identity_id']}")
    print(f"   - Name: {user_identity['metadata']['name']}")
    print(f"   - Public key: {user_identity['public_key'][:20]}...")

    # IMPORTANT: Store private key securely!
    private_key = user_identity.pop('_private_key')
    print(f"   - Private key: {private_key[:20]}... (store securely!)")

    # Create an agent identity
    print("\n2. Creating agent identity...")
    agent_identity = identity_mgr.create_identity(
        identity_type="agent",
        metadata={
            "name": "MirrorAgent",
            "version": "1.0.0",
            "description": "Reflective conversation agent"
        }
    )

    print(f"   ✓ Created agent: {agent_identity['identity_id']}")
    print(f"   - Name: {agent_identity['metadata']['name']}")
    print(f"   - Version: {agent_identity['metadata']['version']}")

    agent_private_key = agent_identity.pop('_private_key')

    # Retrieve an identity
    print("\n3. Retrieving user identity...")
    retrieved = identity_mgr.get_identity(user_identity['identity_id'])

    if retrieved:
        print(f"   ✓ Retrieved: {retrieved['identity_id']}")
        print(f"   - Type: {retrieved['identity_type']}")
        print(f"   - Created: {retrieved['created_at']}")

    # Sign and verify a claim
    print("\n4. Signing and verifying a claim...")
    claim = "I am the legitimate user Alice"

    signature = identity_mgr.sign_claim(
        user_identity['identity_id'],
        claim,
        private_key
    )

    print(f"   ✓ Signed claim")
    print(f"   - Signature: {signature[:30]}...")

    # Verify the signature
    is_valid = identity_mgr.verify_claim(
        user_identity['identity_id'],
        claim,
        signature
    )

    print(f"   ✓ Verification: {'VALID' if is_valid else 'INVALID'}")

    # Validate identity structure
    print("\n5. Validating identity...")
    is_valid_structure = identity_mgr.validate_identity(user_identity)

    print(f"   ✓ Identity structure: {'VALID' if is_valid_structure else 'INVALID'}")

    print("\n" + "=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

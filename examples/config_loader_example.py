# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Example: Using the checksummed config loader.
"""

from mirrordna import ConfigLoader, SecureConfigLoader


def main():
    print("MirrorDNA Config Loader Example\n" + "=" * 50)

    # Create config loader
    print("\n1. Initializing config loader...")
    config_loader = ConfigLoader()

    print("   ✓ Config loader ready")

    # Save a configuration with checksum
    print("\n2. Saving configuration with checksum...")
    agent_config = {
        "agent_name": "MirrorAgent",
        "model": "claude-sonnet-4",
        "max_tokens": 4096,
        "temperature": 0.7,
        "capabilities": ["conversation", "analysis", "reflection"],
        "safety_settings": {
            "content_filter": True,
            "rate_limit": 100,
            "timeout_seconds": 30
        }
    }

    checksum_meta = config_loader.save_config(
        name="agent_config",
        config=agent_config,
        version="1.0.0",
        checksum_algorithm="sha256"
    )

    print(f"   ✓ Config saved: agent_config")
    print(f"   - Version: {checksum_meta.version}")
    print(f"   - Algorithm: {checksum_meta.algorithm}")
    print(f"   - Hash: {checksum_meta.hash[:16]}...")
    print(f"   - Created: {checksum_meta.created_at}")

    # Load configuration with verification
    print("\n3. Loading configuration with verification...")
    loaded_config = config_loader.load_config("agent_config", verify=True)

    print(f"   ✓ Config loaded and verified")
    print(f"   - Agent: {loaded_config['agent_name']}")
    print(f"   - Model: {loaded_config['model']}")
    print(f"   - Capabilities: {len(loaded_config['capabilities'])}")

    # Check integrity
    print("\n4. Verifying configuration integrity...")
    is_valid = config_loader.verify_config_integrity("agent_config")

    print(f"   ✓ Integrity check: {'PASSED' if is_valid else 'FAILED'}")

    # List all configurations
    print("\n5. Listing all configurations...")
    all_configs = config_loader.list_configs()

    print(f"   ✓ Found {len(all_configs)} configuration(s):")
    for name, meta in all_configs.items():
        print(f"      - {name}")
        print(f"        Has checksum: {meta['has_checksum']}")
        print(f"        Version: {meta['version']}")

    # Use secure config loader
    print("\n6. Using secure config loader with whitelist...")
    secure_loader = SecureConfigLoader(
        allowed_configs=["agent_config"]
    )

    # This will work (in whitelist)
    try:
        secure_config = secure_loader.load_config("agent_config")
        print(f"   ✓ Loaded whitelisted config: agent_config")
    except ValueError as e:
        print(f"   ✗ Error: {e}")

    # This will fail (not in whitelist)
    print("\n7. Attempting to load non-whitelisted config...")
    try:
        secure_loader.load_config("malicious_config")
        print(f"   ✗ Should have failed!")
    except (ValueError, FileNotFoundError) as e:
        print(f"   ✓ Blocked as expected: Not in whitelist")

    # Calculate checksums
    print("\n8. Calculating checksums for data...")
    test_data = {"key": "value", "number": 42}

    sha256_hash = config_loader.calculate_checksum(test_data, "sha256")
    sha512_hash = config_loader.calculate_checksum(test_data, "sha512")

    print(f"   ✓ SHA-256: {sha256_hash[:32]}...")
    print(f"   ✓ SHA-512: {sha512_hash[:32]}...")

    # Get checksum info
    print("\n9. Retrieving checksum metadata...")
    checksum_info = config_loader.get_checksum_info("agent_config")

    if checksum_info:
        print(f"   ✓ Algorithm: {checksum_info.algorithm}")
        print(f"   ✓ Hash: {checksum_info.hash}")
        print(f"   ✓ Version: {checksum_info.version}")
        print(f"   ✓ Created: {checksum_info.created_at}")

    print("\n" + "=" * 50)
    print("Checksummed config loader provides:")
    print("  - Integrity verification (SHA-256, SHA-512)")
    print("  - Version tracking")
    print("  - Secure loading with whitelists")
    print("  - Tamper detection")
    print("=" * 50)
    print("Example completed successfully!")


if __name__ == "__main__":
    main()

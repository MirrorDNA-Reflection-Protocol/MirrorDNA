#!/usr/bin/env node
/**
 * MirrorDNA SDK - Basic Usage Example
 *
 * Demonstrates how to use the MirrorDNA JavaScript SDK for common operations:
 * 1. Load a vault configuration
 * 2. Compute state hash for a directory
 * 3. Validate a timeline file
 * 4. Get continuity status
 */

const fs = require('fs');
const path = require('path');
const { MirrorDNAClient } = require('../mirrordnaClient.js');

function printSection(title) {
    console.log('\n' + '='.repeat(60));
    console.log(`  ${title}`);
    console.log('='.repeat(60));
}

function main() {
    console.log('MirrorDNA JavaScript SDK - Basic Usage Example');
    console.log('='.repeat(60));

    // Initialize client
    const client = new MirrorDNAClient();

    // Example 1: Load vault configuration
    printSection('1. Loading Vault Configuration');

    // Use example vault from repo if it exists
    const vaultPath = path.join(__dirname, '../../../examples/minimal_vault.yaml');

    let vaultConfig;
    if (fs.existsSync(vaultPath)) {
        try {
            vaultConfig = client.loadVaultConfig(vaultPath);
            console.log('✓ Loaded vault configuration');
            console.log(`  Vault ID: ${vaultConfig.vault_id}`);
            console.log(`  Name: ${vaultConfig.name}`);
            console.log(`  Path: ${vaultConfig.path}`);
            console.log(`  Created: ${vaultConfig.created_at}`);
        } catch (e) {
            console.log(`✗ Error loading vault: ${e.message}`);
        }
    } else {
        console.log(`ℹ Example vault not found at: ${vaultPath}`);
        console.log('  Creating a sample vault config in memory...');

        // Create sample config
        vaultConfig = {
            vault_id: 'vault_demo_001',
            name: 'Demo Vault',
            path: './demo_data',
            created_at: '2025-11-14T10:00:00Z'
        };
        console.log(`  Created sample vault: ${vaultConfig.vault_id}`);
    }

    // Example 2: Compute state hash for a directory
    printSection('2. Computing Directory State Hash');

    // Use current directory as example
    const testDir = path.join(__dirname, '..');  // sdk/js directory

    try {
        const stateHash = client.computeStateHash(testDir);
        console.log(`✓ Computed state hash for: ${testDir}`);
        console.log(`  Hash: ${stateHash}`);
        console.log(`  Length: ${stateHash.length} characters (SHA-256)`);

        // Compute again to show determinism
        const stateHash2 = client.computeStateHash(testDir);
        if (stateHash === stateHash2) {
            console.log('✓ Hash is deterministic (same result on re-computation)');
        } else {
            console.log('✗ Warning: Hash changed between computations');
        }
    } catch (e) {
        console.log(`✗ Error computing state hash: ${e.message}`);
    }

    // Example 3: Validate timeline
    printSection('3. Validating Timeline File');

    // Create a sample timeline for demonstration
    const sampleTimeline = {
        timeline_id: 'demo_timeline_001',
        event_count: 2,
        events: [
            {
                id: 'evt_001',
                timestamp: '2025-11-14T10:00:00Z',
                event_type: 'session_start',
                actor: 'mc_demo_agent_001',
                payload: { platform: 'Demo' }
            },
            {
                id: 'evt_002',
                timestamp: '2025-11-14T10:05:00Z',
                event_type: 'memory_created',
                actor: 'mc_demo_agent_001',
                payload: { content: 'User prefers JavaScript' }
            }
        ]
    };

    // Save to temporary file
    const timelinePath = '/tmp/demo_timeline.json';
    fs.writeFileSync(timelinePath, JSON.stringify(sampleTimeline, null, 2));

    try {
        const result = client.validateTimeline(timelinePath);

        if (result.valid) {
            console.log('✓ Timeline is valid');
            console.log(`  Timeline ID: ${result.timeline_id}`);
            console.log(`  Event count: ${result.event_count}`);
            console.log(`  First event: ${result.first_event || 'N/A'}`);
            console.log(`  Last event: ${result.last_event || 'N/A'}`);
        } else {
            console.log('✗ Timeline validation failed');
            console.log(`  Errors: ${result.errors.join(', ')}`);
        }
    } catch (e) {
        console.log(`✗ Error validating timeline: ${e.message}`);
    }

    // Example 4: Get continuity status
    printSection('4. Getting Continuity Status');

    try {
        const status = client.getContinuityStatus({
            timelinePath: timelinePath
        });

        console.log('Continuity Status:');
        console.log(`  Timestamp: ${status.timestamp}`);
        console.log(`  Timeline valid: ${status.timeline_valid}`);
        console.log(`  Event count: ${status.event_count || 0}`);

        if (status.state_hash) {
            console.log(`  State hash: ${status.state_hash.substring(0, 16)}...`);
        }
    } catch (e) {
        console.log(`✗ Error getting continuity status: ${e.message}`);
    }

    // Example 5: Data checksum
    printSection('5. Computing Data Checksum');

    const sampleData = {
        id: 'mc_example_001',
        version: '1.0.0',
        vault_id: 'vault_example',
        created_at: '2025-11-14T10:00:00Z'
    };

    const checksum = client.computeDataChecksum(sampleData);
    console.log('✓ Computed checksum for sample data');
    console.log(`  Checksum: ${checksum}`);
    console.log(`  Data: ${JSON.stringify(sampleData)}`);

    // Verify determinism
    const checksum2 = client.computeDataChecksum(sampleData);
    if (checksum === checksum2) {
        console.log('✓ Checksum is deterministic');
    }

    // Summary
    printSection('Summary');
    console.log(`
The MirrorDNA SDK provides simple tools for:
- Loading and validating vault configurations
- Computing deterministic state hashes
- Validating timeline event logs
- Tracking continuity status

All operations are local-only and use Node.js built-in modules.

Next steps:
- Explore the full protocol in src/mirrordna/
- Check out examples/ for more advanced usage
- Read docs/ for protocol specifications
    `);

    console.log('✓ Example completed successfully!\n');
}

// Run if called directly
if (require.main === module) {
    main();
}

module.exports = { main };

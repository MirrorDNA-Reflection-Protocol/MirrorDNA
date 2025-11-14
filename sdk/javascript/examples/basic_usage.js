#!/usr/bin/env node
/**
 * Basic usage example for MirrorDNA SDK (JavaScript/Node.js).
 *
 * This example demonstrates:
 * 1. Creating a MirrorDNA client
 * 2. Creating a Master Citation
 * 3. Computing state hashes
 * 4. Creating and validating timeline events
 * 5. Checking continuity status
 *
 * No backend required - everything runs locally with files.
 */

const MirrorDNAClient = require('../mirror_dna_client');

function main() {
    console.log('='.repeat(60));
    console.log('MirrorDNA SDK - Basic Usage Example (JavaScript)');
    console.log('='.repeat(60));
    console.log();

    // 1. Initialize client
    console.log('1. Initializing MirrorDNA client...');
    const client = new MirrorDNAClient('./sdk_demo_data_js');
    console.log(`   ✓ Client initialized, data dir: ${client.dataDir}`);
    console.log();

    // 2. Create a Master Citation
    console.log('2. Creating Master Citation...');
    const citation = client.createMasterCitation(
        'agent_assistant_js_001',
        'vault_main_storage',
        '1.0.0'
    );
    console.log(`   Citation ID: ${citation.id}`);
    console.log(`   Vault ID: ${citation.vault_id}`);
    console.log(`   Checksum: ${citation.checksum.substring(0, 16)}...`);
    console.log();

    // 3. Save citation to file
    console.log('3. Saving citation to file...');
    const citationPath = client.saveCitation(citation);
    console.log(`   ✓ Saved to: ${citationPath}`);
    console.log();

    // 4. Compute state hash for arbitrary data
    console.log('4. Computing state hashes...');
    const userData = {
        name: 'Alice',
        preferences: {
            language: 'JavaScript',
            theme: 'dark'
        },
        created: '2025-11-14T10:00:00Z'
    };

    const hash1 = client.computeStateHash(userData);
    console.log(`   Hash of user data: ${hash1}`);

    // Demonstrate determinism - same data = same hash
    const hash2 = client.computeStateHash(userData);
    console.log(`   Hash (computed again): ${hash2}`);
    console.log(`   ✓ Hashes match: ${hash1 === hash2}`);
    console.log();

    // 5. Create timeline events
    console.log('5. Creating timeline events...');
    const actorId = citation.id;

    // Session start
    const event1 = client.createTimelineEvent(
        'session_start',
        actorId,
        {
            platform: 'SDK_Demo_JS',
            version: '1.0.0'
        }
    );
    console.log(`   Event 1: ${event1.event_type} (${event1.id})`);

    // Memory created
    const event2 = client.createTimelineEvent(
        'memory_created',
        actorId,
        {
            content: 'User prefers JavaScript for development',
            tier: 'long_term'
        }
    );
    console.log(`   Event 2: ${event2.event_type} (${event2.id})`);

    // Memory created
    const event3 = client.createTimelineEvent(
        'memory_created',
        actorId,
        {
            content: 'User uses dark theme',
            tier: 'long_term'
        }
    );
    console.log(`   Event 3: ${event3.event_type} (${event3.id})`);

    // Session end
    const event4 = client.createTimelineEvent(
        'session_end',
        actorId,
        {
            duration_seconds: 300,
            outcome: 'successful'
        }
    );
    console.log(`   Event 4: ${event4.event_type} (${event4.id})`);
    console.log();

    // 6. Validate timeline
    console.log('6. Validating timeline...');
    const events = [event1, event2, event3, event4];
    const validation = client.validateTimeline(events);

    console.log(`   Valid: ${validation.valid}`);
    console.log(`   Total events: ${validation.total_events}`);
    console.log(`   Event types: ${JSON.stringify(validation.event_types)}`);
    console.log(`   Unique actors: ${validation.unique_actors}`);
    console.log(`   Timespan: ${validation.timespan.first} to ${validation.timespan.last}`);
    console.log();

    // 7. Check continuity status
    console.log('7. Checking continuity status...');
    const status = client.getContinuityStatus(actorId);

    console.log(`   Identity: ${status.identity_id.substring(0, 40)}...`);
    console.log(`   Status: ${status.status}`);
    console.log(`   Total events: ${status.total_events}`);
    console.log(`   Last activity: ${status.last_activity}`);
    console.log();

    // 8. Save timeline to file
    console.log('8. Saving timeline...');
    const timelinePath = client.saveTimeline(actorId);
    console.log(`   ✓ Saved to: ${timelinePath}`);
    console.log();

    // 9. Verify checksum
    console.log('9. Verifying citation checksum...');
    const citationWithoutChecksum = Object.fromEntries(
        Object.entries(citation).filter(([k]) => k !== 'checksum')
    );
    const isValid = client.verifyChecksum(
        citationWithoutChecksum,
        citation.checksum
    );
    console.log(`   ✓ Checksum valid: ${isValid}`);
    console.log();

    // 10. Load timeline from file
    console.log('10. Loading timeline from file...');
    const loadedEvents = client.loadTimeline(timelinePath);
    console.log(`    ✓ Loaded ${loadedEvents.length} events`);
    console.log();

    console.log('='.repeat(60));
    console.log('✓ Demo completed successfully!');
    console.log('='.repeat(60));
    console.log();
    console.log('Files created:');
    console.log(`  - ${citationPath}`);
    console.log(`  - ${timelinePath}`);
    console.log();
    console.log('Continuity Status Summary:');
    console.log(`  Identity: ${status.identity_id.substring(0, 50)}...`);
    console.log(`  Status: ${status.status.toUpperCase()}`);
    console.log(`  Events: ${status.total_events}`);
    console.log(`  Valid: ${status.valid}`);
    console.log();
}

// Run the example
if (require.main === module) {
    main();
}

module.exports = main;

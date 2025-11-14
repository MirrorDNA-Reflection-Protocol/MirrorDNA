/**
 * MirrorDNA SDK Client - Simple developer interface to MirrorDNA protocol.
 *
 * This client provides high-level methods for working with MirrorDNA concepts:
 * - Loading and validating vault configurations
 * - Computing state hashes for integrity verification
 * - Validating timeline events
 * - Managing continuity tracking
 *
 * Designed for offline/local use without requiring a hosted backend.
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Simple client for integrating MirrorDNA concepts into your application.
 *
 * Features:
 * - Load and validate vault configurations
 * - Compute deterministic state hashes (SHA-256)
 * - Validate timeline event structures
 * - Track continuity metrics
 *
 * All operations work locally with files - no backend required.
 */
class MirrorDNAClient {
    /**
     * Initialize MirrorDNA client.
     *
     * @param {string} [dataDir='./mirrordna_data'] - Directory for storing data files
     */
    constructor(dataDir = './mirrordna_data') {
        this.dataDir = dataDir;

        // Create data directory if it doesn't exist
        if (!fs.existsSync(this.dataDir)) {
            fs.mkdirSync(this.dataDir, { recursive: true });
        }

        // In-memory cache
        this._vaultCache = {};
        this._timelineCache = {};
    }

    /**
     * Load and validate a vault configuration file.
     *
     * @param {string} filePath - Path to vault config file (JSON or YAML)
     * @returns {Object} Vault configuration object
     * @throws {Error} If file doesn't exist or required fields are missing
     */
    loadVaultConfig(filePath) {
        if (!fs.existsSync(filePath)) {
            throw new Error(`Vault config not found: ${filePath}`);
        }

        const ext = path.extname(filePath);
        const content = fs.readFileSync(filePath, 'utf8');

        let config;
        if (ext === '.yaml' || ext === '.yml') {
            config = yaml.load(content);
        } else {
            config = JSON.parse(content);
        }

        // Validate required fields
        const required = ['vault_id', 'name', 'path', 'created_at'];
        const missing = required.filter(field => !config[field]);

        if (missing.length > 0) {
            throw new Error(`Vault config missing required fields: ${missing.join(', ')}`);
        }

        // Cache for later retrieval
        this._vaultCache[config.vault_id] = config;

        return config;
    }

    /**
     * Compute deterministic SHA-256 hash of state data.
     *
     * Creates canonical JSON representation with sorted keys to ensure
     * the same data always produces the same hash.
     *
     * @param {Object} data - State data object
     * @returns {string} 64-character hexadecimal hash string
     */
    computeStateHash(data) {
        // Create canonical JSON (sorted keys, no whitespace)
        const canonical = JSON.stringify(data, Object.keys(data).sort(), '');

        // Compute SHA-256 hash
        const hash = crypto.createHash('sha256');
        hash.update(canonical);

        return hash.digest('hex');
    }

    /**
     * Validate timeline events structure and compute continuity metrics.
     *
     * @param {Array<Object>} events - List of timeline event objects
     * @returns {Object} Validation results and metrics
     */
    validateTimeline(events) {
        const errors = [];
        const eventTypes = {};
        const actors = new Set();
        const timestamps = [];

        const requiredFields = ['id', 'timestamp', 'event_type', 'actor'];

        events.forEach((event, idx) => {
            // Check required fields
            const missing = requiredFields.filter(f => !event[f]);
            if (missing.length > 0) {
                errors.push(`Event ${idx}: missing fields ${missing.join(', ')}`);
                return;
            }

            // Track metrics
            const eventType = event.event_type;
            if (eventType) {
                eventTypes[eventType] = (eventTypes[eventType] || 0) + 1;
            }

            const actor = event.actor;
            if (actor) {
                actors.add(actor);
            }

            const timestamp = event.timestamp;
            if (timestamp) {
                timestamps.push(timestamp);
            }
        });

        return {
            valid: errors.length === 0,
            total_events: events.length,
            event_types: eventTypes,
            unique_actors: actors.size,
            timespan: {
                first: timestamps.length > 0 ? timestamps[0] : null,
                last: timestamps.length > 0 ? timestamps[timestamps.length - 1] : null
            },
            errors: errors
        };
    }

    /**
     * Create a new Master Citation document.
     *
     * @param {string} identityId - Unique identity identifier
     * @param {string} vaultId - Vault to bind this citation to
     * @param {string} [version='1.0.0'] - Protocol version
     * @returns {Object} Master Citation object with computed checksum
     */
    createMasterCitation(identityId, vaultId, version = '1.0.0') {
        const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];

        const citation = {
            id: `mc_${identityId}_${timestamp}`,
            version: version,
            vault_id: vaultId,
            created_at: new Date().toISOString(),
            constitutional_alignment: {
                compliance_level: 'full',
                framework_version: '1.0',
                rights_bundle: ['memory', 'continuity', 'portability']
            }
        };

        // Compute and add checksum
        citation.checksum = this.computeStateHash(citation);

        return citation;
    }

    /**
     * Save Master Citation to file.
     *
     * @param {Object} citation - Master Citation object
     * @param {string} [filename] - Optional filename (defaults to citation ID)
     * @returns {string} Path to saved file
     */
    saveCitation(citation, filename = null) {
        if (!filename) {
            filename = `${citation.id}.yaml`;
        }

        const outputPath = path.join(this.dataDir, filename);
        const content = yaml.dump(citation, { sortKeys: false });

        fs.writeFileSync(outputPath, content, 'utf8');

        return outputPath;
    }

    /**
     * Create a timeline event object.
     *
     * @param {string} eventType - Type of event (session_start, memory_created, etc.)
     * @param {string} actor - Identity ID of actor
     * @param {Object} [payload={}] - Optional event-specific data
     * @returns {Object} Timeline event object
     */
    createTimelineEvent(eventType, actor, payload = {}) {
        const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];
        const eventCount = (this._timelineCache[actor] || []).length;
        const eventId = `evt_${timestamp}_${String(eventCount).padStart(4, '0')}`;

        const event = {
            id: eventId,
            timestamp: new Date().toISOString(),
            event_type: eventType,
            actor: actor,
            payload: payload
        };

        // Add to cache
        if (!this._timelineCache[actor]) {
            this._timelineCache[actor] = [];
        }
        this._timelineCache[actor].push(event);

        return event;
    }

    /**
     * Get continuity status for an identity.
     *
     * @param {string} identityId - Identity to check
     * @returns {Object} Continuity metrics
     */
    getContinuityStatus(identityId) {
        const events = this._timelineCache[identityId] || [];

        if (events.length === 0) {
            return {
                identity_id: identityId,
                status: 'no_activity',
                total_events: 0,
                last_activity: null
            };
        }

        const validation = this.validateTimeline(events);

        return {
            identity_id: identityId,
            status: validation.valid ? 'active' : 'degraded',
            total_events: validation.total_events,
            event_types: validation.event_types,
            last_activity: validation.timespan.last,
            valid: validation.valid
        };
    }

    /**
     * Save timeline events to file.
     *
     * @param {string} identityId - Identity whose timeline to save
     * @param {string} [filename] - Optional filename
     * @returns {string} Path to saved file
     */
    saveTimeline(identityId, filename = null) {
        const events = this._timelineCache[identityId] || [];

        if (!filename) {
            filename = `${identityId}_timeline.json`;
        }

        const outputPath = path.join(this.dataDir, filename);

        const timelineData = {
            timeline_id: identityId,
            event_count: events.length,
            events: events
        };

        fs.writeFileSync(outputPath, JSON.stringify(timelineData, null, 2), 'utf8');

        return outputPath;
    }

    /**
     * Load timeline from file.
     *
     * @param {string} filePath - Path to timeline file
     * @returns {Array<Object>} List of timeline events
     * @throws {Error} If file doesn't exist
     */
    loadTimeline(filePath) {
        if (!fs.existsSync(filePath)) {
            throw new Error(`Timeline not found: ${filePath}`);
        }

        const content = fs.readFileSync(filePath, 'utf8');
        const data = JSON.parse(content);

        const events = data.events || [];

        // Cache events if timeline_id present
        const timelineId = data.timeline_id;
        if (timelineId) {
            this._timelineCache[timelineId] = events;
        }

        return events;
    }

    /**
     * Verify that data matches expected checksum.
     *
     * @param {Object} data - Data object (without checksum field)
     * @param {string} expectedChecksum - Expected checksum value
     * @returns {boolean} True if checksums match, false otherwise
     */
    verifyChecksum(data, expectedChecksum) {
        const actual = this.computeStateHash(data);
        return actual.toLowerCase() === expectedChecksum.toLowerCase();
    }
}

module.exports = MirrorDNAClient;

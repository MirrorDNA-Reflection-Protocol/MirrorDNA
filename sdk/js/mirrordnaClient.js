/**
 * MirrorDNA Developer SDK - JavaScript Client
 *
 * Simple, local-only client for MirrorDNA protocol operations.
 * Provides easy-to-use interface for vault config loading, state hashing, and timeline validation.
 *
 * This SDK is designed for:
 * - Local development and testing
 * - Understanding MirrorDNA concepts
 * - Building simple Node.js integrations
 *
 * For production use, see the full TypeScript SDK in ../javascript/
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

/**
 * Simple MirrorDNA client for local operations.
 *
 * Features:
 * - Load and validate vault configurations
 * - Compute deterministic state hashes for directories
 * - Validate timeline JSON/YAML files
 *
 * All operations are local-only using Node.js built-in modules.
 */
class MirrorDNAClient {
    constructor() {
        this.lastVaultConfig = null;
        this.lastStateHash = null;
    }

    /**
     * Load and validate a vault configuration file.
     *
     * @param {string} filePath - Path to vault config file (JSON or YAML)
     * @returns {Object} Vault configuration object
     * @throws {Error} If file doesn't exist or config is invalid
     *
     * @example
     * const client = new MirrorDNAClient();
     * const config = client.loadVaultConfig('vault.json');
     * console.log(config.vault_id);
     */
    loadVaultConfig(filePath) {
        if (!fs.existsSync(filePath)) {
            throw new Error(`Vault config not found: ${filePath}`);
        }

        // Read file
        const content = fs.readFileSync(filePath, 'utf8');
        let data;

        // Parse based on extension
        const ext = path.extname(filePath).toLowerCase();
        if (ext === '.yaml' || ext === '.yml') {
            // For YAML, try to use js-yaml if available, otherwise throw
            try {
                const yaml = require('js-yaml');
                data = yaml.load(content);
            } catch (e) {
                throw new Error('js-yaml required for YAML files. Install with: npm install js-yaml');
            }
        } else {
            data = JSON.parse(content);
        }

        // Basic validation
        const requiredFields = ['vault_id', 'name', 'path', 'created_at'];
        const missing = requiredFields.filter(field => !(field in data));

        if (missing.length > 0) {
            throw new Error(`Vault config missing required fields: ${missing.join(', ')}`);
        }

        this.lastVaultConfig = data;
        return data;
    }

    /**
     * Compute deterministic SHA-256 hash of directory contents.
     *
     * Creates a hash based on file paths and contents in alphabetical order.
     * Useful for detecting changes in vault state.
     *
     * @param {string} directory - Path to directory to hash
     * @param {string[]} ignorePatterns - Optional patterns to ignore
     * @returns {string} Hexadecimal SHA-256 hash string
     * @throws {Error} If directory doesn't exist
     *
     * @example
     * const client = new MirrorDNAClient();
     * const hash1 = client.computeStateHash('./my_vault');
     * // ... make changes ...
     * const hash2 = client.computeStateHash('./my_vault');
     * if (hash1 !== hash2) {
     *     console.log('Vault state changed!');
     * }
     */
    computeStateHash(directory, ignorePatterns = null) {
        if (!fs.existsSync(directory)) {
            throw new Error(`Directory not found: ${directory}`);
        }

        const stats = fs.statSync(directory);
        if (!stats.isDirectory()) {
            throw new Error(`Path is not a directory: ${directory}`);
        }

        // Default ignore patterns
        if (!ignorePatterns) {
            ignorePatterns = ['.git', 'node_modules', '__pycache__', '.DS_Store', '.pyc'];
        }

        // Collect all file hashes
        const fileHashes = [];
        this._walkDirectory(directory, directory, fileHashes, ignorePatterns);

        // Sort for determinism
        fileHashes.sort();

        // Compute final hash
        const combined = fileHashes.join('\n');
        const hash = crypto.createHash('sha256').update(combined).digest('hex');

        this.lastStateHash = hash;
        return hash;
    }

    /**
     * Recursively walk directory and collect file hashes.
     * @private
     */
    _walkDirectory(baseDir, currentDir, fileHashes, ignorePatterns) {
        const entries = fs.readdirSync(currentDir);

        for (const entry of entries) {
            // Check if should ignore
            if (this._shouldIgnore(entry, ignorePatterns)) {
                continue;
            }

            const fullPath = path.join(currentDir, entry);
            const stats = fs.statSync(fullPath);

            if (stats.isDirectory()) {
                this._walkDirectory(baseDir, fullPath, fileHashes, ignorePatterns);
            } else if (stats.isFile()) {
                try {
                    // Compute file hash
                    const content = fs.readFileSync(fullPath);
                    const fileHash = crypto.createHash('sha256').update(content).digest('hex');

                    // Get relative path
                    const relativePath = path.relative(baseDir, fullPath);

                    // Add to list
                    fileHashes.push(`${relativePath}:${fileHash}`);
                } catch (e) {
                    // Skip files that can't be read
                    continue;
                }
            }
        }
    }

    /**
     * Check if filename/dirname matches any ignore pattern.
     * @private
     */
    _shouldIgnore(name, patterns) {
        for (const pattern of patterns) {
            if (pattern.startsWith('*')) {
                if (name.endsWith(pattern.substring(1))) {
                    return true;
                }
            } else if (name.includes(pattern)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Validate timeline file structure and return summary.
     *
     * Checks that timeline file contains required fields and valid event structure.
     *
     * @param {string} filePath - Path to timeline file (JSON or YAML)
     * @returns {Object} Validation results with timeline summary
     *
     * @example
     * const client = new MirrorDNAClient();
     * const result = client.validateTimeline('timeline.json');
     * if (result.valid) {
     *     console.log(`Timeline valid with ${result.event_count} events`);
     * }
     */
    validateTimeline(filePath) {
        const errors = [];

        if (!fs.existsSync(filePath)) {
            return {
                valid: false,
                errors: [`File not found: ${filePath}`]
            };
        }

        // Load timeline file
        let data;
        try {
            const content = fs.readFileSync(filePath, 'utf8');
            const ext = path.extname(filePath).toLowerCase();

            if (ext === '.yaml' || ext === '.yml') {
                try {
                    const yaml = require('js-yaml');
                    data = yaml.load(content);
                } catch (e) {
                    return {
                        valid: false,
                        errors: ['js-yaml required for YAML files']
                    };
                }
            } else {
                data = JSON.parse(content);
            }
        } catch (e) {
            return {
                valid: false,
                errors: [`Failed to parse file: ${e.message}`]
            };
        }

        // Extract events
        let events, timelineId;
        if (Array.isArray(data)) {
            events = data;
            timelineId = 'unknown';
        } else if (typeof data === 'object') {
            events = data.events || [];
            timelineId = data.timeline_id || 'unknown';
        } else {
            return {
                valid: false,
                errors: ["Timeline file must be an array or object with 'events' key"]
            };
        }

        // Validate event structure
        const requiredEventFields = ['id', 'timestamp', 'event_type', 'actor'];

        events.forEach((event, i) => {
            if (typeof event !== 'object' || event === null) {
                errors.push(`Event ${i} is not an object`);
                return;
            }

            const missing = requiredEventFields.filter(field => !(field in event));
            if (missing.length > 0) {
                errors.push(`Event ${i} missing fields: ${missing.join(', ')}`);
            }
        });

        // Build summary
        const result = {
            valid: errors.length === 0,
            event_count: events.length,
            timeline_id: timelineId,
            errors: errors
        };

        if (events.length > 0) {
            result.first_event = events[0].timestamp || 'unknown';
            result.last_event = events[events.length - 1].timestamp || 'unknown';
        }

        return result;
    }

    /**
     * Compute deterministic SHA-256 checksum for object data.
     *
     * Uses canonical JSON serialization (sorted keys) for determinism.
     *
     * @param {Object} data - Object to hash
     * @returns {string} Hexadecimal SHA-256 hash string
     *
     * @example
     * const client = new MirrorDNAClient();
     * const checksum = client.computeDataChecksum({id: 'test', value: 42});
     */
    computeDataChecksum(data) {
        // Create canonical JSON (sorted keys)
        const canonicalJson = JSON.stringify(data, Object.keys(data).sort());
        return crypto.createHash('sha256').update(canonicalJson).digest('hex');
    }

    /**
     * Get continuity status summary for vault and timeline.
     *
     * Convenience method that combines vault config, state hash, and timeline validation.
     *
     * @param {string} vaultPath - Optional path to vault config
     * @param {string} timelinePath - Optional path to timeline file
     * @returns {Object} Continuity status information
     *
     * @example
     * const client = new MirrorDNAClient();
     * const status = client.getContinuityStatus({
     *     vaultPath: 'vault.json',
     *     timelinePath: 'timeline.json'
     * });
     * console.log(`Vault: ${status.vault_id}, Events: ${status.event_count}`);
     */
    getContinuityStatus({ vaultPath = null, timelinePath = null } = {}) {
        const status = {
            timestamp: new Date().toISOString(),
            vault_loaded: false,
            timeline_valid: false
        };

        if (vaultPath) {
            try {
                const vault = this.loadVaultConfig(vaultPath);
                status.vault_loaded = true;
                status.vault_id = vault.vault_id;
                status.vault_name = vault.name;
            } catch (e) {
                status.vault_error = e.message;
            }
        }

        if (timelinePath) {
            const result = this.validateTimeline(timelinePath);
            status.timeline_valid = result.valid;
            status.event_count = result.event_count || 0;
            status.timeline_errors = result.errors || [];
        }

        // Compute state hash if we have a vault
        if (vaultPath && status.vault_loaded && this.lastVaultConfig) {
            try {
                const vaultDir = this.lastVaultConfig.path;
                if (fs.existsSync(vaultDir)) {
                    status.state_hash = this.computeStateHash(vaultDir);
                }
            } catch (e) {
                status.state_hash_error = e.message;
            }
        }

        return status;
    }
}

// Convenience functions for quick operations

/**
 * Quick utility to hash a directory.
 *
 * @param {string} directory - Path to directory
 * @returns {string} SHA-256 hash string
 */
function quickHashDirectory(directory) {
    const client = new MirrorDNAClient();
    return client.computeStateHash(directory);
}

/**
 * Quick utility to check if timeline is valid.
 *
 * @param {string} filePath - Path to timeline file
 * @returns {boolean} True if valid, false otherwise
 */
function quickValidateTimeline(filePath) {
    const client = new MirrorDNAClient();
    const result = client.validateTimeline(filePath);
    return result.valid;
}

// Exports
module.exports = {
    MirrorDNAClient,
    quickHashDirectory,
    quickValidateTimeline
};

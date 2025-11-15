// FEU Enforcement: Master Citation v15.2
// FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

/**
 * Identity management for MirrorDNA
 */

import { Identity, IdentityType, StorageAdapter } from './types';
import { CryptoUtils } from './crypto';
import { MemoryStorage } from './storage';

export class IdentityManager {
  private storage: StorageAdapter;
  private crypto: typeof CryptoUtils;

  constructor(storage?: StorageAdapter) {
    this.storage = storage || new MemoryStorage();
    this.crypto = CryptoUtils;
  }

  /**
   * Generate a unique identity ID
   */
  private generateIdentityId(identityType: IdentityType): string {
    const typePrefixMap: Record<IdentityType, string> = {
      user: 'usr',
      agent: 'agt',
      system: 'sys'
    };

    const prefix = typePrefixMap[identityType];
    const suffix = this.randomHex(8);

    return `mdna_${prefix}_${suffix}`;
  }

  private randomHex(length: number): string {
    const bytes = Math.ceil(length / 2);
    const hex = Array.from(crypto.getRandomValues(new Uint8Array(bytes)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
    return hex.substring(0, length);
  }

  /**
   * Create a new identity
   */
  async createIdentity(
    identityType: IdentityType,
    metadata?: Identity['metadata']
  ): Promise<Identity & { _privateKey: string }> {
    const identityId = this.generateIdentityId(identityType);
    const { publicKey, privateKey } = this.crypto.generateKeypair();

    const identity: Identity = {
      identity_id: identityId,
      identity_type: identityType,
      created_at: new Date().toISOString(),
      public_key: publicKey
    };

    if (metadata) {
      identity.metadata = metadata;
    }

    await this.storage.create('identities', identity);

    return {
      ...identity,
      _privateKey: privateKey
    };
  }

  /**
   * Get an identity by ID
   */
  async getIdentity(identityId: string): Promise<Identity | null> {
    return await this.storage.read('identities', identityId);
  }

  /**
   * Sign a claim with an identity's private key
   */
  signClaim(identityId: string, claim: string, privateKey: string): string {
    const message = `${identityId}:${claim}`;
    return this.crypto.sign(message, privateKey);
  }

  /**
   * Verify a claim signature
   */
  async verifyClaim(identityId: string, claim: string, signature: string): Promise<boolean> {
    const identity = await this.getIdentity(identityId);
    if (!identity) {
      return false;
    }

    const message = `${identityId}:${claim}`;
    return this.crypto.verify(message, signature, identity.public_key);
  }
}

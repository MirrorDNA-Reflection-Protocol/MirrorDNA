// FEU Enforcement: Master Citation v15.2
// FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

/**
 * Cryptographic utilities for MirrorDNA
 */

import * as nacl from 'tweetnacl';
import { createHash } from 'crypto';

export class CryptoUtils {
  /**
   * Generate an Ed25519 keypair
   */
  static generateKeypair(): { publicKey: string; privateKey: string } {
    const keypair = nacl.sign.keyPair();

    return {
      publicKey: Buffer.from(keypair.publicKey).toString('base64'),
      privateKey: Buffer.from(keypair.secretKey).toString('base64')
    };
  }

  /**
   * Sign a message with a private key
   */
  static sign(message: string, privateKey: string): string {
    const messageBytes = Buffer.from(message, 'utf8');
    const privateKeyBytes = Buffer.from(privateKey, 'base64');

    const signature = nacl.sign.detached(messageBytes, privateKeyBytes);

    return Buffer.from(signature).toString('base64');
  }

  /**
   * Verify a message signature
   */
  static verify(message: string, signature: string, publicKey: string): boolean {
    try {
      const messageBytes = Buffer.from(message, 'utf8');
      const signatureBytes = Buffer.from(signature, 'base64');
      const publicKeyBytes = Buffer.from(publicKey, 'base64');

      return nacl.sign.detached.verify(messageBytes, signatureBytes, publicKeyBytes);
    } catch {
      return false;
    }
  }

  /**
   * Hash data using SHA-256
   */
  static hash(data: string | Record<string, any>): string {
    const dataStr = typeof data === 'string' ? data : JSON.stringify(data);
    return createHash('sha256').update(dataStr).digest('hex');
  }
}

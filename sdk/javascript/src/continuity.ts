/**
 * Continuity tracking for MirrorDNA sessions
 */

import { Session, StorageAdapter } from './types';
import { MemoryStorage } from './storage';

export class ContinuityTracker {
  private storage: StorageAdapter;

  constructor(storage?: StorageAdapter) {
    this.storage = storage || new MemoryStorage();
  }

  /**
   * Generate a unique session ID
   */
  private generateSessionId(): string {
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];
    const suffix = this.randomHex(4);
    return `sess_${timestamp}_${suffix}`;
  }

  private randomHex(length: number): string {
    const bytes = Math.ceil(length / 2);
    const hex = Array.from(crypto.getRandomValues(new Uint8Array(bytes)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
    return hex.substring(0, length);
  }

  /**
   * Create a new session
   */
  async createSession(
    agentId: string,
    userId: string,
    parentSessionId: string | null = null,
    contextMetadata?: Session['context_metadata']
  ): Promise<Session> {
    const sessionId = this.generateSessionId();

    const session: Session = {
      session_id: sessionId,
      parent_session_id: parentSessionId,
      agent_id: agentId,
      user_id: userId,
      started_at: new Date().toISOString(),
      ended_at: null
    };

    if (contextMetadata) {
      session.context_metadata = contextMetadata;
    }

    await this.storage.create('sessions', session);
    return session;
  }

  /**
   * Get a session by ID
   */
  async getSession(sessionId: string): Promise<Session | null> {
    return await this.storage.read('sessions', sessionId);
  }

  /**
   * End a session
   */
  async endSession(sessionId: string, finalState?: any): Promise<Session | null> {
    const updates: Partial<Session> = {
      ended_at: new Date().toISOString()
    };

    if (finalState) {
      const session = await this.getSession(sessionId);
      if (session) {
        updates.context_metadata = {
          ...session.context_metadata,
          final_state: finalState
        };
      }
    }

    return await this.storage.update('sessions', sessionId, updates);
  }

  /**
   * Get the full lineage (ancestor chain) of a session
   */
  async getSessionLineage(sessionId: string): Promise<Session[]> {
    const lineage: Session[] = [];
    let currentSessionId: string | null = sessionId;

    while (currentSessionId) {
      const session = await this.getSession(currentSessionId);
      if (!session) {
        break;
      }

      lineage.unshift(session); // Prepend to list
      currentSessionId = session.parent_session_id;
    }

    return lineage;
  }

  /**
   * Get aggregated context from session lineage
   */
  async getContext(sessionId: string): Promise<any> {
    const lineage = await this.getSessionLineage(sessionId);

    return {
      session_count: lineage.length,
      sessions: lineage.map(session => ({
        session_id: session.session_id,
        started_at: session.started_at,
        ended_at: session.ended_at,
        metadata: session.context_metadata || {}
      }))
    };
  }

  /**
   * Check if a session exists
   */
  async sessionExists(sessionId: string): Promise<boolean> {
    const session = await this.getSession(sessionId);
    return session !== null;
  }
}

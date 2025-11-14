/**
 * Memory management for MirrorDNA
 */

import { Memory, MemoryTier, StorageAdapter } from './types';
import { MemoryStorage } from './storage';

export class MemoryManager {
  private storage: StorageAdapter;

  constructor(storage?: StorageAdapter) {
    this.storage = storage || new MemoryStorage();
  }

  /**
   * Generate a unique memory ID
   */
  private generateMemoryId(): string {
    const timestamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0];
    const suffix = this.randomHex(4);
    return `mem_${timestamp}_${suffix}`;
  }

  private randomHex(length: number): string {
    const bytes = Math.ceil(length / 2);
    const hex = Array.from(crypto.getRandomValues(new Uint8Array(bytes)))
      .map(b => b.toString(16).padStart(2, '0'))
      .join('');
    return hex.substring(0, length);
  }

  /**
   * Write a new memory
   */
  async writeMemory(
    content: string | Record<string, any>,
    tier: MemoryTier,
    sessionId: string,
    agentId: string,
    userId: string,
    metadata?: Memory['metadata']
  ): Promise<Memory> {
    const validTiers: MemoryTier[] = ['short_term', 'long_term', 'episodic'];
    if (!validTiers.includes(tier)) {
      throw new Error(`Invalid tier: ${tier}`);
    }

    const memoryId = this.generateMemoryId();

    const memory: Memory = {
      memory_id: memoryId,
      tier,
      content,
      source: {
        session_id: sessionId,
        timestamp: new Date().toISOString(),
        agent_id: agentId,
        user_id: userId
      }
    };

    if (metadata) {
      memory.metadata = metadata;
    }

    await this.storage.create('memories', memory);
    return memory;
  }

  /**
   * Read memories with optional filters
   */
  async readMemory(
    tier?: MemoryTier,
    filters?: any,
    limit: number = 100
  ): Promise<Memory[]> {
    const queryFilters = filters || {};

    if (tier) {
      queryFilters.tier = tier;
    }

    return await this.storage.query('memories', queryFilters, limit);
  }

  /**
   * Get a specific memory by ID
   */
  async getMemory(memoryId: string): Promise<Memory | null> {
    return await this.storage.read('memories', memoryId);
  }

  /**
   * Update a memory record
   */
  async updateMemory(memoryId: string, updates: any): Promise<Memory | null> {
    return await this.storage.update('memories', memoryId, updates);
  }

  /**
   * Search memories by content (simple text search)
   */
  async searchMemory(
    query: string,
    tier?: MemoryTier,
    filters?: any,
    limit: number = 10
  ): Promise<Memory[]> {
    const memories = await this.readMemory(tier, filters, 1000);
    const queryLower = query.toLowerCase();

    const matching = memories.filter(memory => {
      const content = typeof memory.content === 'string'
        ? memory.content
        : JSON.stringify(memory.content);

      return content.toLowerCase().includes(queryLower);
    });

    // Sort by timestamp (most recent first)
    matching.sort((a, b) => {
      return new Date(b.source.timestamp).getTime() - new Date(a.source.timestamp).getTime();
    });

    return matching.slice(0, limit);
  }

  /**
   * Archive a memory
   */
  async archiveMemory(memoryId: string): Promise<Memory | null> {
    const memory = await this.getMemory(memoryId);
    if (!memory) {
      return null;
    }

    const metadata = {
      ...memory.metadata,
      archived: true,
      archived_at: new Date().toISOString()
    };

    return await this.updateMemory(memoryId, { metadata });
  }

  /**
   * Increment the access count for a memory
   */
  async incrementAccessCount(memoryId: string): Promise<Memory | null> {
    const memory = await this.getMemory(memoryId);
    if (!memory) {
      return null;
    }

    const accessCount = (memory.metadata?.access_count || 0) + 1;
    const metadata = {
      ...memory.metadata,
      access_count: accessCount,
      last_accessed: new Date().toISOString()
    };

    return await this.updateMemory(memoryId, { metadata });
  }
}

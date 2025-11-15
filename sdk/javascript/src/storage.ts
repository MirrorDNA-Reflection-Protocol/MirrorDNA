// FEU Enforcement: Master Citation v15.2
// FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

/**
 * Storage layer for MirrorDNA
 */

import { StorageAdapter } from './types';
import { promises as fs } from 'fs';
import * as path from 'path';
import * as os from 'os';

export class MemoryStorage implements StorageAdapter {
  private data: Map<string, Map<string, any>>;

  constructor() {
    this.data = new Map();
  }

  async create(collection: string, record: any): Promise<string> {
    if (!this.data.has(collection)) {
      this.data.set(collection, new Map());
    }

    const collectionData = this.data.get(collection)!;
    const idField = this.getIdField(collection);
    const recordId = record[idField];

    if (!recordId) {
      throw new Error(`Record must contain '${idField}' field`);
    }

    if (collectionData.has(recordId)) {
      throw new Error(`Record with ID '${recordId}' already exists`);
    }

    collectionData.set(recordId, record);
    return recordId;
  }

  async read(collection: string, recordId: string): Promise<any | null> {
    const collectionData = this.data.get(collection);
    return collectionData?.get(recordId) || null;
  }

  async update(collection: string, recordId: string, updates: any): Promise<any | null> {
    const collectionData = this.data.get(collection);
    if (!collectionData || !collectionData.has(recordId)) {
      return null;
    }

    const record = collectionData.get(recordId);
    const updated = { ...record, ...updates };
    collectionData.set(recordId, updated);
    return updated;
  }

  async delete(collection: string, recordId: string): Promise<boolean> {
    const collectionData = this.data.get(collection);
    if (!collectionData) {
      return false;
    }
    return collectionData.delete(recordId);
  }

  async query(collection: string, filters?: any, limit: number = 100): Promise<any[]> {
    const collectionData = this.data.get(collection);
    if (!collectionData) {
      return [];
    }

    let results = Array.from(collectionData.values());

    if (filters) {
      results = results.filter(record => {
        return Object.entries(filters).every(([key, value]) => {
          const recordValue = this.getNestedValue(record, key);
          return recordValue === value;
        });
      });
    }

    return results.slice(0, limit);
  }

  private getIdField(collection: string): string {
    const idFieldMap: Record<string, string> = {
      identities: 'identity_id',
      sessions: 'session_id',
      memories: 'memory_id',
      agent_dna: 'agent_dna_id'
    };
    return idFieldMap[collection] || 'id';
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }
}

export class JSONFileStorage implements StorageAdapter {
  private storageDir: string;

  constructor(storageDir?: string) {
    this.storageDir = storageDir || path.join(os.homedir(), '.mirrordna', 'data');
  }

  private async ensureDir(): Promise<void> {
    await fs.mkdir(this.storageDir, { recursive: true });
  }

  private getCollectionFile(collection: string): string {
    return path.join(this.storageDir, `${collection}.json`);
  }

  private async loadCollection(collection: string): Promise<Record<string, any>> {
    const filePath = this.getCollectionFile(collection);
    try {
      const data = await fs.readFile(filePath, 'utf8');
      return JSON.parse(data);
    } catch {
      return {};
    }
  }

  private async saveCollection(collection: string, data: Record<string, any>): Promise<void> {
    await this.ensureDir();
    const filePath = this.getCollectionFile(collection);
    await fs.writeFile(filePath, JSON.stringify(data, null, 2));
  }

  private getIdField(collection: string): string {
    const idFieldMap: Record<string, string> = {
      identities: 'identity_id',
      sessions: 'session_id',
      memories: 'memory_id',
      agent_dna: 'agent_dna_id'
    };
    return idFieldMap[collection] || 'id';
  }

  async create(collection: string, record: any): Promise<string> {
    const data = await this.loadCollection(collection);
    const idField = this.getIdField(collection);
    const recordId = record[idField];

    if (!recordId) {
      throw new Error(`Record must contain '${idField}' field`);
    }

    if (data[recordId]) {
      throw new Error(`Record with ID '${recordId}' already exists`);
    }

    data[recordId] = record;
    await this.saveCollection(collection, data);
    return recordId;
  }

  async read(collection: string, recordId: string): Promise<any | null> {
    const data = await this.loadCollection(collection);
    return data[recordId] || null;
  }

  async update(collection: string, recordId: string, updates: any): Promise<any | null> {
    const data = await this.loadCollection(collection);
    if (!data[recordId]) {
      return null;
    }

    data[recordId] = { ...data[recordId], ...updates };
    await this.saveCollection(collection, data);
    return data[recordId];
  }

  async delete(collection: string, recordId: string): Promise<boolean> {
    const data = await this.loadCollection(collection);
    if (!data[recordId]) {
      return false;
    }

    delete data[recordId];
    await this.saveCollection(collection, data);
    return true;
  }

  async query(collection: string, filters?: any, limit: number = 100): Promise<any[]> {
    const data = await this.loadCollection(collection);
    let results = Object.values(data);

    if (filters) {
      results = results.filter(record => {
        return Object.entries(filters).every(([key, value]) => {
          const recordValue = this.getNestedValue(record, key);
          return recordValue === value;
        });
      });
    }

    return results.slice(0, limit);
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }
}

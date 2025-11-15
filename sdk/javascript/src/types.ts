// FEU Enforcement: Master Citation v15.2
// FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

/**
 * MirrorDNA TypeScript type definitions
 */

export type IdentityType = 'user' | 'agent' | 'system';

export type MemoryTier = 'short_term' | 'long_term' | 'episodic';

export interface Identity {
  identity_id: string;
  identity_type: IdentityType;
  created_at: string;
  public_key: string;
  metadata?: {
    name?: string;
    description?: string;
    version?: string;
    custom?: Record<string, any>;
  };
}

export interface Session {
  session_id: string;
  parent_session_id: string | null;
  agent_id: string;
  user_id: string;
  started_at: string;
  ended_at: string | null;
  context_metadata?: {
    restored_from?: string;
    topic?: string;
    tags?: string[];
    prior_memories_count?: number;
    custom?: Record<string, any>;
  };
}

export interface MemorySource {
  session_id: string;
  timestamp: string;
  agent_id: string;
  user_id: string;
}

export interface Memory {
  memory_id: string;
  tier: MemoryTier;
  content: string | Record<string, any>;
  source: MemorySource;
  metadata?: {
    tags?: string[];
    relevance_score?: number;
    access_count?: number;
    last_accessed?: string;
    embedding_vector?: number[];
    custom?: Record<string, any>;
  };
}

export interface AgentDNA {
  agent_dna_id: string;
  agent_id: string;
  version: string;
  personality_traits: {
    tone: string;
    style: string;
    values: string[];
    custom?: Record<string, any>;
  };
  behavioral_constraints: string[];
  capabilities: string[];
  constitutional_alignment?: {
    framework?: string;
    safety_rules?: string[];
    compliance_level?: 'full' | 'partial' | 'custom';
  };
}

export interface ValidationResult {
  is_valid: boolean;
  errors: string[];
  schema_name?: string;
}

export interface StorageAdapter {
  create(collection: string, record: any): Promise<string>;
  read(collection: string, record_id: string): Promise<any | null>;
  update(collection: string, record_id: string, updates: any): Promise<any | null>;
  delete(collection: string, record_id: string): Promise<boolean>;
  query(collection: string, filters?: any, limit?: number): Promise<any[]>;
}

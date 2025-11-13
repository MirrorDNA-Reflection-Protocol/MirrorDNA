"""
Memory management for MirrorDNA.
"""

import secrets
from datetime import datetime
from typing import Dict, Any, Optional, List, Union

from .validator import validate_schema
from .storage import StorageAdapter, JSONFileStorage


class MemoryManager:
    """Manages memory records across tiers."""

    def __init__(self, storage: Optional[StorageAdapter] = None):
        """
        Initialize memory manager.

        Args:
            storage: Storage adapter (uses JSONFileStorage if None)
        """
        self.storage = storage or JSONFileStorage()

    def _generate_memory_id(self) -> str:
        """
        Generate a unique memory ID.

        Returns:
            Generated memory ID
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        suffix = secrets.token_hex(4)  # 8 characters

        return f"mem_{timestamp}_{suffix}"

    def write_memory(
        self,
        content: Union[str, Dict[str, Any]],
        tier: str,
        session_id: str,
        agent_id: str,
        user_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Write a new memory.

        Args:
            content: Memory content (text or structured data)
            tier: Memory tier (short_term, long_term, episodic)
            session_id: Session where memory was created
            agent_id: Agent that created the memory
            user_id: User associated with the memory
            metadata: Optional metadata (tags, relevance_score, etc.)

        Returns:
            Memory record

        Raises:
            ValueError: If tier is invalid or validation fails
        """
        if tier not in ["short_term", "long_term", "episodic"]:
            raise ValueError(f"Invalid tier: {tier}")

        memory_id = self._generate_memory_id()

        memory = {
            "memory_id": memory_id,
            "tier": tier,
            "content": content,
            "source": {
                "session_id": session_id,
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "agent_id": agent_id,
                "user_id": user_id
            }
        }

        if metadata:
            memory["metadata"] = metadata

        # Validate against schema
        result = validate_schema(memory, "memory")
        if not result.is_valid:
            raise ValueError(f"Memory validation failed: {', '.join(result.errors)}")

        # Store memory
        self.storage.create("memories", memory)

        return memory

    def read_memory(
        self,
        tier: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Read memories with optional filters.

        Args:
            tier: Optional tier filter
            filters: Optional additional filters
            limit: Maximum number of results

        Returns:
            List of memory records
        """
        query_filters = filters or {}

        if tier:
            query_filters["tier"] = tier

        return self.storage.query("memories", query_filters, limit)

    def get_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific memory by ID.

        Args:
            memory_id: Memory ID

        Returns:
            Memory record or None if not found
        """
        return self.storage.read("memories", memory_id)

    def update_memory(
        self,
        memory_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update a memory record.

        Args:
            memory_id: Memory ID
            updates: Fields to update

        Returns:
            Updated memory record or None if not found
        """
        return self.storage.update("memories", memory_id, updates)

    def search_memory(
        self,
        query: str,
        tier: Optional[str] = None,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search memories by content (simple text search).

        Args:
            query: Search query
            tier: Optional tier filter
            filters: Optional additional filters
            limit: Maximum number of results

        Returns:
            List of matching memory records
        """
        # Get all memories matching filters
        memories = self.read_memory(tier, filters, limit=1000)

        # Simple text search (case-insensitive)
        query_lower = query.lower()
        matching = []

        for memory in memories:
            content = memory.get("content", "")

            # Handle both string and dict content
            if isinstance(content, str):
                content_str = content
            else:
                content_str = str(content)

            if query_lower in content_str.lower():
                matching.append(memory)

        # Sort by timestamp (most recent first)
        matching.sort(
            key=lambda m: m["source"]["timestamp"],
            reverse=True
        )

        return matching[:limit]

    def archive_memory(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Archive a memory (mark as archived in metadata).

        Args:
            memory_id: Memory ID

        Returns:
            Updated memory record or None if not found
        """
        memory = self.get_memory(memory_id)
        if not memory:
            return None

        metadata = memory.get("metadata", {})
        metadata["archived"] = True
        metadata["archived_at"] = datetime.utcnow().isoformat() + "Z"

        return self.update_memory(memory_id, {"metadata": metadata})

    def increment_access_count(self, memory_id: str) -> Optional[Dict[str, Any]]:
        """
        Increment the access count for a memory.

        Args:
            memory_id: Memory ID

        Returns:
            Updated memory record or None if not found
        """
        memory = self.get_memory(memory_id)
        if not memory:
            return None

        metadata = memory.get("metadata", {})
        access_count = metadata.get("access_count", 0)
        metadata["access_count"] = access_count + 1
        metadata["last_accessed"] = datetime.utcnow().isoformat() + "Z"

        return self.update_memory(memory_id, {"metadata": metadata})

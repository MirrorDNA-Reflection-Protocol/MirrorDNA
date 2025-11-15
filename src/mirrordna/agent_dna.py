# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Agent DNA management for MirrorDNA.
"""

from typing import Dict, Any, Optional, List

from .validator import validate_schema
from .storage import StorageAdapter, JSONFileStorage


class AgentDNAManager:
    """Manages agent DNA definitions."""

    def __init__(self, storage: Optional[StorageAdapter] = None):
        """
        Initialize agent DNA manager.

        Args:
            storage: Storage adapter (uses JSONFileStorage if None)
        """
        self.storage = storage or JSONFileStorage()

    def _generate_dna_id(self, agent_id: str, version: str) -> str:
        """
        Generate a DNA ID from agent ID and version.

        Args:
            agent_id: Agent identity ID
            version: Semantic version

        Returns:
            Generated DNA ID
        """
        # Extract agent name from ID (e.g., mdna_agt_mirror01 -> mirror01)
        agent_name = agent_id.replace("mdna_agt_", "")

        # Convert version to safe format (e.g., 1.2.3 -> v1_2_3)
        version_safe = version.replace(".", "_")

        return f"dna_{agent_name}_{version_safe}"

    def create_agent_dna(
        self,
        agent_id: str,
        version: str,
        personality_traits: Dict[str, Any],
        behavioral_constraints: List[str],
        capabilities: List[str],
        constitutional_alignment: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new agent DNA record.

        Args:
            agent_id: Associated agent identity ID
            version: Semantic version (e.g., "1.0.0")
            personality_traits: Personality definition
            behavioral_constraints: List of behavior rules
            capabilities: List of agent capabilities
            constitutional_alignment: Optional alignment framework reference

        Returns:
            Agent DNA record

        Raises:
            ValueError: If validation fails
        """
        agent_dna_id = self._generate_dna_id(agent_id, version)

        agent_dna = {
            "agent_dna_id": agent_dna_id,
            "agent_id": agent_id,
            "version": version,
            "personality_traits": personality_traits,
            "behavioral_constraints": behavioral_constraints,
            "capabilities": capabilities
        }

        if constitutional_alignment:
            agent_dna["constitutional_alignment"] = constitutional_alignment

        # Validate against schema
        result = validate_schema(agent_dna, "agent")
        if not result.is_valid:
            raise ValueError(f"Agent DNA validation failed: {', '.join(result.errors)}")

        # Store agent DNA
        self.storage.create("agent_dna", agent_dna)

        return agent_dna

    def get_agent_dna(self, agent_dna_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve agent DNA by ID.

        Args:
            agent_dna_id: Agent DNA ID

        Returns:
            Agent DNA record or None if not found
        """
        return self.storage.read("agent_dna", agent_dna_id)

    def get_agent_dna_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all DNA versions for an agent.

        Args:
            agent_id: Agent identity ID

        Returns:
            List of agent DNA records
        """
        return self.storage.query("agent_dna", {"agent_id": agent_id})

    def get_latest_agent_dna(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the latest DNA version for an agent.

        Args:
            agent_id: Agent identity ID

        Returns:
            Latest agent DNA record or None if not found
        """
        dna_records = self.get_agent_dna_by_agent(agent_id)

        if not dna_records:
            return None

        # Sort by version (assumes semantic versioning)
        def version_key(dna):
            version = dna["version"]
            parts = version.split(".")
            return tuple(int(p) for p in parts)

        dna_records.sort(key=version_key, reverse=True)

        return dna_records[0]

    def update_agent_dna(
        self,
        agent_dna_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Update an agent DNA record.

        Args:
            agent_dna_id: Agent DNA ID
            updates: Fields to update

        Returns:
            Updated agent DNA record or None if not found
        """
        return self.storage.update("agent_dna", agent_dna_id, updates)

    def validate_agent_dna(self, agent_dna: Dict[str, Any]) -> bool:
        """
        Validate an agent DNA record.

        Args:
            agent_dna: Agent DNA record to validate

        Returns:
            True if valid, False otherwise
        """
        result = validate_schema(agent_dna, "agent")
        return result.is_valid

    def get_behavior_constraints(self, agent_dna_id: str) -> List[str]:
        """
        Get behavior constraints for an agent DNA.

        Args:
            agent_dna_id: Agent DNA ID

        Returns:
            List of behavioral constraints
        """
        agent_dna = self.get_agent_dna(agent_dna_id)

        if not agent_dna:
            return []

        return agent_dna.get("behavioral_constraints", [])

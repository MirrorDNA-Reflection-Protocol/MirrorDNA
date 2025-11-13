"""
Reflection engine for agent introspection and meta-cognition.

The reflection engine enables agents to:
- Introspect on their own state and capabilities
- Perform meta-cognitive evaluation
- Track decision rationales
- Monitor behavioral alignment
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum

from .storage import StorageAdapter, JSONFileStorage
from .agent_dna import AgentDNAManager


class ReflectionType(Enum):
    """Types of reflections an agent can perform."""
    DECISION = "decision"  # Reflection on a decision made
    CAPABILITY = "capability"  # Reflection on capabilities
    ALIGNMENT = "alignment"  # Reflection on constitutional alignment
    PERFORMANCE = "performance"  # Reflection on performance
    STATE = "state"  # Reflection on current state
    META = "meta"  # Meta-reflection (reflecting on reflections)


@dataclass
class Reflection:
    """A single reflection record."""
    reflection_id: str
    agent_id: str
    reflection_type: str
    timestamp: str
    context: Dict[str, Any]
    observation: str
    evaluation: Optional[str] = None
    insights: Optional[List[str]] = None
    actions_taken: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class ReflectionEngine:
    """Engine for agent introspection and meta-cognition."""

    def __init__(
        self,
        agent_id: str,
        storage: Optional[StorageAdapter] = None,
        dna_manager: Optional[AgentDNAManager] = None
    ):
        """
        Initialize reflection engine for an agent.

        Args:
            agent_id: Agent identity ID
            storage: Storage adapter
            dna_manager: Agent DNA manager for alignment checks
        """
        self.agent_id = agent_id
        self.storage = storage or JSONFileStorage()
        self.dna_manager = dna_manager or AgentDNAManager(self.storage)
        self._reflection_count = 0

    def _generate_reflection_id(self) -> str:
        """Generate a unique reflection ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self._reflection_count += 1
        return f"refl_{self.agent_id.replace('mdna_agt_', '')}_{timestamp}_{self._reflection_count:04d}"

    async def reflect_on_decision(
        self,
        decision: str,
        context: Dict[str, Any],
        rationale: str,
        constraints_checked: List[str]
    ) -> Reflection:
        """
        Reflect on a decision made by the agent.

        Args:
            decision: The decision made
            context: Context in which decision was made
            rationale: Why this decision was made
            constraints_checked: Behavioral constraints considered

        Returns:
            Reflection record
        """
        reflection_id = self._generate_reflection_id()

        # Check alignment with DNA
        alignment_check = await self._check_alignment(decision, constraints_checked)

        observation = f"Decision: {decision}"
        evaluation = f"Rationale: {rationale}"

        insights = []
        if alignment_check["aligned"]:
            insights.append("Decision aligns with behavioral constraints")
        else:
            insights.append(f"Alignment issues: {', '.join(alignment_check['violations'])}")

        insights.append(f"Constraints considered: {len(constraints_checked)}")

        reflection = Reflection(
            reflection_id=reflection_id,
            agent_id=self.agent_id,
            reflection_type=ReflectionType.DECISION.value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            context=context,
            observation=observation,
            evaluation=evaluation,
            insights=insights,
            metadata={
                "decision": decision,
                "constraints_checked": constraints_checked,
                "alignment": alignment_check
            }
        )

        await self.storage.create("reflections", asdict(reflection))
        return reflection

    async def reflect_on_capability(
        self,
        capability: str,
        usage_context: str,
        success: bool,
        performance_notes: Optional[str] = None
    ) -> Reflection:
        """
        Reflect on use of a capability.

        Args:
            capability: Capability used
            usage_context: Context of usage
            success: Whether usage was successful
            performance_notes: Optional performance observations

        Returns:
            Reflection record
        """
        reflection_id = self._generate_reflection_id()

        observation = f"Used capability: {capability} in context: {usage_context}"
        evaluation = f"Success: {success}"

        insights = []
        if success:
            insights.append(f"Capability '{capability}' performed as expected")
        else:
            insights.append(f"Capability '{capability}' did not meet expectations")

        if performance_notes:
            insights.append(f"Notes: {performance_notes}")

        reflection = Reflection(
            reflection_id=reflection_id,
            agent_id=self.agent_id,
            reflection_type=ReflectionType.CAPABILITY.value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            context={"usage_context": usage_context},
            observation=observation,
            evaluation=evaluation,
            insights=insights,
            metadata={
                "capability": capability,
                "success": success,
                "performance_notes": performance_notes
            }
        )

        await self.storage.create("reflections", asdict(reflection))
        return reflection

    async def reflect_on_state(
        self,
        state_snapshot: Dict[str, Any],
        observations: List[str]
    ) -> Reflection:
        """
        Reflect on current agent state.

        Args:
            state_snapshot: Current state data
            observations: Observations about the state

        Returns:
            Reflection record
        """
        reflection_id = self._generate_reflection_id()

        observation = "State reflection: " + "; ".join(observations)

        insights = []
        insights.append(f"State dimensions captured: {len(state_snapshot.keys())}")
        insights.extend(observations)

        reflection = Reflection(
            reflection_id=reflection_id,
            agent_id=self.agent_id,
            reflection_type=ReflectionType.STATE.value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            context=state_snapshot,
            observation=observation,
            insights=insights,
            metadata={"state_snapshot": state_snapshot}
        )

        await self.storage.create("reflections", asdict(reflection))
        return reflection

    async def meta_reflect(
        self,
        reflection_ids: List[str],
        synthesis: str
    ) -> Reflection:
        """
        Perform meta-reflection on previous reflections.

        Args:
            reflection_ids: IDs of reflections to reflect upon
            synthesis: Synthesized insights from reviewing reflections

        Returns:
            Meta-reflection record
        """
        reflection_id = self._generate_reflection_id()

        observation = f"Meta-reflection on {len(reflection_ids)} prior reflections"
        evaluation = synthesis

        insights = [
            f"Analyzed {len(reflection_ids)} reflections",
            "Synthesis: " + synthesis
        ]

        reflection = Reflection(
            reflection_id=reflection_id,
            agent_id=self.agent_id,
            reflection_type=ReflectionType.META.value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            context={"reflection_ids": reflection_ids},
            observation=observation,
            evaluation=evaluation,
            insights=insights,
            metadata={"source_reflections": reflection_ids}
        )

        await self.storage.create("reflections", asdict(reflection))
        return reflection

    async def get_reflections(
        self,
        reflection_type: Optional[ReflectionType] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Retrieve reflections for this agent.

        Args:
            reflection_type: Optional filter by type
            limit: Maximum number of reflections to return

        Returns:
            List of reflection records
        """
        filters = {"agent_id": self.agent_id}

        if reflection_type:
            filters["reflection_type"] = reflection_type.value

        reflections = await self.storage.query("reflections", filters, limit)

        # Sort by timestamp (most recent first)
        reflections.sort(
            key=lambda r: r.get("timestamp", ""),
            reverse=True
        )

        return reflections

    async def introspect_capabilities(self) -> Dict[str, Any]:
        """
        Introspect on agent's own capabilities.

        Returns:
            Capability introspection data
        """
        # Get latest agent DNA
        dna = self.dna_manager.get_latest_agent_dna(self.agent_id)

        if not dna:
            return {
                "agent_id": self.agent_id,
                "capabilities": [],
                "error": "No DNA found for agent"
            }

        # Get capability usage reflections
        capability_reflections = await self.get_reflections(
            ReflectionType.CAPABILITY,
            limit=50
        )

        capabilities_data = {}
        for capability in dna.get("capabilities", []):
            # Find reflections for this capability
            cap_refs = [
                r for r in capability_reflections
                if r.get("metadata", {}).get("capability") == capability
            ]

            success_count = sum(
                1 for r in cap_refs
                if r.get("metadata", {}).get("success", False)
            )

            capabilities_data[capability] = {
                "usage_count": len(cap_refs),
                "success_count": success_count,
                "success_rate": success_count / len(cap_refs) if cap_refs else 0.0
            }

        return {
            "agent_id": self.agent_id,
            "capabilities": dna.get("capabilities", []),
            "capability_performance": capabilities_data,
            "total_capability_reflections": len(capability_reflections)
        }

    async def _check_alignment(
        self,
        action: str,
        constraints_checked: List[str]
    ) -> Dict[str, Any]:
        """
        Check if an action aligns with agent DNA constraints.

        Args:
            action: Action to check
            constraints_checked: Constraints that were considered

        Returns:
            Alignment check result
        """
        dna = self.dna_manager.get_latest_agent_dna(self.agent_id)

        if not dna:
            return {
                "aligned": True,
                "violations": [],
                "note": "No DNA constraints to check"
            }

        all_constraints = dna.get("behavioral_constraints", [])

        # Check if all relevant constraints were considered
        violations = []
        for constraint in all_constraints:
            # Simple check: was this constraint in the list?
            if constraint not in constraints_checked:
                # This is a potential oversight
                violations.append(f"Constraint not verified: {constraint}")

        return {
            "aligned": len(violations) == 0,
            "violations": violations,
            "constraints_total": len(all_constraints),
            "constraints_checked": len(constraints_checked)
        }

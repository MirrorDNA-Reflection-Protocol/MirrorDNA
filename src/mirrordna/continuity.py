# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Continuity tracking for MirrorDNA sessions.
"""

import secrets
from datetime import datetime
from typing import Dict, Any, Optional, List

from .validator import validate_schema
from .storage import StorageAdapter, JSONFileStorage


class ContinuityTracker:
    """Manages session continuity and lineage."""

    def __init__(self, storage: Optional[StorageAdapter] = None):
        """
        Initialize continuity tracker.

        Args:
            storage: Storage adapter (uses JSONFileStorage if None)
        """
        self.storage = storage or JSONFileStorage()

    def _generate_session_id(self) -> str:
        """
        Generate a unique session ID.

        Returns:
            Generated session ID
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        suffix = secrets.token_hex(4)  # 8 characters

        return f"sess_{timestamp}_{suffix}"

    def create_session(
        self,
        agent_id: str,
        user_id: str,
        parent_session_id: Optional[str] = None,
        context_metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a new session.

        Args:
            agent_id: Agent identity ID
            user_id: User identity ID
            parent_session_id: Optional parent session ID for continuity
            context_metadata: Optional context metadata

        Returns:
            Session record

        Raises:
            ValueError: If validation fails
        """
        session_id = self._generate_session_id()

        session = {
            "session_id": session_id,
            "parent_session_id": parent_session_id,
            "agent_id": agent_id,
            "user_id": user_id,
            "started_at": datetime.utcnow().isoformat() + "Z",
            "ended_at": None
        }

        if context_metadata:
            session["context_metadata"] = context_metadata

        # Validate against schema
        result = validate_schema(session, "continuity")
        if not result.is_valid:
            raise ValueError(f"Session validation failed: {', '.join(result.errors)}")

        # Store session
        self.storage.create("sessions", session)

        return session

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a session by ID.

        Args:
            session_id: Session ID

        Returns:
            Session record or None if not found
        """
        return self.storage.read("sessions", session_id)

    def end_session(
        self,
        session_id: str,
        final_state: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        End a session.

        Args:
            session_id: Session ID
            final_state: Optional final state metadata

        Returns:
            Updated session record or None if not found
        """
        updates = {
            "ended_at": datetime.utcnow().isoformat() + "Z"
        }

        if final_state:
            # Merge final state into context_metadata
            session = self.get_session(session_id)
            if session:
                context_metadata = session.get("context_metadata", {})
                context_metadata["final_state"] = final_state
                updates["context_metadata"] = context_metadata

        return self.storage.update("sessions", session_id, updates)

    def get_session_lineage(self, session_id: str) -> List[Dict[str, Any]]:
        """
        Get the full lineage (ancestor chain) of a session.

        Args:
            session_id: Session ID

        Returns:
            List of sessions from oldest ancestor to current
        """
        lineage = []
        current_session_id = session_id

        while current_session_id:
            session = self.get_session(current_session_id)
            if not session:
                break

            lineage.insert(0, session)  # Prepend to list
            current_session_id = session.get("parent_session_id")

        return lineage

    def get_context(self, session_id: str) -> Dict[str, Any]:
        """
        Get aggregated context from session lineage.

        Args:
            session_id: Session ID

        Returns:
            Aggregated context metadata
        """
        lineage = self.get_session_lineage(session_id)

        context = {
            "session_count": len(lineage),
            "sessions": []
        }

        for session in lineage:
            context["sessions"].append({
                "session_id": session["session_id"],
                "started_at": session["started_at"],
                "ended_at": session.get("ended_at"),
                "metadata": session.get("context_metadata", {})
            })

        return context

    def session_exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: Session ID

        Returns:
            True if session exists, False otherwise
        """
        return self.get_session(session_id) is not None

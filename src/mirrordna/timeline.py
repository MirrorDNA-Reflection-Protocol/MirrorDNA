"""
Enhanced timeline and lineage tracking for MirrorDNA.

Provides advanced capabilities for:
- Timeline querying and visualization
- Lineage analysis and branching
- Context evolution tracking
- Session relationships
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set, Tuple
from collections import defaultdict

from .continuity import ContinuityTracker
from .storage import StorageAdapter, JSONFileStorage


class TimelineAnalyzer:
    """Advanced timeline and lineage analysis."""

    def __init__(
        self,
        continuity: Optional[ContinuityTracker] = None,
        storage: Optional[StorageAdapter] = None
    ):
        """
        Initialize timeline analyzer.

        Args:
            continuity: Continuity tracker instance
            storage: Storage adapter
        """
        self.storage = storage or JSONFileStorage()
        self.continuity = continuity or ContinuityTracker(self.storage)

    async def get_timeline(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get timeline of sessions with optional filters.

        Args:
            user_id: Optional filter by user
            agent_id: Optional filter by agent
            start_time: Optional start timestamp (ISO 8601)
            end_time: Optional end timestamp (ISO 8601)
            limit: Maximum number of sessions

        Returns:
            List of sessions in chronological order
        """
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if agent_id:
            filters["agent_id"] = agent_id

        sessions = await self.storage.query("sessions", filters, limit=limit * 2)

        # Filter by time range
        if start_time or end_time:
            filtered = []
            for session in sessions:
                session_time = session.get("started_at", "")

                if start_time and session_time < start_time:
                    continue
                if end_time and session_time > end_time:
                    continue

                filtered.append(session)
            sessions = filtered

        # Sort by start time
        sessions.sort(key=lambda s: s.get("started_at", ""))

        return sessions[:limit]

    async def get_lineage_tree(
        self,
        root_session_id: str
    ) -> Dict[str, Any]:
        """
        Build complete lineage tree from a root session.

        Args:
            root_session_id: Starting session ID

        Returns:
            Tree structure with all descendants
        """
        root_session = await self.continuity.get_session(root_session_id)
        if not root_session:
            return {}

        tree = {
            "session": root_session,
            "children": []
        }

        # Find all sessions that have this as parent
        all_sessions = await self.storage.query("sessions", {}, limit=10000)
        children = [
            s for s in all_sessions
            if s.get("parent_session_id") == root_session_id
        ]

        # Recursively build subtrees
        for child in children:
            subtree = await self.get_lineage_tree(child["session_id"])
            tree["children"].append(subtree)

        return tree

    async def detect_branches(
        self,
        root_session_id: str
    ) -> List[List[str]]:
        """
        Detect branching points in session lineage.

        Args:
            root_session_id: Starting session ID

        Returns:
            List of branches (each branch is a list of session IDs)
        """
        tree = await self.get_lineage_tree(root_session_id)

        branches = []

        def traverse(node: Dict[str, Any], current_branch: List[str]):
            current_branch = current_branch + [node["session"]["session_id"]]

            children = node.get("children", [])

            if not children:
                # Leaf node - end of branch
                branches.append(current_branch)
            elif len(children) == 1:
                # Single child - continue branch
                traverse(children[0], current_branch)
            else:
                # Multiple children - branching point
                for child in children:
                    traverse(child, current_branch)

        if tree:
            traverse(tree, [])

        return branches

    async def get_context_evolution(
        self,
        session_ids: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Track how context evolved across a sequence of sessions.

        Args:
            session_ids: List of session IDs in order

        Returns:
            List of context snapshots with diffs
        """
        evolution = []
        prev_context = {}

        for session_id in session_ids:
            session = await self.continuity.get_session(session_id)
            if not session:
                continue

            current_context = session.get("context_metadata", {})

            # Calculate diff from previous
            added = {
                k: v for k, v in current_context.items()
                if k not in prev_context or prev_context[k] != v
            }

            removed = {
                k: prev_context[k] for k in prev_context
                if k not in current_context
            }

            evolution.append({
                "session_id": session_id,
                "started_at": session.get("started_at"),
                "context": current_context,
                "diff": {
                    "added": added,
                    "removed": removed
                }
            })

            prev_context = current_context

        return evolution

    async def get_session_metrics(
        self,
        user_id: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Calculate metrics about sessions.

        Args:
            user_id: Optional filter by user
            agent_id: Optional filter by agent

        Returns:
            Dictionary of metrics
        """
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if agent_id:
            filters["agent_id"] = agent_id

        sessions = await self.storage.query("sessions", filters, limit=10000)

        # Calculate metrics
        total_sessions = len(sessions)
        ended_sessions = [s for s in sessions if s.get("ended_at")]
        active_sessions = [s for s in sessions if not s.get("ended_at")]

        # Session durations
        durations = []
        for session in ended_sessions:
            start = datetime.fromisoformat(session["started_at"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(session["ended_at"].replace("Z", "+00:00"))
            duration = (end - start).total_seconds()
            durations.append(duration)

        avg_duration = sum(durations) / len(durations) if durations else 0

        # Session tree depth
        max_depth = 0
        for session in sessions:
            lineage = await self.continuity.get_session_lineage(session["session_id"])
            max_depth = max(max_depth, len(lineage))

        # Branching factor
        parent_counts = defaultdict(int)
        for session in sessions:
            parent_id = session.get("parent_session_id")
            if parent_id:
                parent_counts[parent_id] += 1

        max_branches = max(parent_counts.values()) if parent_counts else 0

        return {
            "total_sessions": total_sessions,
            "active_sessions": len(active_sessions),
            "ended_sessions": len(ended_sessions),
            "average_duration_seconds": avg_duration,
            "max_lineage_depth": max_depth,
            "max_branching_factor": max_branches,
            "unique_users": len(set(s.get("user_id") for s in sessions if s.get("user_id"))),
            "unique_agents": len(set(s.get("agent_id") for s in sessions if s.get("agent_id")))
        }

    async def find_related_sessions(
        self,
        session_id: str,
        max_distance: int = 2
    ) -> Dict[str, List[str]]:
        """
        Find sessions related to a given session.

        Args:
            session_id: Starting session ID
            max_distance: Maximum distance in lineage tree

        Returns:
            Dictionary of relationship types to session IDs
        """
        related = {
            "ancestors": [],
            "descendants": [],
            "siblings": []
        }

        # Get lineage (ancestors)
        lineage = await self.continuity.get_session_lineage(session_id)
        if len(lineage) > 1:
            related["ancestors"] = [s["session_id"] for s in lineage[:-1]]

        # Get descendants
        tree = await self.get_lineage_tree(session_id)

        def collect_descendants(node: Dict[str, Any], depth: int = 0):
            if depth >= max_distance:
                return

            for child in node.get("children", []):
                related["descendants"].append(child["session"]["session_id"])
                collect_descendants(child, depth + 1)

        collect_descendants(tree)

        # Get siblings (sessions with same parent)
        session = await self.continuity.get_session(session_id)
        if session and session.get("parent_session_id"):
            parent_id = session["parent_session_id"]
            all_sessions = await self.storage.query("sessions", {}, limit=10000)
            siblings = [
                s["session_id"] for s in all_sessions
                if s.get("parent_session_id") == parent_id
                and s["session_id"] != session_id
            ]
            related["siblings"] = siblings

        return related

    async def get_concurrent_sessions(
        self,
        time_window: Optional[Tuple[str, str]] = None
    ) -> List[List[str]]:
        """
        Find sessions that overlapped in time.

        Args:
            time_window: Optional (start, end) tuple to filter

        Returns:
            List of groups of concurrent session IDs
        """
        sessions = await self.storage.query("sessions", {}, limit=10000)

        # Filter by time window if provided
        if time_window:
            start, end = time_window
            sessions = [
                s for s in sessions
                if s.get("started_at", "") >= start
                and s.get("started_at", "") <= end
            ]

        # Find overlapping sessions
        concurrent_groups = []

        for i, session_a in enumerate(sessions):
            group = [session_a["session_id"]]

            start_a = session_a.get("started_at")
            end_a = session_a.get("ended_at") or datetime.utcnow().isoformat() + "Z"

            for session_b in sessions[i+1:]:
                start_b = session_b.get("started_at")
                end_b = session_b.get("ended_at") or datetime.utcnow().isoformat() + "Z"

                # Check overlap
                if start_a <= end_b and start_b <= end_a:
                    group.append(session_b["session_id"])

            if len(group) > 1:
                concurrent_groups.append(group)

        return concurrent_groups

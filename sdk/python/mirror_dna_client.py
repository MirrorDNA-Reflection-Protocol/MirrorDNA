"""
MirrorDNA SDK Client - Simple developer interface to MirrorDNA protocol.

This client provides high-level methods for working with MirrorDNA concepts:
- Loading and validating vault configurations
- Computing state hashes for integrity verification
- Validating timeline events
- Managing continuity tracking

Designed for offline/local use without requiring a hosted backend.
"""

import json
import yaml
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from datetime import datetime


class MirrorDNAClient:
    """
    Simple client for integrating MirrorDNA concepts into your application.

    Features:
    - Load and validate vault configurations
    - Compute deterministic state hashes (SHA-256)
    - Validate timeline event structures
    - Track continuity metrics

    All operations work locally with files - no backend required.
    """

    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """
        Initialize MirrorDNA client.

        Args:
            data_dir: Optional directory for storing data files.
                     Defaults to ./mirrordna_data/
        """
        if data_dir is None:
            data_dir = Path.cwd() / "mirrordna_data"

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # In-memory cache
        self._vault_cache: Dict[str, Any] = {}
        self._timeline_cache: Dict[str, List[Dict]] = {}

    def load_vault_config(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load and validate a vault configuration file.

        Args:
            path: Path to vault config file (JSON or YAML)

        Returns:
            Dictionary containing vault configuration

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If required fields are missing
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Vault config not found: {path}")

        # Load file based on extension
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                config = yaml.safe_load(f)
            else:
                config = json.load(f)

        # Validate required fields
        required = ['vault_id', 'name', 'path', 'created_at']
        missing = [field for field in required if field not in config]

        if missing:
            raise ValueError(f"Vault config missing required fields: {missing}")

        # Cache for later retrieval
        self._vault_cache[config['vault_id']] = config

        return config

    def compute_state_hash(self, data: Dict[str, Any]) -> str:
        """
        Compute deterministic SHA-256 hash of state data.

        Creates canonical JSON representation with sorted keys to ensure
        the same data always produces the same hash.

        Args:
            data: State data dictionary

        Returns:
            64-character hexadecimal hash string
        """
        # Create canonical JSON (sorted keys, no whitespace)
        canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))

        # Compute SHA-256 hash
        sha256 = hashlib.sha256()
        sha256.update(canonical_json.encode('utf-8'))

        return sha256.hexdigest()

    def validate_timeline(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate timeline events structure and compute continuity metrics.

        Args:
            events: List of timeline event dictionaries

        Returns:
            Dictionary with validation results and metrics:
            - valid: Whether all events are valid
            - total_events: Number of events
            - event_types: Count of each event type
            - actors: Unique actors in timeline
            - timespan: First and last timestamps
            - errors: List of validation errors (if any)
        """
        errors = []
        event_types = {}
        actors = set()
        timestamps = []

        required_fields = ['id', 'timestamp', 'event_type', 'actor']

        for idx, event in enumerate(events):
            # Check required fields
            missing = [f for f in required_fields if f not in event]
            if missing:
                errors.append(f"Event {idx}: missing fields {missing}")
                continue

            # Track metrics
            event_type = event.get('event_type')
            if event_type:
                event_types[event_type] = event_types.get(event_type, 0) + 1

            actor = event.get('actor')
            if actor:
                actors.add(actor)

            timestamp = event.get('timestamp')
            if timestamp:
                timestamps.append(timestamp)

        return {
            'valid': len(errors) == 0,
            'total_events': len(events),
            'event_types': event_types,
            'unique_actors': len(actors),
            'timespan': {
                'first': min(timestamps) if timestamps else None,
                'last': max(timestamps) if timestamps else None
            },
            'errors': errors
        }

    def create_master_citation(
        self,
        identity_id: str,
        vault_id: str,
        version: str = "1.0.0"
    ) -> Dict[str, Any]:
        """
        Create a new Master Citation document.

        Args:
            identity_id: Unique identity identifier
            vault_id: Vault to bind this citation to
            version: Protocol version (default: "1.0.0")

        Returns:
            Master Citation dictionary with computed checksum
        """
        citation = {
            "id": f"mc_{identity_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "version": version,
            "vault_id": vault_id,
            "created_at": datetime.utcnow().isoformat() + "Z",
            "constitutional_alignment": {
                "compliance_level": "full",
                "framework_version": "1.0",
                "rights_bundle": ["memory", "continuity", "portability"]
            }
        }

        # Compute and add checksum
        citation["checksum"] = self.compute_state_hash(citation)

        return citation

    def save_citation(
        self,
        citation: Dict[str, Any],
        filename: Optional[str] = None
    ) -> Path:
        """
        Save Master Citation to file.

        Args:
            citation: Master Citation dictionary
            filename: Optional filename (defaults to citation ID)

        Returns:
            Path to saved file
        """
        if filename is None:
            filename = f"{citation['id']}.yaml"

        output_path = self.data_dir / filename

        with open(output_path, 'w') as f:
            yaml.dump(citation, f, default_flow_style=False, sort_keys=False)

        return output_path

    def create_timeline_event(
        self,
        event_type: str,
        actor: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a timeline event dictionary.

        Args:
            event_type: Type of event (session_start, memory_created, etc.)
            actor: Identity ID of actor
            payload: Optional event-specific data

        Returns:
            Timeline event dictionary
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        event_id = f"evt_{timestamp}_{len(self._timeline_cache.get(actor, []))}"

        event = {
            "id": event_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "event_type": event_type,
            "actor": actor,
            "payload": payload or {}
        }

        # Add to cache
        if actor not in self._timeline_cache:
            self._timeline_cache[actor] = []
        self._timeline_cache[actor].append(event)

        return event

    def get_continuity_status(
        self,
        identity_id: str
    ) -> Dict[str, Any]:
        """
        Get continuity status for an identity.

        Args:
            identity_id: Identity to check

        Returns:
            Dictionary with continuity metrics
        """
        events = self._timeline_cache.get(identity_id, [])

        if not events:
            return {
                "identity_id": identity_id,
                "status": "no_activity",
                "total_events": 0,
                "last_activity": None
            }

        validation = self.validate_timeline(events)

        return {
            "identity_id": identity_id,
            "status": "active" if validation['valid'] else "degraded",
            "total_events": validation['total_events'],
            "event_types": validation['event_types'],
            "last_activity": validation['timespan']['last'],
            "valid": validation['valid']
        }

    def save_timeline(
        self,
        identity_id: str,
        filename: Optional[str] = None
    ) -> Path:
        """
        Save timeline events to file.

        Args:
            identity_id: Identity whose timeline to save
            filename: Optional filename

        Returns:
            Path to saved file
        """
        events = self._timeline_cache.get(identity_id, [])

        if filename is None:
            filename = f"{identity_id}_timeline.json"

        output_path = self.data_dir / filename

        timeline_data = {
            "timeline_id": identity_id,
            "event_count": len(events),
            "events": events
        }

        with open(output_path, 'w') as f:
            json.dump(timeline_data, f, indent=2)

        return output_path

    def load_timeline(
        self,
        path: Union[str, Path]
    ) -> List[Dict[str, Any]]:
        """
        Load timeline from file.

        Args:
            path: Path to timeline file

        Returns:
            List of timeline events
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Timeline not found: {path}")

        with open(path, 'r') as f:
            data = json.load(f)

        events = data.get('events', [])

        # Cache events if timeline_id present
        timeline_id = data.get('timeline_id')
        if timeline_id:
            self._timeline_cache[timeline_id] = events

        return events

    def verify_checksum(
        self,
        data: Dict[str, Any],
        expected_checksum: str
    ) -> bool:
        """
        Verify that data matches expected checksum.

        Args:
            data: Data dictionary (without checksum field)
            expected_checksum: Expected checksum value

        Returns:
            True if checksums match, False otherwise
        """
        actual = self.compute_state_hash(data)
        return actual.lower() == expected_checksum.lower()

"""
MirrorDNA Developer SDK - Python Client

Simple, local-only client for MirrorDNA protocol operations.
Provides easy-to-use interface for vault config loading, state hashing, and timeline validation.

This SDK is designed for:
- Local development and testing
- Understanding MirrorDNA concepts
- Building simple integrations

For production use, see the full protocol implementation in src/mirrordna/
"""

import os
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union


class MirrorDNAClient:
    """
    Simple MirrorDNA client for local operations.

    Features:
    - Load and validate vault configurations
    - Compute deterministic state hashes for directories
    - Validate timeline JSON/YAML files

    All operations are local-only with no external dependencies beyond pyyaml.
    """

    def __init__(self):
        """Initialize MirrorDNA client."""
        self.last_vault_config = None
        self.last_state_hash = None

    def load_vault_config(self, path: str) -> Dict[str, Any]:
        """
        Load and validate a vault configuration file.

        Args:
            path: Path to vault config file (JSON or YAML)

        Returns:
            Dictionary containing vault configuration

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If config is invalid

        Example:
            >>> client = MirrorDNAClient()
            >>> config = client.load_vault_config("vault.yaml")
            >>> print(config['vault_id'])
        """
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Vault config not found: {path}")

        # Load file based on extension
        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                try:
                    import yaml
                    data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError(
                        "PyYAML required for YAML files. Install with: pip install pyyaml"
                    )
            else:
                data = json.load(f)

        # Basic validation
        required_fields = ['vault_id', 'name', 'path', 'created_at']
        missing = [f for f in required_fields if f not in data]

        if missing:
            raise ValueError(f"Vault config missing required fields: {missing}")

        self.last_vault_config = data
        return data

    def compute_state_hash(self, directory: str, ignore_patterns: Optional[list] = None) -> str:
        """
        Compute deterministic SHA-256 hash of directory contents.

        Creates a hash based on file paths and contents in alphabetical order.
        Useful for detecting changes in vault state.

        Args:
            directory: Path to directory to hash
            ignore_patterns: Optional list of patterns to ignore (e.g., ['.git', '__pycache__'])

        Returns:
            Hexadecimal SHA-256 hash string

        Raises:
            FileNotFoundError: If directory doesn't exist

        Example:
            >>> client = MirrorDNAClient()
            >>> hash1 = client.compute_state_hash("./my_vault")
            >>> # Make changes to files...
            >>> hash2 = client.compute_state_hash("./my_vault")
            >>> if hash1 != hash2:
            ...     print("Vault state has changed!")
        """
        directory = Path(directory)

        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")

        if not directory.is_dir():
            raise ValueError(f"Path is not a directory: {directory}")

        # Default ignore patterns
        if ignore_patterns is None:
            ignore_patterns = ['.git', '__pycache__', '.DS_Store', '*.pyc']

        # Collect all files in deterministic order
        file_hashes = []

        for root, dirs, files in os.walk(directory):
            # Filter out ignored directories
            dirs[:] = [d for d in dirs if not self._should_ignore(d, ignore_patterns)]

            # Process files in alphabetical order
            for filename in sorted(files):
                if self._should_ignore(filename, ignore_patterns):
                    continue

                filepath = Path(root) / filename
                rel_path = filepath.relative_to(directory)

                # Hash file content
                try:
                    with open(filepath, 'rb') as f:
                        file_hash = hashlib.sha256(f.read()).hexdigest()

                    # Combine relative path and content hash
                    file_hashes.append(f"{rel_path}:{file_hash}")
                except (IOError, OSError):
                    # Skip files that can't be read
                    continue

        # Compute final hash from all file hashes
        combined = '\n'.join(sorted(file_hashes))
        final_hash = hashlib.sha256(combined.encode('utf-8')).hexdigest()

        self.last_state_hash = final_hash
        return final_hash

    def _should_ignore(self, name: str, patterns: list) -> bool:
        """Check if filename/dirname matches any ignore pattern."""
        for pattern in patterns:
            if pattern.startswith('*'):
                if name.endswith(pattern[1:]):
                    return True
            elif pattern in name:
                return True
        return False

    def validate_timeline(self, path: str) -> Dict[str, Any]:
        """
        Validate timeline file structure and return summary.

        Checks that timeline file contains required fields and valid event structure.
        Does not perform deep schema validation.

        Args:
            path: Path to timeline file (JSON or YAML)

        Returns:
            Dictionary with validation results and timeline summary:
            {
                'valid': bool,
                'event_count': int,
                'timeline_id': str,
                'errors': list,
                'first_event': str,
                'last_event': str
            }

        Example:
            >>> client = MirrorDNAClient()
            >>> result = client.validate_timeline("timeline.json")
            >>> if result['valid']:
            ...     print(f"Timeline valid with {result['event_count']} events")
            >>> else:
            ...     print(f"Errors: {result['errors']}")
        """
        path = Path(path)
        errors = []

        if not path.exists():
            return {
                'valid': False,
                'errors': [f"File not found: {path}"]
            }

        # Load timeline file
        try:
            with open(path, 'r') as f:
                if path.suffix in ['.yaml', '.yml']:
                    try:
                        import yaml
                        data = yaml.safe_load(f)
                    except ImportError:
                        return {
                            'valid': False,
                            'errors': ["PyYAML required for YAML files"]
                        }
                else:
                    data = json.load(f)
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Failed to parse file: {e}"]
            }

        # Extract events
        if isinstance(data, list):
            events = data
            timeline_id = "unknown"
        elif isinstance(data, dict):
            events = data.get('events', [])
            timeline_id = data.get('timeline_id', 'unknown')
        else:
            return {
                'valid': False,
                'errors': ["Timeline file must be a list or dict with 'events' key"]
            }

        # Validate event structure
        required_event_fields = ['id', 'timestamp', 'event_type', 'actor']

        for i, event in enumerate(events):
            if not isinstance(event, dict):
                errors.append(f"Event {i} is not a dictionary")
                continue

            missing = [f for f in required_event_fields if f not in event]
            if missing:
                errors.append(f"Event {i} missing fields: {missing}")

        # Build summary
        result = {
            'valid': len(errors) == 0,
            'event_count': len(events),
            'timeline_id': timeline_id,
            'errors': errors
        }

        if events:
            result['first_event'] = events[0].get('timestamp', 'unknown')
            result['last_event'] = events[-1].get('timestamp', 'unknown')

        return result

    def compute_data_checksum(self, data: Dict[str, Any]) -> str:
        """
        Compute deterministic SHA-256 checksum for dictionary data.

        Uses canonical JSON serialization (sorted keys) for determinism.

        Args:
            data: Dictionary to hash

        Returns:
            Hexadecimal SHA-256 hash string

        Example:
            >>> client = MirrorDNAClient()
            >>> checksum = client.compute_data_checksum({'id': 'test', 'value': 42})
        """
        canonical_json = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

    def get_continuity_status(
        self,
        vault_path: Optional[str] = None,
        timeline_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get continuity status summary for vault and timeline.

        Convenience method that combines vault config, state hash, and timeline validation.

        Args:
            vault_path: Optional path to vault config
            timeline_path: Optional path to timeline file

        Returns:
            Dictionary with continuity status information

        Example:
            >>> client = MirrorDNAClient()
            >>> status = client.get_continuity_status(
            ...     vault_path="vault.yaml",
            ...     timeline_path="timeline.json"
            ... )
            >>> print(f"Vault: {status['vault_id']}, Events: {status['event_count']}")
        """
        status = {
            'timestamp': self._get_timestamp(),
            'vault_loaded': False,
            'timeline_valid': False
        }

        if vault_path:
            try:
                vault = self.load_vault_config(vault_path)
                status['vault_loaded'] = True
                status['vault_id'] = vault.get('vault_id')
                status['vault_name'] = vault.get('name')
            except Exception as e:
                status['vault_error'] = str(e)

        if timeline_path:
            result = self.validate_timeline(timeline_path)
            status['timeline_valid'] = result['valid']
            status['event_count'] = result.get('event_count', 0)
            status['timeline_errors'] = result.get('errors', [])

        # Compute state hash if we have a vault path
        if vault_path and status['vault_loaded']:
            try:
                vault_dir = Path(self.last_vault_config.get('path', '.'))
                if vault_dir.exists():
                    status['state_hash'] = self.compute_state_hash(str(vault_dir))
            except Exception as e:
                status['state_hash_error'] = str(e)

        return status

    def _get_timestamp(self) -> str:
        """Get current UTC timestamp in ISO format."""
        from datetime import datetime
        return datetime.utcnow().isoformat() + 'Z'


# Convenience functions for quick operations

def quick_hash_directory(directory: str) -> str:
    """
    Quick utility to hash a directory.

    Args:
        directory: Path to directory

    Returns:
        SHA-256 hash string
    """
    client = MirrorDNAClient()
    return client.compute_state_hash(directory)


def quick_validate_timeline(path: str) -> bool:
    """
    Quick utility to check if timeline is valid.

    Args:
        path: Path to timeline file

    Returns:
        True if valid, False otherwise
    """
    client = MirrorDNAClient()
    result = client.validate_timeline(path)
    return result['valid']

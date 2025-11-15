# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Configuration loader for MirrorDNA protocol documents.

Loads and validates Master Citations, Vault configs, and other MirrorDNA protocol configurations.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

from .checksum import compute_file_checksum, verify_checksum


@dataclass
class MasterCitation:
    """Master Citation document."""
    id: str
    version: str
    vault_id: str
    created_at: str
    checksum: str
    predecessor: Optional[str] = None
    successor: Optional[str] = None
    updated_at: Optional[str] = None
    identity_ref: Optional[str] = None
    constitutional_ref: Optional[str] = None
    tags: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class VaultConfig:
    """Vault configuration."""
    vault_id: str
    name: str
    path: str
    created_at: str
    entries: Optional[list] = None
    metadata: Optional[Dict[str, Any]] = None


class ConfigLoader:
    """Loads and validates MirrorDNA protocol configuration documents."""

    def __init__(self, schema_dir: Optional[Path] = None):
        """
        Initialize config loader.

        Args:
            schema_dir: Directory containing JSON schemas
        """
        if schema_dir is None:
            # Default to schema/ directory in repo
            schema_dir = Path(__file__).parent.parent.parent / "schema"

        self.schema_dir = Path(schema_dir)
        self._schema_cache: Dict[str, Dict] = {}

    def _load_schema(self, schema_name: str) -> Dict[str, Any]:
        """Load JSON schema from file."""
        if schema_name in self._schema_cache:
            return self._schema_cache[schema_name]

        schema_file = self.schema_dir / f"{schema_name}.schema.json"

        if not schema_file.exists():
            raise FileNotFoundError(f"Schema not found: {schema_file}")

        with open(schema_file, 'r') as f:
            schema = json.load(f)

        self._schema_cache[schema_name] = schema
        return schema

    def _load_file(self, path: Union[str, Path]) -> Dict[str, Any]:
        """Load JSON or YAML file."""
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, 'r') as f:
            if path.suffix in ['.yaml', '.yml']:
                try:
                    return yaml.safe_load(f)
                except NameError:
                    raise ImportError("PyYAML not installed. Install with: pip install pyyaml")
            else:
                return json.load(f)

    def _validate(self, data: Dict[str, Any], schema_name: str) -> None:
        """Validate data against schema."""
        if not JSONSCHEMA_AVAILABLE:
            # Skip validation if jsonschema not available (warn but don't fail)
            return

        schema = self._load_schema(schema_name)

        try:
            jsonschema.validate(instance=data, schema=schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Validation failed for {schema_name}: {e.message}")

    def load_master_citation(
        self,
        path: Union[str, Path],
        verify_checksum: bool = True
    ) -> MasterCitation:
        """
        Load and validate a Master Citation document.

        Args:
            path: Path to Master Citation file (JSON or YAML)
            verify_checksum: Whether to verify embedded checksum

        Returns:
            MasterCitation object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If validation fails or checksum mismatch
        """
        data = self._load_file(path)

        # Validate against schema
        self._validate(data, "master_citation")

        # Verify checksum if requested
        if verify_checksum and 'checksum' in data:
            # Create a copy without checksum for verification
            data_without_checksum = {k: v for k, v in data.items() if k != 'checksum'}
            expected_checksum = data['checksum']

            from .checksum import compute_state_checksum
            actual_checksum = compute_state_checksum(data_without_checksum)

            if actual_checksum != expected_checksum:
                raise ValueError(
                    f"Checksum mismatch in Master Citation. "
                    f"Expected: {expected_checksum}, Got: {actual_checksum}"
                )

        # Create dataclass instance
        return MasterCitation(**{
            k: v for k, v in data.items()
            if k in MasterCitation.__dataclass_fields__
        })

    def load_vault_config(
        self,
        path: Union[str, Path]
    ) -> VaultConfig:
        """
        Load and validate a Vault configuration.

        Args:
            path: Path to vault config file (JSON or YAML)

        Returns:
            VaultConfig object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If validation fails
        """
        data = self._load_file(path)

        # Validate against schema (if we have one)
        # For now, basic validation only
        required_fields = ['vault_id', 'name', 'path', 'created_at']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Vault config missing required field: {field}")

        # Create dataclass instance
        return VaultConfig(**{
            k: v for k, v in data.items()
            if k in VaultConfig.__dataclass_fields__
        })

    def load_timeline_events(
        self,
        path: Union[str, Path],
        validate_events: bool = True
    ) -> list:
        """
        Load timeline events from file.

        Args:
            path: Path to timeline events file (JSON or YAML)
            validate_events: Whether to validate each event against schema

        Returns:
            List of timeline event dictionaries

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If validation fails
        """
        data = self._load_file(path)

        events = data if isinstance(data, list) else data.get('events', [])

        if validate_events:
            for event in events:
                self._validate(event, "timeline_event")

        return events

    def validate_config(
        self,
        data: Dict[str, Any],
        schema_name: str
    ) -> bool:
        """
        Validate configuration data against schema.

        Args:
            data: Configuration data
            schema_name: Name of schema to validate against

        Returns:
            True if valid

        Raises:
            ValueError: If validation fails
        """
        self._validate(data, schema_name)
        return True

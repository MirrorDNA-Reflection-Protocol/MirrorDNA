# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Schema validation for MirrorDNA data structures.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


@dataclass
class ValidationResult:
    """Result of schema validation."""
    is_valid: bool
    errors: List[str]
    schema_name: Optional[str] = None


class Validator:
    """JSON Schema validator for MirrorDNA data structures."""

    def __init__(self, schemas_dir: Optional[Path] = None):
        """
        Initialize validator with schema directory.

        Args:
            schemas_dir: Path to directory containing schema files.
                        If None, uses default schemas/ directory.
        """
        if schemas_dir is None:
            # Default to schemas/ directory in repo root
            current_dir = Path(__file__).parent
            schemas_dir = current_dir.parent.parent / "schemas"

        self.schemas_dir = Path(schemas_dir)
        self._schema_cache: Dict[str, Dict] = {}

    def load_schema(self, schema_name: str) -> Dict[str, Any]:
        """
        Load a JSON schema by name.

        Args:
            schema_name: Name of schema (e.g., "identity", "continuity")

        Returns:
            Loaded JSON schema as dictionary

        Raises:
            FileNotFoundError: If schema file doesn't exist
            json.JSONDecodeError: If schema file is invalid JSON
        """
        if schema_name in self._schema_cache:
            return self._schema_cache[schema_name]

        schema_file = self.schemas_dir / f"{schema_name}.schema.json"

        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {schema_file}")

        with open(schema_file, 'r') as f:
            schema = json.load(f)

        self._schema_cache[schema_name] = schema
        return schema

    def validate(self, data: Dict[str, Any], schema_name: str) -> ValidationResult:
        """
        Validate data against a named schema.

        Args:
            data: Data to validate
            schema_name: Name of schema to validate against

        Returns:
            ValidationResult with validation status and any errors
        """
        if not JSONSCHEMA_AVAILABLE:
            return ValidationResult(
                is_valid=False,
                errors=["jsonschema library not available. Install with: pip install jsonschema"],
                schema_name=schema_name
            )

        try:
            schema = self.load_schema(schema_name)
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Failed to load schema '{schema_name}': {str(e)}"],
                schema_name=schema_name
            )

        errors = []
        try:
            jsonschema.validate(instance=data, schema=schema)
            return ValidationResult(is_valid=True, errors=[], schema_name=schema_name)
        except jsonschema.ValidationError as e:
            errors.append(f"Validation error: {e.message}")
            if e.path:
                path_str = ".".join(str(p) for p in e.path)
                errors[-1] += f" at path: {path_str}"
        except jsonschema.SchemaError as e:
            errors.append(f"Schema error: {e.message}")
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")

        return ValidationResult(is_valid=False, errors=errors, schema_name=schema_name)


# Global validator instance
_validator = None


def get_validator() -> Validator:
    """Get or create global validator instance."""
    global _validator
    if _validator is None:
        _validator = Validator()
    return _validator


def validate_schema(data: Dict[str, Any], schema_name: str) -> ValidationResult:
    """
    Validate data against a named schema (convenience function).

    Args:
        data: Data to validate
        schema_name: Name of schema to validate against

    Returns:
        ValidationResult with validation status and any errors
    """
    validator = get_validator()
    return validator.validate(data, schema_name)

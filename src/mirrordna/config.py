# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Checksummed configuration loader for MirrorDNA.

Provides verified configuration loading with:
- Hash-based integrity verification
- Multiple format support (JSON, YAML)
- Config versioning
- Secure defaults
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict


@dataclass
class ConfigChecksum:
    """Configuration checksum metadata."""
    algorithm: str
    hash: str
    version: str
    created_at: str


class ConfigLoader:
    """Checksummed configuration loader with integrity verification."""

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize config loader.

        Args:
            config_dir: Directory containing config files
        """
        if config_dir is None:
            config_dir = Path.home() / ".mirrordna" / "config"

        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Dict[str, Any]] = {}

    def calculate_checksum(
        self,
        data: Union[str, bytes, Dict[str, Any]],
        algorithm: str = "sha256"
    ) -> str:
        """
        Calculate checksum for data.

        Args:
            data: Data to checksum
            algorithm: Hash algorithm (sha256, sha512, etc.)

        Returns:
            Hexadecimal hash digest
        """
        if isinstance(data, dict):
            # Convert dict to canonical JSON
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        elif isinstance(data, str):
            data_bytes = data.encode('utf-8')
        else:
            data_bytes = data

        hash_obj = hashlib.new(algorithm)
        hash_obj.update(data_bytes)
        return hash_obj.hexdigest()

    def save_config(
        self,
        name: str,
        config: Dict[str, Any],
        version: str = "1.0.0",
        checksum_algorithm: str = "sha256"
    ) -> ConfigChecksum:
        """
        Save configuration with checksum.

        Args:
            name: Configuration name
            config: Configuration data
            version: Configuration version
            checksum_algorithm: Hash algorithm to use

        Returns:
            Checksum metadata
        """
        from datetime import datetime

        # Calculate checksum
        checksum_hash = self.calculate_checksum(config, checksum_algorithm)

        # Create checksum metadata
        checksum_meta = ConfigChecksum(
            algorithm=checksum_algorithm,
            hash=checksum_hash,
            version=version,
            created_at=datetime.utcnow().isoformat() + "Z"
        )

        # Save config file
        config_file = self.config_dir / f"{name}.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2, sort_keys=True)

        # Save checksum file
        checksum_file = self.config_dir / f"{name}.checksum.json"
        with open(checksum_file, 'w') as f:
            json.dump(asdict(checksum_meta), f, indent=2)

        return checksum_meta

    def load_config(
        self,
        name: str,
        verify: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Load configuration with optional verification.

        Args:
            name: Configuration name
            verify: Whether to verify checksum
            use_cache: Whether to use cached config

        Returns:
            Configuration data

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If checksum verification fails
        """
        # Check cache
        if use_cache and name in self._cache:
            return self._cache[name]

        # Load config file
        config_file = self.config_dir / f"{name}.json"
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as f:
            config = json.load(f)

        # Verify checksum if requested
        if verify:
            checksum_file = self.config_dir / f"{name}.checksum.json"
            if not checksum_file.exists():
                raise FileNotFoundError(f"Checksum file not found: {checksum_file}")

            with open(checksum_file, 'r') as f:
                checksum_meta = json.load(f)

            # Calculate current checksum
            current_checksum = self.calculate_checksum(
                config,
                checksum_meta["algorithm"]
            )

            # Verify
            if current_checksum != checksum_meta["hash"]:
                raise ValueError(
                    f"Checksum verification failed for config '{name}'. "
                    f"Expected: {checksum_meta['hash']}, "
                    f"Got: {current_checksum}"
                )

        # Cache config
        if use_cache:
            self._cache[name] = config

        return config

    def get_checksum_info(self, name: str) -> Optional[ConfigChecksum]:
        """
        Get checksum metadata for a config.

        Args:
            name: Configuration name

        Returns:
            Checksum metadata or None if not found
        """
        checksum_file = self.config_dir / f"{name}.checksum.json"
        if not checksum_file.exists():
            return None

        with open(checksum_file, 'r') as f:
            data = json.load(f)

        return ConfigChecksum(**data)

    def verify_config_integrity(self, name: str) -> bool:
        """
        Verify config integrity without loading.

        Args:
            name: Configuration name

        Returns:
            True if integrity check passes
        """
        try:
            self.load_config(name, verify=True, use_cache=False)
            return True
        except (FileNotFoundError, ValueError):
            return False

    def list_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        List all available configurations.

        Returns:
            Dictionary of config names to metadata
        """
        configs = {}

        for config_file in self.config_dir.glob("*.json"):
            if config_file.stem.endswith(".checksum"):
                continue

            name = config_file.stem
            checksum_info = self.get_checksum_info(name)

            configs[name] = {
                "file": str(config_file),
                "has_checksum": checksum_info is not None,
                "version": checksum_info.version if checksum_info else None,
                "created_at": checksum_info.created_at if checksum_info else None
            }

        return configs

    def clear_cache(self, name: Optional[str] = None):
        """
        Clear configuration cache.

        Args:
            name: Optional specific config to clear (clears all if None)
        """
        if name:
            self._cache.pop(name, None)
        else:
            self._cache.clear()


class SecureConfigLoader(ConfigLoader):
    """Enhanced config loader with additional security features."""

    def __init__(self, config_dir: Optional[Path] = None, allowed_configs: Optional[list] = None):
        """
        Initialize secure config loader.

        Args:
            config_dir: Directory containing config files
            allowed_configs: Whitelist of allowed config names
        """
        super().__init__(config_dir)
        self.allowed_configs = set(allowed_configs) if allowed_configs else None

    def load_config(
        self,
        name: str,
        verify: bool = True,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Load configuration with security checks.

        Args:
            name: Configuration name
            verify: Whether to verify checksum (always True for SecureConfigLoader)
            use_cache: Whether to use cached config

        Returns:
            Configuration data

        Raises:
            ValueError: If config name not in whitelist or verification fails
        """
        # Check whitelist
        if self.allowed_configs and name not in self.allowed_configs:
            raise ValueError(f"Config '{name}' not in allowed list")

        # Force verification
        return super().load_config(name, verify=True, use_cache=use_cache)

"""
MirrorDNA - Identity and Continuity Protocol Layer

MirrorDNA provides a standardized protocol for persistent identity, memory,
and continuity for AI agents and users.
"""

__version__ = "1.0.0"

from .validator import validate_schema, ValidationResult
from .identity import IdentityManager
from .continuity import ContinuityTracker
from .memory import MemoryManager
from .agent_dna import AgentDNAManager
from .crypto import CryptoUtils
from .storage import StorageAdapter, JSONFileStorage
from .reflection import ReflectionEngine, ReflectionType, Reflection
from .config import ConfigLoader, SecureConfigLoader, ConfigChecksum
from .timeline import TimelineAnalyzer

__all__ = [
    "validate_schema",
    "ValidationResult",
    "IdentityManager",
    "ContinuityTracker",
    "MemoryManager",
    "AgentDNAManager",
    "CryptoUtils",
    "StorageAdapter",
    "JSONFileStorage",
    "ReflectionEngine",
    "ReflectionType",
    "Reflection",
    "ConfigLoader",
    "SecureConfigLoader",
    "ConfigChecksum",
    "TimelineAnalyzer",
]

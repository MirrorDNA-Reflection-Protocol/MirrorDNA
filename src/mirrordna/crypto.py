# FEU Enforcement: Master Citation v15.2
# FACT/ESTIMATE/UNKNOWN tagging mandatory | Information only, non-advisory

"""
Cryptographic utilities for MirrorDNA identity and verification.
"""

import hashlib
import json
import base64
from typing import Tuple, Dict, Any

try:
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class CryptoUtils:
    """Cryptographic operations for identity and verification."""

    @staticmethod
    def generate_keypair() -> Tuple[str, str]:
        """
        Generate an Ed25519 keypair.

        Returns:
            Tuple of (public_key, private_key) as base64-encoded strings

        Raises:
            RuntimeError: If cryptography library not available
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError(
                "cryptography library not available. "
                "Install with: pip install cryptography"
            )

        # Generate private key
        private_key = ed25519.Ed25519PrivateKey.generate()

        # Get public key
        public_key = private_key.public_key()

        # Serialize to bytes
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )

        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )

        # Encode to base64
        public_key_b64 = base64.b64encode(public_bytes).decode('utf-8')
        private_key_b64 = base64.b64encode(private_bytes).decode('utf-8')

        return public_key_b64, private_key_b64

    @staticmethod
    def sign(message: str, private_key: str) -> str:
        """
        Sign a message with a private key.

        Args:
            message: Message to sign
            private_key: Base64-encoded private key

        Returns:
            Base64-encoded signature

        Raises:
            RuntimeError: If cryptography library not available
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError(
                "cryptography library not available. "
                "Install with: pip install cryptography"
            )

        # Decode private key
        private_bytes = base64.b64decode(private_key)
        private_key_obj = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)

        # Sign message
        message_bytes = message.encode('utf-8')
        signature = private_key_obj.sign(message_bytes)

        # Encode signature
        return base64.b64encode(signature).decode('utf-8')

    @staticmethod
    def verify(message: str, signature: str, public_key: str) -> bool:
        """
        Verify a message signature.

        Args:
            message: Original message
            signature: Base64-encoded signature
            public_key: Base64-encoded public key

        Returns:
            True if signature is valid, False otherwise
        """
        if not CRYPTO_AVAILABLE:
            raise RuntimeError(
                "cryptography library not available. "
                "Install with: pip install cryptography"
            )

        try:
            # Decode public key and signature
            public_bytes = base64.b64decode(public_key)
            signature_bytes = base64.b64decode(signature)

            public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_bytes)

            # Verify signature
            message_bytes = message.encode('utf-8')
            public_key_obj.verify(signature_bytes, message_bytes)

            return True
        except Exception:
            return False

    @staticmethod
    def hash(data: Any) -> str:
        """
        Hash data using SHA-256.

        Args:
            data: Data to hash (will be JSON-serialized if not string)

        Returns:
            Hex-encoded hash digest
        """
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data, sort_keys=True)

        hash_obj = hashlib.sha256(data_str.encode('utf-8'))
        return hash_obj.hexdigest()

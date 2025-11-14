"""
Tests for checksum computation and verification.
"""

import pytest
from pathlib import Path
from mirrordna import (
    compute_file_checksum,
    compute_state_checksum,
    compute_text_checksum,
    verify_checksum
)


class TestChecksumComputation:
    """Test checksum computation functions."""

    def test_compute_text_checksum(self):
        """Test computing checksum of text."""
        text = "Hello, MirrorDNA!"
        checksum = compute_text_checksum(text)

        assert isinstance(checksum, str)
        assert len(checksum) == 64  # SHA-256 produces 64 hex characters
        assert all(c in "0123456789abcdef" for c in checksum)

    def test_compute_text_checksum_deterministic(self):
        """Test that same text produces same checksum."""
        text = "Test message"

        checksum1 = compute_text_checksum(text)
        checksum2 = compute_text_checksum(text)

        assert checksum1 == checksum2

    def test_compute_text_checksum_different_inputs(self):
        """Test that different text produces different checksums."""
        text1 = "Message A"
        text2 = "Message B"

        checksum1 = compute_text_checksum(text1)
        checksum2 = compute_text_checksum(text2)

        assert checksum1 != checksum2

    def test_compute_state_checksum(self):
        """Test computing checksum of state dictionary."""
        state = {
            "id": "test_001",
            "value": 42,
            "nested": {
                "key": "value"
            }
        }

        checksum = compute_state_checksum(state)

        assert isinstance(checksum, str)
        assert len(checksum) == 64

    def test_compute_state_checksum_deterministic(self):
        """Test that same state produces same checksum."""
        state = {
            "session_count": 5,
            "user_id": "alice",
            "timestamp": "2025-11-14T10:00:00Z"
        }

        checksum1 = compute_state_checksum(state)
        checksum2 = compute_state_checksum(state)

        assert checksum1 == checksum2

    def test_compute_state_checksum_key_order_independent(self):
        """Test that key order doesn't affect checksum (canonical JSON)."""
        state1 = {
            "a": 1,
            "b": 2,
            "c": 3
        }

        state2 = {
            "c": 3,
            "a": 1,
            "b": 2
        }

        checksum1 = compute_state_checksum(state1)
        checksum2 = compute_state_checksum(state2)

        assert checksum1 == checksum2

    def test_compute_state_checksum_nested(self):
        """Test checksum of nested state."""
        state = {
            "identity": {
                "id": "alice",
                "created": "2025-01-01"
            },
            "continuity": {
                "sessions": 10,
                "events": 100
            }
        }

        checksum = compute_state_checksum(state)

        assert len(checksum) == 64

    def test_compute_file_checksum(self, tmp_path):
        """Test computing checksum of file."""
        # Create test file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test file content")

        checksum = compute_file_checksum(test_file)

        assert isinstance(checksum, str)
        assert len(checksum) == 64

    def test_compute_file_checksum_deterministic(self, tmp_path):
        """Test that same file produces same checksum."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Same content")

        checksum1 = compute_file_checksum(test_file)
        checksum2 = compute_file_checksum(test_file)

        assert checksum1 == checksum2

    def test_compute_file_checksum_different_files(self, tmp_path):
        """Test that different files produce different checksums."""
        file1 = tmp_path / "file1.txt"
        file2 = tmp_path / "file2.txt"

        file1.write_text("Content A")
        file2.write_text("Content B")

        checksum1 = compute_file_checksum(file1)
        checksum2 = compute_file_checksum(file2)

        assert checksum1 != checksum2

    def test_compute_file_checksum_not_found(self):
        """Test error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            compute_file_checksum("/nonexistent/file.txt")

    def test_compute_file_checksum_binary(self, tmp_path):
        """Test checksum of binary file."""
        binary_file = tmp_path / "binary.dat"
        binary_file.write_bytes(b"\x00\x01\x02\x03\x04\x05")

        checksum = compute_file_checksum(binary_file)

        assert len(checksum) == 64


class TestChecksumVerification:
    """Test checksum verification."""

    def test_verify_text_checksum(self):
        """Test verifying text checksum."""
        text = "Test message"
        checksum = compute_text_checksum(text)

        assert verify_checksum(text, checksum) is True

    def test_verify_text_checksum_mismatch(self):
        """Test verification fails with wrong checksum."""
        text = "Test message"
        wrong_checksum = "0" * 64

        assert verify_checksum(text, wrong_checksum) is False

    def test_verify_state_checksum(self):
        """Test verifying state checksum."""
        state = {
            "id": "test_001",
            "value": 42
        }

        checksum = compute_state_checksum(state)

        assert verify_checksum(state, checksum) is True

    def test_verify_state_checksum_mismatch(self):
        """Test verification fails when state changes."""
        state = {
            "id": "test_001",
            "value": 42
        }

        checksum = compute_state_checksum(state)

        # Modify state
        state["value"] = 100

        assert verify_checksum(state, checksum) is False

    def test_verify_file_checksum(self, tmp_path):
        """Test verifying file checksum."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("File content")

        checksum = compute_file_checksum(test_file)

        assert verify_checksum(test_file, checksum) is True

    def test_verify_file_checksum_after_modification(self, tmp_path):
        """Test verification fails after file is modified."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("Original content")

        checksum = compute_file_checksum(test_file)

        # Modify file
        test_file.write_text("Modified content")

        assert verify_checksum(test_file, checksum) is False

    def test_verify_checksum_case_insensitive(self):
        """Test that checksum verification is case insensitive."""
        text = "Test"
        checksum = compute_text_checksum(text)

        # Test with uppercase checksum
        assert verify_checksum(text, checksum.upper()) is True

        # Test with lowercase checksum
        assert verify_checksum(text, checksum.lower()) is True


class TestEdgeCases:
    """Test edge cases for checksum functions."""

    def test_empty_text_checksum(self):
        """Test checksum of empty text."""
        checksum = compute_text_checksum("")

        assert len(checksum) == 64

    def test_empty_state_checksum(self):
        """Test checksum of empty dictionary."""
        checksum = compute_state_checksum({})

        assert len(checksum) == 64

    def test_unicode_text_checksum(self):
        """Test checksum of Unicode text."""
        text = "Hello 世界 🌍"
        checksum = compute_text_checksum(text)

        assert len(checksum) == 64

        # Verify deterministic
        checksum2 = compute_text_checksum(text)
        assert checksum == checksum2

    def test_large_state_checksum(self):
        """Test checksum of large state dictionary."""
        state = {
            f"key_{i}": f"value_{i}"
            for i in range(1000)
        }

        checksum = compute_state_checksum(state)

        assert len(checksum) == 64

    def test_state_with_none_values(self):
        """Test checksum of state with None values."""
        state = {
            "id": "test_001",
            "value": None,
            "optional": None
        }

        checksum = compute_state_checksum(state)

        assert len(checksum) == 64


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

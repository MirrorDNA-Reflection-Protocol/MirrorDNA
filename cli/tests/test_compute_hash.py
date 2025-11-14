"""
Tests for compute-hash command.
"""

import pytest
from pathlib import Path
import tempfile
import shutil
from cli.commands.compute_hash import compute_vault_hash


class TestComputeHash:
    """Test compute-hash command functionality."""

    def test_deterministic_hash_same_content(self):
        """Test that same content produces same hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            vault_path.mkdir()

            # Create test files
            (vault_path / "file1.txt").write_text("Hello World\n")
            (vault_path / "file2.txt").write_text("Test content\n")

            # Compute hash twice
            hash1, _ = compute_vault_hash(vault_path)
            hash2, _ = compute_vault_hash(vault_path)

            assert hash1 == hash2, "Same content should produce same hash"

    def test_deterministic_hash_different_content(self):
        """Test that different content produces different hash."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault1 = Path(tmpdir) / "vault1"
            vault2 = Path(tmpdir) / "vault2"
            vault1.mkdir()
            vault2.mkdir()

            # Create different content
            (vault1 / "file.txt").write_text("Content A\n")
            (vault2 / "file.txt").write_text("Content B\n")

            hash1, _ = compute_vault_hash(vault1)
            hash2, _ = compute_vault_hash(vault2)

            assert hash1 != hash2, "Different content should produce different hashes"

    def test_hash_with_subdirectories(self):
        """Test hashing with nested directory structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            vault_path.mkdir()

            # Create nested structure
            (vault_path / "config").mkdir()
            (vault_path / "logs").mkdir()
            (vault_path / "config" / "config.json").write_text('{"key": "value"}')
            (vault_path / "logs" / "log.txt").write_text("Log entry\n")

            hash_val, file_hashes = compute_vault_hash(vault_path)

            # Should have hashes for both files
            assert len(file_hashes) == 2
            assert "config/config.json" in file_hashes
            assert "logs/log.txt" in file_hashes

            # Hash should be reproducible
            hash_val2, _ = compute_vault_hash(vault_path)
            assert hash_val == hash_val2

    def test_hash_normalization(self):
        """Test that text normalization works (line endings, whitespace)."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault1 = Path(tmpdir) / "vault1"
            vault2 = Path(tmpdir) / "vault2"
            vault1.mkdir()
            vault2.mkdir()

            # Write with different line endings
            (vault1 / "file.txt").write_text("Line 1\nLine 2\n")
            (vault2 / "file.txt").write_text("Line 1\r\nLine 2\r\n")

            hash1, _ = compute_vault_hash(vault1)
            hash2, _ = compute_vault_hash(vault2)

            # Should produce same hash after normalization
            assert hash1 == hash2, "Line ending normalization should produce same hash"

    def test_empty_directory_raises_error(self):
        """Test that empty directory raises an error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            vault_path = Path(tmpdir) / "vault"
            vault_path.mkdir()

            with pytest.raises(ValueError, match="No files found"):
                compute_vault_hash(vault_path)

    def test_nonexistent_path_raises_error(self):
        """Test that nonexistent path raises an error."""
        with pytest.raises(FileNotFoundError):
            compute_vault_hash(Path("/nonexistent/path"))

    def test_file_instead_of_directory_raises_error(self):
        """Test that passing a file instead of directory raises an error."""
        with tempfile.NamedTemporaryFile() as tmpfile:
            with pytest.raises(ValueError, match="not a directory"):
                compute_vault_hash(Path(tmpfile.name))

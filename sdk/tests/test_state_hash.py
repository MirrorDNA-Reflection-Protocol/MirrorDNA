"""
Tests for MirrorDNA SDK state hashing functionality.

These tests verify that:
1. State hashing is deterministic (same input → same hash)
2. State changes are detected (different input → different hash)
3. Hash computation is consistent across runs
4. Edge cases are handled properly
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add SDK to path
sys.path.insert(0, str(Path(__file__).parent.parent / "python"))

from mirrordna_client import MirrorDNAClient


class TestStateHash:
    """Test suite for state hash computation."""

    def setup_method(self):
        """Set up test fixtures."""
        self.client = MirrorDNAClient()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_deterministic_hashing(self):
        """Test that same directory produces same hash."""
        # Create test directory with files
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")

        # Compute hash twice
        hash1 = self.client.compute_state_hash(str(test_dir))
        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should be identical
        assert hash1 == hash2, "Hashes should be deterministic"
        assert len(hash1) == 64, "SHA-256 hash should be 64 hex characters"

    def test_change_detection(self):
        """Test that file changes result in different hash."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("original content")

        # Compute initial hash
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Modify file
        (test_dir / "file1.txt").write_text("modified content")

        # Compute new hash
        hash2 = self.client.compute_state_hash(str(test_dir))

        # Hashes should be different
        assert hash1 != hash2, "Hash should change when file content changes"

    def test_new_file_detection(self):
        """Test that adding files changes hash."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("content1")

        # Initial hash
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Add new file
        (test_dir / "file2.txt").write_text("content2")

        # New hash
        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should be different
        assert hash1 != hash2, "Hash should change when new file added"

    def test_file_deletion_detection(self):
        """Test that deleting files changes hash."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.txt").write_text("content2")

        # Initial hash
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Delete file
        (test_dir / "file2.txt").unlink()

        # New hash
        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should be different
        assert hash1 != hash2, "Hash should change when file deleted"

    def test_empty_directory(self):
        """Test hashing empty directory."""
        test_dir = Path(self.temp_dir) / "empty_vault"
        test_dir.mkdir()

        # Should work without errors
        hash_val = self.client.compute_state_hash(str(test_dir))

        assert isinstance(hash_val, str), "Should return string hash"
        assert len(hash_val) == 64, "Should be valid SHA-256 hash"

    def test_nested_directories(self):
        """Test hashing with nested directory structure."""
        test_dir = Path(self.temp_dir) / "nested_vault"
        test_dir.mkdir()

        # Create nested structure
        (test_dir / "subdir1").mkdir()
        (test_dir / "subdir1" / "file1.txt").write_text("content1")
        (test_dir / "subdir2").mkdir()
        (test_dir / "subdir2" / "file2.txt").write_text("content2")

        # Compute hash
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Modify nested file
        (test_dir / "subdir1" / "file1.txt").write_text("modified")

        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should detect change in nested file
        assert hash1 != hash2, "Should detect changes in nested directories"

    def test_ignore_patterns(self):
        """Test that ignore patterns work correctly."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("content1")
        (test_dir / "file2.pyc").write_text("compiled")

        # Hash with default ignore patterns (includes *.pyc)
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Modify ignored file
        (test_dir / "file2.pyc").write_text("modified compiled")

        hash2 = self.client.compute_state_hash(str(test_dir))

        # Hash should be same (*.pyc is ignored by default)
        assert hash1 == hash2, "Ignored files should not affect hash"

    def test_ignore_git_directory(self):
        """Test that .git directories are ignored."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        (test_dir / "file1.txt").write_text("content1")

        # Hash without .git
        hash1 = self.client.compute_state_hash(str(test_dir))

        # Add .git directory
        (test_dir / ".git").mkdir()
        (test_dir / ".git" / "config").write_text("git config")

        # Hash with .git
        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should be same (.git is ignored)
        assert hash1 == hash2, ".git directory should be ignored"

    def test_alphabetical_ordering(self):
        """Test that files are processed in alphabetical order."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()

        # Create files in different order
        (test_dir / "z_file.txt").write_text("z")
        (test_dir / "a_file.txt").write_text("a")
        (test_dir / "m_file.txt").write_text("m")

        hash1 = self.client.compute_state_hash(str(test_dir))

        # Remove and recreate in different order
        shutil.rmtree(test_dir)
        test_dir.mkdir()

        (test_dir / "a_file.txt").write_text("a")
        (test_dir / "m_file.txt").write_text("m")
        (test_dir / "z_file.txt").write_text("z")

        hash2 = self.client.compute_state_hash(str(test_dir))

        # Should be same (alphabetical processing)
        assert hash1 == hash2, "Hash should be same regardless of creation order"

    def test_directory_not_found(self):
        """Test error handling for non-existent directory."""
        try:
            self.client.compute_state_hash("/nonexistent/directory")
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError as e:
            assert "not found" in str(e).lower()

    def test_path_is_file_not_directory(self):
        """Test error handling when path is a file, not directory."""
        test_file = Path(self.temp_dir) / "test.txt"
        test_file.write_text("content")

        try:
            self.client.compute_state_hash(str(test_file))
            assert False, "Should raise ValueError"
        except ValueError as e:
            assert "not a directory" in str(e).lower()

    def test_last_state_hash_stored(self):
        """Test that last computed hash is stored in client."""
        test_dir = Path(self.temp_dir) / "test_vault"
        test_dir.mkdir()
        (test_dir / "file1.txt").write_text("content1")

        hash_val = self.client.compute_state_hash(str(test_dir))

        assert self.client.last_state_hash == hash_val, "Should store last hash"


def run_tests():
    """Run all tests manually (no pytest required)."""
    test_instance = TestStateHash()
    test_methods = [
        method for method in dir(test_instance)
        if method.startswith('test_')
    ]

    passed = 0
    failed = 0

    for test_method in test_methods:
        try:
            test_instance.setup_method()
            getattr(test_instance, test_method)()
            test_instance.teardown_method()
            print(f"✓ {test_method}")
            passed += 1
        except Exception as e:
            print(f"✗ {test_method}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed")
    return failed == 0


if __name__ == "__main__":
    # Can run with pytest or directly
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        # Run without pytest
        print("Running tests without pytest...\n")
        success = run_tests()
        sys.exit(0 if success else 1)
